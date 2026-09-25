#!/usr/bin/env python3
"""为 book.json 里还没有音频的句子生成示范 mp3（edge-tts），并做响度归一（ffmpeg）。
用法：python3 tools/gen_audio.py [--force]
"""
import asyncio, json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE, RATE = 'en-US-JennyNeural', '-10%'
plain = lambda t: re.sub(r'\s+', ' ', re.sub(r'[*↗↘]', '', t).replace('‿', ' ')).strip()

async def main(force):
    import edge_tts
    book = json.load(open(f'{ROOT}/book.json', encoding='utf-8'))
    os.makedirs(f'{ROOT}/audio', exist_ok=True)
    changed = 0
    for u in book['units']:
        for s in u['sentences']:
            rel = f"audio/{s['id']}.mp3"; out = f'{ROOT}/{rel}'
            if not force and s.get('audio') and os.path.exists(out): continue
            raw = out + '.raw.mp3'
            await edge_tts.Communicate(plain(s['t']), VOICE, rate=RATE).save(raw)
            subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', raw, '-af', 'loudnorm=I=-14:TP=-1:LRA=9',
                            '-ar', '24000', '-ac', '1', '-b:a', '64k', out], check=True)
            os.remove(raw); s['audio'] = rel; changed += 1
            print(s['id'], plain(s['t']))
    if changed:
        json.dump(book, open(f'{ROOT}/book.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f'{changed} 个音频已生成')

asyncio.run(main('--force' in sys.argv))
