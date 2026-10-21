# Romanization validation (model-assisted; not native-speaker verified)

**Reviewer:** Claude (a language model that reads Bengali but is not a native speaker). Replace or confirm with a native speaker before the paper says "hand-checked".

## 1. Review of the 100 samples (`romanization_handcheck.csv`, `romanization_review.md`)
- Readable and meaning-preserving: **99/100** (one garbled word: সংজ্ঞা -> "songgga").
- Free of any non-natural feature: **17/100**. Main deviations: English loanwords/names romanized from their Bengali spelling (55 rows), word-final conjunct vowel (52), ব-ফলা (27), ক্ষ (17), chandrabindu (8), জ্ঞ (5), হওয়া (4).

## 2. Check against natural typing
Data: `nahidstaq/bangla-transliteration-data` (45,675 social-media comments with natural Banglish and Bengali; 38,320 pairs aligned word-by-word, equal token count). The Bengali side may be machine-derived from the Roman text, and alignment adds a little noise (≈1% junk matches), so treat percentages as approximate.

| Bengali | ours (rule-based) | most typed spellings |
|---|---|---|
| জন্য (n=1737) | jony | jonno 85%, jnno 6% |
| ভালো (n=2436) | bhalo | valo 80%, vlo 11%, bhalo 2% |
| ভাই (n=7531) | bhai | vai 78%, bhai 6% |
| একটি (n=443) | ekoti | ekti 89% |
| ক্ষতি (n=32) | kkhoti | khoti 81% |
| স্বপ্ন (n=3) | sbopn | shopno 67%, sopno 33% |
| তথ্য (n=26) | tothy | tottho 38%, totto 15% |
| হওয়া (n=61) | hooya | howa 54% |
| ইমেইল (n=141) | imeil | **email 96%** (kept in Latin) |
| ইন্ডিয়া (n=14) | indiya | **india 100%** |
| সুন্দর / খুব / অনেক / কিন্তু / সম্পর্কে | same as ours | 64-79% typed identically |

Overall, the rule-based spelling equals the typed spelling for **44%** of tokens (words seen >= 5 times, 329,923 tokens). It is a readable but systematically different orthography: it misses ভ->v, final-conjunct doubling and Latin retention of English words, all of which my first-pass review missed or understated (ভ->v was missed entirely).

## 3. Second variant: `roman_nat`
`bn_roman2.py`: dominant typed spelling per Bengali word (lookup of 12,694 word types seen >= 2 times) with tuned rules as fallback. Held-out evaluation on unseen word types: character error rate vs typed form 0.318 -> 0.300 (modest; the gain comes from the lookup). Lookup covers 67-78% of tokens of our test sets. Limits: dominant form only (no spelling variation), social-media domain, abbreviations such as "kmn"/"aci" are copied from typing habits.

## 4. Does the script-gap result depend on the romanizer? (Jev, test, rot0)
| task | native | rule-based | natural-style |
|---|---|---|---|
| XNLI-bn acc | 0.751 | 0.572 | 0.584 |
| MASSIVE acc | 0.757 | 0.481 | 0.526 |
| SentNoB macro-F1 | 0.623 | 0.527 | 0.536 |
| SIB-200 acc | 0.897 | 0.725 | 0.706 |

The large native-vs-romanized drop holds under both variants (largest difference between variants: 4.5 points on MASSIVE). Open models have **not** been run on `roman_nat` yet.

## 5. Bengali option labels (`LABELS_BN` in `tasks/bengali.py`)
Sentiment (নিরপেক্ষ/ইতিবাচক/নেতিবাচক) and the seven SIB-200 topics are standard terms. The two NLI labels (অন্তর্ভুক্তি, বিরোধিতা) are the least certain; an alternative wording (নিহিত, বিরোধ) gives the same Jev accuracy (0.761 vs 0.757, English-label baseline 0.751), so the finding does not hinge on that choice. Native-speaker confirmation still wanted.

## 6. User-written Banglish (`banglish_gold_completed.csv`, 100 sentences, one typist, 2026-10-14)
This replaces the model-assisted review above as the reference. One person's writing, so it shows what a native speaker does, not what all speakers do (e.g. this typist writes ভ as "bh": 30 times vs 7 word-initial "v", unlike the "v" majority in the social-media corpus).

**Fidelity of our romanizers to this typist** (100 sentences):
| | token exact match (aligned sentences) | character error rate |
|---|---|---|
| rule-based (`roman`) | 46.1% | 0.323 |
| natural-style (`roman_nat`) | 55.7% | 0.292 |

**Code-mixing, which neither romanizer produces.** Roughly 15% of this typist's words are English where a transliteration of the Bengali word would otherwise appear (use, information, travel, maximum, level, change, standard, government, preparation ...), and 82 of 100 sentences contain at least one. This is substitution, not just loanword spelling. Count is approximate (English wordlist match, with Bengali look-alikes such as ache/kora/eta/boro removed by hand; still includes about a dozen proper nouns).

**End-to-end on the 40 whole-text items** (SentNoB 20 + MASSIVE 20; the other 60 sentences are single sentences cut from longer inputs and cannot be scored). Jev accuracy on the same items:
| | native | rule-based | natural-style | user's Banglish |
|---|---|---|---|---|
| all 40 | 0.675 | 0.650 | 0.575 | 0.650 |
| MASSIVE (20) | 0.70 | 0.65 | 0.55 | 0.75 |
| SentNoB (20) | 0.65 | 0.65 | 0.60 | 0.55 |
Standard error at n=20 is about 10 points, so none of these differences is meaningful. What can be said: with the user's Banglish, 3 of the 27 native-correct items became wrong, far fewer than the 25-point drops on the full synthetic test sets. That is a hint, not evidence, that synthetic romanization may overstate the gap for code-mixed, human-written Banglish. Testing it needs a larger human-written set.

## 7. [SUPERSEDED by section 8] First 160 whole-text items (2026-10-17)
Items: 80 SentNoB + 80 MASSIVE test items romanized by the same typist (files 1 and 2). Jev accuracy on the same items, paired differences with 95% bootstrap CIs:

| | native | rule-based | natural-style | user's Banglish |
|---|---|---|---|---|
| MASSIVE (80) | 0.788 | 0.488 | 0.525 | 0.700 |
| SentNoB (80) | 0.688 | 0.538 | 0.538 | 0.575 |
| pooled (160) | 0.738 | 0.512 | 0.531 | 0.637 |

| comparison (pooled, n=160) | difference | 95% CI |
|---|---|---|
| user's Banglish - native | -0.100 | [-0.163, -0.037] |
| rule-based - native | -0.225 | [-0.300, -0.144] |
| natural-style - native | -0.206 | [-0.281, -0.131] |
| user's Banglish - rule-based | +0.125 | [+0.050, +0.200] |

Per task: MASSIVE human - native -0.087 [-0.175, 0.000] vs rule-based -0.300 [-0.425, -0.188] (human minus rule-based +0.212 [+0.100, +0.325]); SentNoB human - native -0.113 [-0.200, -0.037] vs rule-based -0.150 [-0.250, -0.050] (difference between the two romanizations not significant).

**Reading.** Romanization costs Jev accuracy on real human Banglish, but about half as much as on the synthetic versions pooled, and on MASSIVE about a third (-9 vs -30 points). The natural-style variant did not close the difference. Exploratory split (not preregistered): MASSIVE items where the typist kept or substituted an English word lose 2 points (0.818 -> 0.795) vs 17 points on items with none (0.750 -> 0.583); the SentNoB split is inconsistent (n=29/51). Caveats: one typist; SentNoB items were screened to exclude abusive/political text; MASSIVE and SentNoB only (XNLI-bn pairs are in file 3, not yet written); only Jev has been run on these items.


## 8. All human-written items: 882 whole-text items (2026-10-17) - CORRECTS section 7
Items: SentNoB 327, MASSIVE 497, XNLI-bn 58 pairs; Jev accuracy on the same items, paired 95% bootstrap CIs.

| | n | native | rule-based | natural-style | user's Banglish |
|---|---|---|---|---|---|
| MASSIVE | 497 | 0.767 | 0.503 | 0.551 | 0.553 |
| SentNoB | 327 | 0.645 | 0.557 | 0.535 | 0.544 |
| XNLI-bn | 58 | 0.724 | 0.534 | 0.621 | 0.517 |
| all | 882 | 0.719 | 0.525 | 0.550 | 0.548 |

Differences from native (pooled): user's Banglish -0.171 [-0.202, -0.138]; rule-based -0.194 [-0.230, -0.159]; natural-style -0.169 [-0.202, -0.138]; user minus rule-based +0.023 [-0.003, +0.046].

**The section 7 conclusion (human gap about half the synthetic gap) does not hold at this sample size.** With 882 items the human-written and synthetic romanizations produce about the same loss for Jev (-17 vs -17 to -19 points).

Why the first 160 looked different: results by file.
| | n | native | rule | natural | user |
|---|---|---|---|---|---|
| MASSIVE, files 1-2 (hand-picked) | 80 | 0.788 | 0.488 | 0.525 | 0.700 |
| MASSIVE, file 3 (random, screened) | 417 | 0.763 | 0.506 | 0.556 | 0.525 |
| SentNoB, files 1-2 | 80 | 0.688 | 0.538 | 0.538 | 0.575 |
| SentNoB, file 3 | 247 | 0.632 | 0.563 | 0.534 | 0.534 |

Two things differ between files and cannot be separated here:
1. *Item selection.* I removed garbled machine translations by hand from files 1-2 (the 75 MASSIVE candidates were cut to 60).
2. *Typing style changed sharply.* Items containing an English word: MASSIVE 80% (file 1), 40% (file 2), 11% (file 3); English words per word 22% / 11% / 2%; sentences starting with a capital 100% / 100% / 3%; character error rate to the natural-style romanizer 0.30 / 0.18 / 0.09.

**Provenance question (open).** File 3's text is far closer to our rule-based romanizer than files 1-2 are: character error rate 0.047 vs 0.279 and 0.176, and 28.7% of rows are identical to the rule-based output vs 0% and 2.5%. Short simple sentences match by chance for any phonetic scheme, so this does not show that file 3 was derived from a tool, but it means file 3 may not be independent of our romanizer. Until the user says how file 3 was produced, treat it as unverified and report files 1-2 (hand-written, code-mixed) and file 3 separately.

Exploratory (not preregistered), pooled MASSIVE + SentNoB: with an English word in the user's text, MASSIVE accuracy is native 0.824 / rule 0.624 / user 0.765 (n=85); with none, 0.755 / 0.478 / 0.510 (n=412). English words in the romanized text appear to protect Jev, which is mostly English-trained; where there are none, the synthetic gap is a fair estimate of the human one.


## 9. Provenance resolved (2026-10-20) - CORRECTS the framing of section 8
The author confirmed: files 1-2 (220 rows) were **written by hand**; file 3 (780 rows) was **produced with a transliteration tool and reviewed by the author**. The three romanization kinds are therefore:
(a) rule-based and (b) natural-style synthetic (ours), (c) hand-written Banglish (files 1-2), (d) tool-assisted, human-reviewed Banglish (file 3).
Section 8 pooled (c) and (d) as "human" and concluded the human gap equals the synthetic gap; that was wrong for hand-written text. The 160-item result of section 7 stands as a result for **hand-written** Banglish, with its limits (one author, 160 items, hand-screened items).

Paired accuracy difference, user's Banglish minus rule-based romanization (positive = easier), tasks pooled, 95% bootstrap CI over items:
| model | hand-written, n=160 | tool-assisted + reviewed, n=722 |
|---|---|---|
| Jev | +0.125 [+0.050, +0.200] | +0.000 [-0.022, +0.024] |
| d3-mini | +0.094 [+0.031, +0.163] | -0.006 [-0.029, +0.017] |
| d3-nano | +0.156 [+0.081, +0.231] | +0.024 [+0.000, +0.046] |
| d3-lite | +0.212 [+0.144, +0.287] | +0.044 [+0.025, +0.068] |
| d3-edge | +0.188 [+0.119, +0.256] | +0.057 [+0.035, +0.078] |
| Gemma-4-E4B | +0.125 [+0.069, +0.194] | +0.012 [-0.007, +0.032] |
| Laya-multilingual | +0.094 [+0.050, +0.144] | +0.033 [+0.017, +0.051] |
| Julia-1 (near chance) | -0.062 [-0.175, +0.062] | -0.046 [-0.082, -0.007] |

**Supported statement:** hand-written, code-mixed Banglish is easier for seven of eight models than our rule-based romanization, by 9 to 21 points; a tool-assisted romanization reviewed by the author behaves like the synthetic ones (about 0 to 6 points easier). Limits: the eight models share the same items, so these are not eight independent confirmations; one author wrote the Banglish; 160 items; tasks SentNoB and MASSIVE (XNLI-bn pairs only exist in the tool-assisted file).
**For the paper:** report the synthetic gap as a stress test, report hand-written Banglish as the realistic condition on a small sample, and describe file 3 as tool-assisted with the tool named and the review procedure stated (open: which tool, how many rows were edited).

## 10. All three files hand-written; spelling-correction control (2026-10-21) - current reference, supersedes sections 7-9 for the final numbers
The author reports that all three files (975 rows requested; 970 returned) were reviewed and handwritten. File 3 was rewritten between 2026-10-17 and 2026-10-21 (773 of 775 rows changed; style now matches files 1-2: 99% capitalised, 37% of sentences contain an English word, character error rate to our rule-based romanizer 0.127, 4% identical rows). Five rows (ids 244-248) were removed. The earlier tool-assisted draft of file 3 and its results are archived in `analysis/archive/` and are not used. The author also corrected spellings in 81 of 935 Bengali sentences before writing the Banglish, so items are matched to the dataset by their original text and a corrected-text control is included.

Jev, 877 whole-text items (SentNoB 325, MASSIVE 494, XNLI-bn pairs 58), accuracy and paired 95% bootstrap CIs over items:
| | SentNoB | MASSIVE | XNLI-bn | all |
|---|---|---|---|---|
| native (original text) | 0.646 | 0.765 | 0.724 | 0.718 |
| native, corrected text | 0.652 | 0.765 | 0.724 | 0.721 |
| rule-based, corrected text | 0.563 | 0.502 | 0.534 | 0.527 |
| natural-style, corrected text | 0.538 | 0.555 | 0.603 | 0.552 |
| author's Banglish | 0.563 | 0.638 | 0.621 | 0.609 |

| comparison | all | SentNoB | MASSIVE | XNLI-bn |
|---|---|---|---|---|
| corrected - original Bengali | +0.002 [-0.002, +0.007] | +0.006 | 0.000 | 0.000 |
| Banglish - corrected Bengali | -0.112 [-0.141, -0.083] | -0.089 [-0.142, -0.037] | -0.128 [-0.166, -0.089] | -0.103 [-0.224, 0.000] |
| rule-based - corrected | -0.194 [-0.229, -0.160] | -0.089 | -0.263 | -0.190 |
| natural-style - corrected | -0.169 [-0.202, -0.136] | -0.114 | -0.211 | -0.121 |
| Banglish - rule-based | +0.082 [+0.054, +0.112] | 0.000 [-0.049, +0.049] | +0.136 [+0.097, +0.174] | +0.086 [+0.017, +0.172] |
| Banglish - natural-style | +0.057 [+0.030, +0.087] | +0.025 [-0.025, +0.077] | +0.083 [+0.047, +0.119] | +0.017 [-0.086, +0.121] |

**Reading.** (1) Correcting spellings does not change Jev's accuracy, so it is not a confound. (2) Hand-written Banglish costs Jev about 11 points. (3) Our synthetic romanizations overstate that cost by about 6-8 points pooled: by 14 (rule-based) or 8 (natural-style) on MASSIVE, about 9 on XNLI-bn (58 pairs, wide CI), and not at all on SentNoB. (4) The earlier conclusions in sections 7 (Banglish gap half the synthetic gap) and 8 (equal) were each artefacts of sample size, hand-screening and file provenance; the pooled estimate above is the one to cite. Caveats: one author; SentNoB items were screened to exclude abusive/political text; open-model results pending (Kaggle round 2).

## 11. All models on the hand-written Banglish (Kaggle round 2, 2026-10-21)
877 whole-text items (SentNoB 325, MASSIVE 494, XNLI-bn pairs 58); every model answered every item except Julia-1 (MASSIVE needs more than 20 options, so 383 items). Pooled accuracy is item-weighted, so MASSIVE (56% of items) dominates. Paired 95% bootstrap CIs over items.

| model | corrected Bengali | rule-based | natural-style | author's Banglish | Banglish - corrected | Banglish - rule-based |
|---|---|---|---|---|---|---|
| Jev | 0.721 | 0.527 | 0.552 | 0.609 | -0.112 [-0.141, -0.082] | +0.082 [+0.051, +0.111] |
| d3-flash (4-bit) | 0.706 | 0.412 | 0.457 | 0.547 | -0.158 [-0.193, -0.127] | +0.136 [+0.107, +0.168] |
| Gemma-4-E4B | 0.655 | 0.462 | 0.513 | 0.576 | -0.079 [-0.107, -0.051] | +0.114 [+0.088, +0.143] |
| d3-mini | 0.705 | 0.414 | 0.442 | 0.521 | -0.184 [-0.220, -0.149] | +0.107 [+0.080, +0.136] |
| d3-nano | 0.626 | 0.299 | 0.332 | 0.440 | -0.186 [-0.224, -0.151] | +0.141 [+0.113, +0.174] |
| d3-lite | 0.551 | 0.201 | 0.242 | 0.342 | -0.209 [-0.242, -0.171] | +0.141 [+0.113, +0.172] |
| d3-edge | 0.310 | 0.149 | 0.202 | 0.320 | +0.010 [-0.027, +0.047] | +0.171 [+0.141, +0.197] |
| Laya-multilingual | 0.249 | 0.139 | 0.172 | 0.228 | -0.021 [-0.050, +0.009] | +0.089 [+0.066, +0.112] |
| Julia-1 (383 items, near chance) | 0.428 | 0.441 | 0.418 | 0.384 | -0.044 [-0.107, +0.021] | -0.057 [-0.112, 0.000] |

Spelling correction alone changed no model by more than 0.5 points.

**Findings.** (1) Jev has the highest accuracy on the author's Banglish (0.609); Gemma-4-E4B is second (0.576) and loses the least among models that are above chance natively (-7.9); the open decision models lose 16 to 21 points. (2) For every model above chance, hand-written Banglish is easier than our rule-based romanization (+8 to +17 points, all CIs exclude zero), so the synthetic stress test overstates absolute loss for all of them. (3) The ordering of the eight models above chance is nearly the same under the rule-based romanization and under the Banglish (Kendall tau 0.93, bootstrap 0.86-1.00; the only swap is a tie between d3-flash and d3-mini, 0.412 vs 0.414) and identical under the natural-style romanization (tau 1.00), so the synthetic test is a reasonable proxy for ranking models even though it exaggerates the size of the drop. (4) d3-edge and Laya show about zero loss only because they are near chance on the original text (floor effect); Julia-1 is near chance throughout. Caveats: one author; SentNoB items screened to exclude abusive/political text; XNLI-bn is only 58 pairs; the nine models are scored on the same items, so the agreement between them is not nine independent confirmations; d3-flash is a 4-bit quantised model.

## 12. laya-bangla v2 (algolyzer/laya-bangla, published 2026-10-18; revision v2 = 4c5eb48932)
A Bangla fine-tune of Laya-multilingual (trained on MASSIVE bn train, SIB-200 train, BanglaPSG, BanTH, BanHate, an eLearning sentiment set). Our harness, test splits, English-worded questions:
| | MASSIVE | SIB-200 | SentNoB (macro-F1) | XNLI-bn | Belebele |
|---|---|---|---|---|---|
| native: laya-bangla / Laya-multilingual / Jev | 0.575 / 0.179 / 0.757 | 0.750 / 0.588 / 0.897 | 0.464 / 0.263 / 0.623 | 0.625 / 0.635 / 0.751 | 0.313 / 0.287 / 0.918 |
| romanized (rule-based): laya-bangla | 0.077 | 0.250 | 0.216 | 0.435 | - |
On the hand-written Banglish (877 items): laya-bangla 0.529 on corrected Bengali -> 0.293 on Banglish (-23.6 [-27.3, -20.0]; MASSIVE -34.0), Jev -11.2; Banglish is +10.6 [+8.0, +13.3] easier than the rule-based romanization. The fine-tune improves a great deal on its training tasks but not on XNLI-bn, remains far below Jev on every task, and does not transfer to romanized text for tasks it was trained on only in Bengali script. Rotation range <= 2.8 points (MASSIVE 0.3), much lower than base Laya-multilingual (MASSIVE 8.7).
