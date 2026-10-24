#!/bin/bash
# Start the pending Dakshina kernels as GPU slots free up (Kaggle allows 2 batch GPU sessions at once).
cd "$(dirname "$0")"
RUNNING_IDS=""
PENDING="main_M2_b:ipolas/bn-s1-dak2-b main_M2_kev:ipolas/bn-s1-dak2-kev main_M2_cl:ipolas/bn-s1-dak2-cl main_M2_gemma:ipolas/bn-s1-dak2-gemma main_M2_flash:ipolas/bn-s1-dak2-flash"
count_running() { n=0; for id in $RUNNING_IDS; do kaggle kernels status $id 2>&1 | grep -qE "QUEUED|RUNNING" && n=$((n+1)); done; echo $n; }
while [ -n "$PENDING" ]; do
  if [ "$(count_running)" -lt 2 ]; then
    next=${PENDING%% *}; PENDING=${PENDING#"$next"}; PENDING=${PENDING# }
    dir=${next%%:*}; id=${next##*:}
    if (cd $dir && kaggle kernels push -p . 2>&1 | grep -q "successfully pushed"); then echo "launched $id $(date)"; RUNNING_IDS="$RUNNING_IDS $id"; else echo "push failed for $id; will retry"; PENDING="$next $PENDING"; fi
  fi
  sleep 300
done
echo "all launched $(date)"
