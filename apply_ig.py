#!/usr/bin/env python3
"""应用 IG 编辑器生成的数据到 index.html 的 igData。

用法: python3 apply_ig.py ig-data.json

支持两种格式：
  1) 多账号（ig-editor.html 导出）: {"accounts":[{profile,posts,stories}, ...]}
  2) 旧版单账号:                   {"profile":{...}, "posts":[...]}
"""
import json, re, sys


def normalize(data):
    """统一成 {accounts:[{profile,posts,stories}]} 结构。"""
    if isinstance(data.get('accounts'), list) and data['accounts']:
        accounts = []
        for a in data['accounts']:
            accounts.append({
                'profile': a.get('profile', {}) or {},
                'posts': a.get('posts', []) or [],
                'stories': a.get('stories', []) or [],
            })
        return {'accounts': accounts}
    # 旧版单账号
    return {'accounts': [{
        'profile': data.get('profile', {}) or {},
        'posts': data.get('posts', []) or [],
        'stories': data.get('stories', []) or [],
    }]}


def build_block(data):
    """生成注入 index.html 的 igData 代码块。"""
    acc_lines = []
    for a in data['accounts']:
        prof = json.dumps(a['profile'], ensure_ascii=False, separators=(',', ':'))
        posts = json.dumps(a['posts'], ensure_ascii=False, separators=(',', ':'))
        stories = json.dumps(a['stories'], ensure_ascii=False, separators=(',', ':'))
        acc_lines.append(
            '    {profile:%s,posts:%s,stories:%s}' % (prof, posts, stories)
        )
    accounts_js = '[\n' + ',\n'.join(acc_lines) + '\n  ]'
    return 'const igData={\n  accounts:' + accounts_js + '\n};'


def main():
    if len(sys.argv) < 2:
        raise SystemExit("用法: python3 apply_ig.py ig-data.json")

    with open(sys.argv[1], encoding='utf-8') as f:
        data = normalize(json.load(f))

    path = 'index.html'
    with open(path, encoding='utf-8') as f:
        html = f.read()

    new_block = build_block(data)

    # 1) 如果已有 const igData={...}; 数据块，直接替换
    pattern = r'const igData=\{[\s\S]*?\n\};'
    if re.search(pattern, html):
        html = re.sub(pattern, lambda m: new_block, html, count=1)
    else:
        # 2) 否则插到兜底逻辑（if(typeof igData...）之前
        anchor = "if(typeof igData==='undefined'"
        idx = html.find(anchor)
        if idx == -1:
            raise SystemExit("在 index.html 里没找到 igData 兜底逻辑，请检查文件。")
        html = html[:idx] + new_block + '\n' + html[idx:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    total_posts = sum(len(a['posts']) for a in data['accounts'])
    total_stories = sum(len(a['stories']) for a in data['accounts'])
    print("完成：%d 个账号，%d 条帖子，%d 条快拍"
          % (len(data['accounts']), total_posts, total_stories))
    for a in data['accounts']:
        p = a['profile']
        print("  @%s  头像=%s  帖子=%d  快拍=%d"
              % (p.get('id', ''), '有' if p.get('avatar') else '无',
                 len(a['posts']), len(a['stories'])))


if __name__ == '__main__':
    main()
