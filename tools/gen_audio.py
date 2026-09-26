#!/usr/bin/env python3
"""为 book.json（女声 Jenny / 男声 Guy，按句子的 voice 字段 f/m 选择） 里还没有音频的句子生成示范 mp3（edge-tts），并做响度归一（ffmpeg）。
用法：python3 tools/gen_audio.py [--force]
"""
import asyncio, json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICES, RATE = {'f': 'en-US-JennyNeural', 'm': 'en-US-GuyNeural'}, '-10%'
plain = lambda t: re.sub(r'\s+', ' ', re.sub(r'[*↗↘]', '', t).replace('‿', ' ')).strip()

async def one(s, sem, force):
    import edge_tts
    rel = f"audio/{s['id']}.mp3"; out = f'{ROOT}/{rel}'
    if not force and s.get('audio') and os.path.exists(out): return 0
    async with sem:
        raw = out + '.raw.mp3'
        for k in range(5):
            try:
                await edge_tts.Communicate(plain(s['t']), VOICES.get(s.get('voice'), VOICES['f']), rate=RATE).save(raw); break
            except Exception as e:
                print('retry', s['id'], e, flush=True); await asyncio.sleep(2 + 3 * k)
        else:
            raise RuntimeError('TTS failed: ' + s['id'])
        p = await asyncio.create_subprocess_exec('ffmpeg', '-y', '-v', 'error', '-i', raw, '-af', 'loudnorm=I=-14:TP=-1:LRA=9',
                                                 '-ar', '24000', '-ac', '1', '-b:a', '48k', out)
        if await p.wait() != 0: raise RuntimeError('ffmpeg failed: ' + s['id'])
        os.remove(raw)
    s['audio'] = rel
    return 1

async def main(force):
    book = json.load(open(f'{ROOT}/book.json', encoding='utf-8'))
    os.makedirs(f'{ROOT}/audio', exist_ok=True)
    sem = asyncio.Semaphore(6)
    items = [s for u in book['units'] for s in u['sentences']]
    changed = 0
    for i in range(0, len(items), 60):  # 分批，每批写回一次，中断后可续跑
        changed += sum(await asyncio.gather(*(one(s, sem, force) for s in items[i:i+60])))
        json.dump(book, open(f'{ROOT}/book.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'{min(i+60, len(items))}/{len(items)}', flush=True)
    print(f'{changed} 个音频已生成')

asyncio.run(main('--force' in sys.argv))
