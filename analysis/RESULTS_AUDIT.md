# Results audit (2026-10-21)

## Checks that passed
| check | result |
|---|---|
| Reproduce a published number | Jev Belebele ben_Beng recomputed from the authors' Zenodo responses 0.9167; our own live re-run 0.918 [0.899, 0.936] |
| Independent measurements of the same models by laya-bangla's authors | base Laya-multilingual: MASSIVE intent 0.179 (theirs 0.18), SIB-200 0.588 (0.57-0.58); laya-bangla v2: SIB-200 0.750 (0.76), SentNoB accuracy 0.482 (0.48-0.49). MASSIVE for laya-bangla differs (0.575 vs 0.81) because they use a two-step scenario-then-intent protocol and we ask one 59-way question |
| Jev run-to-run stability (300 requests resent) | same answer 99% (bnli 100%, MASSIVE 99%, SentNoB 98%); accuracy 0.760 vs 0.763; mean change in top probability 0.012-0.020 |
| Jev sensitivity to question wording (SentNoB, n=1586) | accuracy 0.660 default, 0.647 options only, 0.661 Bengali wording |
| Package drift (Laya 0.4.3/0.4.6 vs 0.4.11) | 6,563 identical requests: same choice 100%, change in top probability 0.0000 |
| Spelling correction as a confound | corrected vs original Bengali: +0.2 points (Jev, [-0.2, +0.7]); at most 0.6 points for any model |
| Unit tests | 38 harness tests + 7 analysis tests pass |
| Statistics | cluster bootstrap by premise/passage; paired comparisons on identical items; completeness guard for unfinished conditions |

## Problems found (and what was done)
- **Laya-multilingual SentNoB is wording-sensitive:** macro-F1 0.263 (default English), 0.321 (options only), 0.376 (Bengali wording); share of "neutral" predictions 83% / 68% / 55%. The conclusion "far below Jev (0.623)" holds under all three; report as a range. Laya-bangla is stable (0.464 / 0.447 / 0.432). Other models were not tested for wording sensitivity (limitation).
- **Three of my own claims were wrong at some point and were corrected:** "Banglish gap is half the synthetic gap" (small sample), "equal" (pooled a tool-assisted file as human), "identical ranking" (it is a near tie, Kendall tau 0.93). Current statements are in `romanization_validation.md` sections 10-11.
- A task-registry unit test failed because local-file tasks had no source name; fixed (documentation only, no effect on numbers).
- A table bug (coincidental cache matches for romanization variants that were never run) was found and fixed; a completeness guard now prevents the same mistake.
- Two Kaggle jobs failed from my own driver mistakes (d3 loading arguments; a duplicated environment variable). No results from failed jobs were used.

## Limitations that remain (state in the paper)
One author wrote all Banglish; SentNoB items screened for abusive text; MASSIVE is 56% of the pooled human-Banglish items; XNLI-bn pairs only 58; XNLI-bn and MASSIVE are translated, not native; SentNoB split is a third-party mirror with unverified provenance; possible training-data contamination in Jev, Gemma and the Qwen-based d3 models is unknown (laya-bangla trained on MASSIVE and SIB-200 train splits); d3-flash is 4-bit quantised and evaluated on a 400-item-per-task subset; d3 (27B) and Kev were not run; Julia-1 cannot answer MASSIVE; latency/cost not benchmarked cleanly; calibration-gate results rest on very few accepted items for some models; many comparisons, no multiplicity correction (descriptive).
