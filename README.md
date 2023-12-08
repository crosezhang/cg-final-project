# cg-final-project

## This project utilizes a dual-method approach to accurately identify contaminants in sequencing data. 

It integrates the Kraken algorithm, which relies on reference databases, with the database-independent algorithm PhylOligo. By analyzing sequencing reads, Kraken constructs a taxonomic profile to flag potential contaminants. Concurrently, PhylOligo develops a distance matrix to compute relations between sequencing reads. Our program leverages these outputs to pinpoint potential contaminants. The program cross-references the findings from analyzing each of the outputs to identify high-confidence contaminants. Additionally, it conducts an analysis of the sequences flagged by both methods, providing insights into the reliability and correlation of the outcomes from these distinct approaches.

## Creating test fasta files:
# TO DO: write how to create test files using the program
input requires full genome sequencing of prokaryotic
run the script create_test_file.py

## Running the program:

Designed to be run on Linux OS using anaconda.

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
We will be using the minikraken 8GB database with krakenuniq to allow our program to run on most machines regardless of processing power. Download this database using the following commands. The complete download should take around 5 minutes. The uncompressing process also should take a few minutes.

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

Once you have all of the appropriate packages installed, you should be able to run the bash file using the following command and entering the appropriate arguments, where the inputfile name is the fasta file of the sequences, and output is the txt file indicating the identified contaminants by the analysis.
```
bash cont-pipeline.sh <fastas-directory> <kraken-output-directory> <phyloligo-output-directory> <overall-output-directory>
```
