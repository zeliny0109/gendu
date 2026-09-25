# 项目说明（给 Claude Code）

这是一个纯前端单文件应用 `index.html`（HTML + CSS + 原生 JS，无框架、无构建）。

## 功能结构（index.html 内 <script> 部分，按注释分块）
- 音高追踪（YIN）：`track()`，输出以半音为单位、按说话人中位数归一化的语调曲线
- 相似度：`similarity()`，两条曲线时间归一化后的皮尔逊相关
- 结尾语调判断：`tailDelta()` / `judgeTone()`，比较句末最后约 18% 与中后段的平均音高
- 按停顿切句：`split()`（课文音频模式）
- 句子库：`PRESET`
- 示范录音存储：IndexedDB（`idb`），自定义句子存 localStorage

## 常用任务
- 本地运行：`python3 -m http.server 8000`，打开 http://localhost:8000
- 部署：推送 main 分支即自动部署到 GitHub Pages https://zeliny0109.github.io/gendu/ （.github/workflows/pages.yml），必须是 https 才能在手机上用麦克风
- PWA：manifest.webmanifest + sw.js（离线缓存）+ 图标；改了 index.html 记得把 sw.js 的 VERSION 加一
- 修改时保持无构建工具（主逻辑仍在单个 index.html 里）；麦克风相关代码需在 https 或 localhost 下测试
