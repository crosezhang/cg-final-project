# cg-final-project

## This project utilizes a dual-method approach to accurately identify contaminants in sequencing data. 

It integrates the Kraken algorithm, which relies on reference databases, with the database-independent algorithm PhylOligo. By analyzing sequencing reads, Kraken constructs a taxonomic profile to flag potential contaminants. Concurrently, PhylOligo develops a distance matrix to compute relations between sequencing reads. Our program leverages these outputs to pinpoint potential contaminants. The program cross-references the findings from analyzing each of the outputs to identify high-confidence contaminants. Additionally, it conducts an analysis of the sequences flagged by both methods, providing insights into the reliability and correlation of the outcomes from these distinct approaches. We utilized [KrakenUniq](https://github.com/fbreitwieser/krakenuniq/tree/master) and [PhylOligo](https://github.com/itsmeludo/PhylOligo) in addition to using some of the PhylOligo source code in our python analysis file as the conda package itself wasn't working in some parts. We have labeled these parts in our code (lines 204-234)

## Creating test fasta files:
input requires a main genome file and a contaminant genome file
run the script create_test_file.py
```
python3 create_test_file.py [main genome file path] [number of sequences from main genome file] [contaminant genome file path] [number of sequences from contaminant genome file] [sequence length]
```

## Running the program:

Designed to be run on Linux OS using anaconda.

First clone this repo to get the necessary files.
```
git clone https://github.com/crosezhang/cg-final-project.git
cd cg-final-project
```

Begin by creating a new environment in anaconda 
```
conda create -n cont-detection
conda activate cont-detection
conda config --add channels bioconda
conda config --add channels itsmeludo
```

Then, install krakenuniq using the following command
```
conda install -c bioconda krakenuniq
```
We will be using the minikraken 8GB database with krakenuniq to allow our program to run on most machines regardless of processing power. Download this database using the following commands. The complete download may take up to 30 minutes depending on internet speeds. If curl isn't working, then download the file from [this link](https://ccb.jhu.edu/software/kraken/dl/minikraken_20171019_8GB.tgz) and continue with the rest of the operations. The uncompressing process also should take a few minutes.

```
curl -O https://ccb.jhu.edu/software/kraken/dl/minikraken_20171019_8GB.tgz
mkdir minikraken
tar -xvzf minikraken_20171019_8GB.tgz -C ./minikraken
mv ./minikraken/minikraken_20171019_8GB/* ./minikraken
rm -r ./minikraken/minikraken_20171019_8GB
```

After setting up krakenuniq and the associated minikraken database, install phyloligo with conda
```
conda install phyloligo -c itsmeludo
```

Once you have all of the appropriate packages installed, you should be able to run the bash file using the following command and entering the appropriate arguments.
```
bash contam-pipeline.sh <fastas-dir> <kraken-output-dir> <phyloligo-output-dir> <overall-output-dir>
```
To obtain our results, we used the following command based on the structure of our repo.
```
bash contam-pipeline.sh ./fastas ./kraken ./phyloligo ./output
```

If the Python analysis script doesn't work due to missing packages, use `pip3` to import the missing packages.
