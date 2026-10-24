"""Original royalty-free music beds for Love God. reels (generated in code)."""
import numpy as np, wave
SR = 44100
def note(m): return 440 * 2 ** ((m - 69) / 12)
def bed(out, chords, secs=15.0, arp=True, bright=0.3, decay=2.2, seed=1):
    N = int(SR * secs); t_all = np.arange(N) / SR; mix = np.zeros((N, 2))
    def env(n, a, r):
        e = np.ones(n); a = int(a * SR); r = int(r * SR); e[:a] = np.linspace(0, 1, a); e[-r:] *= np.linspace(1, 0, r); return e
    def add(sig, start, pan=0, g=1):
        s = int(start * SR); e = min(N, s + len(sig)); sig = sig[:e - s] * g
        mix[s:e, 0] += sig * (1 - pan); mix[s:e, 1] += sig * (1 + pan)
    CL = secs / len(chords)
    for i, ch in enumerate(chords):
        n = int((CL + 1.5) * SR); tt = np.arange(n) / SR
        for m in ch:
            f = note(m)
            pad = np.sin(2*np.pi*f*tt) + bright*np.sin(2*np.pi*2.002*f*tt) + 0.5*np.sin(2*np.pi*f*1.003*tt)
            add(pad * env(n, 1.4, 1.5), i * CL, pan=((m % 3) - 1) * 0.35, g=0.045)
        add(np.sin(2*np.pi*note(ch[0]-24)*tt) * env(n, 0.8, 1.2), i * CL, g=0.10)
        if arp:
            seq = [ch[0]+12, ch[1]+12, ch[2]+12, ch[1]+12]
            for k in range(4):
                f = note(seq[k]); m = int(2.2*SR); tk = np.arange(m) / SR
                p = (np.sin(2*np.pi*f*tk) + 0.3*np.sin(2*np.pi*2*f*tk)) * np.exp(-tk*decay)
                add(p * env(m, 0.01, 0.2), i*CL + k*CL/4, pan=0.3 if k % 2 else -0.3, g=0.06)
    d1, d2 = int(0.31*SR), int(0.47*SR); wet = np.zeros_like(mix)
    wet[d1:, 0] += mix[:-d1, 1]*0.35; wet[d2:, 1] += mix[:-d2, 0]*0.3; mix += wet
    mix *= np.minimum(1, t_all/1.0)[:, None]; fo = int(1.5*SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
    mix /= np.max(np.abs(mix)) / 0.85
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
if __name__ == "__main__":
    # morning: bright D major lift (D A Bm G)
    bed("tools/music_morning_15s.wav", [[62,66,69],[57,61,64,69],[59,62,66],[55,59,62,67]], bright=0.45, decay=2.8)
    # night: slow, low, no arpeggio movement (Am F C Em)
    bed("tools/music_night_15s.wav", [[57,60,64],[53,57,60],[48,52,55,60],[52,55,59]], arp=True, bright=0.15, decay=1.4)
    # hope: E-flat major (Eb Bb Cm Ab)
    bed("tools/music_hope_15s.wav", [[63,67,70],[58,62,65,70],[60,63,67],[56,60,63,68]], bright=0.35, decay=2.0)
