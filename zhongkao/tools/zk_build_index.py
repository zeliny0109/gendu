#!/usr/bin/env python3
"""生成 data/index.json：各科名称、计入总分、收录年份、题数、考点数。先对每科跑 zk_stats.py。"""
import json, os, glob, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')
META = [  # 泉州 2026 口径：计入 800 分总分的分值
    ('yuwen', '语文', 150), ('shuxue', '数学', 150), ('yingyu', '英语', 150),
    ('wuli', '物理', 90), ('huaxue', '化学', 60), ('daofa', '道德与法治', 50), ('lishi', '历史', 50),
]
subs = []
for sid, name, weight in META:
    base = os.path.join(DATA, sid)
    if not os.path.exists(os.path.join(base, 'kp.json')):
        subs.append({'id': sid, 'name': name, 'weight': weight, 'ready': False}); continue
    subprocess.run([sys.executable, os.path.join(HERE, 'zk_stats.py'), sid], check=True, stdout=subprocess.DEVNULL)
    years, nq = [], 0
    for f in sorted(glob.glob(os.path.join(base, 'papers', '*.json'))):
        p = json.load(open(f, encoding='utf-8'))
        years.append({'year': p['year'], 'n': len(p['questions']), 'total': p.get('total'), 'minutes': p.get('minutes')})
        nq += len(p['questions'])
    kp = json.load(open(os.path.join(base, 'kp.json'), encoding='utf-8'))
    subs.append({'id': sid, 'name': name, 'weight': weight, 'ready': bool(years), 'years': years, 'questions': nq,
                 'kps': sum(len(m['kps']) for m in kp['modules']),
                 'lessons': os.path.exists(os.path.join(base, 'lessons.json')),
                 'listening': sorted(int(os.path.basename(f)[:4]) for f in glob.glob(os.path.join(base, 'listening', '*.json')))})
json.dump({'subjects': subs}, open(os.path.join(DATA, 'index.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for s in subs: print(s['name'], '就绪' if s['ready'] else '未就绪', s.get('questions', 0), '题', s.get('kps', 0), '考点')
