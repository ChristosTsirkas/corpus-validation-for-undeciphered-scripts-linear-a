#!/usr/bin/env python3
"""
Does the affix measure have power to detect DIRECTION at all?

The observed prefix share (0.425) sits 0.23 sd from the null. A reviewer asks
whether that means the language is directionless, or whether the method simply
cannot detect direction at this corpus size. These are different claims and the
difference matters, because §5.5 withdraws an argument on the strength of it.

METHOD. Build synthetic corpora with a KNOWN affixation direction - strongly
suffixing, strongly prefixing, and balanced - at the observed corpus size and
length distribution. Run the same measure and null model. Measure the detection
rate.

If the method detects a strongly suffixing synthetic corpus, then the observed
null is evidence about the language. If it does not, the observed null is
evidence about the method and nothing else.
"""
import os
import random, statistics, collections, sys

# Stages run from the repository root as `python3 src/<stage>.py`, so src/
# must be on sys.path before sibling stages can be imported normally.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from corpus_io import json_load  # noqa: E402
import grid_null as gn  # noqa: E402
import typology as ty  # noqa: E402

sys.path.insert(0, 'src')


random.seed(20260731)
TRIALS = 500
N_REPS = 25      # replications per condition in the graded-skew analysis

# NOTE ON RUNTIME. The graded-skew analysis is the most expensive stage in the
# project: 8 conditions x 25 replications x 200 permutations, each permutation
# recomputing affix relations over ~500 types. Roughly 20 minutes single-core.
# The published results are bundled at data/power_analysis.json so that readers
# need not re-run it; see docs/METHODOLOGY.md for how to reproduce a single
# condition in about two minutes.


def make_corpus(n_stems, lengths, signs, direction, affix_rate=0.35,
                n_affixes=6) -> list[tuple[str, ...]]:
    """Synthesize a corpus with known affixation direction.

    direction: 'suffix', 'prefix' or 'balanced'.
    Each stem may appear bare and also with an affix at the given edge, so the
    stem is independently attested and the measure can find it.
    """
    stems = []
    for length in lengths[:n_stems]:
        stems.append(tuple(random.choice(signs) for _ in range(max(2, length))))
    affixes = [tuple(random.choice(signs) for _ in range(random.choice([1, 2])))
               for _ in range(n_affixes)]
    out = list(stems)
    for st in stems:
        if random.random() > affix_rate:
            continue
        af = random.choice(affixes)
        if isinstance(direction, float):          # graded: P(prefix)
            out.append((af + st) if random.random() < direction else (st + af))
        elif direction == 'suffix':
            out.append(st + af)
        elif direction == 'prefix':
            out.append(af + st)
        else:
            out.append((af + st) if random.random() < 0.5 else (st + af))
    return out


def prefix_share(types) -> tuple[float | None, int]:
    pre, suf = ty.find_affixes(collections.Counter(types))
    tot = len(pre) + len(suf)
    return (len(pre) / tot if tot else None), tot


def detect(types, trials=TRIALS) -> tuple[float | None, float | None, float | None, int]:
    """Is the observed prefix share distinguishable from its null?"""
    obs, tot = prefix_share(types)
    if obs is None or tot < 10:
        return None, None, None, tot
    dists = gn.positional_dists(list(types))
    null = []
    for _ in range(trials):
        r = gn.resample(list(types), dists)
        share, _ = prefix_share(r)
        if share is not None:
            null.append(share)
    if len(null) < 20:
        return obs, None, None, tot
    m, s = float(statistics.mean(null)), float(statistics.pstdev(null)) or 1e-9
    return obs, m, (obs - m) / s, tot


def main() -> None:
    g = json_load('data/signgroups_by_genre.json')
    real = [tuple(t) for t in g['administrative'] if len(t) > 1]
    real_types = sorted(set(real))
    lengths = [len(t) for t in real_types]
    signs = sorted({s for t in real_types for s in t})

    print('POWER OF THE AFFIX-DIRECTION MEASURE')
    print(f'  real corpus: {len(real_types)} types, {len(signs)} signs\n')

    obs, m, z, tot = detect(real_types)
    print('  OBSERVED (administrative)')
    if obs is None or m is None or z is None:
        print(f'    too few affix relations ({tot}) for a stable estimate\n')
    else:
        print(f'    prefix share {obs:.3f}   null {m:.3f}   z = {z:+.2f}   '
              f'relations {tot}\n')

    print('  SYNTHETIC CONTROLS at the same size and length distribution')
    print('  Two affixation rates: one matching the observed number of affix')
    print(f'  relations ({tot}), one higher, to separate power from effect size.')
    print(f'  {"direction":12s}{"rate":>6}{"prefix share":>14}{"null":>8}{"z":>8}{"n":>7}  detected?')
    for rate in (0.13, 0.35):
      for direction in ('suffix', 'balanced', 'prefix'):
        zs = []
        for _ in range(5):
            syn = make_corpus(len(real_types), lengths, signs, direction,
                              affix_rate=rate)
            o, mm, zz, tt = detect(sorted(set(syn)), trials=100)
            if zz is not None:
                zs.append((o, mm, zz, tt))
        if not zs:
            print(f'  {direction:12s}{rate:>6.2f}  no affix relations generated')
            continue
        o = float(statistics.mean(x[0] for x in zs))
        mm = float(statistics.mean(x[1] for x in zs))
        zz = float(statistics.mean(x[2] for x in zs))
        tt = int(float(statistics.mean(x[3] for x in zs)))
        det = 'YES' if abs(zz) > 1.96 else 'no'
        print(f'  {direction:12s}{rate:>6.2f}{o:>14.3f}{mm:>8.3f}{zz:>8.2f}{tt:>7}  {det}')

    print()
    print('  GRADED SKEW: what magnitude of directional preference is detectable')
    print('  at the observed corpus size? The received figure in the literature')
    print('  is 59% prefixal.')
    print(f'  {N_REPS} replications per condition, 200 permutations each.')
    print(f'  {"true P(prefix)":>15}{"observed":>10}{"null":>8}{"z":>8}{"n":>7}  detection rate')
    for p in (0.50, 0.59, 0.65, 0.75, 0.85, 0.95, 0.99, 1.00):
        zs = []
        for _ in range(N_REPS):
            syn = make_corpus(len(real_types), lengths, signs, p, affix_rate=0.13)
            o, mm, zz, tt = detect(sorted(set(syn)), trials=200)
            if zz is not None:
                zs.append((o, mm, zz, tt))
        if not zs:
            continue
        o = float(statistics.mean(x[0] for x in zs))
        mm = float(statistics.mean(x[1] for x in zs))
        zz = float(statistics.mean(x[2] for x in zs))
        tt = int(float(statistics.mean(x[3] for x in zs)))
        hits = sum(1 for x in zs if abs(x[2]) > 1.96)
        rate = 100 * hits / len(zs)
        print(f'  {p:>15.2f}{o:>10.3f}{mm:>8.3f}{zz:>8.2f}{tt:>7}  {hits:>3}/{len(zs):<3} ({rate:4.0f}%)')

    print()
    print('READING')
    print('  If the strongly suffixing and strongly prefixing controls are')
    print('  detected, the observed null is evidence about the LANGUAGE.')
    print('  If they are not, the observed null is evidence about the METHOD,')
    print('  and no conclusion about affixation direction follows either way.')


if __name__ == '__main__':
    main()
