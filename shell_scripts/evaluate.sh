#! /bin/bash

scripts=`dirname "$0"`
base=$scripts/..


translations=$1/translations



src=sign
trg=de
data=$1
eval_set=test
# cloned from https://github.com/bricksdont/moses-scripts
MOSES=$base/tools/moses-scripts/scripts

model_name=baseline5_sign_de
num_threads=1

##########################################

OMP_NUM_THREADS=$num_threads python -m sockeye.translate \
				-i $1/Extracted_data/$eval_set.preprocessed.$src \
				-o $translations/$eval_set.preprocessed.$model_name.$trg \
				-m $1/models/$model_name \
				--beam-size 10 \
				--length-penalty-alpha 1.0 \
				--batch-size 16\




#undo BPE

cat $translations/$eval_set.preprocessed.$model_name.de | sed 's/\@\@ //g' > $translations/$eval_set.truecased.$model_name.de
 #undo truecasing


cat $translations/$eval_set.truecased.$model_name.de| $MOSES/recaser/detruecase.perl > $translations/$eval_set.tokenized.$model_name.de

#undo tokenization

cat $translations/$eval_set.tokenized.$model_name.de | $MOSES/tokenizer/detokenizer.perl -l $spoken > $translations/$eval_set.$model_name.de
#cat $translations/test.preprocessed.$model_name.sign > $translations/test.$model_name.sign
# compute case-sensitive BLEU on detokenized data

cat $translations/$eval_set.$model_name.de | sacrebleu $data/Extracted_data/$eval_set.de
