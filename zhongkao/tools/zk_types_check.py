#!/usr/bin/env python3
"""检查 data/<科目>/types.json。用法：python3 tools/zk_types_check.py shuxue"""
import json, sys, os, re, glob
subj = sys.argv[1]
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', subj)
qs = set()
for f in glob.glob(os.path.join(base, 'papers', '*.json')):
    qs |= {q['id'] for q in json.load(open(f, encoding='utf-8'))['questions']}
T = json.load(open(os.path.join(base, 'types.json'), encoding='utf-8'))
errs, ids, covered = 0, set(), set()
if len(re.sub(r'\s', '', T.get('strategy', ''))) < 150: print('警告 strategy 太短'); 
for t in T['types']:
    for k in ('id', 'name', 'pos', 'qs', 'md'):
        if k not in t: print('错误', t.get('id'), '缺', k); errs += 1
    if not t['id'].startswith(subj + '.t.'): print('错误 id 前缀应为', subj + '.t.', t['id']); errs += 1
    if t['id'] in ids: print('错误 id 重复', t['id']); errs += 1
    ids.add(t['id'])
    for q in t['qs']:
        if q not in qs: print('错误', t['id'], '题目不存在', q); errs += 1
        covered.add(q)
    for q in re.findall(r'\[\[q:([^\]]+)\]\]', t['md']):
        if q not in qs: print('错误', t['id'], '示范题不存在', q); errs += 1
    for f in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', t['md']):
        if not os.path.exists(os.path.join(base, f)): print('错误', t['id'], '图不存在', f); errs += 1
    for sec in ('## 这道题长什么样', '## 解题步骤', '## 答题规范', '## 常见失分', '## 真题示范'):
        if sec not in t['md']: print('警告', t['id'], '缺', sec)
    n = len(re.sub(r'\s', '', t['md']))
    if n < 400 or n > 3000: print('警告', t['id'], '字数', n)
print(f"{len(T['types'])} 张题型卡，覆盖真题 {len(covered)}/{len(qs)} 条，错误 {errs}")
sys.exit(1 if errs else 0)
