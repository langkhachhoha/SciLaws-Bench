# Trạng thái dự án và việc tiếp theo

Cập nhật 2026-10-31. File này để bật lại công việc trên máy khác. Memory của
Claude Code nằm trong `~/.claude` nên không đi theo repo; những gì cần giữ đều ở
đây và trong `CLAUDE.md`. `CLAUDE.md` giữ các quy tắc và chi tiết kỹ thuật, file
này giữ bối cảnh, kết quả và kế hoạch.

## Mục tiêu

Viết bài báo đề xuất một **Agent Harness cho bài toán khám phá định luật bằng thí
nghiệm chủ động**, đánh giá trên SciLaws-Parallel, chỉ dùng **66 bài Type I**,
metric **S_S**. Agent tham chiếu trong `baseline_agent/` là baseline phải vượt.
Giữ nguyên `harness/` và các giới hạn của `SimulatorTask`; harness mới viết bên
cạnh `baseline_agent/`.

## Bật lại trên máy mới

```bash
git clone https://github.com/langkhachhoha/SciLaws-Bench.git && cd SciLaws-Bench
python3.11 -m venv .venv
.venv/bin/pip install -r requirements-agent.txt
.venv/bin/hf download RealSR/SciLaws-Bench --repo-type dataset --local-dir . --include 'tasks/*'
ls tasks/typeI | wc -l; ls tasks/typeII | wc -l     # phải là 66 và 52; thiếu thì tải lại
export AWS_PROFILE=reddy-research AWS_REGION=us-east-1
aws sts get-caller-identity                         # profile phải được cấu hình lại trên máy mới
.venv/bin/python scripts/run_status.py experiments/parallel_typeI_br-glm-5   # kiểm tra nhanh, không tốn tiền
```

`tasks/` và `.venv/` không nằm trong git. Các file trong `experiments/` có ghi
đường dẫn tuyệt đối của máy cũ, điều này không ảnh hưởng gì.

## Kết quả đã có

Agent tham chiếu, thêm guidance cho `<experiment>` ở các dòng có ghi, 30 turn,
Type I, S_S strict chia cho 66. Judge là Opus
4.6 trên Bedrock, không phải GPT-5.4-mini như bài báo, nên phải ghi rõ khi báo cáo.

| Run | S_S | Nộp | Experiment TB /10 | Turn TV | Chi phí agent | Thư mục |
|---|---|---|---|---|---|---|
| GLM-5, thinking bật | **0,489** | 66/66 | 6,6 | 25 | $28,10 | `experiments/parallel_typeI_br-glm-5/` |
| Qwen3 Coder 30B, không thinking | **0,337** | 66/66 | 4,6 | 11 | $1,07 | đã xoá, commit `240e29b` |
| Qwen3 Coder 30B, có guidance | **0,341** | 66/66 | 4,3 | 9 | $1,06 | `experiments/parallel_typeI_br-qwen3-coder-30b_guided/` |
| MiniMax M2.5, reasoning, có guidance | **0,447** | 66/66 | 5,0 | 19,5 | $6,00 | `experiments/parallel_typeI_br-minimax-m2-5_guided/` |

Mốc Parallel Type I của bài báo (`baseline_agent/all_results.md`): GPT-5.5 0,602,
GLM-5.2 0,564, Opus 4.8 0,530, DeepSeek-V4 Pro 0,511, GPT-5-mini 0,447,
gpt-4o-mini 0,345. Không model nào trong 9 model của bài báo gọi được trên tài
khoản này, nên GLM-5 và Qwen3 Coder là hai mốc thay thế: một lớn, một nhỏ.

Các model đã thử và bỏ (chi tiết trong `CLAUDE.md`): gpt-oss-20b trả về rỗng ở
phần lớn turn; GLM-4.7 Flash tắt thinking lặp ở 46/66 bài, run đã xoá; Qwen3 32B
chỉ có context 32k; Llama 4 Maverick nộp sau khoảng 6 turn; Nova Lite cũng lặp; gpt-oss-120b trả rỗng như bản 20b và nộp sớm.
Dữ liệu pilot và script ở `experiments/pilot_small_models/` tại commit `240e29b`.

## Phát hiện chính, là cơ sở cho harness mới

### 1. Lỗi `equal length` làm mất nhiều turn nhất

Model gửi các mảng dài khác nhau vì tưởng simulator tự ghép lưới, trong khi các
mảng được ghép theo từng vị trí và phải dài bằng nhau
(`harness/sim_runtime.py:322`). Prompt chỉ có ví dụ một biến nên không nói rõ quy
tắc này, và thông báo lỗi không nêu độ dài hay cách sửa.

| Chỉ số | GLM-5 | Qwen3 Coder 30B |
|---|---|---|
| Bài có ≥1 experiment thất bại | 34/66 | 22/66 |
| Lần gọi thất bại | 58 | 185 |
| Tỷ lệ trên tổng số turn | 3,7% | 21,5% |
| Chuỗi thất bại liên tiếp dài nhất | 2 | 30 |
| Bài có chuỗi ≥3 | 0 | 11 |

GLM-5 mắc lỗi ở nhiều bài hơn, nên nguyên nhân gốc là ở harness, không phải do
model yếu. Khác biệt nằm ở khả năng hồi phục. Ba bài Qwen gần như mất trắng:
`mincer_earnings_acs_pums__log_wage` (30 lỗi, 0 experiment),
`binary_pulsar_post_keplerian_atnf__PBDOT` (27), `spirometry_nhanes__FEV1_L` (25).

Đếm "câu trả lời giống hệt câu trước" là chưa đủ: chỉ số đó bỏ sót kiểu luân phiên
A-B-A-B và kiểu mỗi lần sai một khác. Nên đếm số lần gọi thất bại và chuỗi dài
nhất. `run_status.py` và `score_typeI.json` hiện vẫn dùng chỉ số cũ.

### 2. Thí nghiệm phát lại: vì sao có model thoát được

Lấy lịch sử đúng lúc gặp lỗi rồi gọi lại, 15 lần mỗi ô, đếm số lần sửa đúng
(`experiments/pilot_small_models/replay_loop.py` tại commit `240e29b`). Mẫu nhỏ, lịch sử lấy từ Flash.

| | Ngay sau lỗi đầu | Sau khi đã lặp 5 lần |
|---|---|---|
| GLM-5, tắt thinking, T=0,4 | 15/15 | 5/15 |
| GLM-5, tắt thinking, T mặc định | 14/15 | 10/15 |
| GLM-5, bật thinking | 15/15 | 15/15 |
| Flash, tắt thinking, T=0,4 | 1/15 | 0/15 |
| Flash, tắt thinking, T mặc định | 2/15 | 3/15 |
| Flash, bật thinking | 11/15 | 10/15 |

Rút ra: model mạnh tự sửa được; thinking giúp thoát lỗi, chỉ cần một hai câu đọc
lại lỗi; vòng lặp tự củng cố, cả GLM-5 cũng bị kéo xuống 5/15; temperature giúp ít.

### 3. Agent bỏ phí ngân sách

GLM-5 dùng 6,6/10 experiment, 48/66 bài nộp trước turn 30. Qwen nộp ở turn trung vị
11 với 4,6 experiment. Agent không được báo số turn hay ngân sách còn lại. Trên GLM-5,
số experiment chưa cho thấy liên hệ rõ với điểm.

### 4. Chi phí nằm ở lịch sử gửi lại mỗi turn

Với GLM-5, input chiếm 86% chi phí và reasoning chỉ khoảng 6%, nên tắt thinking gần
như không tiết kiệm. Reasoning không bị đưa vào lịch sử. Lịch sử cuối mỗi bài gồm
44% text của assistant, 42% feedback của tool, 13% đề bài. Bedrock tự cache khoảng
16% input của GLM-5 nhưng không đều; chưa biết có được giảm giá không. Cost Explorer
có số liệu sau khoảng một ngày, so token input bị tính tiền với tổng `prompt_tokens`.

### 5. Hai điểm dễ sai khi tính điểm

- `strict_mean` của scorer chỉ chia cho số bài có nộp. Phải dùng `score_typeI.json`.
- Lượt cuối vẫn nhận công thức khi không có experiment nào thành công, nên một bài
  có thể có điểm từ kiến thức sẵn có. `mincer` trên Qwen được 0,25 theo cách đó.

### 6. Sửa lỗi `<experiment>`: gần hết lỗi, nhưng điểm chưa tăng

`guided_agent/experiment_guidance.py` bọc `get_task_prompt` và `run_experiment` của
task. Từ 2026-10-31 đây là bản chính: bật mặc định ở chế độ Parallel, cả ba script
ghi vào thư mục `*_guided`; `--no-experiment-guidance` hoặc `EXPERIMENT_GUIDANCE=0`
trả về agent tham chiếu. Prompt của 36 bài nhiều biến có thêm quy tắc ghép theo vị trí và hai ví dụ dùng cột
của chính bài đó. Lỗi `equal length` trả thêm độ dài từng mảng và một
`corrected_request` hợp lệ. Request vẫn được chấp nhận hay từ chối như cũ, nên mọi
giới hạn của `SimulatorTask` giữ nguyên. 30 bài một biến giữ nguyên prompt.

Lỗi `equal length` có hai ý định: 106/179 lần là kiểu lưới (`[4 giá trị]` với
`[3 giá trị]`), 73/179 lần là kiểu giữ cố định (`[116.0]`).

| Chỉ số | Không guidance | Có guidance |
|---|---|---|
| S_S | 0,337 | 0,341 |
| Experiment thất bại | 185 ở 22 bài | 5 ở 5 bài |
| Trong đó `equal length` | 179 | 1 |
| Bài có chuỗi ≥3 | 11 | 0 |
| Chuỗi dài nhất | 30 | 1 |
| Experiment TB /10 | 4,6 | 4,3 |
| Bài nộp bằng lượt ép | 3 | 0 |
| Bài có 0 experiment | 1 | 0 |

S_S lệch +0,004, khoảng tin cậy bootstrap ghép cặp 95% là [−0,030; +0,038], nên
chưa có bằng chứng guidance làm tăng điểm. Có 20/66 bài đổi điểm (11 tăng, 9 giảm),
nhưng 8/30 bài một biến có prompt giống hệt cũng đổi, nên đây là mức nhiễu giữa hai
lần chạy và chấm. Nhóm 36 bài nhiều biến giữ nguyên 0,333.

Pilot trên 5 bài tệ nhất từng cho 3 bài lên 0,5, nhưng run đủ không lặp lại: cả ba
vẫn ở 0,25. Vì vậy đừng đánh giá trên một lần chạy của vài bài.

Rút ra: lỗi format không phải nút thắt chính của Qwen. Ba bài gần như mất trắng ở run
cũ được 0,25 và run mới cũng 0,25. Bỏ được lỗi, model vẫn dừng sớm (4,3/10
experiment, turn trung vị 9).

Còn một khoảng trống: `commuting_gravity_lodes__flow_Tij` lặp y nguyên 23 turn. Model
viết tay 70 điểm và đếm sai, 70 vượt `MAX_CORRECTED_POINTS` = 64 nên không có
`corrected_request`, model chuyển sang `[107.0] * 70`, không phải JSON hợp lệ. Kiểu
này nhận `Invalid response` thay vì `<experiment_output>` nên không được tính vào
"experiment thất bại"; `run_status.py` chỉ thể hiện qua số bài lặp câu trả lời.

### 7. MiniMax M2.5: model reasoning rẻ, S_S 0,447

Cần một model reasoning rẻ hơn GLM-5 ($1,00 / $3,20) mà không phải dùng `high`. Gọi
thử 10 model ở cả 4 mức effort cho thấy nhiều model rẻ chỉ reasoning ở `high`, nên
chỉ còn MiniMax M2.5 ($0,30 / $1,20), Kimi K2 Thinking ($0,60 / $2,50) và gpt-oss-120b
($0,15 / $0,60). Bảng phân loại ở `CLAUDE.md`.

Pilot 6 bài, có guidance, `medium`, judge Opus 4.6. Chọn các bài GLM-5 hơn Qwen nhiều,
cộng `cepheid`, `mincer` và `commuting_gravity`, nên số này chỉ để xếp hạng hai model
rẻ, không phải ước lượng S_S.

| Chỉ số | MiniMax M2.5 | gpt-oss-120b | GLM-5 | Qwen, guidance |
|---|---|---|---|---|
| Điểm TB trên 6 bài | 0,583 | 0,375 | 0,750 | 0,292 |
| Experiment TB /10 | 5,2 | 2,2 | | |
| Turn TV | 19 | 11,5 | | |
| Reply rỗng | 0/119 | 4/78 | | |
| Chi phí mỗi bài | $0,08 | $0,02 | ≈$0,43 | ≈$0,02 |

MiniMax reasoning ở mọi mức, kể cả không gửi effort, nên `medium` chỉ là danh nghĩa.
`commuting_gravity` dùng đủ 10/10 experiment và được 0,75, bằng GLM-5, trong khi Qwen
lặp 23 turn ở bài này.

Run đủ 66 bài (2026-10-31) có S_S 0,447, nộp 66/66, không bài nào bị gián đoạn, chi
phí agent $6,00, bằng 21% GLM-5 ($0,09 so với $0,43 mỗi bài). Judge của cả ba run là
Opus 4.6. So sánh ghép cặp trên 66 bài, khoảng tin cậy bootstrap 95%:

| So sánh | Chênh lệch S_S | KTC 95% | Hơn / kém / bằng |
|---|---|---|---|
| MiniMax − GLM-5 | −0,042 | [−0,095; +0,011] | 12 / 20 / 34 |
| MiniMax − Qwen, guidance | +0,106 | [+0,057; +0,155] | 26 / 6 / 34 |

| Chỉ số | MiniMax | GLM-5, không guidance | Qwen, guidance |
|---|---|---|---|
| S_S 30 bài một biến | 0,458 | 0,458 | 0,350 |
| S_S 36 bài nhiều biến | 0,438 | 0,514 | 0,333 |
| Bài đạt từ 0,75 trở lên | 8 | 16 | 2 |
| Bài dùng đủ 10 experiment | 0 | 6 | 0 |
| Bài nộp trước turn 30 | 59 | 48 | 65 |
| Experiment thất bại | 22 ở 17 bài | 58 ở 34 bài | 5 ở 5 bài |

- MiniMax hơn Qwen rõ ràng. Với GLM-5, một lần chạy chưa tách được khác biệt, và phép so
  sánh này lẫn cả model lẫn guidance vì GLM-5 chạy không guidance.
- GLM-5 hơn ở bài nhiều biến và ở nhóm điểm cao; bài một biến thì hoà.
- Reasoning giúp model làm việc lâu hơn (turn trung vị 19,5 so với 9 của Qwen), nhưng
  vẫn chỉ dùng 5,0/10 experiment. Tương quan giữa số experiment và điểm là −0,04.
- 22 lần thất bại gồm 11 `n_samples` vượt trần, 9 `equal length`, 2 vượt số điểm. Chuỗi
  dài nhất là 3. Reply rỗng 2/1329 turn.
- `commuting_gravity` từ 0,75 ở pilot xuống 0,5 với 5 experiment ở run đủ, thêm một ví dụ
  cho thấy không nên kết luận từ một lần chạy của vài bài.

S_S trùng với GPT-5-mini của bài báo (0,447), nhưng judge khác nên chỉ để tham khảo.

**Contract check làm mất điểm oan.** `her_hor_pt_acid_kucernak__current_density` được
judge cho 0,5 nhưng tính 0 vì `predict returned non-finite values`. Check này
(`_sample_matrix` trong `harness/evaluate_parallel.py`) chạy `predict` trên 8 dòng trải
theo `range` của metadata. `c_acid` chỉ có `values: [0.5, 4.0]`, không có `range`, nên
bị thử trên [0; 1]; dòng đầu có `c_acid = 0` và `c_acid ** (-m)` thành `inf`. Công thức
vẫn hữu hạn trên cả 676 dòng train. GLM-5 mất đúng bài này (judge cho 0,25), còn Qwen
thì không. Điểm chính thức giữ nguyên vì `harness/` đóng băng; nếu dùng điểm judge,
MiniMax là 0,455 và GLM-5 là 0,492. Có 9/66 bài có input không có `range`.

## Việc tiếp theo

1. Đưa "số lần gọi experiment thất bại" và "chuỗi thất bại dài nhất" vào phần cuối
   của các script chạy; `scripts/run_status.py` đã có.
2. Viết tiếp harness cạnh `baseline_agent/`, dùng lại `SimulatorTask`:
   - bắt lỗi JSON có biểu thức Python và cho `corrected_request` với yêu cầu dài hơn
     64 điểm (bài `commuting_gravity`);
   - phát hiện lỗi lặp sớm, ép model đọc lại lỗi trước khi hành động;
   - báo số turn và số experiment còn lại, vì Qwen vẫn dùng chưa đến nửa ngân sách;
   - dùng prompt caching hoặc rút gọn output cũ để giảm input;
   - chạy thử contract check trước khi nộp và cho model sửa, để công thức đúng không bị
     tính 0 như `her_hor_pt_acid_kucernak__current_density`.
3. Chạy mỗi cấu hình nhiều lần trước khi kết luận, vì một lần chạy không tách được
   tác dụng cỡ 0,03 khỏi nhiễu. Sau đó thử guidance trên GLM-5.
4. Dùng cùng judge với các mốc: `JUDGE_MODEL=global.anthropic.claude-opus-4-6-v1`.
5. Cân nhắc metric phụ không cần judge: lỗi dự đoán so với định luật ẩn không nhiễu,
   hiệu quả (experiment, turn, token), và chấm lại 2–3 lần để đo độ dao động của judge.

## Lưu ý vận hành

- Tài khoản AWS dùng chung và chạy bằng credit. Không API nào cho biết credit còn
  lại, phải hỏi chủ tài khoản trước khi chạy lớn. Tháng 10/2026 đã dùng khoảng $10k.
- Quota Claude theo ngày rất nhỏ. Hôm 30/10 profile `us.` của Opus 4.6 báo 429, nên
  judge dùng profile `global.`; nếu gặp 429, chạy lại script để chấm tiếp.
- Script chạy trong tmux và resume được: chạy lại đúng lệnh. Nhớ dán từng dòng một.
- Không sửa file `.sh` đang chạy. Mỗi bài mới import lại `call_llm_api.py`, nên sửa
  file này khi run đang chạy phải giữ nguyên hành vi.
- Theo dõi: `watch -n 20 .venv/bin/python scripts/run_status.py <run_dir>`. Màn hình
  tmux chỉ in khi có bài xong.
