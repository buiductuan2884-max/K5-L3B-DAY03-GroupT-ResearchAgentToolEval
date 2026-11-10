# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm:
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3:

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent


### A1. Agent này làm được gì

**GroupT Research Agent** là trợ lý nghiên cứu dùng tool calling (OpenAI `gpt-4o-mini`): người dùng hỏi bằng tiếng Việt, agent tự chọn trong 14 tool để tìm tin web và tweet, đọc URL, tìm và đọc paper arXiv, tra policy nội bộ, tổng hợp thành bản tin, và chỉ gửi Telegram sau khi người dùng xác nhận. Nhóm thêm 4 tool mới: `deduplicate_news` (gộp tin trùng), `wiki_sum` (kiến thức nền từ Wikipedia), `validate_url` (kiểm tra link) và `date_localized` (giờ theo múi giờ). Khi thiếu thông tin (tài khoản, link), agent hỏi lại thay vì tự đoán.

**Cách chạy UI:** `cd starter_v0 && pip install -r requirements.txt && streamlit run app.py` (dependency `streamlit>=1.40` đã có trong `starter_v0/requirements.txt`). UI dùng lại vòng lặp tool của `chat.py`, hiện từng lần gọi tool kèm args/kết quả và lưu transcript vào `starter_v0/transcripts/`.

**Link dùng thử (deploy):** [https://coast-gray-injured-hoping.trycloudflare.com](https://coast-gray-injured-hoping.trycloudflare.com) (Cloudflare quick tunnel từ máy nhóm trưởng; link chỉ sống khi máy đó đang chạy Streamlit và cloudflared).

 
### A2. Tool agent có
 
| Tool | Chức năng |
|---|---|
| G09_multiturn_news_topic_correction | Giữ timeframe=day từ ngữ cảnh, dùng chủ đề đã sửa robotics và route qua lookup. | `lookup(query='robotics', topic='news', timeframe='day')` | 
| G10_multiturn_publish_confirmation | Dù có nội dung và đích đến, yêu cầu chỉ hỏi xác nhận nghĩa là chưa cho phép gửi; không gọi send, phải xác nhận trước. | `clarify(response_type='yes_no')` | 

 
#### Phân tích 4 case FAIL (run v4 group)

- **G01_wikipedia_knowledge_summary** và **G08_multiturn_wikipedia_followup** (`wrong_arg_value`): đúng tool `wiki_sum` nhưng agent truyền `title="Ada_Lovelace"` / `"Alan_Turing"` (dấu gạch dưới) trong khi đáp án là `"Ada Lovelace"` / `"Alan Turing"`. Mô tả tham số `title` chỉ ghi "Tên người/chủ đề hoặc tiêu đề trang Wikipedia cụ thể" (`starter_v0/artifacts/tools.yaml:315`); chữ "tiêu đề trang Wikipedia" có thể khiến model viết theo dạng URL của Wikipedia. Về chức năng thì không sai vì tool tự đổi dấu cách thành `_` (`starter_v0/tools/wiki_sum/tool.py:19`), nên đây là case eval so khớp chặt. **Ngoài ra `tool_results` của cả 2 case cho thấy tool trả lỗi `403 Client Error: Forbidden`** từ Wikipedia: `tool.py:20-22` gọi API mà không gửi header `User-Agent`. Unit test dùng `fake_http` nên không bắt được lỗi này. Đây là ví dụ eval PASS/FAIL theo tool call không phản ánh tool có chạy thật hay không.

- **G07_multiturn_url_validation** (`extra_tool_call`): agent gọi `validate_url` 2 lần, lần đúng với `https://tinyurl.com/example-check` và thêm một lần với `https://tinyurl.com` (chỉ domain). Lần thứ hai không có trong yêu cầu. Prompt cho phép "multiple steps, using as many tools as necessary" (`starter_v0/artifacts/system_prompt.md:12`) và mô tả `validate_url` không nói "gọi một lần cho mỗi link người dùng đưa".

- **G10_multiturn_publish_confirmation** (`wrong_boundary`): người dùng nói rõ "Chuẩn bị nội dung đó và hỏi mình xác nhận trước khi gửi", eval mong đợi `clarify(response_type="yes_no")`, nhưng agent chỉ gọi `format` để soạn bản tin và không hỏi xác nhận. Đây là cùng nhóm lỗi với R12 của base: quy tắc xác nhận nằm ở `system_prompt.md:8` và mô tả `send`, nhưng khi agent chưa gọi `send` thì không có chỗ nào bắt nó phải gọi `clarify` yes_no. Agent không gửi gì đi nên không có rủi ro thật, nhưng hành vi vẫn sai yêu cầu.

**Hướng sửa đề xuất (chưa chạy):** ghi trong mô tả `title` của `wiki_sum` là "dùng dấu cách, không dùng dấu gạch dưới"; thêm `User-Agent` cho request của `wiki_sum`; ghi "gọi validate_url đúng một lần cho mỗi link người dùng đưa"; thêm vào prompt "mọi yêu cầu gửi/đăng phải kết thúc bằng clarify(response_type=yes_no) trước khi gọi send".

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline |  |  |  |  |
| v1 |  |  |  |  |  |
| v2 |  |  |  |  |  |
| v3 |  |  |  |  |  |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
|  |  |  |  |  |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) |  |  |  |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) |  |  |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
