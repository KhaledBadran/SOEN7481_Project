# A Combined Approach to Detect a Flaky Tests in Python
#### Khaled Badran (40069733)
#### Haya Samaana  (40207520)


REQUIREMENTS
------------
Our project relies mainly on sklearn, pandas, numpy, keras as python libraries.
It also requires the installation of [PyNose](https://github.com/jetbrains-research/pynose) (a JetBrains IDE extension).


Files
------------
Our code submission contains the following files:

* `./requirements.txt`: a pip environment for our project 
* `./scripts/tests/*`: Tests used in our projects 
* `./script/filter_inactive_repos.py`: a script that checks whether a Github repo is active or not. 
* `./script/collect_files.py`: a script to install the raw content from the test files on GitHub.
* `./script/combine_data.py`: combines the data about the test vocabulary, test smell and flakiness in one file.
* `./script/json_to_csv.py`: parses the results from the PyNose tool to locate the infected test function in a test class
 and store the data in csv format. 
* `./script/model.ipynb`: a jupyter notebook where we build, optimize and evaluate the models for the baseline and combined approaches. 


Notes
------------
* GPU is not required.
* To check for project activity on GitHub, a valid GitHub token is required. 
* Finding the optimal parameters takes ~1 hour.
* To establish the baseline (vocabulary) model, we rely heavily on the steps followed by a previous study: 

