# Trạng thái dự án và việc tiếp theo

Cập nhật 2026-10-30. File này để bật lại công việc trên máy khác. Memory của
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

Đều là agent tham chiếu, 30 turn, Type I, S_S strict chia cho 66. Judge là Opus
4.6 trên Bedrock, không phải GPT-5.4-mini như bài báo, nên phải ghi rõ khi báo cáo.

| Run | S_S | Nộp | Experiment TB /10 | Turn TV | Chi phí agent | Thư mục |
|---|---|---|---|---|---|---|
| GLM-5, thinking bật | **0,489** | 66/66 | 6,6 | 25 | $28,10 | `experiments/parallel_typeI_br-glm-5/` |
| Qwen3 Coder 30B, không thinking | **0,337** | 66/66 | 4,6 | 11 | $1,07 | `experiments/parallel_typeI_br-qwen3-coder-30b/` |

Mốc Parallel Type I của bài báo (`baseline_agent/all_results.md`): GPT-5.5 0,602,
GLM-5.2 0,564, Opus 4.8 0,530, DeepSeek-V4 Pro 0,511, GPT-5-mini 0,447,
gpt-4o-mini 0,345. Không model nào trong 9 model của bài báo gọi được trên tài
khoản này, nên GLM-5 và Qwen3 Coder là hai mốc thay thế: một lớn, một nhỏ.

Các model đã thử và bỏ (chi tiết trong `CLAUDE.md`): gpt-oss-20b trả về rỗng ở
phần lớn turn; GLM-4.7 Flash tắt thinking lặp ở 46/66 bài, run đã xoá; Qwen3 32B
chỉ có context 32k; Llama 4 Maverick nộp sau khoảng 6 turn; Nova Lite cũng lặp.
Dữ liệu pilot và script ở `experiments/pilot_small_models/`.

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
(`experiments/pilot_small_models/replay_loop.py`). Mẫu nhỏ, lịch sử lấy từ Flash.

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

## Việc tiếp theo

1. Đưa "số lần gọi experiment thất bại" và "chuỗi thất bại dài nhất" vào
   `scripts/run_status.py` và phần cuối của các script chạy.
2. Viết harness mới cạnh `baseline_agent/`, dùng lại `SimulatorTask`:
   - thêm ví dụ hai biến vào prompt và làm rõ quy tắc ghép theo vị trí;
   - bọc thông báo lỗi để nêu độ dài từng mảng và cách sửa;
   - phát hiện lỗi lặp sớm, ép model đọc lại lỗi trước khi hành động;
   - báo số turn và số experiment còn lại;
   - dùng prompt caching hoặc rút gọn output cũ để giảm input.
3. Đo trước trên 22 bài Qwen có experiment thất bại, rồi chạy đủ 66 bài với cả hai
   model. Lọc danh sách từ trajectory của run Qwen.
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
