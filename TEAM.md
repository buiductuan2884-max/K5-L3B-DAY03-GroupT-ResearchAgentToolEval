# Team

## Thông tin nhóm

- Tên nhóm: GroupT
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-GroupT-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/buiductuan2884-max/K5-L3B-DAY03-GroupT-ResearchAgentToolEval, `main`, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Bùi Đức Tuấn | 2A202603902 |       | buiductuan2884-max | Nhóm trưởng |
|   2 | Hoàng Đức An | 2A202603800 | anduchoang2701@gmail.com | katogithub2701 | Thành viên |
|   3 | Nguyễn Mạnh Cường    | 2A202603904     | nggmanhcuong25@gmail.com    | NMCcg  |    thành  viên     |
|   4 | Võ Thanh Huy | 2A202603879 |       | VThanh-Huy | Thành viên |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

report/team/2A202603904_NguyenManhCuong.md


Sao chép mục dưới đây cho từng thành viên.

## BuiDucTuan-2A202603902

### Phần việc phụ trách

- Nhóm trưởng: fork repo, chia việc, review và merge nhánh của các thành viên vào `main`
- CP1: chạy baseline v0 và ghi `version_log.csv`
- CP2: viết lại mô tả `lookup`, `fetch`, `format` trong `tools.yaml` (v2); chạy eval v1-v4
- CP5: UI Streamlit (`starter_v0/app.py`), link dùng thử qua Cloudflare Tunnel, chat live `chat.py` (B4)
- Báo cáo nhóm: B1, B2 (bản nháp), B4, B6 và các mục dữ kiện

### Đóng góp cụ thể

- Baseline v0 (0.65) và các run base v1, v2, v3 (0.90), v4 (0.90), group v4 (0.60), tất cả `provider_error_cases == 0`
- Merge 3-way các nhánh `hoangducan`, `ThanhHuy` (phần v2), `nguyenmanhcuong`; khai báo `deduplicate_news` trong `tools.yaml`
- UI Streamlit dùng lại `run_model_tool_loop` của `chat.py`, hiện từng lần gọi tool (args + kết quả, lỗi hiện ✗), lưu transcript; sửa lỗi `UnicodeEncodeError` trên Windows
- Transcript chat live 4 lượt (`starter_v0/transcripts/v3_openai_20261110T222531182603.transcript.json`)

### Bằng chứng

- Commit trên `main`: `4bb6dac` (v0), `f239a1c` + `0b7cb18` (v2), `d4bfb40` (v3), `a68630d` (v4 + group), `511f239` (UI), `814a3d0` (B4), `a8d57c9` (B6)

## HoangDucAn-2A202603800

### Phần việc phụ trách

- Điều chỉnh system prompt

- Điều chỉnh tool clarify, timeline, social_search

- Phân tích các case lỗi

### Đóng góp cụ thể

- Điều chỉnh system prompt trong system_prompt.md và triển khai thành version 1

- Tool clarify, timeline, social_search được điều chỉnh mô tả tool và mô tả các tham số

- Lập bảng thể các case lỗi, phân tích vì sao lỗi

### Bằng chứng

- Các commit trên nhánh riêng (/hoangducan) gồm commit e5b9844, 0836b0d, 000009a, 6f844ce

## NguyenManhCuong-2A202603904

### Phần việc phụ trách

Cường: thực hiện công việc CP3 và CP4

### Đóng góp cụ thể
- Xây dựng 4 tools mới: DupChecker, Wiki-sum, validate_url, Date-localized
- xây dựng 10 case single turn và mutli turn
### Bằng chứng

- lịch sử commit

## VoThanhHuy-2A202603879

### Phần việc phụ trách

- CP2: viết lại mô tả 4 tool `send`, `policy`, `papers`, `paper_text` trong `tools.yaml` (phần của v2)
- Phần A báo cáo nhóm (A1) và phân tích các case FAIL của group eval (B3)

### Đóng góp cụ thể

- Mô tả `send` có boundary xác nhận: phải gọi `clarify` yes_no trước, chỉ đặt `confirmed=true` sau khi người dùng đồng ý, không dùng cho câu ngoài phạm vi
- Mô tả và tham số của `policy`, `papers`, `paper_text` (khi nào dùng / không dùng, ví dụ tham số)
- Báo cáo cá nhân `report/team/2A202603879_VoThanhHuy.md`

### Bằng chứng

- Commit trên `main`: `35277b4`, `7f99038`, `211c348` (tools.yaml, v2); `e54eb6f`, `8cb78c9`, `1ab7576` (báo cáo cá nhân)
