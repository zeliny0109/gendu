#!/usr/bin/env python3
"""检查 data/<科目>/lessons.json：键是存在的考点、[[q:…]] 指向存在的题、图存在、四节齐全。用法：python3 tools/zk_lessons_check.py wuli"""
import json, sys, os, re, glob
subj = sys.argv[1]
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', subj)
kp = {k['id'] for m in json.load(open(os.path.join(base, 'kp.json'), encoding='utf-8'))['modules'] for k in m['kps']}
qs = set()
for f in glob.glob(os.path.join(base, 'papers', '*.json')):
    qs |= {q['id'] for q in json.load(open(f, encoding='utf-8'))['questions']}
L = json.load(open(os.path.join(base, 'lessons.json'), encoding='utf-8'))
errs = 0
for k, v in L.items():
    if k not in kp: print('错误 考点不存在', k); errs += 1
    for q in re.findall(r'\[\[q:([^\]]+)\]\]', v):
        if q not in qs: print('错误', k, '题目不存在', q); errs += 1
    for f in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', v):
        if not os.path.exists(os.path.join(base, f)): print('错误', k, '图不存在', f); errs += 1
    for sec in ('## 考什么', '## 要点', '## 易错点', '## 真题精讲'):
        if sec not in v: print('警告', k, '缺', sec)
    n = len(re.sub(r'\s', '', v))
    if n < 250 or n > 2000: print('警告', k, '字数', n)
print(f'{len(L)} 篇讲解，错误 {errs}')
sys.exit(1 if errs else 0)
