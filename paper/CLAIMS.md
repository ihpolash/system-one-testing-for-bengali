# Claim set (every number comes from analysis/tables and analysis/*.json through paper/numbers.tex)

| # | Claim (scoped) | Evidence | Strongest objection |
|---|---|---|---|
| C1 | Jev has the highest point estimate on all five Bengali tasks among the systems run on the full test sets; the closest open systems are d3-nano and d3-mini on XNLI-bn and d3-flash (4-bit, subset). | Tab. main, intervals in appendix | Different pipelines; d3-flash subset; possible contamination |
| C2 | Rule-based romanization lowers every system's accuracy on every task where it was run, by 13.5 to 35.9 points on average. | Tab. main, audit check | Tool-made text; Belebele not romanized |
| C3 | On 1,500 Dakshina sentences, all 12 systems keep their own Bengali-script topic answer more often under native-speaker romanization than under rule-based romanization (3.3 to 12.9 points, every interval excludes zero); native-speaker beats natural-style for 11 of 12; natural-style is close to rule-based (-1.8 to +4.5). | Tab. Dakshina, Fig. 1, released predictions | Agreement is not accuracy; Wikipedia sentences and one topic question; unknown number of annotators |
| C4 | The ordering of systems is almost the same under native-speaker and rule-based romanization (Kendall tau 0.89 over the 11 systems with 1,500 sentences). | Tab. Dakshina | Same sentences for all systems |
| C5 | Open models are overconfident on Bengali; one temperature fitted on a disjoint dev split removes most of it and transfers less fully to rule-based romanized text. | Tab. ECE, Fig. 3-4 | Exploratory; gate results rest on few items |
| C6 | Option-order sensitivity concentrates in the encoder models. | Fig. 5 | Three rotations only |
| C7 | The harness reproduces independent numbers for Jev, Laya-multilingual and laya-bangla. | analysis/RESULTS_AUDIT.md | Only some tasks comparable |

Not claimed: that this is the first Bengali study of any decision model; any statement about accuracy on romanized text typed by people (the Dakshina sentences have no labels); anything about Kev-9B/27B, d3-27B or Microsoft-Decision-1.

Corrections made on the way: an AI-generated Banglish condition used in earlier drafts was removed entirely (it was never hand-written); the natural-style romanizer's lookup corpus contained 4,144 Dakshina sentences and was rebuilt without them.
