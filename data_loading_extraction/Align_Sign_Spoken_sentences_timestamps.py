"""

Input: directory with ilex-files from https://www.sign-lang.uni-hamburg.de/meinedgs/ling/start-name_de.html

Output: 
    - document with sentences in sign language + mouthings, separated with <sep> (one sentence per line)
    - document with timestamps for sign language + mouthings, separated with <sep> (one sentence per line, time starts by zero frames each sentence)
    - document wth corresponding sentences in German (one sentence per line)

Options:
    - input-dir: directory whith ilex-files (required)
    - output-dir: directory where the output files should be saved (default: working directory)
    - de: outputfile with sentences in spoken German (default: TRUE)
    - testing: if true, only a subset of the ilex-files is used (default: FALSE)

"""

import os
import argparse
import random
from collections import defaultdict
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
from datetime import datetime
import frames



def get_args():

    parser = argparse.ArgumentParser(description='Parsing arguments like input path, output path, ...')
    parser.add_argument("--input_dir", required=True, type=str, help='Path to input directory')
    parser.add_argument("--output_dir", default=os.getcwd(), type=str, help='Path to output directory')
    parser.add_argument("--name", default='sentences', type=str, help='name for output files')
    parser.add_argument("--testing", default=False, type=bool, help='only uses a small subset if set True')
    

    return parser.parse_args()

def main(args):
    input_dir = args.input_dir
    output_dir = args.output_dir
    testing = args.testing
    name = args.name

    files = []
    error_list = [] #list of files where an error occured
    line_counter = 1 #Variable for debugging errors that only occur in specific lines



    if testing == True:
        files = random.sample(os.listdir(input_dir), 5)
    
    else:
        files = os.listdir(input_dir)
    
    print('Extract data...')
    for file in tqdm(files):

        glosses = defaultdict(str) #dictionary with the gloss id as key, and the corresponding gloss as value
        token_id = defaultdict(str) # defaultdict with the token id as key, and the corresponding gloss id as value
        german_sents = []
        relevant_tiers = defaultdict(list) #dictionnary of tiers that are relevant for the output
        sign_words = []
        mouth_words = []


        filename = os.fsdecode(os.path.join(input_dir, file))

        try:
            infile = open(filename)
            soup = BeautifulSoup(infile.read(), 'lxml')
            infile.close()
        except UnicodeDecodeError:
            error_list.append(filename)
            continue
        
        #extract glosses and corresponding ids
        extracted_glosses = soup.find('ilex-data').findAll('type')

        for item in extracted_glosses:
            glosses[item['id']] = item['name']
        
        extracted_token_ids = soup.find('ilex-data').findAll('token')

        for item in extracted_token_ids:
            token_id[item['id']] = item['type']
    

        
        #extract tiers of the participants

        all_tiers = soup.find('ilex-data').findAll('tier')

        signs = {}
        
        ger = {}

        mouth = {}

        for item in all_tiers:

            if re.match('Lexem.*', item['name']):
                signs[item['participation']] = item['id']
            
            if re.match('Deutsche ', item['name']):
                ger[item['participation']] = item['id']

            if re.match('Mundbild.*', item['name']):
                mouth[item['participation']] = item['id']


        raw = soup.find('ilex-data').findAll('tag')

        


        #extract lines from raw document
        #%f is microseconds in the datetime format, not frames. I use microseconds because it's native to datetime, and it should not cause any problems
        # when comparing timestamps
        try:
            for item in (raw):
                if ((item['tier'] == ger['1']) or (item['tier'] == ger['2'])):
                    german_sents.append([item['value'], datetime.strptime(item['timecode_start'], '%H:%M:%S:%f') , datetime.strptime(item['timecode_end'], '%H:%M:%S:%f')])
                        

                elif ((item['tier'] == signs['1']) or (item['tier'] == signs['2'])):
                    try:
                        word = glosses[token_id[item['token_dom']]]
                        
                    except KeyError:
                        word = glosses[token_id[item['token_nondom']]]
                    
                    sign_words.append([word, datetime.strptime(item['timecode_start'], '%H:%M:%S:%f'), datetime.strptime(item['timecode_end'], '%H:%M:%S:%f')])
                
               
                
                if ((item['tier'] == mouth['1']) or (item['tier'] == mouth['2'])):
                    mouth_words.append([item['value'], datetime.strptime(item['timecode_start'], '%H:%M:%S:%f') , datetime.strptime(item['timecode_end'], '%H:%M:%S:%f')])
        except KeyError:
            error_list.append(filename)
            continue

        wordcounter = 0
        sentcounter = 0
        mouthcounter = 0
        ger_sents_only = []
        timestamps = []
        sign_sents = []



        
        
        for sent in german_sents:
            new_sign_sent = ""
            new_mouth_sent=""
            new_time_sign = ""
            new_time_mouthings = ""
            

            #calculate total frames until the beginning of the sentence to make sure that every sentence starts at zero frames
   
            zero_point =  frames.fps_50_to_fps_30(frames.timestamp_to_50_fps(sent[1]))
            
            #Breakpoint for debugging: line_counter should have the same number as a problematic line in the output documents
            #if line_counter == 25871:
                #breakpoint()

            

            
            while (wordcounter < len(sign_words)) and (sign_words[wordcounter][1] >= sent[1]) and (sign_words[wordcounter][2] <= sent[2]):
                new_sign_sent += sign_words[wordcounter][0] + " "
                new_time_sign += str(frames.fps_50_to_fps_30(frames.timestamp_to_50_fps(sign_words[wordcounter][1])) - zero_point) + " "

                #check if any mouthings are available
                if (mouthcounter == len(mouth_words) -1):
                        wordcounter += 1
                        continue
                mouth_words[mouthcounter][0] = mouth_words[mouthcounter][0].replace("\xa0", " ")

                if (len(mouth_words[mouthcounter][0].split()) > 1):
                    mouth_words[mouthcounter][0] = mouth_words[mouthcounter][0].replace(" ", "-")
                    
                
                if ((mouth_words[mouthcounter][1] >= sign_words[wordcounter][1]) and (mouth_words[mouthcounter][1] <= sign_words[wordcounter][2])):
                    
                        
                    new_mouth_sent += mouth_words[mouthcounter][0] + ' '
                    new_time_mouthings += str(frames.fps_50_to_fps_30(frames.timestamp_to_50_fps(mouth_words[mouthcounter][1])) - zero_point) + ' '

                    mouthcounter += 1
                
                wordcounter += 1


            

            if (new_sign_sent != ""):
                ger_sents_only.append(sent[0])
                sign_sents.append(str(new_sign_sent + ' <sep> ' + new_mouth_sent))
                timestamps.append(str(new_time_sign + ' <sep> ' + new_time_mouthings))
                line_counter += 1 #Variable for debugging

        
        with open(os.fsdecode(os.path.join(output_dir + '/' + name + '.time')), 'a') as outfile:
            outfile.write("\n".join(map(str, timestamps)))
            outfile.write("\n")
                        
               
        with open(os.fsdecode(os.path.join(output_dir + '/' + name + '.sign')), 'a') as outfile:
            outfile.write("\n".join(map(str, sign_sents)))
            outfile.write("\n")
                    

        
        with open(os.fsdecode(os.path.join(output_dir + '/' + name + '.de')), 'a') as outfile:
            outfile.write("\n".join(map(str, ger_sents_only)))
            outfile.write("\n")

            
        
        
        
    print('There were some errors while reading the following files:')
    print(error_list)

if __name__ == "__main__":
   args = get_args()

   main(args)