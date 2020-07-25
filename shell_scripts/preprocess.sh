#! /bin/bash
#Source: https://github.com/bricksdont/sockeye-toy-models/blob/gpu/scripts/preprocess.sh

scripts=`dirname "$0"`
base=$scripts/..

mkdir -p $base/shared_models
src=$1
trg=$2
spoken=$3 #file ending of spoken language
storage=$4
data=`echo $storage/Extracted_data`


# cloned from https://github.com/bricksdont/moses-scripts
MOSES=$base/tools/moses-scripts/scripts

# change path to preferred temp directory on your machine

#mkdir -p $base/tmp
#TMP=$base/tmp

#################################################################

# normalize train, dev and test

for corpus in train dev test; do
	cat $data/$corpus.$spoken | sed -e "s/\r//g" | perl $MOSES/tokenizer/normalize-punctuation.perl > $data/$corpus.normalized.$spoken
done

# tokenize train, dev and test

for corpus in train dev test; do
	cat $data/$corpus.normalized.$spoken | perl $MOSES/tokenizer/tokenizer.perl -a -q -l $spoken > $data/$corpus.tokenized.$spoken
	cat $data/$corpus.sign | perl $base/data_loading_extraction/moses_tokenizer_sign.perl > $data/$corpus.tokenized.sign
	
done
# clean length and ratio of train (only train!)

$MOSES/training/clean-corpus-n.perl $data/train.tokenized $src $trg $data/train.tokenized.clean 1 100

# learn truecase model on train (learn one model for each language)

$MOSES/recaser/train-truecaser.perl -corpus $data/train.tokenized.$spoken -model $base/shared_models/truecase-model.$spoken

# apply truecase model to train, test and dev

for corpus in train; do
	$MOSES/recaser/truecase.perl -model $base/shared_models/truecase-model.$spoken < $data/$corpus.tokenized.clean.$spoken > $data/$corpus.truecased.$spoken
	cat $data/$corpus.tokenized.clean.sign > $data/$corpus.truecased.sign
done

for corpus in dev test; do
        $MOSES/recaser/truecase.perl -model $base/shared_models/truecase-model.$spoken < $data/$corpus.tokenized.$spoken > $data/$corpus.tokenized.$spoken
		cat $data/$corpus.tokenized.sign > $data/$corpus.truecased.sign
done

# sanity checks
echo "At this point, please check that 1) file sizes are as expected, 2) languages are correct and 3) material is still parallel"