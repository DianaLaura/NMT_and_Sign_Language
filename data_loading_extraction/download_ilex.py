from urllib import request, error
import argparse
from bs4 import BeautifulSoup as Soup
import re
from tqdm import tqdm

def get_args():
    parser = argparse.ArgumentParser(description='Parses output directory')

    parser.add_argument('--output_dir', required=True, type=str, help='directory where the downloaded files are saved')

    args = parser.parse_args()

    return args

def main(args):

    url = 'https://www.sign-lang.uni-hamburg.de/meinedgs/ling/start-name_de.html'
    outputdir = args.output_dir

    infile = request.urlopen(url)
    page = Soup(infile, 'html.parser')

    links = []

    print('Retrieving Links...')

    for i in tqdm(page.findAll('a', attrs={'href': re.compile("\.\./ilex/[0-9]+\.ilex")})):
        link = i.get('href')

        link = re.sub('\.\.', 'https://www.sign-lang.uni-hamburg.de/meinedgs', link)

        links.append(link)
    
    errorlist = []

    print('Downloading files...')
    for url in tqdm(links):
        try:
            filename = outputdir + url[51:]
            request.urlretrieve(url, filename)
        except error.HTTPError:
            errorlist.append(url)
            continue
    
    print('Done! There were some errors in these urls:')

    for i in range(0,len(errorlist)):
        print(errorlist[i])

if __name__ == '__main__':
    args = get_args()

    main(args)

