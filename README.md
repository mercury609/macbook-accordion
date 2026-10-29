# 风箱之间 / Bellows — MacBook Accordion

Turn your MacBook into a virtual accordion. Move the lid for expression, enter numbered notes, and control the rhythm yourself.

![Pitch-only jianpu performance](docs/screenshot.png)

> This repository contains source code. Build the macOS app with `build.sh`; no prebuilt app or model weights are stored in Git. The installer downloads and verifies the official Demucs model.
> 本仓库提供源码，不包含应用包和模型权重。安装脚本会下载并校验官方模型，运行 `build.sh` 可生成 Mac 应用。

## 中文

这是按照任务清单实现的 Mac 桌面手风琴应用。使用 Python、pygame、NumPy、sounddevice；盖子传感采用 pybooklid。当前构建适用于 Apple Silicon，macOS 14 或更新系统。

### 启动与演奏

1. 完成下方安装与打包后，双击 `dist/MacBookAccordion.app`，不需要安装 Python。右上方「中文 / EN」切换语言。
2. 手动模式：按住 QWERTYUIOP 或 ZXCVBNM,./，同时缓慢开合盖子。黑键见界面底部。Shift 放开升八度，Ctrl 放开降八度，Tab 重置。
3. 没有可用传感器时自动进入模拟模式；按住 ↑ 或 ↓ 推动模拟盖子。气流会累积，停止运动后逐渐泄漏；低于门限时静音。
4. 点击「导入音频 / MIDI」，选择 WAV、MP3、M4A 或 MIDI，也可以拖入文件。清唱关闭人声分离；完整歌曲可打开人声分离。所有模型随包附带，处理在本地进行，不上传音频。
5. 转录后自动进入自动模式。按住任意键按原始时间走谱；全部松开就暂停，再按继续。即使没有气流，按住键也会继续走谱，但不会出声。
6. 点击卷轴中的音符，用「± 半音」改音高或「删除」删音符。「上一页 / 下一页」浏览长乐谱，每页 12 秒。「回到开头」重新开始。
7. 「导出 MIDI」保存修改后的乐谱。转录时间不按节拍网格量化；MIDI 文件只存在格式本身的时间精度限制。

### 手动输入简谱与跟弹

点击「输入简谱」，输入纯音高，例如 `1 1 5 5 6 6 5 | 4 4 3 3 2 2 1`，然后点「生成并跟弹」。支持直接连续输入 `1234567`、粘贴、换行和小节分组。默认 `1=C4`，可用调号 ± 按半音改变主音。

- `1–7`：音级；`1'`：高八度；`1,`：低八度；`#4` / `b7`：升降音。
- 不输入休止符和时值，也不自动安排演奏节奏。
- 每次按下空格、回车或一个琴键，推进一个音。按住延续，全部松开停止；下次按下演奏下一个音。重复相同数字也需要分别按键。
- ↑↓ 仅控制模拟风箱，不推进简谱。发声仍需要气流；BPM 控制不作用于跟弹模式。
- 「重新跟弹」回到第一个音之前。输入窗口内的键盘操作不会演奏或推进乐谱。
- 支持 ⌘V 粘贴、⌘A 全选、方向键、删除、⌘Enter 生成、Esc 关闭。生成会替换当前乐谱；关闭输入窗口保留当前会话的草稿。
- 点击「导出 MIDI」保存音高序列。由于 MIDI 格式必须包含时间，导出使用等长的占位音符（每音 0.5 秒）；它们不控制跟弹时的演奏速度，也不是对实际演奏节奏的录音。

### BPM 调速

音频面板新增 BPM 控制，范围 30–300，可点击 ± 或在数字区域滚轮微调。自动演奏速度 = BPM ÷ 原速基准；点击「恢复原速」回到 1×。调速不改变音高、原始音符时间和 MIDI 导出时间，暂停后仍从当前位置继续。

「原速基准」默认 120，是速度参照，不是自动测得的歌曲 BPM。如果知道录音的实际 BPM，先把原速基准设为该值，再设目标 BPM；否则可参考旁边的倍率调快或调慢。导入新曲后回到 120 / 120（原速）。

### 参数与实现

左侧可调整灵敏度（运动达到最大驱动力所需的角速度，数值越小越灵敏）、运动死区、气流累积、泄漏速度、音量平滑、整体音量、attack、release、簧片失谐和气流噪声。

- `bellows.py`：角度来源、自动回退、角速度、气流模型及标准 Signal。
- `synth.py`：两层微失谐抗混叠锯齿波、噪声、起释音包络、严格气流门控。
- `transcribe.py`：FFmpeg 解码、可选 Demucs 人声分离、Basic Pitch ONNX 离线推理。
- `score.py`：原始时间音符、与风箱无关的走谱时钟、MIDI 导入导出。
- `app.py` / `i18n.py`：中文和英文界面、音符编辑及后台转录。

Basic Pitch 的默认 Python 3.12 安装依赖旧版 TensorFlow，不兼容当前环境，因此使用其官方提供的 ONNX 模型，固定依赖版本。没有自训练转录模型。完整歌曲分离使用 Demucs htdemucs。

### 验证与边界

已检查真实盖子传感器读取、扬声器输出、气流门控与衰减、暂停续播、MIDI 时间保留；使用合成的三音测试音频检查 WAV、MP3、M4A 转录与音高；运行了人声分离到转录的完整通路。合成音测试不等于真实清唱准确度验收：还需用你自己的录音确认旋律效果，自动转录可能出现错音，界面允许手动修正。

此构建仅针对当前 Apple Silicon Mac，不是 Intel 通用包，也未进行 Apple 公证。没有声卡时窗口仍可打开并显示音频不可用。

### 从源代码运行 / 构建

需要 Python 3.12：运行 `./install.sh`，然后 `.venv/bin/python main.py`。`requirements-lock.txt` 固定了此构建所用版本；安装脚本有意跳过 Basic Pitch 的默认 TensorFlow/CoreML 依赖，改用显式安装的 ONNX Runtime。

测试：`.venv/bin/python -m unittest discover -s tests -v`。
模块检查：`.venv/bin/python -m accordion.bellows` 和 `.venv/bin/python -m accordion.synth`。
打包：激活 `.venv` 后运行 `./build.sh`；产物在项目内部的 `dist/`，不要只移动 `.app` 内部的可执行文件。

## English

A desktop accordion for Apple Silicon Macs running macOS 14 or later. Built with Python, pygame, NumPy and sounddevice; pybooklid supplies lid angles.

### Play

1. After installing and building below, double-click `dist/MacBookAccordion.app`; Python is bundled. Use **中文 / EN** to switch languages.
2. In Manual mode, hold a keyboard note while moving the lid gently. White keys: QWERTYUIOP and ZXCVBNM,./. Black keys are listed in the footer. Release Shift to transpose up, Control to transpose down; Tab resets the octave.
3. If the lid sensor is unavailable, simulated mode starts automatically. Hold ↑ / ↓ to move the simulated lid. Air builds with motion, leaks after stopping, and gates sound below a threshold.
4. Import WAV, MP3, M4A or MIDI, or drop a file into the window. Leave vocal isolation off for isolated vocals; enable it for full songs. Models are bundled and processing stays local.
5. In Auto mode, hold any key to advance at the recording's original speed. Release all keys to pause; hold again to resume. Playback time continues while a key is held even without airflow; airflow only controls audible output.
6. Select notes in the piano roll to transpose by a semitone or delete them. Previous / Next browse 12-second pages. Rewind returns the playback clock to zero.
7. Export MIDI to save edits. No beat-grid quantization is applied; exported MIDI has its normal finite timestamp precision.

### Pitch-only numbered notation

Click **Enter jianpu**, enter pitches such as `1 1 5 5 6 6 5 | 4 4 3 3 2 2 1`, and choose **Create & play**. Compact `1234567`, paste, line breaks and bar separators are supported. The default tonic is `1=C4`; use the key ± controls to transpose the tonic by semitones.

- `1–7`: scale degrees; `1'`: octave up; `1,`: octave down; `#4` / `b7`: accidentals.
- No rests or note durations are entered. There is no automatic timing in this mode.
- Press Space, Return or a piano key to advance one note. Hold to sustain; release all performance keys to stop. Press again for the next note, including repeated pitches.
- ↑↓ only operates simulated bellows. Airflow is still required for sound. BPM controls do not affect this mode.
- **Restart notes** resets the sequence. Typing in the editor never triggers playback.
- Supports ⌘V, ⌘A, cursor keys, deletion, ⌘Enter to create, and Esc to close. Creating replaces the current score; closing retains the draft for the current app session.
- **Export MIDI** saves the pitch sequence with equal-length placeholder timestamps (0.5 seconds per note), as MIDI requires timing. Those placeholders do not drive live performance and do not record the rhythm you played.

### BPM control

Adjust BPM from 30–300 with the ± buttons or scroll over the value. Auto playback speed equals target BPM divided by Base BPM. Original speed restores 1×. Pitch, source note timestamps and MIDI export timing stay unchanged; pause/resume keeps the current position.

Base BPM defaults to 120 as a reference; it is not an automatic tempo estimate. If you know the recording’s actual tempo, enter it as Base BPM before choosing a target. Otherwise use the displayed multiplier for relative speed changes. Loading a new score resets both values to 120 (original speed).

### Controls and architecture

The left panel adjusts sensitivity (lower velocity value = more sensitive), motion dead zone, air accumulation/leakage, volume smoothing, master level, attack/release, reed detune and noise.

Sensor input, bellows modeling, synthesis, transcription and score timing live in separate modules. Basic Pitch uses its official ONNX model because its default legacy TensorFlow dependencies do not support this Python environment. Demucs htdemucs provides optional vocal isolation. No custom transcription model is trained.

### Validation and limits

Tests cover sensor fallback, air decay/gating, pause/resume, and off-grid MIDI timing. A synthetic three-note recording was transcribed from WAV, MP3 and M4A. The vocal-isolation-to-transcription path was also exercised. Actual singing accuracy still needs evaluation with your recording; pitch errors can be corrected in the editor.

This build targets Apple Silicon, is not an Intel universal build, and is not Apple-notarized. If audio output is unavailable, the interface remains usable and reports the problem.

### Development

With Python 3.12 installed, run `./install.sh`, then `.venv/bin/python main.py`. The installer deliberately uses the locked ONNX dependencies instead of Basic Pitch's incompatible default TensorFlow/CoreML dependencies. Run `.venv/bin/python -m unittest discover -s tests -v` for tests. Activate `.venv` and run `./build.sh` to create a self-contained app under `dist/`.

See `THIRD_PARTY.md` and `licenses/` for attribution and licenses.
