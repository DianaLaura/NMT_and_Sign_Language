#! /bin/bash
#copied from https://github.com/bricksdont/sockeye-toy-models/blob/gpu/scripts/train.sh

scripts=`dirname "$0"`

src=$1
trg=$2
data=$3/Extracted_data
base=$scripts/..

mkdir -p $3/models

num_threads=1
model_name=baseline

##################################

OMP_NUM_THREADS=$num_threads python -m sockeye.train \
      -o $3/models/$model_name  \
			-s $data/train.truecased.$src \
			-t $data/train.truecased.$trg \
			-vs $data/dev.truecased.$src \
      -vt $data/dev.truecased.$trg \
      --seed=1 \
      --batch-type=word \
      --batch-size=4096 \
      --checkpoint-frequency=4000 \
      --device-ids=0 \
      --decode-and-evaluate-device-id 0 \
      --embed-dropout=0:0 \
      --encoder=transformer \
      --decoder=transformer \
      --num-layers=6:6 \
      --transformer-model-size=512 \
      --transformer-attention-heads=8 \
      --transformer-feed-forward-num-hidden=2048 \
      --transformer-preprocess=n \
      --transformer-postprocess=dr \
      --transformer-dropout-attention=0.1 \
      --transformer-dropout-relu=0.1 \
      --transformer-dropout-prepost=0.1 \
      --transformer-positional-embedding-type fixed \
      --fill-up=replicate \
      --max-seq-len=100:100 \
      --label-smoothing 0.1 \
      --weight-tying \
      --weight-tying-type=src_trg_softmax \
      --num-embed 512:512 \
      --num-words 50000:50000 \
      --word-min-count 1:1 \
      --optimizer=adam \
      --optimized-metric=perplexity \
      --clip-gradient=-1 \
      --initial-learning-rate=0.0001 \
      --learning-rate-reduce-num-not-improved=8 \
      --learning-rate-reduce-factor=0.7 \
      --learning-rate-scheduler-type=plateau-reduce \
      --learning-rate-warmup=0 \
      --max-num-checkpoint-not-improved=32 \
      --min-num-epochs=0 \
      --max-updates 1001000 \
      --weight-init xavier \
      --weight-init-scale 3.0 \
      --weight-init-xavier-factor-type avg