# 口袋宇宙 · iPhone Playground

一个无需依赖、无需构建的中文手机模拟网页。

## 体验

解锁密码：**123456**。点击屏幕底部或向上滑动后输入，支持键盘数字和退格。

- 相册：9 张原创 SVG 风景插画、大图切换、临时添加本地图片。
- 音乐：3 首本地合成的原创示例旋律，播放、暂停、切歌、拖动进度及音量。
- 备忘录：保存到当前浏览器 localStorage。
- 设置：切换网页背景、重新锁屏；时钟内有秒表。
- 点击底部横条返回主屏幕，右侧实体键锁屏。

直接打开 `index.html` 即可使用，所有内置资源均在文件内，无外部素材依赖。

## GitHub Pages

仓库 Settings → Pages → Build and deployment → Source 选择 **GitHub Actions**。
随后在 Actions 运行 `Publish Pocket Universe` 工作流。
成功后访问 https://213499435gun-alt.github.io/sungsho/ 。

此地址只有在 Pages 部署成功后才可访问。模拟密码不提供安全保护，请勿存放敏感信息。

## 自定义

在 `index.html` 中修改 `songs`、`palettes` 和 `names` 可调整音乐曲名及相册。
