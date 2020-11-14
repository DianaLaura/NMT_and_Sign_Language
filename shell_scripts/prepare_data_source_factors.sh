scripts=`dirname "$0"`

src=sign
trg=de
data=$1/Extracted_data
base=$scripts/..

mkdir -p $1/prepared_data_source

num_threads=1
model_name=baseline

#Preparing data (cf. https://awslabs.github.io/sockeye/training.html)
OMP_NUM_THREADS=$num_threads python -m sockeye.prepare_data \
      --source $data/train.preprocessed.sign\
      --target $data/train.preprocessed.$trg \
      --output $1/prepared_data_source/data.version \
      --max-seq-len=200:100 \
      --no-bucketing \
      --source-factors $data/train.preprocessed.mouthings
