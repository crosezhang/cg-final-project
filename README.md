# cg-final-project

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
We will be using the minikraken 8GB database with krakenuniq to allow our program to run on most machines regardless of processing power. The dataase is included already in this repo.

After setting up krakenuniq and the associated minikraken database, install phyloligo with conda
```
conda install phyloligo -c itsmeludo
```
Once you have all of the appropriate packages installed, you should be able to run the bash file using the following command and entering the appropriate arguments
```
bash cont-pipeline.sh <input-filename> <output-filename>
```
