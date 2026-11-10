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

## A1. Agent làm được gì?

**Group T Research Agent** là trợ lý nghiên cứu dùng mô hình ngôn ngữ kết hợp công cụ (tool calling). Agent nhận yêu cầu bằng ngôn ngữ tự nhiên, chọn công cụ phù hợp và truyền tham số tương ứng để hỗ trợ:

- **Tra cứu thông tin:** tìm tin tức/web, bài đăng X (Twitter) theo chủ đề hoặc tài khoản, đọc nội dung từ URL cụ thể.
- **Nghiên cứu học thuật:** tìm bài báo trên arXiv, xem thông tin/abstract, tải PDF và trích xuất văn bản theo số trang.
- **Tổng hợp và tra cứu nội bộ:** định dạng kết quả thành bản tin Markdown; tra cứu quy định trong kho tài liệu chính sách nội bộ.
- **Kiểm tra yêu cầu trước khi thực hiện:** phát hiện thiếu tài khoản, URL hoặc chủ đề bằng tool nhóm `prepare_research_request`; hỏi lại khi chưa đủ thông tin.
- **Hỗ trợ hành động ngoài hệ thống:** có tool gửi Telegram, nhưng phải được xác nhận rõ ràng trước khi gửi.

**Phạm vi và lưu ý:** Khả năng gọi công cụ trực tuyến phụ thuộc API key và tình trạng dịch vụ (Tavily, Firecrawl, RapidAPI, arXiv, Telegram). Agent không nên tự đoán dữ liệu còn thiếu. Trong lần Group Eval gần nhất, luồng xác nhận/hủy gửi Telegram vẫn còn lỗi; **không dùng gửi Telegram thật khi chưa khắc phục và kiểm tra lại chốt xác nhận**.

## A2. Danh sách tool của Agent

| Nhóm | Tool | Công dụng chính |
|---|---|---|
| Core | `clarify` | Hỏi người dùng khi thiếu thông tin hoặc cần xác nhận (`text`, `yes_no`, `choice`). |
| Core | `timeline` | Lấy bài đăng gần đây của một tài khoản X/Twitter theo `screenname` và `limit`. |
| Core | `social_search` | Tìm bài đăng X/Twitter theo từ khóa; chọn bài mới nhất (`Latest`) hoặc phổ biến (`Top`). |
| Core | `lookup` | Tìm web/tin tức bằng Tavily, có lọc loại tin và khoảng thời gian. |
| Core | `fetch` | Đọc nội dung của một URL bằng Firecrawl. |
| Core | `format` | Định dạng các mục thông tin đã thu thập thành bản tin Markdown, không tự tìm kiếm. |
| Bonus | `policy` | Tra cứu chính sách nội bộ theo lĩnh vực: AI research, trích dẫn nguồn, bảo mật, công bố, sử dụng tool. |
| Bonus | `papers` | Tìm bài báo arXiv theo chủ đề, số lượng và kiểu sắp xếp; trả thông tin/abstract. |
| Bonus | `paper_text` | Tải và trích văn bản PDF arXiv theo ID/URL, số trang và giới hạn ký tự. |
| Bonus | `send` | Gửi nội dung tới Telegram; là hành động có tác động bên ngoài, **chỉ được thực hiện sau xác nhận**. |
| Group T | **`prepare_research_request`** | **Tool nhóm thêm:** kiểm tra và chuẩn hóa yêu cầu nghiên cứu; trả `ready`, `needs_clarification` hoặc `error` cùng bước tiếp theo, không tự tìm kiếm. |

## A3. Câu hỏi mẫu để nhóm khác demo

| Câu hỏi gợi ý | Tool kỳ vọng |
|---|---|
| “Tra cứu chính sách nội bộ về bảo vệ dữ liệu cá nhân khi nghiên cứu AI.” | `policy` |
| “Tìm đúng 3 bài báo arXiv mới được nộp gần đây nhất về RAG.” | `papers` |
| “Đọc 2 trang đầu của bài arXiv 1706.03762.” | `paper_text` |
| “Cho mình 5 tweet mới nhất của tài khoản Sam Altman.” | `timeline` |
| “Tin AI nổi bật trong tuần này trên web là gì?” | `lookup` |
| “Trước khi nghiên cứu, hãy kiểm tra yêu cầu lấy 5 tweet mới nhất nhưng mình chưa cung cấp tài khoản; chưa cần lấy tweet.” | **`prepare_research_request`** |
| “Tóm tắt bài viết này giúp mình.” (chưa gửi URL) | `clarify` để hỏi link, không tự đoán |

**Gợi ý demo:** Nếu chưa cấu hình API dịch vụ ngoài, hãy ưu tiên `policy` và `prepare_research_request`. Tránh demo gửi Telegram thật cho đến khi đã sửa và kiểm thử quy trình xác nhận/hủy.


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
