# 项目说明（给 Claude Code）

这是一个纯前端单文件应用 `index.html`（HTML + CSS + 原生 JS，无框架、无构建）。

## 功能结构（index.html 内 <script> 部分，按注释分块）
- 音高追踪（YIN）：`track()`，输出以半音为单位、按说话人中位数归一化的语调曲线
- 时间对齐 + 相似度：`align()`（DTW，把学生曲线对齐到示范时间轴，返回 warped 曲线、播放头映射 map、相关系数），`pearson()`
- 打分：`scoreAttempt()`（别名 `rescore`），总分 = 语调 55% + 结尾语调 30% + 节奏 15%；最高分存 localStorage `gd:best`；`grade()` 给星级
- 结尾语调判断：`tailDelta()` / `judgeTone()`，比较句末最后约 18% 与中后段的平均音高
- 按停顿切句：`split()`（课文音频模式）
- 句子库：`book.json`（按 units 组织，`loadBook()` 读入后展平为 `PRESET`，每句带 `unit`），`unit` 变量控制当前单元过滤（`list()`），`zh` 中文意思，`sec` 板块（`sec` 变量 + `buildSecSel()` 过滤），`who` 说话人，`voice` m/f；内容为仁爱科普版九上全书 909 句；每句可带 `audio` 字段指向 audio/ 下的内置示范 mp3；`ensureModel()` 优先用老师录音（IndexedDB），其次内置音频，都没有才走 speechSynthesis
- 生成内置音频：`python3 tools/gen_audio.py`（edge-tts，女声 Jenny / 男声 Guy，rate -10%，ffmpeg loudnorm），输出 audio/<id>.mp3；sw.js 对 /audio/ 用缓存优先、播放时才缓存
- 课本 PDF 在项目根目录但被 .gitignore 排除，绝不能提交（公开仓库）
- 示范录音存储：IndexedDB（`idb`），自定义句子存 localStorage
- 播放增益：`wire()` 把 Audio 元素接到 GainNode → DynamicsCompressor；`normGain(peak)` 峰值归一，`GAIN` 用户增益（localStorage `gd:gain`）；`playMine()` 按 `c.t0/t1` 掐掉录音前后空白

## 常用任务
- 本地运行：`python3 -m http.server 8000`，打开 http://localhost:8000
- 部署：推送 main 分支即自动部署到 GitHub Pages https://zeliny0109.github.io/gendu/ （.github/workflows/pages.yml），必须是 https 才能在手机上用麦克风
- PWA：manifest.webmanifest + sw.js（离线缓存）+ 图标；改了 index.html 记得把 sw.js 的 VERSION 加一
- 修改时保持无构建工具（主逻辑仍在单个 index.html 里）；麦克风相关代码需在 https 或 localhost 下测试
- Android：android/ 目录用 Bubblewrap 打成 TWA，APK 发布为仓库根目录 gendu.apk；签名密钥在 android/gendu.keystore（不入库），细节见 android/README.md
