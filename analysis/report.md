## RQ1 accuracy / macro-F1, rot0, 95% cluster-bootstrap CI

| task     | variant     | model              |    n |   clusters | metric   |   value |   ci_lo |   ci_hi |   majority |   chance |
|:---------|:------------|:-------------------|-----:|-----------:|:---------|--------:|--------:|--------:|-----------:|---------:|
| Belebele | human_roman | d3-edge            |  900 |        499 | accuracy |   0.341 |   0.31  |   0.372 |    nan     |    0.25  |
| Belebele | human_roman | d3-flash (4/8-bit) |  200 |        172 | accuracy |   0.61  |   0.54  |   0.679 |    nan     |    0.25  |
| Belebele | human_roman | d3-lite            |  900 |        499 | accuracy |   0.371 |   0.341 |   0.4   |    nan     |    0.25  |
| Belebele | human_roman | d3-mini            |  900 |        499 | accuracy |   0.508 |   0.474 |   0.54  |    nan     |    0.25  |
| Belebele | human_roman | d3-nano            |  900 |        499 | accuracy |   0.419 |   0.39  |   0.45  |    nan     |    0.25  |
| Belebele | human_roman | gemma-4-E4B-it     |  900 |        499 | accuracy |   0.588 |   0.556 |   0.618 |    nan     |    0.25  |
| Belebele | human_roman | jev-1.13.0         |  900 |        499 | accuracy |   0.777 |   0.748 |   0.805 |    nan     |    0.25  |
| Belebele | human_roman | julia-1            |  900 |        499 | accuracy |   0.282 |   0.252 |   0.312 |    nan     |    0.25  |
| Belebele | human_roman | laya-bangla v2     |  900 |        499 | accuracy |   0.264 |   0.237 |   0.294 |    nan     |    0.25  |
| Belebele | human_roman | laya-multilingual  |  900 |        499 | accuracy |   0.254 |   0.227 |   0.281 |    nan     |    0.25  |
| Belebele | native      | d3-edge            |  900 |        488 | accuracy |   0.409 |   0.375 |   0.438 |    nan     |    0.25  |
| Belebele | native      | d3-flash (4/8-bit) |  200 |        177 | accuracy |   0.85  |   0.799 |   0.895 |    nan     |    0.25  |
| Belebele | native      | d3-lite            |  900 |        488 | accuracy |   0.577 |   0.545 |   0.609 |    nan     |    0.25  |
| Belebele | native      | d3-mini            |  900 |        488 | accuracy |   0.727 |   0.697 |   0.757 |    nan     |    0.25  |
| Belebele | native      | d3-nano            |  900 |        488 | accuracy |   0.702 |   0.672 |   0.731 |    nan     |    0.25  |
| Belebele | native      | gemma-4-E4B-it     |  900 |        488 | accuracy |   0.773 |   0.746 |   0.801 |    nan     |    0.25  |
| Belebele | native      | jev-1.13.0         |  900 |        488 | accuracy |   0.918 |   0.9   |   0.936 |    nan     |    0.25  |
| Belebele | native      | julia-1            |  881 |        486 | accuracy |   0.287 |   0.257 |   0.317 |    nan     |    0.25  |
| Belebele | native      | laya-bangla v2     |  900 |        488 | accuracy |   0.313 |   0.283 |   0.344 |    nan     |    0.25  |
| Belebele | native      | laya-multilingual  |  900 |        488 | accuracy |   0.287 |   0.259 |   0.316 |    nan     |    0.25  |
| XNLI-bn  | native      | d3-edge            | 1500 |       1077 | accuracy |   0.523 |   0.499 |   0.547 |      0.342 |    0.333 |
| XNLI-bn  | native      | d3-flash (4/8-bit) |  400 |        368 | accuracy |   0.828 |   0.788 |   0.867 |      0.355 |    0.333 |
| XNLI-bn  | native      | d3-lite            | 1500 |       1077 | accuracy |   0.704 |   0.68  |   0.727 |      0.342 |    0.333 |
| XNLI-bn  | native      | d3-mini            | 1500 |       1077 | accuracy |   0.729 |   0.707 |   0.751 |      0.342 |    0.333 |
| XNLI-bn  | native      | d3-nano            | 1500 |       1077 | accuracy |   0.746 |   0.724 |   0.768 |      0.342 |    0.333 |
| XNLI-bn  | native      | gemma-4-E4B-it     | 1500 |       1077 | accuracy |   0.631 |   0.608 |   0.655 |      0.342 |    0.333 |
| XNLI-bn  | native      | jev-1.13.0         | 1500 |       1077 | accuracy |   0.751 |   0.729 |   0.772 |      0.342 |    0.333 |
| XNLI-bn  | native      | julia-1            | 1500 |       1077 | accuracy |   0.382 |   0.359 |   0.406 |      0.342 |    0.333 |
| XNLI-bn  | native      | laya-bangla v2     | 1500 |       1077 | accuracy |   0.625 |   0.598 |   0.651 |      0.342 |    0.333 |
| XNLI-bn  | native      | laya-multilingual  | 1500 |       1077 | accuracy |   0.635 |   0.608 |   0.66  |      0.342 |    0.333 |
| XNLI-bn  | roman       | d3-edge            | 1500 |       1077 | accuracy |   0.445 |   0.419 |   0.469 |      0.342 |    0.333 |
| XNLI-bn  | roman       | d3-flash (4/8-bit) |  400 |        368 | accuracy |   0.598 |   0.551 |   0.642 |      0.355 |    0.333 |
| XNLI-bn  | roman       | d3-lite            | 1500 |       1077 | accuracy |   0.463 |   0.44  |   0.488 |      0.342 |    0.333 |
| XNLI-bn  | roman       | d3-mini            | 1500 |       1077 | accuracy |   0.562 |   0.538 |   0.586 |      0.342 |    0.333 |
| XNLI-bn  | roman       | d3-nano            | 1500 |       1077 | accuracy |   0.497 |   0.472 |   0.52  |      0.342 |    0.333 |
| XNLI-bn  | roman       | gemma-4-E4B-it     | 1500 |       1077 | accuracy |   0.519 |   0.495 |   0.543 |      0.342 |    0.333 |
| XNLI-bn  | roman       | jev-1.13.0         | 1500 |       1077 | accuracy |   0.572 |   0.548 |   0.596 |      0.342 |    0.333 |
| XNLI-bn  | roman       | julia-1            | 1500 |       1077 | accuracy |   0.316 |   0.293 |   0.34  |      0.342 |    0.333 |
| XNLI-bn  | roman       | laya-bangla v2     | 1500 |       1077 | accuracy |   0.435 |   0.409 |   0.46  |      0.342 |    0.333 |
| XNLI-bn  | roman       | laya-multilingual  | 1500 |       1077 | accuracy |   0.383 |   0.36  |   0.406 |      0.342 |    0.333 |
| XNLI-bn  | roman_nat   | jev-1.13.0         | 1500 |       1077 | accuracy |   0.584 |   0.561 |   0.606 |      0.342 |    0.333 |
| MASSIVE  | native      | d3-edge            | 1500 |       1500 | accuracy |   0.243 |   0.221 |   0.264 |      0.071 |    0.017 |
| MASSIVE  | native      | d3-flash (4/8-bit) |  403 |        403 | accuracy |   0.819 |   0.782 |   0.854 |      0.077 |    0.017 |
| MASSIVE  | native      | d3-lite            | 1500 |       1500 | accuracy |   0.624 |   0.602 |   0.647 |      0.071 |    0.017 |
| MASSIVE  | native      | d3-mini            | 1500 |       1500 | accuracy |   0.749 |   0.727 |   0.769 |      0.071 |    0.017 |
| MASSIVE  | native      | d3-nano            | 1500 |       1500 | accuracy |   0.705 |   0.682 |   0.729 |      0.071 |    0.017 |
| MASSIVE  | native      | gemma-4-E4B-it     | 1500 |       1500 | accuracy |   0.689 |   0.664 |   0.713 |      0.071 |    0.017 |
| MASSIVE  | native      | jev-1.13.0         | 1500 |       1500 | accuracy |   0.757 |   0.735 |   0.778 |      0.071 |    0.017 |
| MASSIVE  | native      | laya-bangla v2     | 1500 |       1500 | accuracy |   0.575 |   0.549 |   0.599 |      0.071 |    0.017 |
| MASSIVE  | native      | laya-multilingual  | 1500 |       1500 | accuracy |   0.179 |   0.159 |   0.198 |      0.071 |    0.017 |
| MASSIVE  | roman       | d3-edge            | 1500 |       1500 | accuracy |   0.044 |   0.034 |   0.053 |      0.071 |    0.017 |
| MASSIVE  | roman       | d3-flash (4/8-bit) |  403 |        403 | accuracy |   0.412 |   0.365 |   0.459 |      0.077 |    0.017 |
| MASSIVE  | roman       | d3-lite            | 1500 |       1500 | accuracy |   0.121 |   0.105 |   0.139 |      0.071 |    0.017 |
| MASSIVE  | roman       | d3-mini            | 1500 |       1500 | accuracy |   0.383 |   0.357 |   0.409 |      0.071 |    0.017 |
| MASSIVE  | roman       | d3-nano            | 1500 |       1500 | accuracy |   0.221 |   0.201 |   0.242 |      0.071 |    0.017 |
| MASSIVE  | roman       | gemma-4-E4B-it     | 1500 |       1500 | accuracy |   0.429 |   0.404 |   0.455 |      0.071 |    0.017 |
| MASSIVE  | roman       | jev-1.13.0         | 1500 |       1500 | accuracy |   0.481 |   0.458 |   0.507 |      0.071 |    0.017 |
| MASSIVE  | roman       | laya-bangla v2     | 1500 |       1500 | accuracy |   0.077 |   0.064 |   0.091 |      0.071 |    0.017 |
| MASSIVE  | roman       | laya-multilingual  | 1500 |       1500 | accuracy |   0.045 |   0.034 |   0.055 |      0.071 |    0.017 |
| MASSIVE  | roman_nat   | jev-1.13.0         | 1500 |       1500 | accuracy |   0.526 |   0.5   |   0.551 |      0.071 |    0.017 |
| SentNoB  | native      | d3-edge            | 1586 |       1586 | macro_f1 |   0.472 |   0.447 |   0.497 |      0.412 |    0.333 |
| SentNoB  | native      | d3-flash (4/8-bit) |  405 |        405 | macro_f1 |   0.653 |   0.609 |   0.698 |      0.427 |    0.333 |
| SentNoB  | native      | d3-lite            | 1586 |       1586 | macro_f1 |   0.535 |   0.511 |   0.558 |      0.412 |    0.333 |
| SentNoB  | native      | d3-mini            | 1586 |       1586 | macro_f1 |   0.579 |   0.556 |   0.604 |      0.412 |    0.333 |
| SentNoB  | native      | d3-nano            | 1586 |       1586 | macro_f1 |   0.592 |   0.566 |   0.615 |      0.412 |    0.333 |
| SentNoB  | native      | gemma-4-E4B-it     | 1586 |       1586 | macro_f1 |   0.59  |   0.569 |   0.614 |      0.412 |    0.333 |
| SentNoB  | native      | jev-1.13.0         | 1586 |       1586 | macro_f1 |   0.623 |   0.603 |   0.646 |      0.412 |    0.333 |
| SentNoB  | native      | julia-1            | 1586 |       1586 | macro_f1 |   0.403 |   0.378 |   0.425 |      0.412 |    0.333 |
| SentNoB  | native      | laya-bangla v2     | 1586 |       1586 | macro_f1 |   0.464 |   0.44  |   0.49  |      0.412 |    0.333 |
| SentNoB  | native      | laya-multilingual  | 1586 |       1586 | macro_f1 |   0.263 |   0.245 |   0.284 |      0.412 |    0.333 |
| SentNoB  | roman       | d3-edge            | 1586 |       1586 | macro_f1 |   0.366 |   0.343 |   0.389 |      0.412 |    0.333 |
| SentNoB  | roman       | d3-flash (4/8-bit) |  405 |        405 | macro_f1 |   0.519 |   0.468 |   0.563 |      0.427 |    0.333 |
| SentNoB  | roman       | d3-lite            | 1586 |       1586 | macro_f1 |   0.343 |   0.32  |   0.367 |      0.412 |    0.333 |
| SentNoB  | roman       | d3-mini            | 1586 |       1586 | macro_f1 |   0.486 |   0.462 |   0.508 |      0.412 |    0.333 |
| SentNoB  | roman       | d3-nano            | 1586 |       1586 | macro_f1 |   0.408 |   0.382 |   0.432 |      0.412 |    0.333 |
| SentNoB  | roman       | gemma-4-E4B-it     | 1586 |       1586 | macro_f1 |   0.533 |   0.508 |   0.557 |      0.412 |    0.333 |
| SentNoB  | roman       | jev-1.13.0         | 1586 |       1586 | macro_f1 |   0.527 |   0.503 |   0.551 |      0.412 |    0.333 |
| SentNoB  | roman       | julia-1            | 1586 |       1586 | macro_f1 |   0.299 |   0.278 |   0.319 |      0.412 |    0.333 |
| SentNoB  | roman       | laya-bangla v2     | 1586 |       1586 | macro_f1 |   0.216 |   0.197 |   0.236 |      0.412 |    0.333 |
| SentNoB  | roman       | laya-multilingual  | 1586 |       1586 | macro_f1 |   0.141 |   0.128 |   0.155 |      0.412 |    0.333 |
| SentNoB  | roman_nat   | jev-1.13.0         | 1586 |       1586 | macro_f1 |   0.536 |   0.513 |   0.563 |      0.412 |    0.333 |
| SIB-200  | native      | d3-edge            |  204 |        204 | accuracy |   0.475 |   0.407 |   0.544 |      0.25  |    0.143 |
| SIB-200  | native      | d3-flash (4/8-bit) |  204 |        204 | accuracy |   0.892 |   0.848 |   0.931 |      0.25  |    0.143 |
| SIB-200  | native      | d3-lite            |  204 |        204 | accuracy |   0.76  |   0.701 |   0.819 |      0.25  |    0.143 |
| SIB-200  | native      | d3-mini            |  204 |        204 | accuracy |   0.838 |   0.789 |   0.887 |      0.25  |    0.143 |
| SIB-200  | native      | d3-nano            |  204 |        204 | accuracy |   0.848 |   0.799 |   0.892 |      0.25  |    0.143 |
| SIB-200  | native      | gemma-4-E4B-it     |  204 |        204 | accuracy |   0.853 |   0.804 |   0.902 |      0.25  |    0.143 |
| SIB-200  | native      | jev-1.13.0         |  204 |        204 | accuracy |   0.897 |   0.858 |   0.936 |      0.25  |    0.143 |
| SIB-200  | native      | julia-1            |  204 |        204 | accuracy |   0.52  |   0.456 |   0.588 |      0.25  |    0.143 |
| SIB-200  | native      | laya-bangla v2     |  204 |        204 | accuracy |   0.75  |   0.691 |   0.809 |      0.25  |    0.143 |
| SIB-200  | native      | laya-multilingual  |  204 |        204 | accuracy |   0.588 |   0.524 |   0.652 |      0.25  |    0.143 |
| SIB-200  | roman       | d3-edge            |  204 |        204 | accuracy |   0.235 |   0.181 |   0.294 |      0.25  |    0.143 |
| SIB-200  | roman       | d3-flash (4/8-bit) |  204 |        204 | accuracy |   0.627 |   0.564 |   0.691 |      0.25  |    0.143 |
| SIB-200  | roman       | d3-lite            |  204 |        204 | accuracy |   0.265 |   0.206 |   0.324 |      0.25  |    0.143 |
| SIB-200  | roman       | d3-mini            |  204 |        204 | accuracy |   0.549 |   0.485 |   0.623 |      0.25  |    0.143 |
| SIB-200  | roman       | d3-nano            |  204 |        204 | accuracy |   0.377 |   0.314 |   0.446 |      0.25  |    0.143 |
| SIB-200  | roman       | gemma-4-E4B-it     |  204 |        204 | accuracy |   0.73  |   0.667 |   0.789 |      0.25  |    0.143 |
| SIB-200  | roman       | jev-1.13.0         |  204 |        204 | accuracy |   0.725 |   0.662 |   0.784 |      0.25  |    0.143 |
| SIB-200  | roman       | julia-1            |  204 |        204 | accuracy |   0.284 |   0.225 |   0.348 |      0.25  |    0.143 |
| SIB-200  | roman       | laya-bangla v2     |  204 |        204 | accuracy |   0.25  |   0.191 |   0.309 |      0.25  |    0.143 |
| SIB-200  | roman       | laya-multilingual  |  204 |        204 | accuracy |   0.275 |   0.211 |   0.333 |      0.25  |    0.143 |
| SIB-200  | roman_nat   | jev-1.13.0         |  204 |        204 | accuracy |   0.706 |   0.637 |   0.765 |      0.25  |    0.143 |

## RQ1 paired difference vs Jev (accuracy, cluster CI)

| task     | variant     | model              | vs         |   n_common |   acc_diff |   ci_lo |   ci_hi |
|:---------|:------------|:-------------------|:-----------|-----------:|-----------:|--------:|--------:|
| Belebele | human_roman | d3-edge            | jev-1.13.0 |        900 |     -0.436 |  -0.479 |  -0.395 |
| Belebele | human_roman | d3-flash (4/8-bit) | jev-1.13.0 |        200 |     -0.15  |  -0.208 |  -0.09  |
| Belebele | human_roman | d3-lite            | jev-1.13.0 |        900 |     -0.406 |  -0.442 |  -0.372 |
| Belebele | human_roman | d3-mini            | jev-1.13.0 |        900 |     -0.269 |  -0.307 |  -0.236 |
| Belebele | human_roman | d3-nano            | jev-1.13.0 |        900 |     -0.358 |  -0.394 |  -0.319 |
| Belebele | human_roman | gemma-4-E4B-it     | jev-1.13.0 |        900 |     -0.189 |  -0.22  |  -0.154 |
| Belebele | human_roman | julia-1            | jev-1.13.0 |        900 |     -0.494 |  -0.532 |  -0.452 |
| Belebele | human_roman | laya-bangla v2     | jev-1.13.0 |        900 |     -0.512 |  -0.553 |  -0.478 |
| Belebele | human_roman | laya-multilingual  | jev-1.13.0 |        900 |     -0.522 |  -0.562 |  -0.485 |
| Belebele | native      | d3-edge            | jev-1.13.0 |        900 |     -0.509 |  -0.543 |  -0.469 |
| Belebele | native      | d3-flash (4/8-bit) | jev-1.13.0 |        200 |     -0.07  |  -0.107 |  -0.039 |
| Belebele | native      | d3-lite            | jev-1.13.0 |        900 |     -0.341 |  -0.371 |  -0.308 |
| Belebele | native      | d3-mini            | jev-1.13.0 |        900 |     -0.191 |  -0.22  |  -0.165 |
| Belebele | native      | d3-nano            | jev-1.13.0 |        900 |     -0.216 |  -0.245 |  -0.19  |
| Belebele | native      | gemma-4-E4B-it     | jev-1.13.0 |        900 |     -0.144 |  -0.169 |  -0.119 |
| Belebele | native      | julia-1            | jev-1.13.0 |        881 |     -0.631 |  -0.664 |  -0.594 |
| Belebele | native      | laya-bangla v2     | jev-1.13.0 |        900 |     -0.604 |  -0.64  |  -0.569 |
| Belebele | native      | laya-multilingual  | jev-1.13.0 |        900 |     -0.631 |  -0.663 |  -0.597 |
| XNLI-bn  | native      | d3-edge            | jev-1.13.0 |       1500 |     -0.229 |  -0.255 |  -0.199 |
| XNLI-bn  | native      | d3-flash (4/8-bit) | jev-1.13.0 |        400 |      0.075 |   0.031 |   0.115 |
| XNLI-bn  | native      | d3-lite            | jev-1.13.0 |       1500 |     -0.047 |  -0.072 |  -0.023 |
| XNLI-bn  | native      | d3-mini            | jev-1.13.0 |       1500 |     -0.022 |  -0.047 |   0.002 |
| XNLI-bn  | native      | d3-nano            | jev-1.13.0 |       1500 |     -0.005 |  -0.026 |   0.019 |
| XNLI-bn  | native      | gemma-4-E4B-it     | jev-1.13.0 |       1500 |     -0.12  |  -0.146 |  -0.094 |
| XNLI-bn  | native      | julia-1            | jev-1.13.0 |       1500 |     -0.369 |  -0.401 |  -0.339 |
| XNLI-bn  | native      | laya-bangla v2     | jev-1.13.0 |       1500 |     -0.127 |  -0.154 |  -0.098 |
| XNLI-bn  | native      | laya-multilingual  | jev-1.13.0 |       1500 |     -0.116 |  -0.144 |  -0.089 |
| XNLI-bn  | roman       | d3-edge            | jev-1.13.0 |       1500 |     -0.127 |  -0.162 |  -0.099 |
| XNLI-bn  | roman       | d3-flash (4/8-bit) | jev-1.13.0 |        400 |      0.04  |  -0.016 |   0.093 |
| XNLI-bn  | roman       | d3-lite            | jev-1.13.0 |       1500 |     -0.109 |  -0.14  |  -0.074 |
| XNLI-bn  | roman       | d3-mini            | jev-1.13.0 |       1500 |     -0.01  |  -0.036 |   0.015 |
| XNLI-bn  | roman       | d3-nano            | jev-1.13.0 |       1500 |     -0.075 |  -0.107 |  -0.042 |
| XNLI-bn  | roman       | gemma-4-E4B-it     | jev-1.13.0 |       1500 |     -0.053 |  -0.077 |  -0.03  |
| XNLI-bn  | roman       | julia-1            | jev-1.13.0 |       1500 |     -0.256 |  -0.285 |  -0.226 |
| XNLI-bn  | roman       | laya-bangla v2     | jev-1.13.0 |       1500 |     -0.137 |  -0.173 |  -0.103 |
| XNLI-bn  | roman       | laya-multilingual  | jev-1.13.0 |       1500 |     -0.189 |  -0.226 |  -0.154 |
| MASSIVE  | native      | d3-edge            | jev-1.13.0 |       1500 |     -0.515 |  -0.542 |  -0.487 |
| MASSIVE  | native      | d3-flash (4/8-bit) | jev-1.13.0 |        403 |      0.02  |  -0.012 |   0.052 |
| MASSIVE  | native      | d3-lite            | jev-1.13.0 |       1500 |     -0.133 |  -0.157 |  -0.109 |
| MASSIVE  | native      | d3-mini            | jev-1.13.0 |       1500 |     -0.008 |  -0.029 |   0.011 |
| MASSIVE  | native      | d3-nano            | jev-1.13.0 |       1500 |     -0.053 |  -0.074 |  -0.032 |
| MASSIVE  | native      | gemma-4-E4B-it     | jev-1.13.0 |       1500 |     -0.068 |  -0.087 |  -0.048 |
| MASSIVE  | native      | laya-bangla v2     | jev-1.13.0 |       1500 |     -0.182 |  -0.212 |  -0.153 |
| MASSIVE  | native      | laya-multilingual  | jev-1.13.0 |       1500 |     -0.578 |  -0.603 |  -0.553 |
| MASSIVE  | roman       | d3-edge            | jev-1.13.0 |       1500 |     -0.437 |  -0.463 |  -0.41  |
| MASSIVE  | roman       | d3-flash (4/8-bit) | jev-1.13.0 |        403 |     -0.107 |  -0.149 |  -0.06  |
| MASSIVE  | roman       | d3-lite            | jev-1.13.0 |       1500 |     -0.36  |  -0.388 |  -0.331 |
| MASSIVE  | roman       | d3-mini            | jev-1.13.0 |       1500 |     -0.098 |  -0.124 |  -0.074 |
| MASSIVE  | roman       | d3-nano            | jev-1.13.0 |       1500 |     -0.26  |  -0.287 |  -0.232 |
| MASSIVE  | roman       | gemma-4-E4B-it     | jev-1.13.0 |       1500 |     -0.053 |  -0.08  |  -0.029 |
| MASSIVE  | roman       | laya-bangla v2     | jev-1.13.0 |       1500 |     -0.405 |  -0.43  |  -0.376 |
| MASSIVE  | roman       | laya-multilingual  | jev-1.13.0 |       1500 |     -0.437 |  -0.464 |  -0.408 |
| SentNoB  | native      | d3-edge            | jev-1.13.0 |       1586 |     -0.17  |  -0.199 |  -0.143 |
| SentNoB  | native      | d3-flash (4/8-bit) | jev-1.13.0 |        405 |     -0.02  |  -0.065 |   0.017 |
| SentNoB  | native      | d3-lite            | jev-1.13.0 |       1586 |     -0.116 |  -0.142 |  -0.09  |
| SentNoB  | native      | d3-mini            | jev-1.13.0 |       1586 |     -0.078 |  -0.103 |  -0.051 |
| SentNoB  | native      | d3-nano            | jev-1.13.0 |       1586 |     -0.058 |  -0.082 |  -0.033 |
| SentNoB  | native      | gemma-4-E4B-it     | jev-1.13.0 |       1586 |     -0.02  |  -0.035 |  -0.004 |
| SentNoB  | native      | julia-1            | jev-1.13.0 |       1586 |     -0.25  |  -0.284 |  -0.219 |
| SentNoB  | native      | laya-bangla v2     | jev-1.13.0 |       1586 |     -0.177 |  -0.203 |  -0.152 |
| SentNoB  | native      | laya-multilingual  | jev-1.13.0 |       1586 |     -0.357 |  -0.39  |  -0.325 |
| SentNoB  | roman       | d3-edge            | jev-1.13.0 |       1586 |     -0.157 |  -0.189 |  -0.128 |
| SentNoB  | roman       | d3-flash (4/8-bit) | jev-1.13.0 |        405 |     -0.086 |  -0.133 |  -0.037 |
| SentNoB  | roman       | d3-lite            | jev-1.13.0 |       1586 |     -0.158 |  -0.185 |  -0.129 |
| SentNoB  | roman       | d3-mini            | jev-1.13.0 |       1586 |     -0.071 |  -0.097 |  -0.045 |
| SentNoB  | roman       | d3-nano            | jev-1.13.0 |       1586 |     -0.115 |  -0.14  |  -0.09  |
| SentNoB  | roman       | gemma-4-E4B-it     | jev-1.13.0 |       1586 |      0.003 |  -0.019 |   0.024 |
| SentNoB  | roman       | julia-1            | jev-1.13.0 |       1586 |     -0.177 |  -0.21  |  -0.142 |
| SentNoB  | roman       | laya-bangla v2     | jev-1.13.0 |       1586 |     -0.299 |  -0.336 |  -0.263 |
| SentNoB  | roman       | laya-multilingual  | jev-1.13.0 |       1586 |     -0.34  |  -0.376 |  -0.304 |
| SIB-200  | native      | d3-edge            | jev-1.13.0 |        204 |     -0.422 |  -0.49  |  -0.35  |
| SIB-200  | native      | d3-flash (4/8-bit) | jev-1.13.0 |        204 |     -0.005 |  -0.049 |   0.044 |
| SIB-200  | native      | d3-lite            | jev-1.13.0 |        204 |     -0.137 |  -0.201 |  -0.074 |
| SIB-200  | native      | d3-mini            | jev-1.13.0 |        204 |     -0.059 |  -0.098 |  -0.012 |
| SIB-200  | native      | d3-nano            | jev-1.13.0 |        204 |     -0.049 |  -0.103 |   0     |
| SIB-200  | native      | gemma-4-E4B-it     | jev-1.13.0 |        204 |     -0.044 |  -0.091 |   0     |
| SIB-200  | native      | julia-1            | jev-1.13.0 |        204 |     -0.377 |  -0.451 |  -0.292 |
| SIB-200  | native      | laya-bangla v2     | jev-1.13.0 |        204 |     -0.147 |  -0.211 |  -0.083 |
| SIB-200  | native      | laya-multilingual  | jev-1.13.0 |        204 |     -0.309 |  -0.385 |  -0.245 |
| SIB-200  | roman       | d3-edge            | jev-1.13.0 |        204 |     -0.49  |  -0.571 |  -0.417 |
| SIB-200  | roman       | d3-flash (4/8-bit) | jev-1.13.0 |        204 |     -0.098 |  -0.147 |  -0.034 |
| SIB-200  | roman       | d3-lite            | jev-1.13.0 |        204 |     -0.461 |  -0.534 |  -0.39  |
| SIB-200  | roman       | d3-mini            | jev-1.13.0 |        204 |     -0.176 |  -0.253 |  -0.098 |
| SIB-200  | roman       | d3-nano            | jev-1.13.0 |        204 |     -0.348 |  -0.422 |  -0.267 |
| SIB-200  | roman       | gemma-4-E4B-it     | jev-1.13.0 |        204 |      0.005 |  -0.054 |   0.071 |
| SIB-200  | roman       | julia-1            | jev-1.13.0 |        204 |     -0.441 |  -0.525 |  -0.368 |
| SIB-200  | roman       | laya-bangla v2     | jev-1.13.0 |        204 |     -0.475 |  -0.552 |  -0.402 |
| SIB-200  | roman       | laya-multilingual  | jev-1.13.0 |        204 |     -0.451 |  -0.534 |  -0.377 |

## RQ2 calibration, rot0 (pmax)

| task     | variant     | model              |    n |   acc |   mean_conf |   signed_gap |   ece15 |   ece15_mass |   brier |   nll |   aurc |   acc_at_80 |   acc_at_50 |
|:---------|:------------|:-------------------|-----:|------:|------------:|-------------:|--------:|-------------:|--------:|------:|-------:|------------:|------------:|
| Belebele | human_roman | d3-edge            |  900 | 0.341 |       0.487 |        0.146 |   0.146 |        0.146 |   0.759 | 1.42  |  0.564 |       0.361 |       0.404 |
| Belebele | human_roman | d3-flash (4/8-bit) |  200 | 0.61  |       0.726 |        0.116 |   0.123 |        0.125 |   0.54  | 1.085 |  0.221 |       0.675 |       0.74  |
| Belebele | human_roman | d3-lite            |  900 | 0.371 |       0.539 |        0.168 |   0.168 |        0.168 |   0.774 | 1.466 |  0.533 |       0.389 |       0.431 |
| Belebele | human_roman | d3-mini            |  900 | 0.508 |       0.637 |        0.13  |   0.13  |        0.13  |   0.635 | 1.211 |  0.312 |       0.564 |       0.658 |
| Belebele | human_roman | d3-nano            |  900 | 0.419 |       0.662 |        0.244 |   0.246 |        0.244 |   0.794 | 1.585 |  0.452 |       0.442 |       0.504 |
| Belebele | human_roman | gemma-4-E4B-it     |  900 | 0.589 |       0.9   |        0.311 |   0.311 |        0.311 |   0.689 | 2.375 |  0.225 |       0.665 |       0.78  |
| Belebele | human_roman | jev-1.13.0         |  900 | 0.778 |       0.811 |        0.033 |   0.036 |        0.035 |   0.309 | 0.697 |  0.076 |       0.869 |       0.944 |
| Belebele | human_roman | julia-1            |  900 | 0.282 |       0.678 |        0.396 |   0.396 |        0.396 |   1.011 | 2.313 |  0.689 |       0.286 |       0.304 |
| Belebele | human_roman | laya-bangla v2     |  900 | 0.264 |       0.42  |        0.156 |   0.156 |        0.156 |   0.803 | 1.497 |  0.733 |       0.272 |       0.278 |
| Belebele | human_roman | laya-multilingual  |  900 | 0.254 |       0.49  |        0.235 |   0.235 |        0.235 |   0.895 | 1.908 |  0.744 |       0.253 |       0.249 |
| Belebele | native      | d3-edge            |  900 | 0.409 |       0.589 |        0.18  |   0.186 |        0.183 |   0.761 | 1.489 |  0.474 |       0.443 |       0.493 |
| Belebele | native      | d3-flash (4/8-bit) |  200 | 0.85  |       0.893 |        0.043 |   0.055 |        0.059 |   0.206 | 0.42  |  0.033 |       0.944 |       0.98  |
| Belebele | native      | d3-lite            |  900 | 0.577 |       0.718 |        0.141 |   0.141 |        0.141 |   0.574 | 1.13  |  0.24  |       0.639 |       0.751 |
| Belebele | native      | d3-mini            |  900 | 0.727 |       0.807 |        0.081 |   0.081 |        0.081 |   0.39  | 0.779 |  0.104 |       0.803 |       0.913 |
| Belebele | native      | d3-nano            |  900 | 0.702 |       0.838 |        0.136 |   0.136 |        0.136 |   0.442 | 0.949 |  0.139 |       0.779 |       0.867 |
| Belebele | native      | gemma-4-E4B-it     |  900 | 0.773 |       0.959 |        0.186 |   0.188 |        0.186 |   0.399 | 1.37  |  0.081 |       0.854 |       0.944 |
| Belebele | native      | jev-1.13.0         |  900 | 0.917 |       0.896 |       -0.02  |   0.033 |        0.029 |   0.136 | 0.292 |  0.019 |       0.976 |       0.987 |
| Belebele | native      | julia-1            |  881 | 0.287 |       0.574 |        0.286 |   0.286 |        0.286 |   0.899 | 1.725 |  0.683 |       0.287 |       0.286 |
| Belebele | native      | laya-bangla v2     |  900 | 0.313 |       0.463 |        0.15  |   0.15  |        0.16  |   0.796 | 1.485 |  0.666 |       0.325 |       0.353 |
| Belebele | native      | laya-multilingual  |  900 | 0.287 |       0.531 |        0.245 |   0.248 |        0.245 |   0.869 | 1.655 |  0.7   |       0.296 |       0.289 |
| XNLI-bn  | native      | d3-edge            | 1500 | 0.523 |       0.699 |        0.177 |   0.178 |        0.177 |   0.634 | 1.093 |  0.355 |       0.558 |       0.636 |
| XNLI-bn  | native      | d3-flash (4/8-bit) |  400 | 0.828 |       0.819 |       -0.009 |   0.04  |        0.046 |   0.261 | 0.467 |  0.066 |       0.884 |       0.965 |
| XNLI-bn  | native      | d3-lite            | 1500 | 0.704 |       0.762 |        0.058 |   0.059 |        0.064 |   0.416 | 0.743 |  0.153 |       0.758 |       0.833 |
| XNLI-bn  | native      | d3-mini            | 1500 | 0.729 |       0.767 |        0.038 |   0.049 |        0.045 |   0.377 | 0.661 |  0.126 |       0.791 |       0.883 |
| XNLI-bn  | native      | d3-nano            | 1500 | 0.746 |       0.813 |        0.067 |   0.069 |        0.068 |   0.352 | 0.621 |  0.103 |       0.815 |       0.913 |
| XNLI-bn  | native      | gemma-4-E4B-it     | 1500 | 0.631 |       0.959 |        0.327 |   0.327 |        0.327 |   0.684 | 2.421 |  0.214 |       0.667 |       0.759 |
| XNLI-bn  | native      | jev-1.13.0         | 1500 | 0.753 |       0.835 |        0.082 |   0.088 |        0.087 |   0.371 | 0.683 |  0.128 |       0.802 |       0.868 |
| XNLI-bn  | native      | julia-1            | 1500 | 0.382 |       0.801 |        0.419 |   0.42  |        0.419 |   0.957 | 2.375 |  0.591 |       0.388 |       0.417 |
| XNLI-bn  | native      | laya-bangla v2     | 1500 | 0.625 |       0.828 |        0.203 |   0.203 |        0.203 |   0.576 | 1.122 |  0.258 |       0.665 |       0.741 |
| XNLI-bn  | native      | laya-multilingual  | 1500 | 0.635 |       0.911 |        0.276 |   0.276 |        0.276 |   0.609 | 1.469 |  0.217 |       0.697 |       0.785 |
| XNLI-bn  | roman       | d3-edge            | 1500 | 0.445 |       0.509 |        0.065 |   0.066 |        0.067 |   0.644 | 1.074 |  0.455 |       0.47  |       0.515 |
| XNLI-bn  | roman       | d3-flash (4/8-bit) |  400 | 0.598 |       0.619 |        0.022 |   0.031 |        0.05  |   0.501 | 0.847 |  0.239 |       0.653 |       0.75  |
| XNLI-bn  | roman       | d3-lite            | 1500 | 0.463 |       0.502 |        0.039 |   0.057 |        0.062 |   0.628 | 1.043 |  0.461 |       0.476 |       0.507 |
| XNLI-bn  | roman       | d3-mini            | 1500 | 0.562 |       0.582 |        0.02  |   0.038 |        0.041 |   0.55  | 0.922 |  0.305 |       0.598 |       0.656 |
| XNLI-bn  | roman       | d3-nano            | 1500 | 0.497 |       0.565 |        0.068 |   0.071 |        0.075 |   0.603 | 1.006 |  0.381 |       0.528 |       0.595 |
| XNLI-bn  | roman       | gemma-4-E4B-it     | 1500 | 0.519 |       0.92  |        0.402 |   0.402 |        0.402 |   0.854 | 2.672 |  0.355 |       0.548 |       0.612 |
| XNLI-bn  | roman       | jev-1.13.0         | 1500 | 0.573 |       0.762 |        0.189 |   0.197 |        0.196 |   0.599 | 1.053 |  0.293 |       0.597 |       0.679 |
| XNLI-bn  | roman       | julia-1            | 1500 | 0.316 |       0.848 |        0.532 |   0.532 |        0.532 |   1.147 | 3.658 |  0.673 |       0.31  |       0.32  |
| XNLI-bn  | roman       | laya-bangla v2     | 1500 | 0.435 |       0.721 |        0.286 |   0.286 |        0.286 |   0.777 | 1.355 |  0.487 |       0.454 |       0.493 |
| XNLI-bn  | roman       | laya-multilingual  | 1500 | 0.383 |       0.851 |        0.469 |   0.469 |        0.469 |   1.029 | 2.62  |  0.609 |       0.396 |       0.395 |
| XNLI-bn  | roman_nat   | jev-1.13.0         | 1500 | 0.585 |       0.773 |        0.188 |   0.192 |        0.188 |   0.59  | 1.061 |  0.282 |       0.612 |       0.677 |
| MASSIVE  | native      | d3-edge            | 1500 | 0.243 |       0.465 |        0.223 |   0.223 |        0.223 |   0.942 | 3.426 |  0.591 |       0.278 |       0.352 |
| MASSIVE  | native      | d3-flash (4/8-bit) |  403 | 0.819 |       0.838 |        0.019 |   0.044 |        0.038 |   0.242 | 0.592 |  0.04  |       0.932 |       0.975 |
| MASSIVE  | native      | d3-lite            | 1500 | 0.624 |       0.666 |        0.042 |   0.048 |        0.048 |   0.507 | 1.467 |  0.154 |       0.721 |       0.857 |
| MASSIVE  | native      | d3-mini            | 1500 | 0.749 |       0.801 |        0.051 |   0.054 |        0.051 |   0.367 | 1.038 |  0.089 |       0.848 |       0.941 |
| MASSIVE  | native      | d3-nano            | 1500 | 0.705 |       0.773 |        0.068 |   0.073 |        0.068 |   0.407 | 1.07  |  0.104 |       0.805 |       0.928 |
| MASSIVE  | native      | gemma-4-E4B-it     | 1500 | 0.689 |       0.939 |        0.249 |   0.249 |        0.249 |   0.546 | 2.758 |  0.136 |       0.781 |       0.892 |
| MASSIVE  | native      | jev-1.13.0         | 1500 | 0.757 |       0.844 |        0.087 |   0.087 |        0.087 |   0.341 | 1.082 |  0.072 |       0.864 |       0.963 |
| MASSIVE  | native      | laya-bangla v2     | 1500 | 0.575 |       0.51  |       -0.065 |   0.071 |        0.07  |   0.557 | 1.61  |  0.215 |       0.675 |       0.817 |
| MASSIVE  | native      | laya-multilingual  | 1500 | 0.179 |       0.415 |        0.236 |   0.236 |        0.236 |   0.994 | 4.264 |  0.636 |       0.22  |       0.315 |
| MASSIVE  | roman       | d3-edge            | 1500 | 0.044 |       0.467 |        0.423 |   0.423 |        0.423 |   1.216 | 5.231 |  0.931 |       0.045 |       0.057 |
| MASSIVE  | roman       | d3-flash (4/8-bit) |  403 | 0.412 |       0.466 |        0.054 |   0.084 |        0.086 |   0.706 | 2.372 |  0.323 |       0.484 |       0.658 |
| MASSIVE  | roman       | d3-lite            | 1500 | 0.121 |       0.393 |        0.272 |   0.272 |        0.272 |   1.051 | 4.283 |  0.765 |       0.141 |       0.181 |
| MASSIVE  | roman       | d3-mini            | 1500 | 0.383 |       0.487 |        0.104 |   0.104 |        0.104 |   0.763 | 2.748 |  0.353 |       0.457 |       0.612 |
| MASSIVE  | roman       | d3-nano            | 1500 | 0.221 |       0.35  |        0.129 |   0.129 |        0.129 |   0.905 | 3.374 |  0.579 |       0.262 |       0.352 |
| MASSIVE  | roman       | gemma-4-E4B-it     | 1500 | 0.429 |       0.825 |        0.397 |   0.397 |        0.397 |   0.919 | 4.461 |  0.327 |       0.505 |       0.669 |
| MASSIVE  | roman       | jev-1.13.0         | 1500 | 0.481 |       0.562 |        0.081 |   0.081 |        0.081 |   0.664 | 2.782 |  0.269 |       0.573 |       0.723 |
| MASSIVE  | roman       | laya-bangla v2     | 1500 | 0.077 |       0.215 |        0.138 |   0.138 |        0.138 |   1.006 | 4.106 |  0.882 |       0.085 |       0.104 |
| MASSIVE  | roman       | laya-multilingual  | 1500 | 0.045 |       0.513 |        0.468 |   0.468 |        0.468 |   1.311 | 7.348 |  0.923 |       0.052 |       0.067 |
| MASSIVE  | roman_nat   | jev-1.13.0         | 1500 | 0.524 |       0.597 |        0.073 |   0.073 |        0.073 |   0.61  | 2.491 |  0.224 |       0.619 |       0.783 |
| SentNoB  | native      | d3-edge            | 1586 | 0.489 |       0.609 |        0.119 |   0.12  |        0.119 |   0.657 | 1.158 |  0.383 |       0.519 |       0.594 |
| SentNoB  | native      | d3-flash (4/8-bit) |  405 | 0.659 |       0.745 |        0.086 |   0.107 |        0.102 |   0.477 | 0.828 |  0.198 |       0.71  |       0.787 |
| SentNoB  | native      | d3-lite            | 1586 | 0.544 |       0.664 |        0.12  |   0.12  |        0.12  |   0.6   | 1.047 |  0.326 |       0.589 |       0.647 |
| SentNoB  | native      | d3-mini            | 1586 | 0.582 |       0.7   |        0.118 |   0.12  |        0.118 |   0.553 | 0.934 |  0.27  |       0.636 |       0.695 |
| SentNoB  | native      | d3-nano            | 1586 | 0.602 |       0.709 |        0.107 |   0.107 |        0.107 |   0.529 | 0.917 |  0.24  |       0.649 |       0.748 |
| SentNoB  | native      | gemma-4-E4B-it     | 1586 | 0.639 |       0.972 |        0.332 |   0.333 |        0.332 |   0.68  | 3.059 |  0.251 |       0.702 |       0.782 |
| SentNoB  | native      | jev-1.13.0         | 1586 | 0.66  |       0.858 |        0.198 |   0.202 |        0.198 |   0.542 | 1.69  |  0.212 |       0.705 |       0.788 |
| SentNoB  | native      | julia-1            | 1586 | 0.409 |       0.853 |        0.444 |   0.444 |        0.444 |   0.987 | 2.883 |  0.516 |       0.418 |       0.449 |
| SentNoB  | native      | laya-bangla v2     | 1586 | 0.482 |       0.821 |        0.339 |   0.339 |        0.339 |   0.817 | 1.63  |  0.464 |       0.503 |       0.536 |
| SentNoB  | native      | laya-multilingual  | 1586 | 0.303 |       0.832 |        0.529 |   0.53  |        0.529 |   1.124 | 2.46  |  0.674 |       0.296 |       0.3   |
| SentNoB  | roman       | d3-edge            | 1586 | 0.413 |       0.53  |        0.117 |   0.117 |        0.117 |   0.697 | 1.179 |  0.507 |       0.445 |       0.477 |
| SentNoB  | roman       | d3-flash (4/8-bit) |  405 | 0.531 |       0.621 |        0.09  |   0.099 |        0.1   |   0.588 | 1.012 |  0.311 |       0.59  |       0.688 |
| SentNoB  | roman       | d3-lite            | 1586 | 0.412 |       0.6   |        0.187 |   0.187 |        0.187 |   0.738 | 1.265 |  0.526 |       0.431 |       0.463 |
| SentNoB  | roman       | d3-mini            | 1586 | 0.499 |       0.593 |        0.094 |   0.094 |        0.094 |   0.634 | 1.084 |  0.377 |       0.541 |       0.598 |
| SentNoB  | roman       | d3-nano            | 1586 | 0.455 |       0.62  |        0.165 |   0.165 |        0.165 |   0.685 | 1.175 |  0.439 |       0.485 |       0.54  |
| SentNoB  | roman       | gemma-4-E4B-it     | 1586 | 0.573 |       0.947 |        0.374 |   0.374 |        0.374 |   0.774 | 2.997 |  0.295 |       0.632 |       0.715 |
| SentNoB  | roman       | jev-1.13.0         | 1586 | 0.567 |       0.728 |        0.161 |   0.161 |        0.161 |   0.59  | 1.324 |  0.289 |       0.614 |       0.699 |
| SentNoB  | roman       | julia-1            | 1586 | 0.393 |       0.849 |        0.456 |   0.456 |        0.456 |   1.014 | 2.866 |  0.577 |       0.404 |       0.427 |
| SentNoB  | roman       | laya-bangla v2     | 1586 | 0.27  |       0.838 |        0.568 |   0.568 |        0.568 |   1.166 | 2.317 |  0.708 |       0.271 |       0.28  |
| SentNoB  | roman       | laya-multilingual  | 1586 | 0.23  |       0.883 |        0.653 |   0.654 |        0.653 |   1.309 | 2.852 |  0.75  |       0.239 |       0.251 |
| SentNoB  | roman_nat   | jev-1.13.0         | 1586 | 0.569 |       0.742 |        0.173 |   0.173 |        0.173 |   0.601 | 1.389 |  0.298 |       0.616 |       0.694 |
| SIB-200  | native      | d3-edge            |  204 | 0.475 |       0.62  |        0.144 |   0.186 |        0.173 |   0.68  | 1.55  |  0.294 |       0.528 |       0.676 |
| SIB-200  | native      | d3-flash (4/8-bit) |  204 | 0.892 |       0.85  |       -0.042 |   0.063 |        0.061 |   0.159 | 0.303 |  0.021 |       0.957 |       1     |
| SIB-200  | native      | d3-lite            |  204 | 0.76  |       0.809 |        0.049 |   0.073 |        0.07  |   0.352 | 0.757 |  0.091 |       0.853 |       0.922 |
| SIB-200  | native      | d3-mini            |  204 | 0.838 |       0.828 |       -0.01  |   0.049 |        0.041 |   0.237 | 0.454 |  0.041 |       0.914 |       0.971 |
| SIB-200  | native      | d3-nano            |  204 | 0.848 |       0.847 |       -0.001 |   0.082 |        0.066 |   0.233 | 0.469 |  0.041 |       0.92  |       0.961 |
| SIB-200  | native      | gemma-4-E4B-it     |  204 | 0.853 |       0.974 |        0.121 |   0.121 |        0.121 |   0.236 | 0.681 |  0.022 |       0.951 |       1     |
| SIB-200  | native      | jev-1.13.0         |  204 | 0.897 |       0.912 |        0.015 |   0.05  |        0.033 |   0.141 | 0.33  |  0.019 |       0.975 |       0.99  |
| SIB-200  | native      | julia-1            |  204 | 0.52  |       0.848 |        0.329 |   0.331 |        0.329 |   0.798 | 2.266 |  0.364 |       0.564 |       0.588 |
| SIB-200  | native      | laya-bangla v2     |  204 | 0.75  |       0.811 |        0.061 |   0.069 |        0.078 |   0.37  | 0.787 |  0.125 |       0.816 |       0.912 |
| SIB-200  | native      | laya-multilingual  |  204 | 0.588 |       0.872 |        0.284 |   0.29  |        0.284 |   0.673 | 1.736 |  0.23  |       0.62  |       0.765 |
| SIB-200  | roman       | d3-edge            |  204 | 0.235 |       0.455 |        0.22  |   0.22  |        0.22  |   0.907 | 2.16  |  0.631 |       0.264 |       0.304 |
| SIB-200  | roman       | d3-flash (4/8-bit) |  204 | 0.627 |       0.639 |        0.012 |   0.071 |        0.089 |   0.534 | 1.194 |  0.189 |       0.712 |       0.804 |
| SIB-200  | roman       | d3-lite            |  204 | 0.265 |       0.491 |        0.226 |   0.226 |        0.226 |   0.897 | 2.176 |  0.576 |       0.307 |       0.402 |
| SIB-200  | roman       | d3-mini            |  204 | 0.549 |       0.645 |        0.096 |   0.14  |        0.137 |   0.622 | 1.413 |  0.27  |       0.577 |       0.706 |
| SIB-200  | roman       | d3-nano            |  204 | 0.377 |       0.559 |        0.182 |   0.182 |        0.2   |   0.793 | 1.854 |  0.452 |       0.417 |       0.51  |
| SIB-200  | roman       | gemma-4-E4B-it     |  204 | 0.73  |       0.939 |        0.208 |   0.216 |        0.208 |   0.462 | 1.744 |  0.106 |       0.816 |       0.882 |
| SIB-200  | roman       | jev-1.13.0         |  204 | 0.725 |       0.789 |        0.063 |   0.101 |        0.105 |   0.417 | 1.001 |  0.112 |       0.816 |       0.863 |
| SIB-200  | roman       | julia-1            |  204 | 0.284 |       0.857 |        0.573 |   0.574 |        0.573 |   1.234 | 3.841 |  0.635 |       0.301 |       0.343 |
| SIB-200  | roman       | laya-bangla v2     |  204 | 0.25  |       0.52  |        0.27  |   0.27  |        0.27  |   0.916 | 2.098 |  0.635 |       0.27  |       0.314 |
| SIB-200  | roman       | laya-multilingual  |  204 | 0.275 |       0.867 |        0.593 |   0.593 |        0.593 |   1.251 | 4.856 |  0.666 |       0.307 |       0.333 |
| SIB-200  | roman_nat   | jev-1.13.0         |  204 | 0.706 |       0.79  |        0.084 |   0.117 |        0.087 |   0.393 | 0.89  |  0.101 |       0.81  |       0.922 |

## RQ2b temperature scaling (T fitted on native dev)

| task    | model             | test_variant   |     T |   ece15_before |   ece15_after |   brier_before |   brier_after |   nll_before |   nll_after |
|:--------|:------------------|:---------------|------:|---------------:|--------------:|---------------:|--------------:|-------------:|------------:|
| XNLI-bn | d3-edge           | native         | 2.355 |          0.178 |         0.032 |          0.634 |         0.581 |        1.093 |       0.973 |
| XNLI-bn | d3-edge           | roman          | 2.355 |          0.066 |         0.034 |          0.644 |         0.638 |        1.074 |       1.058 |
| XNLI-bn | d3-lite           | native         | 1.539 |          0.059 |         0.045 |          0.416 |         0.412 |        0.743 |       0.718 |
| XNLI-bn | d3-lite           | roman          | 1.539 |          0.057 |         0.034 |          0.628 |         0.624 |        1.043 |       1.035 |
| XNLI-bn | d3-mini           | native         | 1.299 |          0.049 |         0.038 |          0.377 |         0.375 |        0.661 |       0.652 |
| XNLI-bn | d3-mini           | roman          | 1.299 |          0.038 |         0.038 |          0.55  |         0.55  |        0.922 |       0.923 |
| XNLI-bn | d3-nano           | native         | 1.539 |          0.069 |         0.053 |          0.352 |         0.345 |        0.621 |       0.603 |
| XNLI-bn | d3-nano           | roman          | 1.539 |          0.071 |         0.022 |          0.603 |         0.595 |        1.006 |       0.992 |
| XNLI-bn | gemma-4-E4B-it    | native         | 6     |          0.327 |         0.087 |          0.684 |         0.489 |        2.421 |       0.834 |
| XNLI-bn | gemma-4-E4B-it    | roman          | 6     |          0.402 |         0.068 |          0.854 |         0.596 |        2.672 |       1.003 |
| XNLI-bn | jev-1.13.0        | native         | 1.676 |          0.088 |         0.025 |          0.371 |         0.358 |        0.683 |       0.627 |
| XNLI-bn | jev-1.13.0        | roman          | 1.676 |          0.197 |         0.087 |          0.599 |         0.542 |        1.053 |       0.908 |
| XNLI-bn | julia-1           | native         | 6     |          0.42  |         0.098 |          0.957 |         0.671 |        2.375 |       1.104 |
| XNLI-bn | julia-1           | roman          | 6     |          0.532 |         0.203 |          1.147 |         0.748 |        3.658 |       1.246 |
| XNLI-bn | laya-bangla v2    | native         | 2.564 |          0.203 |         0.028 |          0.576 |         0.507 |        1.122 |       0.867 |
| XNLI-bn | laya-bangla v2    | roman          | 2.564 |          0.286 |         0.08  |          0.777 |         0.647 |        1.355 |       1.07  |
| XNLI-bn | laya-multilingual | native         | 3.922 |          0.276 |         0.035 |          0.609 |         0.476 |        1.469 |       0.814 |
| XNLI-bn | laya-multilingual | roman          | 3.922 |          0.469 |         0.186 |          1.029 |         0.736 |        2.62  |       1.212 |
| MASSIVE | d3-edge           | native         | 1.539 |          0.223 |         0.041 |          0.942 |         0.877 |        3.426 |       3.168 |
| MASSIVE | d3-edge           | roman          | 1.539 |          0.423 |         0.191 |          1.216 |         1.035 |        5.231 |       4.387 |
| MASSIVE | d3-lite           | native         | 1.095 |          0.048 |         0.039 |          0.507 |         0.504 |        1.467 |       1.46  |
| MASSIVE | d3-lite           | roman          | 1.095 |          0.272 |         0.225 |          1.051 |         1.02  |        4.283 |       4.138 |
| MASSIVE | d3-mini           | native         | 1.193 |          0.054 |         0.024 |          0.367 |         0.362 |        1.038 |       1.01  |
| MASSIVE | d3-mini           | roman          | 1.193 |          0.104 |         0.033 |          0.763 |         0.748 |        2.748 |       2.656 |
| MASSIVE | d3-nano           | native         | 1.193 |          0.073 |         0.029 |          0.407 |         0.4   |        1.07  |       1.053 |
| MASSIVE | d3-nano           | roman          | 1.193 |          0.129 |         0.063 |          0.905 |         0.885 |        3.374 |       3.281 |
| MASSIVE | gemma-4-E4B-it    | native         | 2.355 |          0.249 |         0.062 |          0.546 |         0.455 |        2.758 |       1.514 |
| MASSIVE | gemma-4-E4B-it    | roman          | 2.355 |          0.397 |         0.103 |          0.919 |         0.73  |        4.461 |       2.621 |
| MASSIVE | jev-1.13.0        | native         | 1.825 |          0.087 |         0.042 |          0.341 |         0.333 |        1.082 |       0.891 |
| MASSIVE | jev-1.13.0        | roman          | 1.825 |          0.081 |         0.1   |          0.664 |         0.674 |        2.782 |       2.335 |
| MASSIVE | laya-bangla v2    | native         | 0.849 |          0.071 |         0.052 |          0.557 |         0.553 |        1.61  |       1.564 |
| MASSIVE | laya-bangla v2    | roman          | 0.849 |          0.138 |         0.201 |          1.006 |         1.04  |        4.106 |       4.28  |
| MASSIVE | laya-multilingual | native         | 2.163 |          0.236 |         0.04  |          0.994 |         0.916 |        4.264 |       3.558 |
| MASSIVE | laya-multilingual | roman          | 2.163 |          0.468 |         0.198 |          1.311 |         1.081 |        7.348 |       4.784 |
| SentNoB | d3-edge           | native         | 2.564 |          0.12  |         0.06  |          0.657 |         0.626 |        1.158 |       1.047 |
| SentNoB | d3-edge           | roman          | 2.564 |          0.117 |         0.031 |          0.697 |         0.659 |        1.179 |       1.092 |
| SentNoB | d3-lite           | native         | 1.986 |          0.12  |         0.035 |          0.6   |         0.574 |        1.047 |       0.967 |
| SentNoB | d3-lite           | roman          | 1.986 |          0.187 |         0.066 |          0.738 |         0.673 |        1.265 |       1.119 |
| SentNoB | d3-mini           | native         | 1.539 |          0.12  |         0.048 |          0.553 |         0.528 |        0.934 |       0.884 |
| SentNoB | d3-mini           | roman          | 1.539 |          0.094 |         0.032 |          0.634 |         0.614 |        1.084 |       1.032 |
| SentNoB | d3-nano           | native         | 1.539 |          0.107 |         0.041 |          0.529 |         0.51  |        0.917 |       0.869 |
| SentNoB | d3-nano           | roman          | 1.539 |          0.165 |         0.077 |          0.685 |         0.647 |        1.175 |       1.087 |
| SentNoB | gemma-4-E4B-it    | native         | 6     |          0.333 |         0.069 |          0.68  |         0.497 |        3.059 |       0.87  |
| SentNoB | gemma-4-E4B-it    | roman          | 6     |          0.374 |         0.075 |          0.774 |         0.554 |        2.997 |       0.949 |
| SentNoB | jev-1.13.0        | native         | 5.062 |          0.202 |         0.073 |          0.542 |         0.485 |        1.69  |       0.848 |
| SentNoB | jev-1.13.0        | roman          | 5.062 |          0.161 |         0.098 |          0.59  |         0.573 |        1.324 |       0.976 |
| SentNoB | julia-1           | native         | 6     |          0.444 |         0.109 |          0.987 |         0.679 |        2.883 |       1.129 |
| SentNoB | julia-1           | roman          | 6     |          0.456 |         0.105 |          1.014 |         0.696 |        2.866 |       1.157 |
| SentNoB | laya-bangla v2    | native         | 4.27  |          0.339 |         0.021 |          0.817 |         0.62  |        1.63  |       1.027 |
| SentNoB | laya-bangla v2    | roman          | 4.27  |          0.568 |         0.236 |          1.166 |         0.734 |        2.317 |       1.187 |
| SentNoB | laya-multilingual | native         | 6     |          0.53  |         0.164 |          1.124 |         0.703 |        2.46  |       1.15  |
| SentNoB | laya-multilingual | roman          | 6     |          0.654 |         0.244 |          1.309 |         0.742 |        2.852 |       1.206 |

## RQ2c confidence-gate transfer (threshold tuned on native dev for 90% accepted accuracy)

| task    | model             | test_variant   |   tau |   dev_target |   coverage |   n_accepted |    n |   accepted_acc |   overall_acc |
|:--------|:------------------|:---------------|------:|-------------:|-----------:|-------------:|-----:|---------------:|--------------:|
| XNLI-bn | d3-lite           | native         | 0.808 |          0.9 |      0.207 |          310 | 1500 |          0.948 |         0.704 |
| XNLI-bn | d3-lite           | roman          | 0.808 |          0.9 |      0.006 |            9 | 1500 |          0.778 |         0.463 |
| XNLI-bn | d3-mini           | native         | 0.763 |          0.9 |      0.43  |          645 | 1500 |          0.907 |         0.729 |
| XNLI-bn | d3-mini           | roman          | 0.763 |          0.9 |      0.073 |          109 | 1500 |          0.862 |         0.562 |
| XNLI-bn | d3-nano           | native         | 0.766 |          0.9 |      0.45  |          675 | 1500 |          0.921 |         0.746 |
| XNLI-bn | d3-nano           | roman          | 0.766 |          0.9 |      0.021 |           31 | 1500 |          0.935 |         0.497 |
| XNLI-bn | gemma-4-E4B-it    | native         | 0.771 |          0.9 |      0.27  |          405 | 1500 |          0.889 |         0.631 |
| XNLI-bn | gemma-4-E4B-it    | roman          | 0.771 |          0.9 |      0.068 |          102 | 1500 |          0.912 |         0.519 |
| XNLI-bn | jev-1.13.0        | native         | 0.805 |          0.9 |      0.359 |          538 | 1500 |          0.89  |         0.753 |
| XNLI-bn | jev-1.13.0        | roman          | 0.805 |          0.9 |      0.173 |          259 | 1500 |          0.857 |         0.573 |
| XNLI-bn | laya-multilingual | native         | 0.783 |          0.9 |      0.173 |          260 | 1500 |          0.858 |         0.635 |
| XNLI-bn | laya-multilingual | roman          | 0.783 |          0.9 |      0.067 |          101 | 1500 |          0.396 |         0.383 |
| MASSIVE | d3-lite           | native         | 0.693 |          0.9 |      0.431 |          646 | 1500 |          0.902 |         0.624 |
| MASSIVE | d3-lite           | roman          | 0.693 |          0.9 |      0.07  |          105 | 1500 |          0.467 |         0.121 |
| MASSIVE | d3-mini           | native         | 0.669 |          0.9 |      0.68  |         1020 | 1500 |          0.901 |         0.749 |
| MASSIVE | d3-mini           | roman          | 0.669 |          0.9 |      0.223 |          335 | 1500 |          0.827 |         0.383 |
| MASSIVE | d3-nano           | native         | 0.675 |          0.9 |      0.617 |          925 | 1500 |          0.886 |         0.705 |
| MASSIVE | d3-nano           | roman          | 0.675 |          0.9 |      0.096 |          144 | 1500 |          0.722 |         0.221 |
| MASSIVE | gemma-4-E4B-it    | native         | 0.844 |          0.9 |      0.51  |          765 | 1500 |          0.888 |         0.689 |
| MASSIVE | gemma-4-E4B-it    | roman          | 0.844 |          0.9 |      0.219 |          329 | 1500 |          0.839 |         0.429 |
| MASSIVE | jev-1.13.0        | native         | 0.588 |          0.9 |      0.691 |         1036 | 1500 |          0.91  |         0.757 |
| MASSIVE | jev-1.13.0        | roman          | 0.588 |          0.9 |      0.227 |          341 | 1500 |          0.883 |         0.481 |
| MASSIVE | laya-bangla v2    | native         | 0.813 |          0.9 |      0.317 |          475 | 1500 |          0.907 |         0.575 |
| MASSIVE | laya-bangla v2    | roman          | 0.813 |          0.9 |      0.008 |           12 | 1500 |          0.167 |         0.077 |
| SentNoB | d3-mini           | native         | 0.842 |          0.9 |      0.055 |           88 | 1586 |          0.943 |         0.582 |
| SentNoB | d3-mini           | roman          | 0.842 |          0.9 |      0.006 |           10 | 1586 |          0.9   |         0.499 |
| SentNoB | d3-nano           | native         | 0.798 |          0.9 |      0.117 |          185 | 1586 |          0.924 |         0.602 |
| SentNoB | d3-nano           | roman          | 0.798 |          0.9 |      0.014 |           22 | 1586 |          0.727 |         0.455 |

## RQ3 script gap (same items, paired cluster CI)

| task                    | model              |    n |   acc_native |   acc_roman |   gap |   ci_lo |   ci_hi |
|:------------------------|:-------------------|-----:|-------------:|------------:|------:|--------:|--------:|
| XNLI-bn                 | d3-edge            | 1500 |        0.523 |       0.445 | 0.078 |   0.051 |   0.107 |
| XNLI-bn                 | d3-flash (4/8-bit) |  400 |        0.828 |       0.598 | 0.23  |   0.179 |   0.282 |
| XNLI-bn                 | d3-lite            | 1500 |        0.704 |       0.463 | 0.241 |   0.209 |   0.27  |
| XNLI-bn                 | d3-mini            | 1500 |        0.729 |       0.562 | 0.167 |   0.14  |   0.194 |
| XNLI-bn                 | d3-nano            | 1500 |        0.746 |       0.497 | 0.249 |   0.222 |   0.276 |
| XNLI-bn                 | gemma-4-E4B-it     | 1500 |        0.631 |       0.519 | 0.113 |   0.092 |   0.134 |
| XNLI-bn                 | jev-1.13.0         | 1500 |        0.751 |       0.572 | 0.179 |   0.154 |   0.203 |
| XNLI-bn                 | julia-1            | 1500 |        0.382 |       0.316 | 0.066 |   0.037 |   0.096 |
| XNLI-bn                 | laya-bangla v2     | 1500 |        0.625 |       0.435 | 0.19  |   0.157 |   0.222 |
| XNLI-bn                 | laya-multilingual  | 1500 |        0.635 |       0.383 | 0.253 |   0.219 |   0.288 |
| MASSIVE                 | d3-edge            | 1500 |        0.243 |       0.044 | 0.199 |   0.178 |   0.219 |
| MASSIVE                 | d3-flash (4/8-bit) |  403 |        0.819 |       0.412 | 0.407 |   0.357 |   0.46  |
| MASSIVE                 | d3-lite            | 1500 |        0.624 |       0.121 | 0.503 |   0.476 |   0.531 |
| MASSIVE                 | d3-mini            | 1500 |        0.749 |       0.383 | 0.366 |   0.336 |   0.393 |
| MASSIVE                 | d3-nano            | 1500 |        0.705 |       0.221 | 0.483 |   0.455 |   0.51  |
| MASSIVE                 | gemma-4-E4B-it     | 1500 |        0.689 |       0.429 | 0.261 |   0.237 |   0.287 |
| MASSIVE                 | jev-1.13.0         | 1500 |        0.757 |       0.481 | 0.276 |   0.252 |   0.303 |
| MASSIVE                 | laya-bangla v2     | 1500 |        0.575 |       0.077 | 0.499 |   0.471 |   0.526 |
| MASSIVE                 | laya-multilingual  | 1500 |        0.179 |       0.045 | 0.135 |   0.113 |   0.154 |
| SentNoB                 | d3-edge            | 1586 |        0.489 |       0.413 | 0.076 |   0.049 |   0.103 |
| SentNoB                 | d3-flash (4/8-bit) |  405 |        0.659 |       0.531 | 0.128 |   0.081 |   0.172 |
| SentNoB                 | d3-lite            | 1586 |        0.544 |       0.412 | 0.131 |   0.104 |   0.157 |
| SentNoB                 | d3-mini            | 1586 |        0.582 |       0.499 | 0.083 |   0.059 |   0.109 |
| SentNoB                 | d3-nano            | 1586 |        0.602 |       0.455 | 0.147 |   0.12  |   0.172 |
| SentNoB                 | gemma-4-E4B-it     | 1586 |        0.639 |       0.573 | 0.066 |   0.046 |   0.084 |
| SentNoB                 | jev-1.13.0         | 1586 |        0.66  |       0.57  | 0.09  |   0.068 |   0.113 |
| SentNoB                 | julia-1            | 1586 |        0.409 |       0.393 | 0.016 |  -0.012 |   0.05  |
| SentNoB                 | laya-bangla v2     | 1586 |        0.482 |       0.27  | 0.212 |   0.182 |   0.239 |
| SentNoB                 | laya-multilingual  | 1586 |        0.303 |       0.23  | 0.073 |   0.054 |   0.089 |
| SIB-200                 | d3-edge            |  204 |        0.475 |       0.235 | 0.24  |   0.147 |   0.319 |
| SIB-200                 | d3-flash (4/8-bit) |  204 |        0.892 |       0.627 | 0.265 |   0.181 |   0.338 |
| SIB-200                 | d3-lite            |  204 |        0.76  |       0.265 | 0.495 |   0.419 |   0.569 |
| SIB-200                 | d3-mini            |  204 |        0.838 |       0.549 | 0.289 |   0.216 |   0.363 |
| SIB-200                 | d3-nano            |  204 |        0.848 |       0.377 | 0.471 |   0.404 |   0.549 |
| SIB-200                 | gemma-4-E4B-it     |  204 |        0.853 |       0.73  | 0.123 |   0.066 |   0.181 |
| SIB-200                 | jev-1.13.0         |  204 |        0.897 |       0.725 | 0.172 |   0.103 |   0.24  |
| SIB-200                 | julia-1            |  204 |        0.52  |       0.284 | 0.235 |   0.164 |   0.309 |
| SIB-200                 | laya-bangla v2     |  204 |        0.75  |       0.25  | 0.5   |   0.431 |   0.578 |
| SIB-200                 | laya-multilingual  |  204 |        0.588 |       0.275 | 0.314 |   0.235 |   0.402 |
| Belebele (human roman.) | d3-edge            |  900 |        0.408 |       0.341 | 0.067 | nan     | nan     |
| Belebele (human roman.) | d3-flash (4/8-bit) |  200 |        0.85  |       0.61  | 0.24  | nan     | nan     |
| Belebele (human roman.) | d3-lite            |  900 |        0.576 |       0.371 | 0.204 | nan     | nan     |
| Belebele (human roman.) | d3-mini            |  900 |        0.726 |       0.508 | 0.218 | nan     | nan     |
| Belebele (human roman.) | d3-nano            |  900 |        0.701 |       0.418 | 0.283 | nan     | nan     |
| Belebele (human roman.) | gemma-4-E4B-it     |  900 |        0.773 |       0.588 | 0.186 | nan     | nan     |
| Belebele (human roman.) | jev-1.13.0         |  900 |        0.917 |       0.777 | 0.14  | nan     | nan     |
| Belebele (human roman.) | julia-1            |  881 |        0.286 |       0.282 | 0.004 | nan     | nan     |
| Belebele (human roman.) | laya-bangla v2     |  900 |        0.313 |       0.263 | 0.05  | nan     | nan     |
| Belebele (human roman.) | laya-multilingual  |  900 |        0.286 |       0.253 | 0.032 | nan     | nan     |

## RQ4 rotation

| task     | model             |    n |   acc_rot0 |   acc_rot1 |   acc_rot2 |   range |   acc_mean_of_rotations |   acc_rotation_averaged |   same_answer_all_rotations |
|:---------|:------------------|-----:|-----------:|-----------:|-----------:|--------:|------------------------:|------------------------:|----------------------------:|
| Belebele | d3-edge           | 1800 |      0.375 |      0.377 |      0.378 |   0.003 |                   0.377 |                   0.378 |                       0.751 |
| Belebele | d3-lite           | 1800 |      0.474 |      0.463 |      0.462 |   0.012 |                   0.466 |                   0.468 |                       0.815 |
| Belebele | d3-nano           | 1800 |      0.561 |      0.561 |      0.571 |   0.011 |                   0.564 |                   0.572 |                       0.821 |
| Belebele | gemma-4-E4B-it    | 1800 |      0.681 |      0.693 |      0.679 |   0.014 |                   0.684 |                   0.698 |                       0.739 |
| Belebele | jev-1.13.0        | 1800 |      0.847 |      0.856 |      0.855 |   0.009 |                   0.853 |                   0.854 |                       0.927 |
| Belebele | julia-1           | 1781 |      0.285 |      0.291 |      0.303 |   0.018 |                   0.293 |                   0.303 |                       0.309 |
| Belebele | laya-bangla v2    | 1800 |      0.289 |      0.27  |      0.268 |   0.021 |                   0.276 |                   0.284 |                       0.284 |
| Belebele | laya-multilingual | 1800 |      0.271 |      0.262 |      0.273 |   0.011 |                   0.268 |                   0.278 |                       0.153 |
| XNLI-bn  | d3-edge           | 1500 |      0.523 |      0.509 |      0.528 |   0.019 |                   0.52  |                   0.519 |                       0.919 |
| XNLI-bn  | d3-lite           | 1500 |      0.704 |      0.705 |      0.711 |   0.007 |                   0.707 |                   0.705 |                       0.955 |
| XNLI-bn  | d3-nano           | 1500 |      0.746 |      0.744 |      0.751 |   0.007 |                   0.747 |                   0.748 |                       0.961 |
| XNLI-bn  | gemma-4-E4B-it    | 1500 |      0.631 |      0.665 |      0.653 |   0.033 |                   0.65  |                   0.655 |                       0.861 |
| XNLI-bn  | jev-1.13.0        | 1500 |      0.751 |      0.751 |      0.755 |   0.005 |                   0.752 |                   0.751 |                       0.967 |
| XNLI-bn  | julia-1           | 1500 |      0.382 |      0.363 |      0.369 |   0.019 |                   0.372 |                   0.381 |                       0.241 |
| XNLI-bn  | laya-bangla v2    | 1500 |      0.625 |      0.634 |      0.622 |   0.012 |                   0.627 |                   0.627 |                       0.893 |
| XNLI-bn  | laya-multilingual | 1500 |      0.635 |      0.635 |      0.635 |   0.001 |                   0.635 |                   0.638 |                       0.905 |
| MASSIVE  | d3-edge           | 1500 |      0.243 |      0.27  |      0.237 |   0.033 |                   0.25  |                   0.262 |                       0.487 |
| MASSIVE  | d3-lite           | 1500 |      0.624 |      0.625 |      0.621 |   0.005 |                   0.623 |                   0.633 |                       0.798 |
| MASSIVE  | d3-nano           | 1500 |      0.705 |      0.707 |      0.716 |   0.011 |                   0.709 |                   0.713 |                       0.845 |
| MASSIVE  | gemma-4-E4B-it    | 1500 |      0.689 |      0.646 |      0.669 |   0.043 |                   0.668 |                   0.686 |                       0.705 |
| MASSIVE  | jev-1.13.0        | 1500 |      0.757 |      0.765 |      0.774 |   0.017 |                   0.766 |                   0.763 |                       0.889 |
| MASSIVE  | laya-bangla v2    | 1500 |      0.575 |      0.572 |      0.575 |   0.003 |                   0.574 |                   0.593 |                       0.663 |
| MASSIVE  | laya-multilingual | 1500 |      0.179 |      0.104 |      0.092 |   0.087 |                   0.125 |                   0.153 |                       0.293 |
| SentNoB  | d3-edge           | 1586 |      0.489 |      0.486 |      0.5   |   0.014 |                   0.492 |                   0.492 |                       0.902 |
| SentNoB  | d3-lite           | 1586 |      0.544 |      0.555 |      0.552 |   0.012 |                   0.55  |                   0.554 |                       0.921 |
| SentNoB  | d3-nano           | 1586 |      0.602 |      0.606 |      0.605 |   0.004 |                   0.604 |                   0.603 |                       0.954 |
| SentNoB  | gemma-4-E4B-it    | 1586 |      0.639 |      0.639 |      0.64  |   0.001 |                   0.64  |                   0.638 |                       0.944 |
| SentNoB  | jev-1.13.0        | 1586 |      0.66  |      0.651 |      0.651 |   0.009 |                   0.654 |                   0.655 |                       0.946 |
| SentNoB  | julia-1           | 1586 |      0.409 |      0.327 |      0.301 |   0.108 |                   0.346 |                   0.323 |                       0.449 |
| SentNoB  | laya-bangla v2    | 1586 |      0.482 |      0.454 |      0.46  |   0.028 |                   0.465 |                   0.46  |                       0.877 |
| SentNoB  | laya-multilingual | 1586 |      0.303 |      0.349 |      0.342 |   0.046 |                   0.331 |                   0.325 |                       0.798 |
| SIB-200  | d3-edge           |  204 |      0.475 |      0.451 |      0.495 |   0.044 |                   0.474 |                   0.475 |                       0.833 |
| SIB-200  | d3-lite           |  204 |      0.76  |      0.77  |      0.76  |   0.01  |                   0.763 |                   0.77  |                       0.956 |
| SIB-200  | d3-nano           |  204 |      0.848 |      0.843 |      0.848 |   0.005 |                   0.846 |                   0.848 |                       0.961 |
| SIB-200  | gemma-4-E4B-it    |  204 |      0.853 |      0.858 |      0.858 |   0.005 |                   0.856 |                   0.853 |                       0.931 |
| SIB-200  | jev-1.13.0        |  204 |      0.897 |      0.902 |      0.907 |   0.01  |                   0.902 |                   0.902 |                       0.971 |
| SIB-200  | julia-1           |  204 |      0.52  |      0.525 |      0.549 |   0.029 |                   0.531 |                   0.554 |                       0.735 |
| SIB-200  | laya-bangla v2    |  204 |      0.75  |      0.745 |      0.73  |   0.02  |                   0.742 |                   0.74  |                       0.941 |
| SIB-200  | laya-multilingual |  204 |      0.588 |      0.598 |      0.588 |   0.01  |                   0.592 |                   0.613 |                       0.843 |

## RQ4 pick positions (K<=7)

| task     | model             |   K |   pick_pos0 |   pick_pos1 |   pick_pos2 |   pick_pos3 |   max_abs_pick_minus_gold |   pick_pos4 |   pick_pos5 |   pick_pos6 |
|:---------|:------------------|----:|------------:|------------:|------------:|------------:|--------------------------:|------------:|------------:|------------:|
| Belebele | d3-edge           |   4 |       0.236 |       0.225 |       0.262 |       0.277 |                     0.035 |     nan     |     nan     |     nan     |
| Belebele | d3-lite           |   4 |       0.24  |       0.25  |       0.241 |       0.269 |                     0.026 |     nan     |     nan     |     nan     |
| Belebele | d3-nano           |   4 |       0.241 |       0.25  |       0.251 |       0.259 |                     0.019 |     nan     |     nan     |     nan     |
| Belebele | gemma-4-E4B-it    |   4 |       0.295 |       0.269 |       0.236 |       0.201 |                     0.042 |     nan     |     nan     |     nan     |
| Belebele | jev-1.13.0        |   4 |       0.266 |       0.25  |       0.238 |       0.246 |                     0.007 |     nan     |     nan     |     nan     |
| Belebele | julia-1           |   4 |       0.461 |       0.19  |       0.195 |       0.154 |                     0.2   |     nan     |     nan     |     nan     |
| Belebele | laya-bangla v2    |   4 |       0.128 |       0.26  |       0.351 |       0.261 |                     0.132 |     nan     |     nan     |     nan     |
| Belebele | laya-multilingual |   4 |       0.227 |       0.185 |       0.238 |       0.35  |                     0.108 |     nan     |     nan     |     nan     |
| XNLI-bn  | d3-edge           |   3 |       0.357 |       0.329 |       0.314 |     nan     |                     0.024 |     nan     |     nan     |     nan     |
| XNLI-bn  | d3-lite           |   3 |       0.344 |       0.332 |       0.324 |     nan     |                     0.011 |     nan     |     nan     |     nan     |
| XNLI-bn  | d3-nano           |   3 |       0.343 |       0.328 |       0.329 |     nan     |                     0.009 |     nan     |     nan     |     nan     |
| XNLI-bn  | gemma-4-E4B-it    |   3 |       0.312 |       0.348 |       0.34  |     nan     |                     0.021 |     nan     |     nan     |     nan     |
| XNLI-bn  | jev-1.13.0        |   3 |       0.333 |       0.337 |       0.33  |     nan     |                     0.004 |     nan     |     nan     |     nan     |
| XNLI-bn  | julia-1           |   3 |       0.171 |       0.418 |       0.412 |     nan     |                     0.163 |     nan     |     nan     |     nan     |
| XNLI-bn  | laya-bangla v2    |   3 |       0.322 |       0.336 |       0.342 |     nan     |                     0.011 |     nan     |     nan     |     nan     |
| XNLI-bn  | laya-multilingual |   3 |       0.325 |       0.333 |       0.342 |     nan     |                     0.008 |     nan     |     nan     |     nan     |
| SentNoB  | d3-edge           |   3 |       0.356 |       0.307 |       0.337 |     nan     |                     0.027 |     nan     |     nan     |     nan     |
| SentNoB  | d3-lite           |   3 |       0.355 |       0.335 |       0.31  |     nan     |                     0.023 |     nan     |     nan     |     nan     |
| SentNoB  | d3-nano           |   3 |       0.339 |       0.339 |       0.323 |     nan     |                     0.011 |     nan     |     nan     |     nan     |
| SentNoB  | gemma-4-E4B-it    |   3 |       0.321 |       0.339 |       0.34  |     nan     |                     0.012 |     nan     |     nan     |     nan     |
| SentNoB  | jev-1.13.0        |   3 |       0.326 |       0.347 |       0.327 |     nan     |                     0.013 |     nan     |     nan     |     nan     |
| SentNoB  | julia-1           |   3 |       0.244 |       0.413 |       0.343 |     nan     |                     0.09  |     nan     |     nan     |     nan     |
| SentNoB  | laya-bangla v2    |   3 |       0.323 |       0.344 |       0.332 |     nan     |                     0.011 |     nan     |     nan     |     nan     |
| SentNoB  | laya-multilingual |   3 |       0.368 |       0.351 |       0.281 |     nan     |                     0.052 |     nan     |     nan     |     nan     |
| SIB-200  | d3-edge           |   7 |       0.253 |       0.087 |       0.19  |       0.141 |                     0.085 |       0.064 |       0.203 |       0.064 |
| SIB-200  | d3-lite           |   7 |       0.172 |       0.119 |       0.136 |       0.154 |                     0.023 |       0.119 |       0.173 |       0.127 |
| SIB-200  | d3-nano           |   7 |       0.188 |       0.118 |       0.129 |       0.145 |                     0.02  |       0.126 |       0.168 |       0.126 |
| SIB-200  | gemma-4-E4B-it    |   7 |       0.163 |       0.139 |       0.105 |       0.157 |                     0.01  |       0.121 |       0.173 |       0.142 |
| SIB-200  | jev-1.13.0        |   7 |       0.175 |       0.145 |       0.096 |       0.165 |                     0.016 |       0.118 |       0.172 |       0.129 |
| SIB-200  | julia-1           |   7 |       0.222 |       0.103 |       0.075 |       0.194 |                     0.054 |       0.118 |       0.193 |       0.095 |
| SIB-200  | laya-bangla v2    |   7 |       0.158 |       0.144 |       0.118 |       0.149 |                     0.01  |       0.131 |       0.162 |       0.139 |
| SIB-200  | laya-multilingual |   7 |       0.227 |       0.096 |       0.114 |       0.181 |                     0.059 |       0.075 |       0.214 |       0.092 |

## RQ5 cost / latency

| model              |   median_latency_s |   mean_input_tokens |   items |   usd_per_1k_decisions |
|:-------------------|-------------------:|--------------------:|--------:|-----------------------:|
| d3-edge            |              0.07  |             297.65  |   11380 |                  0     |
| d3-flash (4/8-bit) |              1.707 |             284.565 |    3224 |                  0     |
| d3-lite            |              0.15  |             297.65  |   11380 |                  0     |
| d3-mini            |              1.361 |             315.128 |   11380 |                  0     |
| d3-nano            |              0.347 |             297.65  |   11380 |                  0     |
| gemma-4-E4B-it     |              0.109 |             255.915 |   11380 |                  0     |
| jev-1.13.0         |              0.312 |             566.809 |   16170 |                  0.024 |
| julia-1            |              0.024 |               0     |    8361 |                  0     |
| laya-bangla v2     |              0.03  |             199.121 |   11380 |                  0     |
| laya-multilingual  |              0.029 |             199.121 |   11380 |                  0     |

