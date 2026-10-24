# Released results

| File | Contents |
|---|---|
| `predictions_test_sets.csv.gz` | one row per system, task, spelling, rotation and item: item id, cluster id, gold and predicted label, top-option confidence, and the probability vector for the open systems. For Jev only the top choice and its confidence (the provider's terms do not allow raw responses or probability vectors). |
| `predictions_dakshina.csv.gz` | per sentence (SHA-256 prefix of the Bengali text), system and spelling: the topic answer and its confidence, and the probability vector for the open systems (not Jev). Sentences are not included; see `docs/DAKSHINA.md`. |
| `MANIFEST.sha256` | SHA-256 of every released file, tables and generated LaTeX included (`shasum -a 256 -c results/MANIFEST.sha256`). |

Licences and caveats. Belebele's answer options are Bengali text, so `predictions_test_sets.csv.gz` contains some Belebele text and is shared under CC BY-SA 4.0 (Belebele, SIB-200 and Dakshina are CC BY-SA 4.0). Gold labels of XNLI-bn (CC BY-NC-SA 4.0) and of MASSIVE (CC BY 4.0) appear as labels only. SentNoB's text is not included; the file does list SentNoB item ids, labels and predictions, and the authors' repository states no licence, so its terms are unconfirmed (see Table `prov` in the paper). If that is a concern, delete the `bn_sentnob` rows and rerun `make audit`; only the SentNoB checks will then be skipped.
