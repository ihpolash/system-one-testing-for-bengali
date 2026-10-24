# Dakshina Bengali sentences

Source: Roark et al., *Processing South Asian Languages Written in the Latin Script: the Dakshina Dataset*, LREC 2020 (arXiv 2007.01176). Licence CC BY-SA 4.0.
10,000 Bengali Wikipedia sentences that native speakers romanized by hand (no transliteration tool); a second set of annotators transcribed them back to Bengali script to validate them.

To rebuild the sentences used here:
```
mkdir -p data/dakshina && cd data/dakshina
curl -sL https://storage.googleapis.com/gresearch/dakshina/dakshina_dataset_v1.0.tar | tar -xf - --include '*/bn/romanized/*'
cd ../.. && python data/make_dakshina.py      # writes data/raw/dakshina_bn.jsonl (8,244 sentences of 6 to 40 words)
```
The experiments use the first 1,500 sentences in hash order (`--limit 1500`; d3-flash, 500). `results/predictions_dakshina.csv.gz` is keyed by the sentence `id` (SHA-256 prefix of the Bengali text).
