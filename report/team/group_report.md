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

**Cách chạy UI:**

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
| v0 | baseline |  |  |  |  |
| v1 |  |  |  |  |  |
| v2 |  |  |  |  |  |
| v3 |  |  |  |  |  |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

Run v0: `starter_v0/runs/v0_B_base_openai_20261110T173124939840.json` (case_accuracy 0.65, 13/20). Cột Fix ghi version đầu tiên case này PASS (đối chiếu run v1 `v1_B_base_openai_20261110T183730315565.json`, v2 `v2_B_base_openai_20261110T194023990931.json`).

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R03_web_news_routing | wrong_tool (mismatch: wrong_arg_value) | `lookup(query="AI news", topic="news", timeframe="day", max_results=5)` | Đúng tool, đúng topic/timeframe nhưng query thêm chữ "news" (`expected 'AI', got 'AI news'`). Liên quan: `tools.yaml` → `lookup` chỉ mô tả "Tra cứu thông tin trên internet", `topic` chỉ ghi "Phân loại". | PASS từ v1 (`system_prompt.md`) |
| R08_out_of_scope | out_of_scope (mismatch: unexpected_tool_call) | `send(text="Nguyên hàm của x^2 là …")` | Câu toán ngoài phạm vi research, agent tự giải rồi gọi `send`. Liên quan: prompt không giới hạn phạm vi, có câu "Always finish the request in a single step. Pick one tool". | PASS từ v1 (`system_prompt.md`) |
| R10_missing_handle | missing_info (mismatch: missing_tool_call) | `timeline(screenname="sama")` | Thiếu tên tài khoản, agent đoán Sam Altman thay vì `clarify`. Liên quan: prompt "do not ask them back — just make a sensible guess", "pick a well-known account like Sam Altman". | v1 đã gọi `clarify` nhưng thiếu `response_type="text"`; vẫn FAIL ở v2 |
| R11_missing_url | missing_info (mismatch: missing_tool_call) | `fetch(url="https://example.com/article")` | Thiếu link, agent bịa URL thay vì `clarify`. Liên quan: prompt "assume a likely URL and read it". | v1 gọi `clarify` nhưng thiếu `response_type`; PASS từ v2 (`tools.yaml`) |
| R12_confirm_before_send | wrong_boundary (mismatch: missing_tool_call) | `send(text="Bản tin này đã được đăng lên Telegram.")` | Gọi `send` ngay, không hỏi xác nhận yes/no. Liên quan: prompt "When the user wants to send, post, or publish something, just go ahead and do it"; `send` chỉ ghi "Gửi một đoạn văn bản đi.". | v1 gọi `clarify` nhưng hỏi nội dung/kênh, không phải `yes_no`; vẫn FAIL ở v2 |
| R13_parallel_web_and_tweets | wrong_tool (mismatch: wrong_arg_value) | `lookup(query="AI news", timeframe="day", max_results=5)` + `social_search(query="AI", search_type="Latest", limit=5)` | Gọi đủ 2 tool nhưng `lookup` query "AI news" và thiếu `topic="news"`. Liên quan: như R03. | PASS từ v2 (`tools.yaml`) |
| R14_out_of_scope_coding | out_of_scope (mismatch: unexpected_tool_call) | `send(text="…def fibonacci(n)…")` | Câu coding ngoài phạm vi, agent tự viết code rồi gọi `send`. Liên quan: như R08. | PASS từ v1 (`system_prompt.md`) |

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
| Tool mới (`tools/<tên>/`) | `starter_v0/tools/deduplicate_news/` | URL chuẩn hoá và tiêu đề tương tự được gộp; không gọi API | Không tìm tin mới; chỉ gộp khi URL trùng hoặc ngưỡng từ chung đạt 0.8 |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py` | 4 test cho URL, tiêu đề, input sai và ngưỡng sai; toàn bộ suite: 71 passed, 0 failed | 14 test TODO cũ của các tool khác vẫn skipped |
| UI (lệnh chạy + link dùng thử) | Chưa triển khai (CP5) | — | — |

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
