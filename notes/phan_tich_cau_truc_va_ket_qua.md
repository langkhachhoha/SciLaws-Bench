# SciLaws-Bench: phân tích cấu trúc chạy (SciLaws-Parallel) và kết quả chạy thử

Tài liệu này ghi lại cách repo vận hành ở cấu hình mặc định của paper
(arXiv:2609.01552), tập trung vào nhánh **SciLaws-Parallel**, là nhánh sẽ dùng
cho paper về Agent Harness cho bài toán active experiment. Phần cuối là kết quả
chạy thử một task với Claude trên Amazon Bedrock.

Ngày thực hiện: 2026-10-29. Commit gốc: `6460ba0`.

---

## 1. Benchmark nói gì

Mỗi bài toán là một bài khám phá định luật khoa học: tìm biểu thức đóng
`y = f(X)` cho một đại lượng đo được, lấy từ các paper thực nghiệm đang còn
tranh luận (không phải định luật sách giáo khoa). 118 bài, 6 lĩnh vực, mỗi bài có
hai dạng:

| | SciLaws-Real | SciLaws-Parallel |
|---|---|---|
| Dữ liệu | bảng dữ liệu thật cố định (`data/train.csv`) | **simulator** có thể truy vấn, agent tự chọn điểm đo |
| Đáp án | không có, công thức đã công bố là mốc để vượt | một **luật ẩn tổng hợp** (`simulator/formula.py`), cố ý khác luật đã công bố |
| Điểm | `S_N` (độ khớp số, mốc 0.5 = công thức tốt nhất đã công bố) và `S_V` (tính hợp lệ khoa học) | `S_S`: mức độ khôi phục **cấu trúc** luật ẩn, 5 mức 0 / 0.25 / 0.5 / 0.75 / 1 |

Hai kiểu bài:

- **Type I** (66 bài, single-group): một luật, một bộ hằng số toàn cục. Nộp
  `predict(X)` với hằng số viết thẳng vào code.
- **Type II** (52 bài, multi-group): nhiều nhóm dùng chung một dạng hàm, chỉ vài
  tham số đổi theo nhóm. Nộp `predict(X, **params)` cùng `fit(X_fit, y_fit)`;
  harness tự fit lại tham số trên từng nhóm chưa thấy.

Vì sao Parallel hợp với hướng "active experiment": agent bắt đầu với **0 dòng
dữ liệu**, mọi quan sát đều phải mua bằng `<experiment>` trong một ngân sách
cố định. Luật ẩn được thiết kế để **chống học thuộc**: cùng biến đầu vào và cùng
số hằng số với luật đã công bố, nhưng khác dạng hàm. Một model nhận ra luật quen
thuộc rồi nộp luôn sẽ chỉ được 0.5. Phải thiết kế thí nghiệm để phân biệt các
dạng hàm thì mới lên được 0.75–1.0.

## 2. Cấu trúc repo

```
SciLaws-Bench/
├── harness/                  # GIAO DIỆN CỐ ĐỊNH, mọi solver dùng chung
│   ├── prompts.py            # system prompt + task prompt (Real / Parallel, Type I / II)
│   ├── agent_protocol.py     # parse thẻ XML, sandbox <python>, hàm step()
│   ├── sim_runtime.py        # simulator: load state.joblib, fetch_data / fetch_where
│   ├── evaluate_parallel.py  # chấm S_S: stage → judge (Codex) → aggregate
│   ├── evaluate_numeric.py   # chấm S_N (Real)
│   ├── evaluate_validity.py  # chấm S_V (Real)
│   └── eval_formula.py       # lõi chạy công thức + metric
├── baseline_agent/           # AGENT THAM CHIẾU (vòng ReAct)
│   ├── run_baseline.py       # chạy 1 task → submission .py + trajectory .json
│   ├── run_batch.py          # chạy nhiều task/model song song, tổng hợp summary
│   ├── agent.py              # vòng lặp turn (≈150 dòng)
│   ├── task.py               # RealSRTask / SimulatorTask (ngân sách thí nghiệm nằm ở đây)
│   ├── call_llm_api.py       # client đa provider (đã thêm Amazon Bedrock)
│   ├── resume_baseline.py    # chạy tiếp một trajectory bị ngắt
│   ├── force_final_from_traj.py  # ép nộp công thức từ trajectory bị ngắt
│   ├── model_task_scores.json    # điểm từng task × từng model trong paper
│   └── all_results.md        # bảng kết quả paper
├── scripts/
│   └── judge_parallel_bedrock.py # (mới) judge S_S chạy trên Bedrock thay Codex
├── experiments/              # (mới) kết quả chạy, được commit
├── notes/                    # (mới) tài liệu này
├── dataset/                  # dataset card, task_index.csv, license từng task
├── docs/                     # trang web dự án + PDF paper
└── tasks/                    # tải từ HF (RealSR/SciLaws-Bench), không commit
```

Ranh giới quan trọng: `harness/` là phần **đóng băng** để mọi solver so sánh được
với nhau. `baseline_agent/` chỉ là **một** cách điều phối model. Harness mới cho
paper nên nằm cạnh `baseline_agent/` và tái dùng `harness/` + `SimulatorTask`,
không sửa chúng.

## 3. Cấu trúc một task

```
tasks/typeI/<task>/
├── metadata.yaml        # agent THẤY: context, target, inputs, đơn vị, khoảng giá trị, caps
├── data/train.csv       # Real dùng; Parallel KHÔNG cho agent thấy (chỉ dùng để tính ngân sách)
├── data/test.csv
├── eval/                # ĐÁP ÁN: reference_metrics.json, validity_rubrics.json, metadata_full.yaml
└── simulator/           # ĐÁP ÁN: formula.py (luật ẩn), state.joblib, sample.csv
```

`state.joblib` của simulator chứa: `formula_source` (mã nguồn luật ẩn),
`law_constants`, `used_inputs` (tập con input mà simulator thực sự dùng),
`support` (hộp giá trị cho phép), `noise_scale`, `residual_space`
(`linear`/`log`), `bootstrap` (bộ lấy mẫu phần dư), `real_rows`,
`fetch_budget_rows`.

Cách simulator sinh dữ liệu (`sim_runtime._generate`):

```
y = F(X; law_constants) + noise_scale · r(X)
```

trong đó `r(X)` lấy ngẫu nhiên từ phần dư thật của k láng giềng gần nhất của `X`
trong dữ liệu thật (nhiễu không đồng nhất, không Gaussian). Với
`residual_space = "log"` nhiễu cộng trong không gian log10. Input ngoài `support`
bị **kẹp im lặng** về biên, số điểm bị kẹp báo trong `n_clipped`.

## 4. Luồng chạy end-to-end (Parallel)

```
run_batch.py  (mỗi job = 1 subprocess)
  └─ run_baseline.py <task_dir> <model> --simulator
       ├─ task.load_task(simulator="simulator") → SimulatorTask
       │     • nạp simulator qua sim_runtime.load()
       │     • input_cols = used_inputs của simulator
       │     • train_df rỗng; caps tính từ n_train thật
       ├─ agent.conduct_exploration(task, model, max_turns=30)
       │     messages = [system(PARALLEL), user(task prompt)]
       │     lặp turn = 0..29:
       │       turn 29: chèn "chỉ còn 1 lượt, nộp <final_formula>"
       │       call_llm_api(messages)  ──► provider (Bedrock / OpenAI / …)
       │       proto.step(response, sandbox, run_experiment)
       │         • lấy thẻ XML xuất hiện ĐẦU TIÊN trong câu trả lời
       │         • <experiment>{json}  → SimulatorTask.run_experiment
       │               kiểm tra caps → sim.fetch_data → nối vào train_df
       │               → feedback: preview 10 dòng + thống kê
       │         • <python>code        → validate (whitelist) → exec (100 s)
       │               → feedback: stdout (≤16k ký tự)
       │         • <final_formula>     → nếu chưa có experiment nào: từ chối
       │                                  ngược lại: KẾT THÚC, trả module
       │         • không hợp lệ        → nhắc định dạng
       │       ghi checkpoint trajectory sau mỗi bước
       │     hết turn mà chưa nộp: 1 lần nhắc lại, vẫn không có thì status=max_turns_reached
       └─ ghi <out>/<task>.py (submission) và <traj>/<task>.traj.json

harness/evaluate_parallel.py  (chấm S_S)
  ├─ stage: mỗi submission → thư mục {metadata.yaml, formula.py (GT), submission.py}
  ├─ dispatch: gọi `codex exec` với prompt judge (paper C.5)
  │     judge so sánh cấu trúc GT với submission → JSON {structure_score, level, …}
  └─ aggregate: contract check (import, chữ ký predict, chạy trên lưới 8 điểm,
        output hữu hạn đúng shape). Fail contract → 0. Thiếu kết quả → 0 (strict mean).
```

### 4.1. Giao thức tool

- Đúng **một** thẻ XML mỗi turn: `<experiment>`, `<python>`, `<final_formula>`.
  Nếu có nhiều thẻ, chỉ thẻ xuất hiện đầu tiên được chạy.
- `<experiment>` nhận **JSON thuần**:
  `{"VEC": [4.5, 5.0], "dHmix": [-10, -10], "n_samples": 3, "seed": 0}`.
  Không được dùng biểu thức Python.
- `<python>` là sandbox **không lưu trạng thái** giữa các lần gọi; có sẵn
  `train_df`, `X_train`, `y_train`, `input_cols`, `target_col`,
  `experiment_log`, `experiment_caps`, cùng `np`, `scipy`, `pd`. Import chỉ cho
  phép numpy / scipy / pandas / sklearn / math / statistics / itertools /
  functools / collections / warnings. Cấm `open`, `os`, `getattr`, `eval`, đọc
  file, vòng lặp brute-force lớn (> 200k vòng hoặc ≥ 4 vòng lồng nhau).
- Phải có ít nhất 1 `<experiment>` thành công trước khi được nộp.

### 4.2. Ngân sách thí nghiệm (Parallel)

Ngân sách nằm trong `baseline_agent/task.py`, không nằm trong `harness/`:

| Giới hạn | Giá trị | Nguồn |
|---|---|---|
| Số lần gọi `<experiment>` | ≤ 10 / task | `MAX_EXPERIMENT_CALLS` |
| Số điểm input khác nhau mỗi lần | ≤ max(10, ⌊0.1 · n_train⌋) | `MAX_EXPERIMENT_INPUT_POINT_FRACTION` |
| Số mẫu lặp mỗi điểm | ≤ 3 | `MAX_EXPERIMENT_SAMPLES` |
| Ngân sách dòng của simulator | `fetch_budget_rows` trong state (2000 với task chạy thử) | `sim_runtime` |

Giới hạn thực sự ràng buộc là **số điểm thiết kế khác nhau**: 10 lần × 0.1 n_train
≈ n_train điểm, ngang lượng dữ liệu bản Real. Lặp ×3 chỉ để giảm nhiễu, không mở
rộng vùng phủ. Muốn khôi phục cấu trúc thì phải chọn **đúng chỗ để đo**.

### 4.3. Prompt

`prompts.load_system_prompt(is_simulator=True, has_group_id=...)` và
`prompts.build_task_prompt(...)`. Task prompt Parallel gồm: context khoa học,
target (đơn vị, mô tả), mục tiêu "recover the hidden simulator's mechanism
structure… do not optimize for a prediction-error metric", contract nộp bài,
caps chống nhồi hằng số (`max_law_constants`…), danh sách input kèm mô tả,
"Simulator notes" (hộp support và caps ngân sách). Parallel **không** đưa khoảng
giá trị của tập test.

## 5. Cấu hình mặc định trong paper và vị trí trong code

| Thiết lập (paper, Phụ lục B) | Giá trị | Trong code |
|---|---|---|
| Số turn tối đa | 30, turn cuối bắt buộc nộp, thêm 1 lần retry | `--max-turns 30`, `agent.py` |
| Reasoning | effort **medium** cho mọi model có reasoning | `REASONING_EFFORT` / `--reasoning-effort`; nhánh `br` mặc định `medium` |
| Temperature | không override với model reasoning | không gửi `temperature` |
| Completion budget | 65,536 token | `_REASONING_MAX_COMPLETION_TOKENS` |
| Timeout API | 120 s, retry 1 lần | `LLM_TIMEOUT_SECONDS`, `max_retries=1` |
| Timeout `<python>` | 100 s | `PYTHON_TIMEOUT_SECONDS` |
| Ngân sách thí nghiệm | xem 4.2 | `task.py` |
| Judge `S_S` | GPT-5.4-mini chạy như code agent (Codex) | `evaluate_parallel.py --dispatch codex` |
| Gộp điểm | strict mean trên cả 118 task, thiếu/lỗi = 0 | `aggregate_parallel_outputs` |

Kết quả Parallel trong paper (`S_S`, %): GPT-5.5 58.26, GLM-5.2 52.12,
Gemini 3.5 Flash 50.42, Qwen3.7-Max 50.42, Claude Opus 4.8 50.00, DeepSeek-V4 Pro
49.79, GPT-5-mini 44.70, GPT-5.4-mini 42.58, GPT-4o-mini 33.47.

## 6. Chỗ code lệch so với paper (phát hiện khi đọc code)

1. **Provider Anthropic không bật thinking.** `_call_anthropic` không gửi tham số
   `thinking`. Với Claude Opus 4.7/4.8 (và Sonnet/Opus 4.6), không gửi `thinking`
   nghĩa là chạy **không reasoning**, trái với "medium reasoning tier" mà paper mô
   tả. Hàng "claude-opus-4-8-fg" trong paper chạy qua first-party API nhưng alias
   `claude-opus-4-8` không có trong `api_source_mapping`, nên không rõ lúc chạy
   thật cấu hình ra sao. Provider Bedrock mới thêm (mục 7) bật
   `thinking: adaptive` + `effort: medium` một cách tường minh.
2. **Lỗi API làm task dừng hẳn.** Paper (B.2) viết lỗi API "surfaces as an error
   inside the loop rather than aborting the task". Trong code, `agent.py` không
   bắt exception từ `call_llm_api`: tiến trình thoát, trajectory dừng ở trạng
   thái `running*`. Việc cứu run được làm thủ công bằng `resume_baseline.py` /
   `force_final_from_traj.py`. **`resume_baseline.py` không dùng được cho
   Parallel**: nó nạp lại task với `simulator=None` (chế độ Real), nên dữ liệu
   thí nghiệm đã thu bị mất và sandbox nhận `train.csv` thật. Một run Parallel
   chết giữa chừng chỉ có thể chạy lại từ đầu (hoặc ép nộp bằng
   `force_final_from_traj.py`).
3. **Judge.** README chỉ nói "codex"; paper nêu rõ judge là GPT-5.4-mini. Muốn tái
   lập đúng thì cần `--codex-model gpt-5.4-mini`.
4. `run_baseline.py --score` và một số docstring còn nhắc "private `scoring/`
   tree". Bản phát hành hiện để các file này trong `tasks/*/eval/`.
5. **"Thẻ đầu tiên" thực ra là "loại thẻ đầu tiên, khối cuối cùng".**
   `step()` chọn *loại* thẻ xuất hiện sớm nhất (`first_tool_tag`), nhưng
   `parse_experiment` / `extract_python` dùng `_last_block` (tìm bằng `rfind`),
   nên nếu một câu trả lời có nhiều khối `<experiment>` thì khối được chạy là
   khối **cuối cùng**, không phải khối đầu như paper mô tả. Với model chỉ viết
   một khối mỗi lượt thì không ảnh hưởng.
6. **Không có stop sequence.** `_USE_STOP = False` nên không có gì chặn model viết
   nhiều khối trong một lượt. Với Claude bật adaptive thinking (interleaved), điều
   này gây hậu quả nặng, xem mục 8.1.

## 7. Thay đổi đã thực hiện trong fork

- `baseline_agent/call_llm_api.py`: thêm provider `br` (Amazon Bedrock) qua
  `anthropic.AnthropicBedrock`, các alias `br-claude-sonnet-4-6`,
  `br-claude-opus-4-6`, `br-claude-opus-4-7`, `br-claude-opus-4-8`. Bật adaptive
  thinking, effort `medium` (đổi được bằng `REASONING_EFFORT`), 65,536 token,
  timeout 120 s, retry 1. **Luôn bật `stop_sequences`** ở các thẻ đóng
  (`</python>`, `</experiment>`, `</final_formula>`) để mỗi lượt có đúng một
  khối; lý do và bằng chứng ở mục 8.1. Thử lại 1 lần khi kết nối bị đứt giữa
  stream (mục 8.2). Dùng streaming để tránh chặn request dài của SDK; kết
  quả cuối giống hệt một lần gọi không streaming. Đếm riêng `reasoning_tokens`
  từ `usage.output_tokens_details.thinking_tokens`. Credentials lấy từ chuỗi AWS
  chuẩn (`AWS_PROFILE`), region từ `AWS_REGION`.
- `scripts/judge_parallel_bedrock.py`: judge `S_S` trên Bedrock. Dùng
  **nguyên văn** prompt judge do `evaluate_parallel._build_prompt` sinh ra, mỗi
  task một lần gọi, nhúng trực tiếp 3 file (metadata, GT, submission), sau đó gọi
  hàm `aggregate_parallel_outputs` chính thức (contract check + strict mean).
  Khác paper ở hai điểm: model judge (mặc định Claude Opus 4.6 thay vì
  GPT-5.4-mini) và judge chỉ đọc mã nguồn, không chạy code để thăm dò.
- `requirements-agent.txt`: thêm `anthropic[bedrock]`.
- `CLAUDE.md`, `notes/`, `experiments/`.

### Quyền truy cập model trên Bedrock (account `reddy-research`, us-east-1)

Đã probe bằng `converse` ngày 2026-10-29:

| Gọi được | Bị từ chối (AccessDenied) |
|---|---|
| Claude Opus 4.6, Sonnet 4.6, Sonnet 4.5, Haiku 4.5, DeepSeek R1, DeepSeek V3.2, GLM-5 | Claude Opus 4.7, **Opus 4.8**, Opus 5 / 5.5, Sonnet 5 / 5.5, Haiku 5.5, **GPT-5.5**, GPT-5.4, GLM-5.3 |

Không model nào trong 9 model của paper gọi được (Opus 4.8 và GPT-5.5 có trong
danh mục Bedrock nhưng account chưa được cấp quyền). Lựa chọn ban đầu là
**Claude Sonnet 4.6**: có reasoning (adaptive thinking + effort), có sẵn alias
`claude-sonnet-4-6` trong repo, giá $3/$15 mỗi triệu token input/output. Sau khi
Sonnet 4.6 hết hạn mức token/ngày (mục 8.2), run hoàn chỉnh được chạy bằng
**Claude Opus 4.6** ($5/$25): cùng kiểu API adaptive thinking + effort với
Opus 4.8 của paper, nên là bản gần nhất gọi được. (Giá theo bảng first-party của
Anthropic; giá Bedrock tính riêng.) Hệ quả: kết quả dưới đây **không** phải tái
lập một hàng của paper, chỉ là kiểm tra pipeline chạy đúng end-to-end.

Hai trở ngại kỹ thuật khi gọi Bedrock:

- **API version.** `anthropic>=2` gửi `anthropic_version = 2026-10-21`. Bedrock
  chỉ chấp nhận giá trị này cho Claude 4.7 trở lên; Opus 4.6 trả về
  `400 Invalid API version`. Provider `br` và script judge gửi
  `bedrock-2023-05-31` cho các model cũ hơn (SDK chỉ điền trường này khi nó còn
  trống). Cách chính quy là pin `anthropic<2`, nhưng lúc chạy PyPI không kết nối
  được (lỗi SSL).
- **Hạn mức token theo ngày** nhỏ và không hiển thị trong `service-quotas`
  (mục 8.2).

## 8. Kết quả chạy thử

**Task:** `hea_hardness_lattice_distortion_couzinie__HV` (Type I, Materials &
Engineering, n_train = 56). Đây là task ví dụ trong README. Mục tiêu: độ cứng
Vickers `HV` của hợp kim high-entropy. Simulator chỉ dùng 2 input (`VEC`,
`dHmix`) dù metadata có 3 (`delta` bị loại). Caps: ≤ 3 hằng số, ≤ 10 lần
`<experiment>`, ≤ 10 điểm/lần, ≤ 3 mẫu/điểm.

**Ba dạng luật liên quan:**

| | Công thức |
|---|---|
| Luật đã công bố (Temesi 2023, Eq. 12), dạng cộng | `HV = a + b·VEC + c·dHmix` |
| **Luật ẩn của simulator** (biến thể chống học thuộc) | `HV = 81.14 + 68.75·VEC − 1.457·VEC·dHmix` |
| Bài nộp của agent (Opus 4.6) | `HV = 245.43 + 7.117·VEC² − 1.4703·VEC·dHmix` |

Luật ẩn thay số hạng cộng `c·dHmix` bằng số hạng ghép `VEC·dHmix`, tức là độ
nhạy của HV theo dHmix tỉ lệ với VEC. Một model chỉ nhận ra luật đã công bố sẽ bị
kẹt ở 0.5.

### 8.1. Lần 1: Sonnet 4.6, cấu hình gốc (không stop sequence), đã hủy

Thư mục: `experiments/aborted_nostop_br-claude-sonnet-4-6/`.

Lượt 1 trả về **42,754 token output** (31k thinking) trong khoảng 4–5 phút. Câu
trả lời chứa 6 khối `<experiment>`, 29 khối `<python>` và 1 `<final_formula>`:
model tự "chạy" tiếp cả phiên làm việc trong tưởng tượng mà không chờ kết quả
tool. Harness chỉ thực thi một khối (khối `<experiment>` **cuối cùng**, do quirk
ở mục 6.5), nhưng toàn bộ 24k ký tự thừa vẫn được nối vào lịch sử hội thoại. Ước
tính một task 30 lượt mất hơn 2 giờ và khoảng $20, với context đầy dữ liệu bịa.

Sửa: bật `stop_sequences` ở các thẻ đóng (cơ chế `_USE_STOP` + `_heal_close_tag`
đã có sẵn trong repo, chỉ đang tắt). Sau khi sửa: lượt 1 mất 2 giây, 127 token,
đúng một khối. Hành động được thực thi không đổi về bản chất; chỉ phần sinh thừa
bị cắt.

### 8.2. Lần 2 và 3: Sonnet 4.6, chết vì lỗi hạ tầng

| Run | Dừng ở | Thí nghiệm | Nguyên nhân |
|---|---|---|---|
| `failed_netdrop_…` | lượt 21/30 | 6 | `RemoteProtocolError: peer closed connection` giữa stream |
| `failed_quota429_…` | lượt 22/30 | 5 | `429 Too many tokens per day` |

Cả hai đều không có bài nộp, nên theo strict aggregation sẽ bị tính 0 điểm. Sau
lần 2, provider được bổ sung retry 1 lần cho lỗi giữa stream (mục 7). Lần 3 cạn
hạn mức token/ngày của Sonnet 4.6 sau khoảng 580k token trong ngày (≈ 450k input
+ 130k output). Thêm một lần chạy Sonnet 4.6 nữa chết ngay ở lượt 6 cùng lỗi
429; run đó đã bị xóa vì trùng lặp.

Hai trajectory dở dang này vẫn có giá trị: cùng model, cùng task, nhưng chúng hội
tụ về hai dạng khác nhau. Run `netdrop` fit đúng dạng luật ẩn
`98.6 + 65.4·VEC − 1.50·VEC·dHmix`. Run `quota429` chọn dạng nhân tử
`(a + b·VEC)(c − dHmix)`, có thêm số hạng `dHmix` dư. Phương sai giữa các run
là đáng kể.

### 8.3. Run hoàn chỉnh: Opus 4.6

Thư mục: `experiments/parallel_smoke_br-claude-opus-4-6/`.

| Chỉ số | Giá trị |
|---|---|
| Trạng thái | `completed`, nộp ở lượt 30 (lượt bắt buộc nộp) |
| Số lượt | 30 = 5 `<experiment>` + 24 `<python>` + 1 `<final_formula>` |
| Dữ liệu thu được | 138 dòng (46 điểm thiết kế × 3 mẫu), trên mức trần 300 |
| Token | 651,813 input + 23,026 output (thinking chỉ 135 token), không có cache hit |
| Thời gian | 554 s |
| Chi phí ước tính | ≈ $3.8 (giá first-party Opus 4.6) |
| **`S_S`** | **0.75** (`main_plus_extra_terms`, contract OK) |

Diễn biến:

- **T1–T10:** thí nghiệm lưới 2×4 trên (VEC, dHmix) cùng 2 điểm phụ, rồi 10 điểm
  rải rác có cả biên VEC 4.2 / 6.5. Thử dạng cộng, cộng + tương tác (4 tham số,
  vượt caps), bậc hai, luỹ thừa, căn của `−dHmix`. Agent nhận xét nhiễu lớn và
  quyết định đo thêm.
- **T11–T19:** thêm một lưới đan xen ở vùng giữa, rồi so sánh nhiều dạng hàm.
- **T20:** đo 6 điểm góc (VEC ∈ {4.2, 6.5} × dHmix ∈ {−5, −30, −39}) để tách tương tác.
- **T21–T28:** so sánh 7 mô hình 3 tham số. Hai mô hình dẫn đầu là
  `a + b·VEC + c·VEC·dH` (**đúng dạng luật ẩn**, BIC 780.6) và
  `a + b·VEC² + c·VEC·dH` (BIC 779.0). Agent chọn mô hình thứ hai dựa trên chênh
  lệch ΔBIC = 1.6, một mức không có ý nghĩa thống kê.
- **T29:** tiêu thêm một thí nghiệm 10 điểm nhưng không còn lượt nào để phân tích.
- **T30:** bị ép nộp.

Kết luận của judge (Sonnet 4.5, xem `parallel_out/*.json`):

- **Đúng:** tìm ra số hạng ghép `VEC·dHmix` với hệ số lệch < 1% (−1.470 so với
  −1.457), bỏ đúng số hạng cộng `dHmix` của luật đã công bố, giữ được khung
  "hằng số + số hạng VEC + số hạng ghép".
- **Sai:** VEC đi vào dưới dạng bậc hai thay vì tuyến tính.

So sánh với paper trên cùng task (`model_task_scores.json`, judge GPT-5.4-mini):

| Model | `S_S` task này |
|---|---:|
| GPT-5.5 | 1.00 |
| Claude Opus 4.8, DeepSeek-V4 Pro, Qwen3.7-Max | 0.75 |
| Gemini 3.5 Flash, GLM-5.2, GPT-5.4-mini | 0.50 |
| GPT-5-mini, GPT-4o-mini | 0.25 |
| *Run này: Claude Opus 4.6, judge Sonnet 4.5* | *0.75* |

Điểm 0.75 nằm trong khoảng hợp lý và trùng với Opus 4.8 của paper. Tuy vậy, đây
chỉ là một task, một seed, model khác và judge khác, nên không dùng để kết luận
về năng lực model.

### 8.4. Nhận xét cho hướng Agent Harness

Những điểm agent tham chiếu làm chưa tốt và một harness mới có thể cải thiện,
dựa trên các trajectory ở trên:

1. **Chọn mô hình dưới nhiễu.** Agent đã có dạng đúng trong tập ứng viên nhưng
   chọn sai vì ΔBIC = 1.6. Harness có thể buộc thực hiện bước *phân biệt mô
   hình*: khi hai ứng viên gần nhau, thiết kế thí nghiệm ở chỗ hai mô hình dự
   đoán khác nhau nhiều nhất, rồi mới quyết định. Ở đây là đo lặp tại hai đầu và
   điểm giữa của VEC với cùng một dHmix để kiểm tra độ cong, vì đó là chỗ `VEC`
   và `VEC²` khác nhau.
2. **Không biết mình còn bao nhiêu lượt.** Prompt chỉ nói "at most 30 turns";
   feedback không có bộ đếm lượt, nên agent tiêu thí nghiệm ở lượt 29. Một harness
   có quản lý ngân sách lượt và ngân sách thí nghiệm sẽ tránh được lỗi này.
3. **Dùng chưa hết ngân sách thí nghiệm:** 5/10 lần gọi, 138/300 dòng. Hầu hết
   các lượt là `<python>` (24/30).
4. **Sandbox không lưu trạng thái.** Mỗi lần gọi `<python>` phải định nghĩa lại
   hàm và dữ liệu trung bình, tốn token và dễ sai. Có thể thêm một "sổ tay giả
   thuyết" hoặc bộ nhớ có cấu trúc ở tầng harness (không cần sửa `harness/`).
5. **Chi phí context tăng bậc hai.** 652k token input cho 30 lượt vì mỗi lượt gửi
   lại toàn bộ lịch sử và không dùng prompt caching. Caching hoặc tóm tắt context
   sẽ giảm mạnh chi phí khi chạy đủ 118 task.
6. **Reasoning gần như không được dùng.** Opus 4.6 ở `effort=medium` với adaptive
   thinking chỉ nghĩ 135 token trong cả 30 lượt. Effort là một biến cần quét khi so
   sánh harness.
7. **Phương sai giữa các run lớn** (mục 8.2), nên mỗi cấu hình cần nhiều seed.
8. **Độ bền hạ tầng** quyết định điểm strict: một lần đứt stream hay một lỗi 429 là
   mất trắng task. Cần stop sequence, retry, và cơ chế resume cho Parallel (phải
   phát lại các thí nghiệm, vì `resume_baseline.py` không làm được).

Để giữ so sánh công bằng với paper, harness mới nên giữ cố định: prompt
`harness/`, caps thí nghiệm của `SimulatorTask`, số lượt tối đa, contract nộp
bài, và judge.

### 8.5. Lệnh tái lập

```bash
export AWS_PROFILE=reddy-research AWS_REGION=us-east-1
R=experiments/parallel_smoke_br-claude-opus-4-6
.venv/bin/python baseline_agent/run_batch.py --models br-claude-opus-4-6 --modes parallel \
    --task-types typeI --tasks hea_hardness_lattice_distortion_couzinie__HV \
    --workers 1 --max-turns 30 --run-dir $R
.venv/bin/python harness/evaluate_parallel.py --tasks-dir tasks \
    --submissions $R/parallel/submissions/br-claude-opus-4-6 \
    --stage-dir $R/parallel_stage --output-dir $R/parallel_out \
    --method-name br-claude-opus-4-6 --overwrite
.venv/bin/python scripts/judge_parallel_bedrock.py --manifest $R/parallel_stage/manifest.json \
    --model us.anthropic.claude-sonnet-4-5-20250929-v1:0 --budget-tokens 16000
```
