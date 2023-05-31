# Repository content

This repository is a companion to article. It contains demonstation of algorithm to find required number of rules for Cleverminer procedure
SD4ft-Miner.

Repository (c) 2022-2023 Petr Masa

## Structure of the repository

The structure of the repository is the following:

+ *dataset_accidents* – contains merged data set Accidents
+ *accidents_profile.html* – contains profiles of the attributes of the Accidents data set used for experiments,
+ *autocnt_sd4ft_accidents.py* – contains source code for replicating experiments on dataset Accidents,
+ *results_accidents* – contain results of experiments on dataset Accidents, each experiment is in subfolder with step summary and log of individual runs,
+ *adults_profile.html* – contains profiles of the attributes of the Adults data set,
+ *autocnt_sd4ft_adults.py* – contains source code for replicating experiments on dataset Adults.
+ *results_adults* – contain results of experiments on dataset Adults, each experiment is in a subfolder with a name containing the expected range of rule count(e.g. task1_30_to_50).

## Structure of the individual folders with experiments

The repository also contains supplementary information (readme files). Data set Adults is downloaded directly from the UCI ML repository. The structure of the folder with results is the following:

+ *log.txt* – contain listing of resulting rules,
+ *step_list* – contain summary information of iteration steps,
+ *result{i}.json* – contain machine processable output of iteration step i with additional information like processing time statistics etc.
