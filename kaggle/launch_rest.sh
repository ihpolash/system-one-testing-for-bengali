#!/bin/bash
cd "$(dirname "$0")"
st() { kaggle kernels status "$1" 2>&1 | grep -E "RUNNING|QUEUED" >/dev/null && echo busy || echo free; }
push() { (cd "$1" && kaggle kernels push -p . 2>&1 | grep -c "successfully pushed"); }
for pair in "main_M2_gemma:ipolas/bn-s1-dak2-gemma:ipolas/bn-s1-dak2-cl" "main_M2_flash:ipolas/bn-s1-dak2-flash:ipolas/bn-s1-dak2-kev"; do
  IFS=: read dir id wait_for <<< "$pair"
  until [ "$(st $wait_for)" = free ]; do sleep 240; done
  until [ "$(push $dir)" = 1 ]; do sleep 240; done
  echo "launched $id $(date)"
done
