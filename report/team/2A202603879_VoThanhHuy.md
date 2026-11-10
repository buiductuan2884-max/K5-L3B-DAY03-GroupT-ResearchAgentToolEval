# Báo cáo cá nhân — Lab Day 03

## 1. Thông tin thành viên

- Họ tên: Võ Thanh Huy
- MSSV: 2A202603879
- Email: huyvo180700@gmail.com

## 2. Phần việc phụ trách

Tôi tham gia hỗ trợ kiểm thử và đánh giá Research Agent, chủ yếu ở phần CP4.

## 3. Đóng góp cụ thể

Trong quá trình làm bài, tôi đã thực hiện các công việc:

- Tìm hiểu yêu cầu của CP4 và cấu trúc các file trong dự án.
- Tích hợp và chạy thử một bộ Eval gồm 10 case trên máy cá nhân.
- Chạy Unit Test cho tool thử nghiệm `prepare_research_request`, kết quả 5/5 test PASS.
- Chạy kiểm tra Tool Contract trên bản thử nghiệm, kết quả 60/60 test PASS.
- Chạy Group Eval bằng Gemini 3.5 Flash-Lite, kết quả thử nghiệm đạt 8/10 case PASS.
- Kiểm tra hai case G04 và G09 bị FAIL để tìm hiểu nguyên nhân.

Sau khi đối chiếu với repo chung, nhóm đang sử dụng 4 tool mới là `deduplicate_news`, `wiki_sum`, `validate_url` và `date_localized`.

Kết quả Group Eval chính thức của nhóm ở phiên bản v4 là **6/10 case PASS**. Bốn case FAIL gồm G01, G07, G08 và G10.

## 4. Bằng chứng

### 4.1. Kết quả thử nghiệm cá nhân

- Chạy Unit Test: 5/5 PASS.
- Chạy Tool Contract: 60/60 PASS.
- Chạy Group Eval bằng Gemini: 8/10 PASS.

File kết quả thử nghiệm cá nhân:

`runs/v3_cp4_B_group_gemini_20261110T231030967596.json`

Kết quả này chỉ phản ánh bộ Eval thử nghiệm riêng, không sử dụng để thay thế kết quả của nhóm trong báo cáo chung.

### 4.2. Kết quả chính thức của nhóm

File Group Eval v4:

`starter_v0/runs/v4_B_group_openai_20261111T000014139367.json`

Kết quả: 6/10 PASS.

Các case FAIL:

- G01 — `G01_wikipedia_knowledge_summary`
- G07 — `G07_multiturn_url_validation`
- G08 — `G08_multiturn_wikipedia_followup`
- G10 — `G10_multiturn_publish_confirmation`

- `136208c`
- `84614e9`

## 5. AI/công cụ đã dùng và cách tự kiểm tra kết quả

Tôi sử dụng ChatGPT để hỗ trợ tìm hiểu yêu cầu bài lab, chuẩn bị nội dung báo cáo, viết code thử nghiệm và tìm cách xử lý lỗi.

Trong quá trình thực hiện, tôi đã gặp vấn đề khi sử dụng AI để tổng hợp thông tin cho báo cáo nhóm.

Do AI chưa có đầy đủ dữ liệu từ repo chính thức và tôi chưa kiểm tra kỹ kết quả, một số thông tin được đưa vào báo cáo bị sai. Cụ thể, bản báo cáo ban đầu sử dụng danh sách tool và bộ Eval của phiên bản thử nghiệm cá nhân thay vì phiên bản nhóm đang sử dụng.

Kết quả 8/10 được ghi trong báo cáo ban đầu không phải kết quả chính thức của nhóm. Sau khi đối chiếu với repo, kết quả chính xác của phiên bản v4 là 6/10.

Khi phát hiện vấn đề, nhóm đã kiểm tra lại thông tin trong `tools.yaml`, `eval_group.json` và các file kết quả trong thư mục `runs/`. Những nội dung sai trong báo cáo được chỉnh sửa để phù hợp với phiên bản chính thức.

Ngoài ra, cần cải thiện cách đặt yêu cầu và System Prompt để hạn chế việc AI tự suy đoán khi thiếu thông tin.

## 6. Tự đánh giá

Qua bài lab này, tôi hiểu rõ hơn cách một AI Agent lựa chọn và gọi tool để xử lý yêu cầu của người dùng.

Tôi học được cách chạy Unit Test, đọc kết quả Eval và phân biệt lỗi từ model với lỗi API.

Khó khăn lớn nhất của tôi là chưa nắm rõ cách quản lý các phiên bản trong dự án nhóm. Điều này khiến tôi nhầm lẫn giữa kết quả chạy trên máy cá nhân và kết quả chính thức trong repo.

Tôi cũng nhận ra rằng kết quả do AI cung cấp không phải lúc nào cũng chính xác, đặc biệt khi AI không được cung cấp đầy đủ dữ liệu.

Trong thời gian tới, tôi cần tìm hiểu thêm về Git, cách đồng bộ phiên bản trong dự án nhóm, System Prompt và Tool Calling. Tôi cũng cần chủ động kiểm tra lại nội dung do AI hỗ trợ tạo ra trước khi đưa vào báo cáo chung.
