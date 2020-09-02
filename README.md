# NMT_and_Sign_Language

1. Clone git-repo
2. run shell_scripts/make_virtualenv.sh
3. #activate virtual environment with source ../venvs/sockeye3/bin/activate
4. run download_install_packages.sh
5. run download_split_data.sh #with bash# (not shell/sh!) -> It requires the path to your preferred storage directory as an argument
6. run preprocess.sh -> 4 Arguments: source language, target language, spoken language, storage directory (same as given before)
8. run prepare_data.sh -> 3 Arguments: source language, target language, storage directory (same as before)
7. run train.sh -> 3 Arguments: source language, target language, storage directory (same as before)
8. run evaluate.sh -> 4 Arguments: source language, target language, spoken language, storage directory
