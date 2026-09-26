# Android 安装包（TWA）

用 [Bubblewrap](https://github.com/GoogleChromeLabs/bubblewrap) 把 https://zeliny0109.github.io/gendu/ 包成 Android 应用（Trusted Web Activity，内核是手机上的 Chrome）。
产物 `gendu.apk` 放在仓库根目录，由 GitHub Pages 提供下载。

## 本目录里的文件

- `twa-manifest.json`：打包配置（包名 io.github.zeliny0109.gendu、名称、颜色、图标地址、签名指纹）。入库。
- `gendu.keystore` + `keystore-password.txt`：签名密钥和口令。**不入库，务必备份**；丢了就无法给已安装的用户推送升级，只能换包名重装。
- 其余（app/、build/、*.apk、*.aab）都是生成物，不入库。

## 重新打包（改了网页不需要重新打包；只在改包名、图标、颜色、版本号时才需要）

工具链在 `~/.bubblewrap/`（JDK 17、Android SDK），`~/.bubblewrap/config.json` 已指好路径。

```bash
cd /data/tendu/android
# 1. 版本号：twa-manifest.json 里 appVersionCode 加 1，appVersion 改成新版本号
# 2. 生成工程并打包
export JAVA_HOME=~/.bubblewrap/jdk PATH=~/.bubblewrap/jdk/bin:$PATH
export BUBBLEWRAP_KEYSTORE_PASSWORD=$(cat keystore-password.txt) BUBBLEWRAP_KEY_PASSWORD=$(cat keystore-password.txt)
bubblewrap update --skipVersionUpgrade
bubblewrap build --skipPwaValidation
# 3. 发布
cp app-release-signed.apk ../gendu.apk && cd .. && git add gendu.apk && git commit -m "APK vX.Y.Z" && git push
```

## 网站侧要求

`/.well-known/assetlinks.json` 里的 SHA-256 指纹必须和签名密钥一致，否则应用打开时顶部会显示 Chrome 地址栏。
换密钥后用下面命令取新指纹并更新该文件：

```bash
~/.bubblewrap/jdk/bin/keytool -list -v -keystore gendu.keystore -alias gendu -storepass "$(cat keystore-password.txt)" | grep SHA256
```

`app-release-bundle.aab` 是上 Google Play 用的格式，需要时也在这个目录里生成。
