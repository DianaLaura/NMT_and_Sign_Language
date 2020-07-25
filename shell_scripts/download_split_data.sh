#! /bin/bash

storage=$1


scripts=`dirname "$0"`
base=$scripts/..

#load data

mkdir -p $storage/DGS_corpus_dirty

mkdir -p $storage/DGS_corpus

mkdir -p $storage/DGS_train

mkdir -p $storage/DGS_test

mkdir -p $storage/DGS_dev

mkdir -p $storage/Extracted_data

python3 ../data_loading_extraction/download_ilex.py --output_dir $storage/DGS_corpus_dirty/

#filter out files that are smaller than 3 kb, because they usually don't contain any usable data

cp `find $storage/DGS_corpus_dirty -type f -size +3k` $storage/DGS_corpus

#split into train and test set

echo 'Splitting into train and test set... '

testindex=`ls $storage/DGS_corpus | awk 'END {print NR*0.2} ' | awk '{print int ($1)}'`

trainindex=`ls $storage/DGS_corpus | wc -l`

trainindex=`expr $trainindex - $testindex`

devindex=`echo $testindex | awk 'END {print $1/2}' | awk '{print int ($1)}'`

list=`ls $storage/DGS_corpus | perl -MList::Util=shuffle -E 'srand42; print shuffle(<STDIN>);'`  #ruby -e 'puts STDIN.readlines.shuffle(random: Random.new(42))'`

cp `echo "$list" | head -$devindex | awk -v var="$storage" '{print var"/DGS_corpus/"$1}'` $storage/DGS_dev/

cp `echo "$list" | tail -$trainindex | awk -v var="$storage" '{print var"/DGS_corpus/"$1}'` $storage/DGS_train/

devindex=`echo $devindex | awk 'END {print $1+1}'`

cp `echo "$list" | head -$testindex | tail -$devindex |  awk -v var="$storage" '{print var"/DGS_corpus/"$1}'` $storage/DGS_test/



#extract data from ilex-files
echo 'Extracting data from test set:'
python3 ../data_loading_extraction/Align_sign_spoken_sentences.py --input_dir $storage/DGS_test/ --output_dir $storage/Extracted_data --name 'test'

echo 'Extracting data from validation set:'

python3 ../data_loading_extraction/Align_sign_spoken_sentences.py --input_dir $storage/DGS_dev/ --output_dir $storage/Extracted_data --name 'dev'

echo 'Extracting data from train set:'
python3 ../data_loading_extraction/Align_sign_spoken_sentences.py --input_dir $storage/DGS_train/ --output_dir $storage/Extracted_data --name 'train'