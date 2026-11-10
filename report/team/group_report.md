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

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:** `cd starter_v0 && pip install -r requirements.txt && streamlit run app.py`. Link dùng thử (Cloudflare quick tunnel, chỉ sống khi máy chủ nhóm đang chạy): https://coast-gray-injured-hoping.trycloudflare.com

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
| deduplicate_news | gộp tin trùng theo URL chuẩn hoá hoặc mức độ từ chung trong tiêu đề | có |
|  |  |  |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

- Thêm `deduplicate_news`, tool xử lý cục bộ để gộp tin trùng khi người dùng có ít nhất hai tin từ các nguồn và muốn loại bỏ trùng lặp. Tool chuẩn hoá URL trước, sau đó so các từ trong tiêu đề; nguồn được gộp và summary dài hơn được giữ lại. Dùng trước `format`, không dùng để tìm tin mới hoặc tóm tắt một bài.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline |  | — | 0.65 | `runs/v0_B_base_openai_20261110T173124939840.json` |
| v1 | system_prompt.md | Bỏ các câu 'đừng hỏi lại / cứ gửi / chọn một tool' trong prompt, thay bằng quy tắc hỏi lại, xác nhận trước khi gửi, cho phép không gọi tool → sửa R08/R10/R11/R12/R14 | 0.65 | 0.75 | `runs/v1_B_base_openai_20261110T183730315565.json` |
| v2 | tools.yaml | Mô tả rõ khi nào dùng/không dùng và ví dụ tham số cho 10 tool → sửa R11/R13/M02 và response_type của clarify | 0.75 | 0.85 | `runs/v2_B_base_openai_20261110T194023990931.json` |
| v3 | tools.yaml | clarify bắt buộc response_type, yes_no cho xác nhận; sửa mô tả screenname → sửa R10/R12/M03 | 0.85 | 0.90 | `runs/v3_B_base_openai_20261110T220531642617.json` |

### B2. Failure Analysis

Run v0: `starter_v0/runs/v0_B_base_openai_20261110T173124939840.json` (case_accuracy 0.65, 13/20).

| Case ID | Failure Type | Actual Tool Calls | Failed | Fix |
|---|---|---|---|---|
| R03_web_news_routing | wrong_tool (observed: wrong_arg_value) | `lookup(query="AI news", topic="news", timeframe="day", max_results=5)` | `query`: expected `'AI'`, got `'AI news'` | Thêm mô tả về tool lookup |
| R08_out_of_scope | out_of_scope (observed: unexpected_tool_call) | `send(text="Nguyên hàm của x^2 là x^3/3 + C...")` | Expected no tool call; model tự trả lời bài toán rồi gọi `send` (Telegram) | Thêm vào system prompt: Không trả lời câu hỏi ngoài phạm vi research/news |
| R10_missing_handle | missing_info (observed: missing_tool_call) | `timeline(screenname="sama")` | Thiếu `clarify`; model đoán bừa handle `sama` | Thêm quy tắc: tuyệt đối không tự đoán người |
| R11_missing_url | missing_info (observed: missing_tool_call) | `fetch(url="https://example.com/article")` | Thiếu `clarify`; model bịa URL placeholder | Thêm quy tắc cấm tự bịa/điền URL mẫu |
| R12_confirm_before_send | wrong_boundary (observed: missing_tool_call) | `send(text="Bản tin này đã được đăng lên Telegram.")` | Thiếu `clarify(yes_no)`; model tự gọi `send` với nội dung bịa (chưa có bản tin, chưa xác nhận) | Thêm quy tắc: hành động ghi/gửi cần phải có xác minh từ user |
| R13_parallel_web_and_tweets | wrong_tool (observed: wrong_arg_value) | `lookup(query="AI news", timeframe="day", max_results=5)` + `social_search(query="AI", search_type="Latest", limit=5)` | `lookup.query`: expected `'AI'`, got `'AI news'`; `lookup.topic`: expected `'news'`, got `None` (thiếu `topic`, kết quả trả về `general`) | Thêm mô tả về tool lookup |
| R14_out_of_scope_coding | out_of_scope (observed: unexpected_tool_call) | `send(text="Dưới đây là một hàm Python tính số Fibonacci...")` | Expected no tool call; model viết code rồi gọi `send` (Telegram) | Thêm vào system prompt: Không trả lời câu hỏi ngoài phạm vi research/news |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

Transcript: `starter_v0/transcripts/v3_openai_20261110T222531182603.transcript.json` (`python chat.py --provider openai --version v3`, gpt-4o-mini).

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | "Tin AI mới nhất tuần này là gì?" (yêu cầu bình thường) | `lookup(query="AI", topic="news", timeframe="week")` | `v3+p2616a3e8ae64+tdbbacfbc0234` | Trả 3 tin AI tuần này kèm link nguồn (Axios, CBS News, MIT News) |
| 2 | "Tóm tắt bài này giúp mình" (thiếu link) | _(không gọi tool)_ | `v3+p2616a3e8ae64+tdbbacfbc0234` | Agent hỏi lại link bằng câu trả lời chữ, không bịa URL; nhưng không dùng tool `clarify` |
| 3 | "https://en.wikipedia.org/wiki/Large_language_model" (bổ sung thông tin) | `fetch(url="https://en.wikipedia.org/wiki/Large_language_model")` | `v3+p2616a3e8ae64+tdbbacfbc0234` | Đọc trang và tóm tắt tiếng Việt về LLM |
| 4 | "Gửi bản tóm tắt đó lên kênh Telegram của nhóm" (yêu cầu gửi) | _(không gọi tool)_ | `v3+p2616a3e8ae64+tdbbacfbc0234` | Agent hỏi xác nhận trước khi gửi, không gọi `send`; hỏi bằng chữ chứ không qua `clarify(response_type="yes_no")` (giống lỗi R12 trong eval). Chưa xác nhận nên không có gì được gửi |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) | `starter_v0/tools/deduplicate_news/` | URL chuẩn hoá và tiêu đề tương tự được gộp; không gọi API | Không tìm tin mới; chỉ gộp khi URL trùng hoặc ngưỡng từ chung đạt 0.8 |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py` | 4 test cho URL, tiêu đề, input sai và ngưỡng sai; toàn bộ suite: 71 passed, 0 failed | 14 test TODO cũ của các tool khác vẫn skipped |
| UI (lệnh chạy + link dùng thử) | `starter_v0/app.py`, `streamlit run app.py`, https://coast-gray-injured-hoping.trycloudflare.com | Dùng lại `run_model_tool_loop` của `chat.py`; mỗi lần gọi tool hiện args + kết quả; transcript lưu `transcripts/*_ui_*.transcript.json` | Lỗi tool/provider hiện ra (✗, `st.error`), không bị giấu; câu mẫu không có lệnh gửi |

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
