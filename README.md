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
- 代码放在 https://github.com/zeliny0109/gendu ，推送到 main 分支后 GitHub Actions 会自动重新部署（见 .github/workflows/pages.yml）。

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

- 老师录的示范：存在浏览器 IndexedDB（按设备、按浏览器分别保存）
- 自己添加的句子、课文音频的句子备注：存在 localStorage

## 修改句子库

在 index.html 里搜索 `const PRESET=`。每句格式：

```js
{id:'p1', t:'My hometown has *changed*‿a *lot*.', tone:'down', type:'陈述句', tip:'可选提示'}
```

- `*单词*` 标重读，`‿` 标连读
- `tone`：`up` 结尾升调，`down` 结尾降调，`updown` 先升后降（选择疑问句）
- `id` 要唯一，老师示范录音按 id 保存
