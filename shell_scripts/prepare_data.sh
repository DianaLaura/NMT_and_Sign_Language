scripts=`dirname "$0"`

src=$1
trg=$2
data=$3/Extracted_data
base=$scripts/..

mkdir -p $3/prepared_data

num_threads=1
model_name=baseline

#Preparing data (cf. https://awslabs.github.io/sockeye/training.html)
OMP_NUM_THREADS=$num_threads python -m sockeye.prepare_data \
      --source $data/train.truecased.$src \
      --target $data/train.truecased.$trg \
      --output $3/prepared_data/data.version \
      --num-samples-per-shard 3000 \
      --shared-vocab \
      --max-seq-len=100:100 \
      --no-bucketing

