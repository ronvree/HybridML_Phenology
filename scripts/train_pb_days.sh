#!/bin/bash

#for SEED in 18 79 5 805 541 299 344 700 831 731
for SEED in 18
do
  python3 -m runs.fit_eval --model_cls LocalChillDaysModel --include_temperature --model_name LocalChillDaysModel_seed${SEED} --seed ${SEED} --locations selection
done
