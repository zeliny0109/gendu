#!/usr/bin/env python3
"""按考点统计真题：出现年份、题数、分值。用法：python3 tools/zk_stats.py wuli"""
import json, sys, os, glob
subj = sys.argv[1]
base = os.path.join(os.path.dirname(__file__), '..', 'data', subj)
kp = json.load(open(os.path.join(base, 'kp.json'), encoding='utf-8'))
st = {k['id']: {'name': k['name'], 'module': m['name'], 'years': set(), 'count': 0, 'score': 0.0, 'qs': []} for m in kp['modules'] for k in m['kps']}
years = []
for f in sorted(glob.glob(os.path.join(base, 'papers', '*.json'))):
    p = json.load(open(f, encoding='utf-8')); years.append(p['year'])
    for q in p['questions']:
        ks = q.get('kp', [])
        for i, k in enumerate(ks):
            if k not in st: continue
            s = st[k]; s['years'].add(p['year']); s['count'] += 1; s['qs'].append(q['id'])
            s['score'] += (q.get('score', 0) or 0) * (0.6 if i == 0 and len(ks) > 1 else (1 if len(ks) == 1 else 0.4 / (len(ks) - 1)))
out = {'subject': subj, 'years': years, 'kps': {k: {**v, 'years': sorted(v['years']), 'score': round(v['score'], 1)} for k, v in st.items()}}
json.dump(out, open(os.path.join(base, 'stats.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
rows = sorted(out['kps'].items(), key=lambda kv: -kv[1]['score'])
for k, v in rows[:25]: print(f"{v['score']:6.1f} 分 {len(v['years'])} 年 {v['count']:3d} 题  {v['module']} / {v['name']}")
