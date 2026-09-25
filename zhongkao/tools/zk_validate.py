#!/usr/bin/env python3
"""校验 zhongkao/data/<科目>/ 下的 kp.json 和 papers/*.json。用法：python3 tools/zk_validate.py wuli"""
import json, sys, os, re, glob

TYPES = {'choice', 'multi', 'blank', 'short', 'draw', 'essay', 'listening'}
ID_RE = re.compile(r'^[a-z0-9._]+$')

def main(subj):
    base = os.path.join(os.path.dirname(__file__), '..', 'data', subj)
    errs, warns = [], []
    kp = json.load(open(os.path.join(base, 'kp.json'), encoding='utf-8'))
    kpids = set()
    for m in kp['modules']:
        for k in m['kps']:
            if not ID_RE.match(k['id']): errs.append(f"kp id 非法: {k['id']}")
            if k['id'] in kpids: errs.append(f"kp id 重复: {k['id']}")
            kpids.add(k['id'])
    used = set()
    for f in sorted(glob.glob(os.path.join(base, 'papers', '*.json'))):
        p = json.load(open(f, encoding='utf-8'))
        tag = os.path.basename(f)
        mids = {m['id'] for m in p.get('materials', [])}
        for m in p.get('materials', []):
            for fig in m.get('figures', []):
                if not os.path.exists(os.path.join(base, fig)): errs.append(f"{tag} 材料 {m['id']} 图不存在: {fig}")
        qids, total = set(), 0
        for q in p['questions']:
            qid = q.get('id', '?')
            for key in ('id', 'no', 'section', 'type', 'score', 'stem', 'answer', 'kp'):
                if key not in q: errs.append(f"{tag} {qid} 缺字段 {key}")
            if qid in qids: errs.append(f"{tag} 题目 id 重复: {qid}")
            qids.add(qid)
            if not qid.startswith(f"{subj}-{p['year']}-"): errs.append(f"{tag} id 前缀不对: {qid}")
            if q.get('type') not in TYPES: errs.append(f"{tag} {qid} type 非法: {q.get('type')}")
            if q.get('type') in ('choice', 'multi') and len(q.get('options') or []) < 2: errs.append(f"{tag} {qid} 选择题缺 options")
            if q.get('material') and q['material'] not in mids: errs.append(f"{tag} {qid} material 不存在: {q['material']}")
            for k in q.get('kp', []):
                if k not in kpids: errs.append(f"{tag} {qid} 考点不存在: {k}")
                used.add(k)
            if not q.get('kp'): errs.append(f"{tag} {qid} 没有标考点")
            for fig in q.get('figures', []):
                if not os.path.exists(os.path.join(base, fig)): errs.append(f"{tag} {qid} 图不存在: {fig}")
            if q.get('answer', '') == '': warns.append(f"{tag} {qid} 无答案")
            if '[?]' in json.dumps(q, ensure_ascii=False): warns.append(f"{tag} {qid} 有存疑 [?]")
            total += q.get('score', 0) or 0
        if abs(total - p.get('total', 0)) > 0.01: errs.append(f"{tag} 分值合计 {total} ≠ total {p.get('total')}")
        print(f"{tag}: {len(p['questions'])} 题，合计 {total} 分")
    unused = kpids - used
    print(f"考点 {len(kpids)} 个，真题覆盖 {len(kpids & used)} 个，未覆盖 {len(unused)} 个")
    for w in warns: print('警告', w)
    for e in errs: print('错误', e)
    sys.exit(1 if errs else 0)

if __name__ == '__main__':
    main(sys.argv[1])
