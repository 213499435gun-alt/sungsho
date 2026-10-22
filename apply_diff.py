#!/usr/bin/env python3
"""应用编辑器生成的增量数据到 index.html 的 myStories 数组。
用法: python3 apply_diff.py diff.json
依赖 Node.js 解析 JS 对象字面量。
"""
import json, re, sys, subprocess

def load_stories(html):
    m = re.search(r'const myStories=(\[[\s\S]*?\]);', html)
    if not m:
        raise SystemExit("找不到 myStories 数组")
    js_arr = m.group(1)
    # 用 node 解析 JS 对象字面量
    node_code = 'const a=' + js_arr + ';process.stdout.write(JSON.stringify(a));'
    out = subprocess.run(['node', '-e', node_code], capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit("Node 解析失败: " + out.stderr)
    return json.loads(out.stdout)

def dump_stories(stories):
    lines = ['  ' + json.dumps(s, ensure_ascii=False, separators=(',', ':')) for s in stories]
    return 'const myStories=[\n' + ',\n'.join(lines) + '\n];'

def main():
    if len(sys.argv) < 2:
        raise SystemExit("用法: python3 apply_diff.py diff.json")
    with open(sys.argv[1], encoding='utf-8') as f:
        diff = json.load(f)
    path = 'index.html'
    with open(path, encoding='utf-8') as f:
        html = f.read()
    stories = load_stories(html)
    print(f"当前 {len(stories)} 页")

    changed_idx = {item['index'] for item in diff.get('changed', [])}
    removed = diff.get('removed', [])

    # 冲突检测：同一索引既 changed 又 removed
    conflict = changed_idx & set(removed)
    if conflict:
        print(f"  ⚠️ 索引 {sorted(conflict)} 同时出现在 changed 和 removed，按 changed（修改）处理，忽略删除")

    # 1) 先应用修改/新增（按索引升序，保证新增顺序正确）
    for item in sorted(diff.get('changed', []), key=lambda x: x['index']):
        idx, page = item['index'], item['page']
        if 0 <= idx < len(stories):
            print(f"  修改第 {idx + 1} 页")
            stories[idx] = page
        elif idx == len(stories):
            print(f"  新增第 {idx + 1} 页")
            stories.append(page)
        else:
            print(f"  ⚠️ 索引 {idx} 超出范围，跳过")

    # 2) 再删除（从大到小，跳过已 changed 的索引）
    for idx in sorted(removed, reverse=True):
        if idx in conflict:
            continue
        if 0 <= idx < len(stories):
            print(f"  删除第 {idx + 1} 页")
            del stories[idx]
    new_block = dump_stories(stories)
    html = re.sub(r'const myStories=\[[\s\S]*?\];', new_block, html, count=1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"完成，现在 {len(stories)} 页")

if __name__ == '__main__':
    main()
