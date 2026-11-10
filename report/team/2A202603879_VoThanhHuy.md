# Báo cáo cá nhân — Lab Day 03

## 1. Thông tin thành viên

- Họ tên: Võ Thanh Huy
- MSSV: 2A202603879
- Email: huyvo180700@gmail.com

## 2. Phần việc phụ trách

Tham gia phần kiểm thử và đánh giá Research Agent, chủ yếu ở CP4. Ngoài ra, hỗ trợ chuẩn bị phần giới thiệu Agent và poster để nhóm sử dụng khi demo.

## 3. Đóng góp cụ thể

Trong quá trình làm bài, tôi đã thực hiện các công việc sau:

- Tích hợp các file CP4 vào dự án và kiểm tra lại cấu trúc thư mục.
- Chạy Unit Test cho tool `prepare_research_request`, kết quả 5/5 test PASS.
- Chạy kiểm tra Tool Contract, kết quả 60/60 test PASS.
- Kiểm tra kết quả Eval: 8 case PASS và 2 case FAIL.
- Xem lại hai case lỗi G04 và G09 để tìm nguyên nhân.
- Hỗ trợ chuẩn bị nội dung Phần A và poster HTML giới thiệu Research Agent.

## 4. Bằng chứng

Các file liên quan đến công việc:

- `starter_v0/data/eval_group.json`: Bộ 10 Eval Case.
- `starter_v0/tests/test_prepare_research_request.py`: Unit Test cho tool mới.
- `starter_v0/tools/prepare_research_request/`: Code và mô tả tool.
- `starter_v0/runs/v3_cp4_B_group_gemini_20261110T231030967596.json`: Kết quả Group Eval.

Commit GitHub: 136208c, 84614e9.

### AI/công cụ đã dùng và cách tự kiểm tra kết quả:

Sử dụng ChatGPT để hỗ trợ tìm hiểu yêu cầu, chuẩn bị nội dung báo cáo, viết và kiểm tra file.

## 5. Tự đánh giá

Qua bài lab này, hiểu rõ hơn cách một AI Agent lựa chọn và gọi công cụ để xử lý yêu cầu của người dùng.

Học được cách chạy Unit Test, đọc kết quả Eval và phân biệt lỗi của model với lỗi API.

Cần tìm hiểu thêm cách viết System Prompt, thiết kế Tool Calling và cải thiện việc xử lý các trường hợp đặc biệt.
D:\Document_D\Vin_AI\K5-L3B-DAY03-GroupT-ResearchAgentToolEval\report\team\2A202603879_VoThanhHuy.md