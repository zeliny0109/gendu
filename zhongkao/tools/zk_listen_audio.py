#!/usr/bin/env python3
"""按 data/yingyu/listening/<年>.json 的听力原文生成练习音频（edge-tts：女声 Jenny / 男声 Guy）。
每个 clip 生成一个 mp3：各说话轮次之间停 0.7 秒，整段按 repeat 读几遍，遍与遍之间停 3 秒。
输出 data/yingyu/audio/<年>/<clip id>.mp3，并把路径写回 clip 的 "audio" 字段。
用法：python3 tools/zk_listen_audio.py [年份…] [--force]
"""
import asyncio, json, os, sys, glob, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, '..', 'data', 'yingyu')
VOICES, RATE = {'f': 'en-US-JennyNeural', 'm': 'en-US-GuyNeural'}, '-5%'

async def tts(text, voice, out):
    import edge_tts
    for k in range(5):
        try:
            await edge_tts.Communicate(text, voice, rate=RATE).save(out); return
        except Exception as e:
            print('retry', e, flush=True); await asyncio.sleep(2 + 3 * k)
    raise RuntimeError('TTS failed: ' + text[:40])

def silence(sec, out):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i', f'anullsrc=r=24000:cl=mono', '-t', str(sec), '-c:a', 'pcm_s16le', out], check=True)

def to_wav(src, out):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-ar', '24000', '-ac', '1', '-c:a', 'pcm_s16le', out], check=True)

async def clip_audio(clip, out, sem):
    async with sem:
        with tempfile.TemporaryDirectory() as td:
            parts = []
            for i, ln in enumerate(clip['lines']):
                mp3 = f'{td}/l{i}.mp3'; wav = f'{td}/l{i}.wav'
                await tts(ln['t'], VOICES.get(ln.get('v'), VOICES['f']), mp3)
                to_wav(mp3, wav); parts.append(wav)
            gap, rgap = f'{td}/gap.wav', f'{td}/rgap.wav'
            silence(0.7, gap); silence(3, rgap)
            once = []
            for i, p in enumerate(parts): once += ([gap] if i else []) + [p]
            seq = []
            for r in range(clip.get('repeat', 2)): seq += ([rgap] if r else []) + once
            lst = f'{td}/list.txt'
            open(lst, 'w').write(''.join(f"file '{p}'\n" for p in seq))
            os.makedirs(os.path.dirname(out), exist_ok=True)
            subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst,
                            '-af', 'loudnorm=I=-16:TP=-1:LRA=9', '-ar', '24000', '-ac', '1', '-b:a', '40k', out], check=True)

async def main(years, force):
    files = sorted(glob.glob(f'{BASE}/listening/*.json'))
    sem = asyncio.Semaphore(4)
    for f in files:
        data = json.load(open(f, encoding='utf-8'))
        if years and str(data['year']) not in years: continue
        jobs = []
        for c in data['clips']:
            rel = f"audio/{data['year']}/{c['id']}.mp3"
            if force or not os.path.exists(f'{BASE}/{rel}'): jobs.append(clip_audio(c, f'{BASE}/{rel}', sem))
            c['audio'] = rel
        await asyncio.gather(*jobs)
        json.dump(data, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(data['year'], f'{len(jobs)} 段生成，共 {len(data["clips"])} 段', flush=True)

args = [a for a in sys.argv[1:] if not a.startswith('--')]
asyncio.run(main(args, '--force' in sys.argv))
