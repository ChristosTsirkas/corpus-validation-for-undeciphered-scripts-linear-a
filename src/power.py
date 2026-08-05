#!/usr/bin/env python3
"""Power calibration for the phonological inheritance test.

'No signal' is uninformative without knowing what magnitude of signal the
corpus could have revealed. Synthetic vowel-dependency of known strength is
injected into words of the observed shape, and the detection rate measured.
"""
import os
import sys, random, collections

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import structural as st  # noqa: E402


sys.path.insert(0,'src'); import phonology_test as pt

random.seed(20260731)
recs = st.load()
vmap = pt.build_map('assumed')
words = pt.words_with_coverage(recs, vmap)
lengths = [len(w) for w in words]
vowels = list('aeiou')
base = collections.Counter(vmap[i] for w in words for i in w)
marg = [base[v] for v in vowels]


def synth(strength) -> list[list[str]]:
    """Generate words where each vowel repeats the previous with prob=strength."""
    out = []
    for length in lengths:
        seq = [random.choices(vowels, weights=marg, k=1)[0]]
        for _ in range(length - 1):
            if random.random() < strength:
                seq.append(seq[-1])                       # harmony
            else:
                seq.append(random.choices(vowels, weights=marg, k=1)[0])
        out.append(seq)
    return out


def mi_of(seqs) -> float:
    idmap = {}
    ws = []
    for k, seq in enumerate(seqs):
        ids = []
        for j, vowel in enumerate(seq):
            key = f'X{k}_{j}'
            idmap[key] = vowel
            ids.append(key)
        ws.append(ids)
    return pt.vowel_mi(ws, idmap)[0]


def detect_rate(strength: float, reps: int = 60, trials: int = 400) -> float:
    hits = 0
    for _ in range(reps):
        seqs = synth(strength)
        obs = mi_of(seqs)
        flat = [v for seq in seqs for v in seq]
        null = []
        for _ in range(trials):
            sh = flat[:]
            random.shuffle(sh)
            it = iter(sh)
            perm = [[next(it) for _ in seq] for seq in seqs]
            null.append(mi_of(perm))
        p = (sum(1 for v in null if v >= obs) + 1) / (trials + 1)
        hits += (p < 0.05)
    return hits / reps


print('POWER CALIBRATION (assumed-value level, n=1217 vowel bigrams)')
print(f'  observed MI in real data : {pt.vowel_mi(words, vmap)[0]:.4f} bits')
print(f'\n  {"harmony strength":>18}{"detection rate":>16}')
for s in (0.05, 0.10, 0.15, 0.20, 0.30):
    print(f'  {s:>18.2f}{detect_rate(s):>16.0%}')
