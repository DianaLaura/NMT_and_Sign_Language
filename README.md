# NMT_and_Sign_Language

1. Clone git-repo
2. run shell_scripts/make_virtualenv.sh
3. activate virtual environment with source ../venvs/sockeye3/bin/activate
4. run download_install_packages.sh
5. run download_split_data.sh with bash (not shell/sh!) -> It requires the path to your preferred storage directory as an argument
6. run preprocess.sh ->  Arguments: source language, target language, spoken language, storage directory (same as given before)
8. run prepare_data.sh -> 3 Arguments: source language, target language, storage directory (same as before)
-> prepare_date_source_factors only take the storage directory as argument (= only 1 argument needed), since the direction of the translation is fixed.
7. run train.sh -> 3 Arguments: source language, target language, storage directory (same as before)
-> train_source_factors_x only take the storage directory as argument (= only 1 argument needed), since the direction of the translation is fixed.
8. run evaluate.sh -> 1 Argument: storage directory. The variables for source/target language need to be set in the script.
