#! /bin/bash

scripts=`dirname "$0"`
base=$scripts/..


translations=$1/translations



src=sign
trg=de
data=$1/test

# cloned from https://github.com/bricksdont/moses-scripts
MOSES=$base/tools/moses-scripts/scripts

model_name=baseline4_sign_de
num_threads=1

##########################################

OMP_NUM_THREADS=$num_threads python -m sockeye.translate \
				-i $1/Extracted_data/test.preprocessed.$src \
				-o $translations/test.preprocessed.$model_name.$trg \
				-m $1/models/$model_name \
				--beam-size 10 \
				--use-cpu \
				--length-penalty-alpha 1.0 \
				--batch-size 16\




#undo BPE

cat $translations/test.preprocessed.$model_name.de | sed 's/\@\@ //g' > $translations/test.truecased.$model_name.de
 #undo truecasing


cat $translations/test.truecased.$model_name.de| $MOSES/recaser/detruecase.perl > $translations/test.tokenized.$model_name.de

#undo tokenization

cat $translations/test.tokenized.$model_name.de | $MOSES/tokenizer/detokenizer.perl -l $spoken > $translations/test.$model_name.de
#cat $translations/test.preprocessed.$model_name.sign > $translations/test.$model_name.sign
# compute case-sensitive BLEU on detokenized data

cat $translations/test.$model_name.de | sacrebleu $data/test.de
