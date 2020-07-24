#! /bin/bash
#copied from https://github.com/bricksdont/sockeye-toy-models/blob/gpu/scripts/train.sh

scripts=`dirname "$0"`

src=$1
trg=$2
data=$3/Extracted_data
train_data=$3/prepared_data/data.version
base=$scripts/..

mkdir -p $3/models


num_threads=1
model_name=baseline



##################################


#-s $data/train.truecased.$src \
#-t $data/train.truecased.$trg \
OMP_NUM_THREADS=$num_threads python -m sockeye.train \
      -o $3/models/$model_name  \
			--prepared-data $train_data\
			-vs $data/dev.truecased.$src \
      -vt $data/dev.truecased.$trg \
      --max-updates 1001000 \
      --seed=1 \
      --batch-type=word \
      --batch-size=3000 \
      --embed-dropout=0:0 \
      --encoder=transformer \
      --decoder=transformer \
      --num-layers=6:6 \
      --checkpoint-interval=4000 \
      --transformer-model-size=512 \
      --transformer-attention-heads=8 \
      --transformer-feed-forward-num-hidden=2048 \
      --transformer-preprocess=n \
      --transformer-postprocess=dr \
      --transformer-dropout-attention=0.1 \
      --transformer-dropout-act=0.1 \
      --transformer-dropout-prepost=0.1 \
      --transformer-positional-embedding-type fixed \
      --max-seq-len=100:100 \
      --label-smoothing 0.1 \
      --weight-tying-type=src_trg_softmax \
      --num-embed 512:512 \
      --num-words 50000:50000 \
      --word-min-count 1:1 \
      --optimizer=adam \
      --optimized-metric=perplexity \
      --initial-learning-rate=0.0001 \
      --learning-rate-reduce-num-not-improved=8 \
      --learning-rate-reduce-factor=0.7 \
      --learning-rate-scheduler-type=plateau-reduce \
      --learning-rate-warmup=0 \
      --max-num-checkpoint-not-improved=32 \
      --min-num-epochs=0 \
      --weight-init xavier \
      --weight-init-scale 3.0 \
      --weight-init-xavier-factor-type avg \
      --gradient-clipping-threshold=1.0 \
      --device-ids=0 \
      --decode-and-evaluate-device-id 0 \
      #--use-cpu \