# Results audit (2026-10-21)

## Checks that passed
| check | result |
|---|---|
| Reproduce a published number | Jev Belebele ben_Beng recomputed from the authors' Zenodo responses 0.9167; our own live re-run 0.918 [0.899, 0.936] |
| Independent measurements of the same models by laya-bangla's authors | base Laya-multilingual: MASSIVE intent 0.179 (theirs 0.18), SIB-200 0.588 (0.57-0.58); laya-bangla v2: SIB-200 0.750 (0.76), SentNoB accuracy 0.482 (0.48-0.49). MASSIVE for laya-bangla differs (0.575 vs 0.81) because they use a two-step scenario-then-intent protocol and we ask one 59-way question |
| Jev run-to-run stability (300 requests resent) | same answer 99% (bnli 100%, MASSIVE 99%, SentNoB 98%); accuracy 0.760 vs 0.763; mean change in top probability 0.012-0.020 |
| Jev sensitivity to question wording (SentNoB, n=1586) | accuracy 0.660 default, 0.647 options only, 0.661 Bengali wording |
| Package drift (Laya 0.4.3/0.4.6 vs 0.4.11) | 6,563 identical requests: same choice 100%, change in top probability 0.0000 |
| Unit tests | 38 harness tests + 7 analysis tests pass |
| Statistics | cluster bootstrap by premise/passage; paired comparisons on identical items; completeness guard for unfinished conditions |

## Problems found (and what was done)
- **Laya-multilingual SentNoB is wording-sensitive:** macro-F1 0.263 (default English), 0.321 (options only), 0.376 (Bengali wording); share of "neutral" predictions 83% / 68% / 55%. The conclusion "far below Jev (0.623)" holds under all three; report as a range. Laya-bangla is stable (0.464 / 0.447 / 0.432). Other models were not tested for wording sensitivity (limitation).
- **Claims that were wrong and were corrected:** an earlier AI-generated "Banglish" condition (since removed entirely; see the README) and its conclusions; and a natural-style romanizer whose lookup corpus contained 4,144 Dakshina sentences (rebuilt without them, all natural-style numbers rerun).
- A task-registry unit test failed because local-file tasks had no source name; fixed (documentation only, no effect on numbers).
- A table bug (coincidental cache matches for romanization variants that were never run) was found and fixed; a completeness guard now prevents the same mistake.
- Two Kaggle jobs failed from my own driver mistakes (d3 loading arguments; a duplicated environment variable). No results from failed jobs were used.

## Limitations that remain (state in the paper)
The Dakshina comparison measures agreement with a system's own Bengali answer, not accuracy (the sentences have no labels), on Wikipedia sentences and one topic question; SentNoB is the only native Bengali text of the five tasks and its split is a third-party mirror; XNLI-bn and MASSIVE are translations; possible training-data contamination (laya-bangla trained on MASSIVE and SIB-200 train splits); d3-flash is 4-bit and covers subsets; d3-27B, Kev-9B/27B not run; Julia-1 cannot answer MASSIVE; calibration-gate results rest on few accepted items for some models; many comparisons, no multiplicity correction (descriptive).
