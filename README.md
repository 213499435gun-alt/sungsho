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

## Instagram 多账号

`index.html` 里的 `igData` 支持多个账号：

```js
const igData = { accounts: [
  { profile: { avatar:'ig/头像.jpg', id:'账号ID', name:'昵称', bio:'简介' },
    posts: [ { images:['ig/a.jpg','ig/b.jpg'], caption:'文案', likes:'18', time:'26.07.11' } ] },
  { profile: { ... }, posts: [ ... ] }
]};
```

- 手机里打开 Instagram → 顶栏 **⇄** 按钮 → 选择账号，即可查看不同账号的主页、帖子和快拍。
- 快拍按账号拆分，存在 `storiesByAccount` 里，键是账号 ID：

```js
const storiesByAccount = {
  '_shotaroo_': [ {type:'image', src:'stories/1.jpg', duration:5, date:'26.09.21', texts:[]} ],
  'friend_acc': [ {type:'image', src:'stories/friend/1.jpg', duration:5, date:'24.01.01', texts:[]} ]
};
```

  账号没有自己的快拍时，回退到 `DEFAULT_STORIES`；列表里也不会显示「我的动态」入口。
- 用 `ig-editor.html` 编辑：左侧「账号列表」可添加/切换/删除账号，每个账号单独编辑头像、ID、简介、帖子和快拍（快拍支持单条更换图片、日期、时长，以及批量导入）。
- 编辑完点「生成数据」，把 JSON 发给我，或保存为 `ig-data.json` 后运行：

```sh
python3 apply_ig.py ig-data.json
```

脚本同时兼容旧的单账号格式（`{profile, posts}`）。
