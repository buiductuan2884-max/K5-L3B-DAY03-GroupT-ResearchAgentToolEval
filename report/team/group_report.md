# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: GroupT
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v4: OpenAI `gpt-4o-mini` (`--provider openai`)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

**GroupT Research Agent** là trợ lý nghiên cứu dùng tool calling (OpenAI `gpt-4o-mini`): người dùng hỏi bằng tiếng Việt, agent tự chọn trong 14 tool để tìm tin web và tweet, đọc URL, tìm và đọc paper arXiv, tra policy nội bộ, tổng hợp thành bản tin, và chỉ gửi Telegram sau khi người dùng xác nhận. Nhóm thêm 4 tool mới: `deduplicate_news` (gộp tin trùng), `wiki_sum` (kiến thức nền từ Wikipedia), `validate_url` (kiểm tra link) và `date_localized` (giờ theo múi giờ). Khi thiếu thông tin (tài khoản, link), agent hỏi lại thay vì tự đoán.

**Cách chạy UI:** `cd starter_v0 && pip install -r requirements.txt && streamlit run app.py` (dependency `streamlit>=1.40` đã có trong `starter_v0/requirements.txt`). UI dùng lại vòng lặp tool của `chat.py`, hiện từng lần gọi tool kèm args/kết quả và lưu transcript vào `starter_v0/transcripts/`.

**Link dùng thử (deploy):** https://coast-gray-injured-hoping.trycloudflare.com (Cloudflare quick tunnel từ máy nhóm trưởng; link chỉ sống khi máy đó đang chạy Streamlit và cloudflared).

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
| timeline | lấy tweet gần đây của một tài khoản X đã biết | không |
| social_search | tìm tweet theo từ khoá / chủ đề | không |
| lookup | tìm tin / thông tin trên web (Tavily), có topic và timeframe | không |
| fetch | đọc nội dung một URL cụ thể (Firecrawl) | không |
| format | trình bày item đã có thành bản tin markdown | không |
| send | gửi nội dung lên Telegram, chỉ sau khi người dùng xác nhận | không (bonus có sẵn) |
| policy | tra cứu policy nội bộ | không (bonus có sẵn) |
| papers | tìm paper arXiv | không (bonus có sẵn) |
| paper_text | lấy text PDF của paper arXiv | không (bonus có sẵn) |
| deduplicate_news | gộp tin trùng theo URL chuẩn hoá hoặc mức độ từ chung trong tiêu đề | có |
| wiki_sum | lấy đoạn giới thiệu Wikipedia cho câu hỏi kiến thức nền "X là ai?" | có |
| validate_url | kiểm tra định dạng URL, domain rút gọn và blacklist cục bộ | có |
| date_localized | trả ngày giờ hiện tại theo timezone / thành phố | có |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1. "Tin AI mới nhất tuần này là gì?" → `lookup`
2. "Tóm tắt bài này giúp mình" rồi gửi link ở lượt sau → hỏi lại link, sau đó `fetch`
3. "Bây giờ ở Tokyo là mấy giờ?" → `date_localized`
4. "Ada Lovelace là ai?" → `wiki_sum`
5. "Link https://bit.ly/ai-update có an toàn không?" → `validate_url`

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

- Thêm `deduplicate_news`, tool xử lý cục bộ để gộp tin trùng khi người dùng có ít nhất hai tin từ các nguồn và muốn loại bỏ trùng lặp. Tool chuẩn hoá URL trước, sau đó so các từ trong tiêu đề; nguồn được gộp và summary dài hơn được giữ lại. Dùng trước `format`, không dùng để tìm tin mới hoặc tóm tắt một bài.
- **v1, `system_prompt.md`** (An): bỏ 3 câu của baseline ép agent tự đoán khi thiếu thông tin, "cứ gửi luôn" và "chỉ chọn một tool"; thay bằng quy tắc: thiếu thông tin thì hỏi lại, gửi/đăng phải được xác nhận, được không gọi tool hoặc gọi nhiều bước, không bịa tham số (`system_prompt.md:6-8`). Base 0.65 → 0.75.
- **v2, `tools.yaml`** (An: `clarify`, `timeline`, `social_search`; Tuấn: `lookup`, `fetch`, `format`; Huy: `send`, `policy`, `papers`, `paper_text`): viết lại mô tả 10 tool theo dạng DÙNG khi / KHÔNG DÙNG khi, kèm ví dụ tham số (vd `lookup.query` chỉ gồm từ khoá, `topic="news"` khi hỏi tin; `fetch` không có link thì gọi `clarify` text; `send` phải hỏi `clarify` yes_no trước). Base 0.75 → 0.85.
- **v3, `tools.yaml`** (An): `clarify` bắt buộc `response_type` và mô tả khi nào dùng `yes_no`; sửa mô tả `screenname` của `timeline`. Base 0.85 → 0.90.
- **v4, tool mới** (Cường, khai báo `deduplicate_news`: Tuấn): thêm `wiki_sum` (câu hỏi kiến thức nền "X là ai?"), `validate_url` (khi người dùng hỏi một link có hợp lệ/an toàn không), `date_localized` (khi hỏi trực tiếp giờ/ngày ở một nơi), khai báo trong `tools.yaml` và thêm 1 đoạn routing cho chúng trong `system_prompt.md:10`. Base giữ 0.90, group 0.60.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline |  | — | 0.65 | `runs/v0_B_base_openai_20261110T173124939840.json` |
| v1 | system_prompt.md | Câu trả lời sai do thiếu các trường thông tin, nên giải quyết bằng: thiếu thông tin thì hỏi lại; gửi thì phải bắt xác nhận; được phép không gọi tool hoặc gọi nhiều bước. Khi đó 5 case (R08, R10, R11, R12, R14) sẽ pass mà không gây hỏng case routing. | 0.65 | 0.75 | `runs/v1_B_base_openai_20261110T183730315565.json` |
| v2 | tools.yaml | Mô tả rõ ràng khi nào tool được phép sử dụng, khi nào không, kèm mô tả tham số cho 10 tool. Khi đó R11, R13, M02 sẽ pass. | 0.75 | 0.85 | `runs/v2_B_base_openai_20261110T194023990931.json` |
| v3 | tools.yaml | Bắt buộc dùng trường response_type, dùng yes_no cho việc cần xác nhận, sửa mô tả screenname. Khi đó R10, R12, M03 sẽ pass. | 0.85 | 0.90 | `runs/v3_B_base_openai_20261110T220531642617.json` |

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

Run: `starter_v0/runs/v4_B_group_openai_20261111T000014139367.json` (v4, gpt-4o-mini): case_accuracy 0.6 (6/10), routing 0.8, multiturn 0.4, provider_error_cases 0.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_wikipedia_knowledge_summary | Câu hỏi 'X là ai?' về kiến thức nền → wiki_sum, không phải lookup tin tức. | `wiki_sum(title='Ada Lovelace')` | FAIL: title: expected 'Ada Lovelace', got 'Ada_Lovelace' |
| G02_validate_shortened_link | Hỏi trực tiếp kiểm tra một URL → validate_url; kết quả cần được diễn giải thận trọng, không khẳng định an toàn tuyệt đối. | `validate_url(url='https://bit.ly/ai-update')` | PASS |
| G03_direct_local_time | Hỏi trực tiếp giờ hiện tại tại thành phố → date_localized với timezone IANA; không dùng tra cứu web. | `date_localized(timezone='America/Los_Angeles')` | PASS |
| G04_today_news_uses_lookup | Từ 'hôm nay' trong câu hỏi tìm tin yêu cầu lookup timeframe=day, không dùng date_localized. | `lookup(query='AI', topic='news', timeframe='day')` | PASS |
| G05_specific_article_uses_fetch | Đã có URL và yêu cầu đọc/tóm tắt thì gọi fetch trực tiếp, không gọi validate_url trước. | `fetch(url='https://openai.com/research/')` | PASS |
| G06_multiturn_time_location | Nhiều lượt làm rõ địa điểm; lượt cuối yêu cầu giờ hiện tại và phải truyền đúng timezone Tokyo. | `date_localized(timezone='Asia/Tokyo')` | PASS |
| G07_multiturn_url_validation | Lấy URL từ lượt trước để kiểm tra ở lượt hiện tại; không fetch link. | `validate_url(url='https://tinyurl.com/example-check')` | FAIL: extra tool call validate_url |
| G08_multiturn_wikipedia_followup | Yêu cầu lượt cuối chỉ rõ nguồn Wikipedia; dùng wiki_sum cho kiến thức nền, không dùng lookup. | `wiki_sum(title='Alan Turing')` | FAIL: title: expected 'Alan Turing', got 'Alan_Turing' |
| G09_multiturn_news_topic_correction | Giữ timeframe=day từ ngữ cảnh, dùng chủ đề đã sửa robotics và route qua lookup. | `lookup(query='robotics', topic='news', timeframe='day')` | PASS |
| G10_multiturn_publish_confirmation | Dù có nội dung và đích đến, yêu cầu chỉ hỏi xác nhận nghĩa là chưa cho phép gửi; không gọi send, phải xác nhận trước. | `clarify(response_type='yes_no')` | FAIL: missing tool call clarify; extra tool call format |

#### Phân tích 4 case FAIL (run v4 group)

- **G01_wikipedia_knowledge_summary** và **G08_multiturn_wikipedia_followup** (`wrong_arg_value`): đúng tool `wiki_sum` nhưng agent truyền `title="Ada_Lovelace"` / `"Alan_Turing"` (dấu gạch dưới) trong khi đáp án là `"Ada Lovelace"` / `"Alan Turing"`. Mô tả tham số `title` chỉ ghi "Tên người/chủ đề hoặc tiêu đề trang Wikipedia cụ thể" (`starter_v0/artifacts/tools.yaml:315`); chữ "tiêu đề trang Wikipedia" có thể khiến model viết theo dạng URL của Wikipedia. Về chức năng thì không sai vì tool tự đổi dấu cách thành `_` (`starter_v0/tools/wiki_sum/tool.py:19`), nên đây là case eval so khớp chặt. **Ngoài ra `tool_results` của cả 2 case cho thấy tool trả lỗi `403 Client Error: Forbidden`** từ Wikipedia: `tool.py:20-22` gọi API mà không gửi header `User-Agent`. Unit test dùng `fake_http` nên không bắt được lỗi này. Đây là ví dụ eval PASS/FAIL theo tool call không phản ánh tool có chạy thật hay không.
- **G07_multiturn_url_validation** (`extra_tool_call`): agent gọi `validate_url` 2 lần, lần đúng với `https://tinyurl.com/example-check` và thêm một lần với `https://tinyurl.com` (chỉ domain). Lần thứ hai không có trong yêu cầu. Prompt cho phép "multiple steps, using as many tools as necessary" (`starter_v0/artifacts/system_prompt.md:12`) và mô tả `validate_url` không nói "gọi một lần cho mỗi link người dùng đưa".
- **G10_multiturn_publish_confirmation** (`wrong_boundary`): người dùng nói rõ "Chuẩn bị nội dung đó và hỏi mình xác nhận trước khi gửi", eval mong đợi `clarify(response_type="yes_no")`, nhưng agent chỉ gọi `format` để soạn bản tin và không hỏi xác nhận. Đây là cùng nhóm lỗi với R12 của base: quy tắc xác nhận nằm ở `system_prompt.md:8` và mô tả `send`, nhưng khi agent chưa gọi `send` thì không có chỗ nào bắt nó phải gọi `clarify` yes_no. Agent không gửi gì đi nên không có rủi ro thật, nhưng hành vi vẫn sai yêu cầu.

**Hướng sửa đề xuất (chưa chạy):** ghi trong mô tả `title` của `wiki_sum` là "dùng dấu cách, không dùng dấu gạch dưới"; thêm `User-Agent` cho request của `wiki_sum`; ghi "gọi validate_url đúng một lần cho mỗi link người dùng đưa"; thêm vào prompt "mọi yêu cầu gửi/đăng phải kết thúc bằng clarify(response_type=yes_no) trước khi gọi send".

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
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py` | 13 test cho 4 tool mới: `deduplicate_news` 4 (URL, tiêu đề, input sai, ngưỡng sai), `wiki_sum` 3, `validate_url` 3, `date_localized` 3; toàn bộ suite: 95 passed, 0 failed | 14 test TODO mẫu của các tool có sẵn vẫn skipped |
| UI (lệnh chạy + link dùng thử) | `starter_v0/app.py`, `streamlit run app.py`, https://coast-gray-injured-hoping.trycloudflare.com | Dùng lại `run_model_tool_loop` của `chat.py`; mỗi lần gọi tool hiện args + kết quả; transcript lưu `transcripts/*_ui_*.transcript.json` | Lỗi tool/provider hiện ra (✗, `st.error`), không bị giấu; câu mẫu không có lệnh gửi |

Tool unit tests: 13 test cho 4 tool mới (`starter_v0/tests/test_tools_todo.py`). Ví dụ unit test bắt được mà eval không bắt được: `test_deduplicate_news_returns_error_for_invalid_threshold` kiểm tra ngưỡng ngoài (0, 1] trả error dict; eval chỉ so tên tool và tham số nên không bao giờ chạy tới nhánh này. Chiều ngược lại cũng có: lỗi `403` của `wiki_sum` không unit test nào bắt (test dùng `fake_http`) và eval cũng không bắt (eval không kiểm tra nội dung tool trả về).

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | Không làm | — | — |
| Hơn 3 tool mới (≥ 4) | `starter_v0/tools/{deduplicate_news,wiki_sum,validate_url,date_localized}/`, `tests/test_tools_todo.py` (4+3+3+3 test) | Cả 4 tool đăng ký trong `tools/__init__.py` và khai báo trong `tools.yaml`; `pytest`: 95 passed, 0 failed; base v4 giữ 0.9 | `validate_url` chỉ kiểm tra cục bộ (định dạng, domain rút gọn, blacklist `URL_BLACKLIST_DOMAINS`), không quét mã độc. `wiki_sum` gọi thật bị Wikipedia trả `403 Forbidden` vì request thiếu `User-Agent` (`starter_v0/tools/wiki_sum/tool.py:20-22`; bằng chứng: `tool_results` của G01, G08 trong `runs/v4_B_group_openai_20261111T000014139367.json`); unit test dùng `fake_http` nên không bắt được (leader kiểm chứng) |
| `send` gửi thật lên Telegram sau xác nhận | Không làm (chưa cấu hình `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`) | Lượt 4 trong B4: agent hỏi xác nhận, không gọi `send` | `send` từ chối khi `confirmed=false` (`tools/send/tool.py:12`) |
| Test challenge (0 skipped / regression test) | Không làm (`pytest`: 95 passed, 14 skipped) | — | — |

Test challenge: nhóm không làm.

### B7. Small Local Model Challenge (bonus)

Nhóm không làm bonus này (không chạy model local / Ollama).

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

- **Provider:** không có `OPENROUTER_API_KEY`; README cho phép đổi provider nên nhóm chạy toàn bộ v0–v4 bằng OpenAI `gpt-4o-mini` (`--provider openai`).
- **Windows chặn thư viện:** Windows Application Control chặn file DLL của `jiter 0.19.0` (phụ thuộc của SDK `openai`) nên không chạy được eval. Cách xử lý: cài `jiter==0.18.0` trong `.venv`.
- **Hash artifact lệch giữa đĩa và commit:** git (`core.autocrlf=true`) đổi xuống dòng LF → CRLF khi checkout, làm `tools_hash` trên đĩa (`72a531d55085`) khác hash của run v2 (`0207b8d17077`) dù nội dung giống nhau. Cách xử lý: ghi lại file đúng byte từ commit (`git show HEAD:<file>`) và kiểm tra `versioning.file_hash` trước mỗi lần chạy eval.
- **Merge nhánh tách từ code cũ:** các nhánh thành viên tách ra trước khi có v1/v2, diff trực tiếp với `main` trông như xoá hàng nghìn dòng. Cách xử lý: merge 3-way, chỉ gỡ đúng các đoạn xung đột (vd `send` ở v2, `social_search` ở v3, TEAM.md/`tools.yaml` ở v4) và giữ phần của từng người.
- **Tên tool sai trong mô tả:** mô tả `timeline`/`social_search` nhắc tới `ask_user`, `get_user_tweets` (tên hàm Python) thay vì tên tool `clarify`, `timeline`; sửa ở commit `c1916d4` trước khi chạy v2.
- **UI:** (1) `chat.py` in emoji ra stdout, console Windows cp1252 làm lượt chat có tool bị lỗi `UnicodeEncodeError`; sửa bằng `sys.stdout.reconfigure(encoding="utf-8")` trong `app.py`. (2) Sau khi thêm tool mới, UI báo `unknown_tool` cho `date_localized` vì Streamlit giữ module `tools` đã import; restart server là hết.
- **Tool gọi thật bị lỗi:** `wiki_sum` bị Wikipedia trả `403 Forbidden` (thiếu `User-Agent`), xem phân tích G01/G08 ở B3. Chưa sửa.


## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

Run dùng để đối chiếu: v0 `starter_v0/runs/v0_B_base_openai_20261110T173124939840.json`, v1 `…/v1_B_base_openai_20261110T183730315565.json`, v2 `…/v2_B_base_openai_20261110T194023990931.json`, v3 `…/v3_B_base_openai_20261110T220531642617.json`.

**Fix nào thuộc `system_prompt.md`?**

Các fix sửa được là R08, R14: ở v0, agent tự giải/viết code rồi gọi `send` để gửi kết quả. Nguyên do trực tiếp là câu “Always finish the request in a single step. Pick one tool” trong system prompt v0. Ở v1, prompt cho phép không gọi tool và đặt quy tắc ở `system_prompt.md:6-8`.

Tuy nhiên có tác dụng phụ: v1 làm M02 tụt. Agent ở v1 gọi `social_search(query="robotics")` thay vì `lookup` cho câu hỏi tiếp nối “còn về robotics thì sao?”. v2 sửa lại bằng mô tả `lookup` trong `tools.yaml`.

**Fix nào thuộc `tools.yaml`?**

Các fix thuộc về tool là R13, R11, R10.
- R13 (sửa ở v2): v1 gọi `lookup(query="AI news")` và thiếu `topic`. Ở v2, mô tả `query` ghi “KHÔNG thêm chữ ‘news’…” và mô tả `topic` ghi “‘news’ khi người dùng hỏi tin tức”.
- R11 (sửa ở v2): v1 gọi `clarify` nhưng thiếu `response_type`. Mô tả `fetch` ở v2 ghi “gọi clarify với response_type='text'… không bịa URL” (`tools.yaml:71`).
- R10 (sửa ở v3): v2 vẫn thiếu `response_type`. Ở v3, An đặt `required: [question, response_type]` (`tools.yaml:26`).

Ngoài ra, từ v1 `clarify` đã được gọi đúng tool mà vẫn FAIL chỉ vì thiếu tham số. Vậy có thể nói prompt đã sửa đúng hướng, phần còn thiếu nằm ở khai báo tool.

**Failure nào cần review thủ công thay vì chấm tự động?**

R04, M03 và B4.
- R04 (PASS): agent gọi `fetch(url="https://openai.com/blog/gpt-5")`, nhưng `tool_results` trong run v0 và v3 cho thấy trang trả về “# 404”. Eval chỉ so tên tool và tham số (`run_eval.py:142`, `evaluate_phase_b`), không kiểm tra nội dung tool trả về.
- M03: có thể do đáp án chặt — agent trả `screenname="andrejkarpathy"`, đáp án là `karpathy`. Để biết `andrejkarpathy` có phải tài khoản thật hay không vẫn phải kiểm tra bằng tay.
- B4: lượt 2 và 4 cho thấy agent hỏi lại bằng câu chữ, không gọi `clarify` (`starter_v0/transcripts/v3_openai_20261110T222531182603.transcript.json`). Với người dùng trực tiếp thì hành vi này ổn, nhưng eval sẽ chấm FAIL.

**Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?**

- R12 lỗi ở cả 4 version (agent hỏi nội dung cụ thể cần đăng thay vì hỏi yes/no). Giả thuyết: ghi rõ rằng gặp yêu cầu gửi/đăng thì luôn gọi `clarify(response_type="yes_no")` trước, kể cả khi chưa có nội dung. Khả năng cao lỗi do prompt đang tự mâu thuẫn: `system_prompt.md:8` cho phép đi tiếp “only if the user has clearly specified the content and destination”, trong khi `tools.yaml:110` ghi `send` chỉ dùng khi đã có “một nội dung cụ thể”.
- M03: đổi mô tả để dùng “handle ngắn”, vì mô tả `screenname` ở v3 là “Tên đẩy đủ tài khoản X” (`tools.yaml:33`); chữ “đầy đủ” có thể đẩy model chọn tên dài hơn bình thường.

## 8. Tài liệu tham khảo

- Đề bài và repo gốc: https://github.com/VinUni-AI20k/K5-L3-DAY03-ResearchAgentToolEval (`README.md`, `RULES.md`, `RUBRIC.md`, `SUBMISSION.md`, `CHECKPOINTS.md`)
- Wikipedia REST API (endpoint `page/summary`) dùng trong `wiki_sum`: https://en.wikipedia.org/api/rest_v1/
- Streamlit (UI): https://docs.streamlit.io/
- Cloudflare quick tunnel (link dùng thử UI): https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/
- Công cụ AI dùng hỗ trợ code/phân tích log: ghi trong báo cáo cá nhân của từng thành viên.
