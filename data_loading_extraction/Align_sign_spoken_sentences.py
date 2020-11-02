"""

Input: directory with ilex-files from https://www.sign-lang.uni-hamburg.de/meinedgs/ling/start-name_de.html

Output: 
    - document with sentences in sign language (one sentence per line)
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

def get_args():

    parser = argparse.ArgumentParser(description='Parsing arguments like input path, output path, ...')
    parser.add_argument("--input_dir", required=True, type=str, help='Path to input directory')
    parser.add_argument("--output_dir", default=os.getcwd(), type=str, help='Path to output directory')
    parser.add_argument ("--de", default=True, type=bool ,help= 'variable to enable/disable the German output file')
    parser.add_argument("--en", default=True, help = 'variable to enable/disable the English output file' )
    parser.add_argument("--sentences", default=True, help='if true, all sentences are saved in one file per language')
    parser.add_argument("--name", default='sentences', type=str, help='name for output files if sentences = true')
    parser.add_argument("--testing", default=False, type=bool, help='only uses a small subset if set True')
    parser.add_argument("--mouthings", default=True, help='If set to True, it also extracts mouthings, and save them in a separate document"')

    return parser.parse_args()

def main(args):
    input_dir = args.input_dir
    output_dir = args.output_dir
    de = args.de   
    testing = args.testing
    name = args.name
    en = args.en
    sentences = args.sentences
    mouthings = args.mouthings
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
        en_sents = []
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

        en = {}

        mouth = {}

        for item in all_tiers:

            if re.match('Lexem.*', item['name']):
                signs[item['participation']] = item['id']
            
            if re.match('Deutsche ', item['name']):
                ger[item['participation']] = item['id']
            
            if re.match('Englische ', item['name']):
                en[item['participation']] = item['id']

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
                
                if (en and ((item['tier'] == en['1']) or (item['tier'] == en['2']))):
                    en_sents.append([item['value'], datetime.strptime(item['timecode_start'], '%H:%M:%S:%f') , datetime.strptime(item['timecode_end'], '%H:%M:%S:%f')])
                
                if (mouthings == True and ((item['tier'] == mouth['1']) or (item['tier'] == mouth['2']))):
                    mouth_words.append([item['value'], datetime.strptime(item['timecode_start'], '%H:%M:%S:%f') , datetime.strptime(item['timecode_end'], '%H:%M:%S:%f')])
        except KeyError:
            error_list.append(filename)
            continue

        wordcounter = 0
        sentcounter = 0
        mouthcounter = 0
        ger_sents_only = []
        mouth_sents = []
        sign_sents = []
        en_sents_only = []



        
        
        for sent in german_sents:
            new_sign_sent = ""
            new_mouth_sent=""
            
            #Breakpoint for debugging: line_counter should have the same number as a problematic line in the output documents
            #if line_counter == 1165:
                #breakpoint()

            

            
            while (wordcounter < len(sign_words)) and (sign_words[wordcounter][1] >= sent[1]) and (sign_words[wordcounter][2] <= sent[2]):
                new_sign_sent += sign_words[wordcounter][0] + " "
                
                if (len(mouth_words[mouthcounter][0].split()) > 1):
                    mouth_words[mouthcounter][0] = mouth_words[mouthcounter][0].replace(" ", "-")
                
                if mouthings==True:
                    
                    #check if mouthings are already as long as sign sentence
                    if (len(new_sign_sent.split()) == len(new_mouth_sent.split())):
                        continue

                    #check if any mouthings are available
                    if (mouthcounter == len(mouth_words) -1):
                            new_mouth_sent += "<empty> "
                            wordcounter += 1
                            continue

                    if (((mouth_words[mouthcounter][1] >= sign_words[wordcounter][1]) and (mouth_words[mouthcounter][1] <= sign_words[wordcounter][2]))) and ((mouth_words[mouthcounter + 1][1] < sign_words[wordcounter][2]) and (mouth_words[mouthcounter + 1][1] <= sign_words[wordcounter][2])):
                    
                        

                        if (mouth_words[mouthcounter][1] - sign_words[wordcounter][1] > sign_words[wordcounter][2] - mouth_words[mouthcounter + 1][1]):
                            new_mouth_sent += (mouth_words[mouthcounter][0] + ' ')
                        
                        else:
                            new_mouth_sent += (mouth_words[mouthcounter + 1][0] + ' ')

                        
                        mouthcounter += 1
                
                    elif ((mouth_words[mouthcounter][1] >= sign_words[wordcounter][1]) and (mouth_words[mouthcounter][1] <= sign_words[wordcounter][2])):
                        new_mouth_sent += (mouth_words[mouthcounter][0] + ' ')

                        if (mouth_words[mouthcounter][2] <= sign_words[wordcounter][2]):
                            mouthcounter += 1
                
                    else:
                        new_mouth_sent += '<empty> '
                wordcounter += 1


            #There are small mismatches in the length between English and German Translation:
            if ((en == True) and sentences and (new_sign_sent != "")):
                try:
                    if ((en_sents[sentcounter][1] >= sent[1]) and (en_sents[sentcounter][2] <= sent[2])) or (en_sents_only[-1] == '-'):
                        en_sents_only.append(en_sents[sentcounter][0])
                        sentcounter += 1
                    else:
                        en_sents_only.append('-')
                except IndexError:
                    if sentcounter == 0:
                        en_sents_only.append('-')
                    else:
                        print('The following file was only loaded partially due to a huge mismatch between English and German Sentences: ', file)
                        print('English sentences: ',len(en_sents))
                        print('German sentences: ', len(german_sents))
            

            if (new_sign_sent != ""):
                ger_sents_only.append(sent[0])
                sign_sents.append(new_sign_sent)
                mouth_sents.append(new_mouth_sent)
                line_counter += 1 #Variable for debugging

        if sentences==True:
            if mouthings==True:
                with open(os.fsdecode(os.path.join(output_dir + '/' + name + '.mouthings')), 'a') as outfile:
                    outfile.write("\n".join(map(str, mouth_sents)))
                    outfile.write("\n")
                        
               
            with open(os.fsdecode(os.path.join(output_dir + '/' + name + '.sign')), 'a') as outfile:
                outfile.write("\n".join(map(str, sign_sents)))
                outfile.write("\n")
                    

            if de==True:
                with open(os.fsdecode(os.path.join(output_dir + '/' + name + '.de')), 'a') as outfile:
                    outfile.write("\n".join(map(str, ger_sents_only)))
                    outfile.write("\n")

            if en==True:
                with open(os.fsdecode(os.path.join(output_dir + '/' + name + '.en')), 'a') as outfile:
                    outfile.write("\n".join(map(str, en_sents_only)))
                    outfile.write("\n")

        elif sentences=="False":
            with open(os.fsdecode(os.path.join(output_dir, file[:-5] + '.sign')), 'w') as outfile:
                outfile.write("\n".join(map(str, sign_sents)))

            if de==True:
                with open(os.fsdecode(os.path.join(output_dir, file[:-5] + '.de')), 'w') as outfile:
                    outfile.write("\n".join(map(str, ger_sents_only)))

            if en==True:
                with open(os.fsdecode(os.path.join(output_dir, file[:-5] + '.en')), 'w') as outfile:
                    outfile.write("\n".join(map(str, en_sents_only)))
        
        
        
    print('There were some errors while reading the following files:')
    print(error_list)

if __name__ == "__main__":
   args = get_args()

   main(args)