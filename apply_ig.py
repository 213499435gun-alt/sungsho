#!/usr/bin/env python3
"""应用 IG 编辑器生成的数据到 index.html 的 igData。用法: python3 apply_ig.py ig-data.json"""
import json, re, sys

def main():
    if len(sys.argv) < 2:
        raise SystemExit("用法: python3 apply_ig.py ig-data.json")
    with open(sys.argv[1], encoding='utf-8') as f:
        data = json.load(f)

    path = 'index.html'
    with open(path, encoding='utf-8') as f:
        html = f.read()

    prof = data.get('profile', {})
    posts = data.get('posts', [])

    # 生成 igData 代码块
    prof_js = json.dumps(prof, ensure_ascii=False, separators=(',', ':'))
    post_lines = ['    ' + json.dumps(p, ensure_ascii=False, separators=(',', ':')) for p in posts]
    posts_js = '[\n' + ',\n'.join(post_lines) + '\n  ]' if posts else '[]'

    new_block = 'const igData={\n  profile:' + prof_js + ',\n  posts:' + posts_js + '\n};\nconst igPosts=igData.posts;'

    html = re.sub(r'const igData=\{[\s\S]*?\};\s*const igPosts=igData\.posts;', new_block, html, count=1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"完成：头像={'有' if prof.get('avatar') else '无'}，ID={prof.get('id','')}，帖子 {len(posts)} 条")

if __name__ == '__main__':
    main()
