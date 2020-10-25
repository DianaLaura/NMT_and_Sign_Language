#! /bin/bash

storage=$1


scripts=`dirname "$0"`
base=$scripts/..

#load data

mkdir -p $storage/DGS_corpus_dirty

mkdir -p $storage/DGS_corpus

mkdir -p $storage/Extracted_data

python3 ../data_loading_extraction/download_ilex.py --output_dir $storage/DGS_corpus_dirty/

#filter out files that are smaller than 3 kb, because they usually don't contain any usable data

cp `find $storage/DGS_corpus_dirty -type f -size +3k` $storage/DGS_corpus

#extract data from ilex-files
echo 'Extracting data:'
python3 ../data_loading_extraction/Align_sign_spoken_sentences.py --input_dir $storage/DGS_corpus/ --output_dir $storage/Extracted_data --name 'full_set'

#split into train and test set


file_length=`wc -l $storage/Extracted_data/full_set.de | awk '{print $1}'`

file_length2=`expr $file_length - 2000 | awk '{print $1}'`

list_dev=($(seq 0 $file_length2 | perl -MList::Util=shuffle -E 'srand42; print shuffle(<STDIN>);'))

file_length2=`expr $file_length - 4000 | awk '{print $1}'`

list_test=($(seq 0 $file_length2 | perl -MList::Util=shuffle -E 'srand42; print shuffle(<STDIN>);'))

IFS=" "


dev=(${list_dev[@]:0:2000})
test=(${list_test[@]:0:2000})

cat $storage/Extracted_data/full_set.de > $storage/Extracted_data/train.de
cat $storage/Extracted_data/full_set.sign > $storage/Extracted_data/train.sign
cat $storage/Extracted_data/full_set.sign > $storage/Extracted_data/train.mouthings
echo 'Sampling sets...' 

for index in "${dev[@]}" 
do
   
  sed -n "${index}p" $storage/Extracted_data/train.de >> $storage/Extracted_data/dev.de
  sed -n "${index}p" $storage/Extracted_data/train.sign >> $storage/Extracted_data/dev.sign
  sed -n "${index}p" $storage/Extracted_data/train.mouthings >> $storage/Extracted_data/dev.mouthings  
  sed -i '' "${index}d" $storage/Extracted_data/train.de
  sed -i '' "${index}d" $storage/Extracted_data/train.sign 
  sed -i '' "${index}d" $storage/Extracted_data/train.mouthings 
done

echo 'Development set created!'

for index in "${test[@]}" 
do

  sed -n "${index}p" $storage/Extracted_data/train.de >> $storage/Extracted_data/test.de
  sed -n "${index}p" $storage/Extracted_data/train.sign >> $storage/Extracted_data/test.sign
  sed -n "${index}p" $storage/Extracted_data/train.mouthings >> $storage/Extracted_data/test.mouthings   
  sed -i '' "${index}d" $storage/Extracted_data/train.de
  sed -i '' "${index}d" $storage/Extracted_data/train.sign
  sed -i '' "${index}d" $storage/Extracted_data/train.mouthings

done

echo 'Test set created!'

echo 'Train set created!'
