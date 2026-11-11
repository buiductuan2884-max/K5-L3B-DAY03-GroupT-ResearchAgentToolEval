# Báo cáo cá nhân — BuiDucTuan-2A202603902

## 1. Thông tin thành viên

- Họ tên: Bùi Đức Tuấn
- MSSV: 2A202603902
- Email:buiductuan2884@gmail.com
- GitHub: buiductuan2884-max
- Vai trò: Nhóm trưởng GroupT

## 2. Phần việc phụ trách

- Nhóm trưởng: fork repo nhóm, chia việc theo checkpoint, review và merge nhánh của các thành viên vào `main`.
- CP1: chạy baseline v0, ghi `version_log.csv`.
- CP2: viết lại mô tả 3 tool `lookup`, `fetch`, `format` trong `tools.yaml` (phần của v2); chạy eval cho v1, v2, v3, v4.
- CP5: UI Streamlit, link dùng thử qua Cloudflare Tunnel, chat live bằng `chat.py`.
- Báo cáo nhóm: B1, B2 (bản nháp đầu), B4, B6 và các mục dữ kiện (A2, A3, mục 3, 5, 8, B5).

## 3. Đóng góp cụ thể

- Baseline và các version: chạy v0 (0.65), v1 (0.75), v2 (0.85), v3 (0.90), v4 (base 0.90, group 0.60) bằng OpenAI `gpt-4o-mini`. Mọi run dùng làm bằng chứng đều có `provider_error_cases == 0` và `measured_cases == total_cases`.
- Tool description (v2): viết lại mô tả `lookup` (query chỉ gồm từ khoá, `topic="news"` khi hỏi tin), `fetch` (không có link thì gọi `clarify` text, không bịa URL) và `format`. Run v2 cho thấy R11 và R13 chuyển từ FAIL sang PASS.
- Merge:
  - merge 3-way các nhánh `hoangducan`, `ThanhHuy` (phần v2) và `nguyenmanhcuong`, chỉ gỡ đúng đoạn xung đột và giữ phần của từng người;
  - sửa tên tool sai trong mô tả (`c1916d4`);
  - khai báo `deduplicate_news` trong `tools.yaml`.
- Kiểm tra trước khi merge: không merge 2 commit đưa mô tả `send` về bản gốc (làm mất phần chặn xác nhận), và không merge phần báo cáo nêu tool/case không có trong repo.
- UI (`starter_v0/app.py`):
  - dùng lại `run_model_tool_loop` của `chat.py`;
  - hiện từng lần gọi tool kèm args và kết quả, tool lỗi hiện ✗;
  - lưu transcript vào `starter_v0/transcripts/`;
  - sửa lỗi `UnicodeEncodeError` khi chạy trên Windows;
  - link dùng thử qua Cloudflare Tunnel.
- Chat live (B4): 4 lượt gồm yêu cầu bình thường, lượt thiếu link rồi bổ sung, và yêu cầu gửi Telegram. Agent hỏi xác nhận, không gửi.
- Phát hiện lỗi:
  - hash artifact lệch giữa đĩa và commit do CRLF;
  - `wiki_sum` bị Wikipedia trả `403` vì thiếu `User-Agent` (thấy trong `tool_results` của run v4 group).

## 4. Bằng chứng

- File/commit/PR:
  - Run: `starter_v0/runs/v0_…173124939840.json`, `v1_…183730315565.json`, `v2_…194023990931.json`, `v3_…220531642617.json`, `v4_B_base_…235953621020.json`, `v4_B_group_…090510008911.json`
  - Transcript: `starter_v0/transcripts/v3_openai_20261110T222531182603.transcript.json`
  - UI: `starter_v0/app.py`, `starter_v0/.streamlit/config.toml`, `starter_v0/requirements.txt`
  - Commit trên `main`: `4bb6dac` (v0), `f239a1c` + `0b7cb18` (v2), `c1916d4` (sửa tên tool), `d4bfb40` (v3), `a68630d` (v4 + group), `511f239` (UI), `814a3d0` (B4), `a8d57c9` (B6)
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:

  Tôi dùng Claude (Claude Code) vào ba việc chính:

  1. Phản biện và brainstorm ý tưởng: nên làm tool mới nào và làm thế nào để kiểm tra một tool hoạt động tốt hay không. Tôi tự đặt ra các tiêu chí chấm điểm: tool dễ viết; tool tách biệt, chạy ổn mà không xung đột với các tool khác, để sau này thêm tool mới thì ít bị xung đột; và tool hữu ích, tức là người dùng có hay hỏi kiểu đó không và tool giải quyết được nhiều bài toán không. AI chấm 7 ý tưởng của nhóm theo đúng các tiêu chí này, còn quyết định chọn tool nào là của nhóm.
  2. Review code của các thành viên khác: chỉ ra chỗ sai và giải thích vì sao sai.
  3. Kiểm tra số liệu và dữ kiện trong bài của thành viên: commit CP4 của một bạn ghi kết quả đạt 80%, nhưng AI đối chiếu với repo và báo lại rằng bộ case và tool trong đó không có trong repo, còn run group thật (file JSON kết quả của model OpenAI) chỉ đạt 60%.

  Cách tôi tự kiểm tra: tự mở file run JSON để đối chiếu số liệu, và hỏi lại trực tiếp người làm phần đó trước khi kết luận.

## 5. Tự đánh giá

Qua bài lab này, tôi học thêm được nhiều về prompting: những lỗi phổ biến khi viết prompt, và khi gặp vấn đề thì có thể tự giải quyết, hoặc cân nhắc đưa cách giải vào system prompt hay tạo skill cho AI.

Điểm mạnh nhất của tôi hôm nay là đôn đốc công việc, phân tích và giải thích yêu cầu của bài cho từng thành viên. Nhờ đó mọi người nắm rõ hơn việc mình cần làm và không làm ra ngoài phạm vi.

Điểm yếu: tôi còn đánh giá quá cao vai trò của skill. Khi đưa ra ý tưởng tool "review lại câu hỏi của người dùng", tôi nghĩ ngay tới việc làm thành skill mà không cân nhắc đưa nó vào system prompt trước. Khả năng quyết định go / no-go của tôi vẫn cần cải thiện. Trong lúc làm nhóm, tôi cũng dễ bị cuốn vào chi tiết và phân tích giải pháp quá sâu mà không để ý tình hình chung, dẫn tới mất thời gian không cần thiết.
