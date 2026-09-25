# 跟读练习（gendu）

单文件网页应用：句子跟读 + 语调曲线对比 + 结尾升降调判断。无依赖、无构建步骤。

## 本机运行（电脑上用）

```bash
cd gendu
python3 -m http.server 8000
```

浏览器打开 http://localhost:8000 。localhost 属于安全上下文，麦克风可以正常使用。

注意：直接双击 index.html（file://）在部分浏览器里麦克风或 IndexedDB 会受限，建议用上面的方式。

## 手机 / 学生使用

已部署到 GitHub Pages（https，麦克风可用）：

**https://zeliny0109.github.io/gendu/**

- 手机浏览器打开后，可"添加到主屏幕"（iPhone 用 Safari 分享菜单；Android 用 Chrome 菜单里的"安装应用"），之后像普通 App 一样点图标打开，离线也能用。
- 代码放在 https://github.com/zeliny0109/gendu ，推送到 main 分支后 GitHub Actions 会自动把内容同步到 gh-pages 分支并重新发布（见 .github/workflows/pages.yml）。

### 九上语法练习

**https://zeliny0109.github.io/gendu/grammar/** （跟读页面的句子列表上方也有入口）

按九上课本编排的语法讲解：现在完成时、被动语态、定语从句（U1–U6），外加构词法词缀、不定代词、不规则动词。有一个“变形器”（同一句话切换时态/句型，主动被动对照着看），以及选择、填空、连词成句、合并句子练习和错题本。

### Android 安装包

不想用浏览器安装的话，可以直接装 APK（约 1.2 MB，需要手机上有 Chrome）：

**https://zeliny0109.github.io/gendu/gendu.apk**

手机浏览器打开这个链接下载，安装时允许"来自此来源的应用"。装好后是独立的"跟读练习"应用，页面内容仍来自上面的网址，网页更新后应用自动跟着更新，不用重新安装。打包方法见 android/README.md。

### 更新方法

```bash
cd /data/tendu
# 改完 index.html 后：
git add -A && git commit -m "更新" && git push
```

改了 index.html 之后把 `sw.js` 里的 `VERSION` 改个号（如 gendu-v2），手机端才会立刻换新缓存。

### 局域网 / Tailscale 临时访问

手机访问电脑的局域网 IP（http://192.168.x.x:8000）时，浏览器会因为不是 https 而禁用麦克风。
如果电脑和手机都在同一个 Tailscale 网络里，可以用 Tailscale 提供 https：

```bash
cd /data/tendu && python3 -m http.server 8000 &
tailscale serve --bg 8000        # 输出形如 https://zelin.tailc23635.ts.net/
```

## 数据存储

- 全书示范音频在 audio/ 目录（播放过的句子会缓存到手机，之后离线可用）（用 edge-tts 的 en-US-JennyNeural 生成，见 CLAUDE.md），随网页发布，不依赖手机的朗读引擎
- 老师录的示范：存在浏览器 IndexedDB（按设备、按浏览器分别保存），优先于内置音频
- 自己添加的句子、课文音频的句子备注：存在 localStorage

## 修改句子库（整本书）

当前内容：仁爱科普版英语九年级上册，6 个单元共 909 句。来自课本中所有完整的对话和短文（听说、听力原文、功能对话、语音、思维技能、阅读策略、主题阅读、语法、口头交际、以读促写、复习），带填空的练习题没有收录。课本 PDF 只放在本地，`.gitignore` 已排除，不会上传。

句子放在 `book.json`，按单元组织：

```json
{ "id": "u1", "name": "Unit 1", "sentences": [
  { "id": "u1-001", "t": "What was *communication* like in the *past*?", "zh": "过去的通讯是什么样的？", "tone": "down", "sec": "听说", "who": "A", "voice": "f", "tip": "可选提示", "audio": "audio/u1-001.mp3" }
]}
```

- `*单词*` 标重读，`‿` 标连读；`zh` 是中文意思；`sec` 是板块（页面上可按板块筛选）；`who` 是说话人；`voice` 为 `m`/`f`，生成音频时分别用男声 Guy、女声 Jenny
- `tone`：`up` 结尾升调，`down` 结尾降调，`updown` 先升后降（选择疑问句）
- `id` 全书唯一，老师示范录音和最高分都按 id 保存
- 加完句子运行 `python3 tools/gen_audio.py`，会给没有音频的句子生成示范 mp3（需要 `pip install edge-tts` 和 ffmpeg）并写回 `audio` 字段；中断后重跑会接着生成
- 改完把 `sw.js` 里的 `VERSION` 加一

## 打分

- 总分 = 语调相似 55% + 结尾语调 30% + 节奏 15%，90 分优秀（★★★）、75 良好、60 及格
- 语调相似：先用动态时间规整（DTW）把学生曲线在时间上对齐到示范，再算相关系数，所以读得快慢、停顿位置不同不影响分数；画出来的"我的"曲线也是对齐后的
- 节奏：学生有声段时长与示范时长的比值，相差一倍记 0 分
- 每句的最高分和练习次数存在 localStorage（`gd:best`），列表里显示星级，单元顶部显示进度

## 播放

所有播放经 Web Audio 增益 + 限幅器输出。每段音频先按峰值归一，再乘"播放音量"里的增益（默认 1.6×，可调 1–3×）。播放"我的"录音时自动掐掉前后空白。
