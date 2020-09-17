#! /bin/bash

scripts=`dirname "$0"`
base=$scripts/..


translations=$4/translations

mkdir -p $translations

src=$1
trg=$2
spoken=$3
data=$4/Extracted_data

# cloned from https://github.com/bricksdont/moses-scripts
MOSES=$base/tools/moses-scripts/scripts

model_name=baseline3_de_sign
num_threads=1

##########################################

OMP_NUM_THREADS=$num_threads python -m sockeye.translate \
				-i $4/Extracted_data/test.preprocessed.$src \
				-o $translations/test.preprocessed.$model_name.$trg \
				-m $4/models/$model_name \
				--beam-size 10 \
				--length-penalty-alpha 1.0 \
				--device-ids 0 \
				--batch-size 16


#undo BPE

cat $translations/test.bpe.$model_name.$spoken | sed 's/\@\@ //g' > $translations/test.truecased.$model_name.$spoken
# undo truecasing

cat $translations/test.truecased.$model_name.$spoken| $MOSES/recaser/detruecase.perl > $translations/test.tokenized.$model_name.$spoken

# undo tokenization

cat $translations/test.tokenized.$model_name.$spoken | $MOSES/tokenizer/detokenizer.perl -l $spoken > $translations/test.$model_name.$spoken
cat $translations/test.preprocessed.$model_name.sign > $translations/test.$model_name.sign
# compute case-sensitive BLEU on detokenized data

cat $translations/test.$model_name.$trg | sacrebleu $data/test.$trg
