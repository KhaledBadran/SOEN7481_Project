#!/usr/bin/env python
# coding: utf-8

# In[65]:


import requests
from pathlib import Path
import pandas as pd
from numpy import random
from time import sleep
from tqdm import tqdm
from bs4 import UnicodeDammit

# from typeguard import typechecked
import numpy as np


# In[2]:


# ! pip install typechecked


# In[287]:


DATA_FOLDER: Path = Path("..", "data")
VOCABULARY_DATA_FILE: Path = Path("vocabulary", "data_file.csv")
TEST_SMELLS_DATA_FILE: Path = Path("repos_csvs", "merged_csvs.csv")
TEST_FLAKINESS_DATA_FILE: Path = Path("python_flaky_tests", "active_repos.csv")
OUTPUT_DATA_FILE: Path = Path("oracle", "oracle.csv")
TEST_FLAKINESS_DATA_FILE_CLEANED: Path = Path(
    "python_flaky_tests", "active_repos_clean.csv"
)


# From file path in vocabulary dataframe (ex: https://github.com/tensorflow/tensorflow)
# get the repo_name (tensorflow/tensorflow)
# @typechecked
def get_repo_name_from_url(url: str) -> str:
    parts = url.split("/")
    return parts[-2] + "_&_" + parts[-1]


# replace the '/' with '_&_' in the file_names in the test_flakiness data (ex: tests/unit/test_geometry.py becomes
# tests_&_unit_&_test_geometry.py)
# @typechecked
def update_file_name(file_path: str) -> str:
    fixed_file_name = file_path.replace("/", "_&_")
    return fixed_file_name


# checks multiple columns in the dataframe to determine whether a test function is flaky
def determine_flakiness(data):

    if (
        data["Flaky_randomOrder_withinIteration"]
        or data["Flaky_sameOrder_withinIteration"]
        or data["Order-dependent"]
        or data["Flaky_Infrastructure"]
    ):
        return True
    else:
        return False


# Creates the dataframe for the test vocabulary
def create_vocabulary_df() -> pd.DataFrame:
    vocab_data_file: Path = Path.joinpath(DATA_FOLDER, VOCABULARY_DATA_FILE)
    vocabulary_: pd.DataFrame = pd.read_csv(vocab_data_file)

    # remove non-test functions
    vocabulary_.drop(vocabulary_[vocabulary_.isTest == False].index, inplace=True)

    # rename columns
    vocabulary_.rename(
        columns={
            "projectName": "repo_name",
            "functionName": "func_name",
            "fileName": "file_name",
            "Body": "body",
            "className": "class_name",
        },
        inplace=True,
    )

    # keep relevant columns only
    vocabulary_ = vocabulary_[
        [
            "repo_name",
            "file_name",
            "class_name",
            "func_name",
            "body",
            "voc_size",
            "important_voc",
        ]
    ]

    return vocabulary_


# Creates the dataframe for the test smells
def create_test_smells_df() -> pd.DataFrame:

    # read csv file
    test_smell_data_file: Path = Path.joinpath(DATA_FOLDER, TEST_SMELLS_DATA_FILE)
    test_smells_df_: pd.DataFrame = pd.read_csv(test_smell_data_file)

    # rename columns
    test_smells_df_.rename(
        columns={
            "test_file": "file_name",
            "test_function": "func_name",
            "test_case": "class_name",
        },
        inplace=True,
    )

    return test_smells_df_.copy()


# Creates the dataframe for the test flakiness
def create_test_flakiness_df() -> pd.DataFrame:

    # read csv file
    test_flakiness_file: Path = Path.joinpath(DATA_FOLDER, TEST_FLAKINESS_DATA_FILE)
    test_flakiness_df_: pd.DataFrame = pd.read_csv(test_flakiness_file)

    # rename columns
    test_flakiness_df_.rename(
        columns={
            "Test_filename": "file_name",
            "Test_funcname": "func_name",
            "Test_classname": "class_name",
        },
        inplace=True,
    )

    test_flakiness_df_["repo_name"] = test_flakiness_df_["Project_URL"].apply(
        get_repo_name_from_url
    )

    test_flakiness_df_["file_name"] = test_flakiness_df_["file_name"].astype(str)
    test_flakiness_df_["file_name"] = test_flakiness_df_["file_name"].apply(
        update_file_name
    )
    test_flakiness_df_["flaky"] = test_flakiness_df_.apply(determine_flakiness, axis=1)

    # keep releavant columns only
    test_flakiness_df_ = test_flakiness_df_[
        ["repo_name", "file_name", "class_name", "func_name", "flaky"]
    ]

    return test_flakiness_df_.copy()


# In[284]:


vocabulary: pd.DataFrame = create_vocabulary_df()
test_smells: pd.DataFrame = create_test_smells_df()
test_flakiness: pd.DataFrame = create_test_flakiness_df()


# In[227]:


test_flakiness.shape


# In[236]:


tem = test_flakiness


# In[237]:


# test_flakiness.to_csv(str(Path(DATA_FOLDER, OUTPUT_DATA_FILE)))


# In[275]:


test_flakiness = tem


# In[276]:


# # Test just our repos chunk1
# test_flakiness=test_flakiness[test_flakiness['repo_name'].isin(list(vocabulary['repo_name']))]
# test_flakiness


# In[285]:


# remove all rows with Null Class
test_flakiness = test_flakiness[~test_flakiness["class_name"].isnull()]
test_flakiness


# In[286]:


# update class_name. tests.test_camera.TestCamera    to TestCameratest_flakiness
for i in test_flakiness.index:
    name = test_flakiness["class_name"][i]
    #     print(name)
    ind = name.rfind(".")
    if ind > 0:

        test_flakiness["class_name"][i] = name[ind + 1 :]
    elif ind <= 0:
        #         print(name,'----')
        #         print(test_flakiness['class_name'][i])
        test_flakiness["class_name"][i] = name


# In[288]:


test_flakiness.to_csv(str(Path(DATA_FOLDER, TEST_FLAKINESS_DATA_FILE_CLEANED)))


# In[289]:


test_flakiness


# In[307]:


combined_data = test_flakiness.merge(
    test_smells,
    on=["repo_name", "file_name", "class_name", "func_name"],
    how="left",
)

combined_data = combined_data.merge(
    vocabulary,
    on=["repo_name", "file_name", "class_name", "func_name"],
    how="left",
)

combined_data.to_csv(str(Path(DATA_FOLDER, OUTPUT_DATA_FILE)))


# In[309]:


combined_data.isnull().sum()


# In[268]:


combined_data[combined_data["flaky"] == True]


# In[72]:


combined_data = test_flakiness.merge(
    vocabulary,
    on=["repo_name", "file_name", "class_name"],
    how="inner",
)

combined_data = combined_data.merge(
    test_smells,
    on=["repo_name", "file_name", "class_name"],
    how="inner",
)

# combined_data.to_csv(str(Path(DATA_FOLDER, OUTPUT_DATA_FILE)))


# In[88]:


t_v = test_smells.merge(
    vocabulary,
    on=["repo_name", "file_name", "class_name", "func_name"],
    how="inner",
)


# In[89]:


t_v


# In[94]:


t_v_f = t_v.merge(
    test_flakiness,
    on=["repo_name", "file_name", "class_name", "func_name"],
    how="outer",
)


# In[95]:


t_v_f


# In[73]:


combined_data


# In[ ]:


# del test_smells['Unnamed: 0']
combined_data = test_smells.merge(
    test_flakiness,
    on=["repo_name", "file_name", "class_name", "func_name"],
    how="outer",
)


# In[ ]:


# del test_smells['Unnamed: 0']
combined_data = vocabulary.merge(
    test_smells,
    on=["repo_name", "file_name", "class_name", "func_name"],
    how="outer",
)


# In[ ]:


combined_data.shape


# In[ ]:


vocabulary.shape


# In[ ]:


# In[ ]:


combined_data.shape


# In[ ]:


combined_data


# In[97]:


w = test_smells[test_smells["repo_name"] == "alejoe91_&_MEArec"]
w


# In[98]:


z = vocabulary[vocabulary["repo_name"] == "alejoe91_&_MEArec"]
# z=vocabulary[vocabulary['repo_name']=='fechbmaster_&_3DNIRmapper']
z.head(10)


# In[174]:


# f=test_flakiness[test_flakiness['repo_name']=='fechbmaster_&_3DNIRmapper']
f = test_flakiness[test_flakiness["repo_name"] == "F-I-D-O_&_Future-Config"]
f.head(10)


# In[175]:


test_flakiness.head(100)


# In[34]:


combined_data = z.merge(
    f,
    on=["repo_name", "file_name", "class_name", "func_name"],
    how="inner",
)


# In[35]:


combined_data


# In[ ]:


combined_data[combined_data["repo_name"] == "fechbmaster_&_3DNIRmapper"]


# In[36]:


test_flakiness.head(10)


# In[102]:


test_flakiness[test_flakiness["class_name"].isnull()]


# In[103]:


test_flakiness.shape


# In[110]:


test_flakiness = test_flakiness[
    test_flakiness["repo_name"].isin(list(vocabulary["repo_name"]))
]
test_flakiness


# In[124]:


tf = test_flakiness[test_flakiness["repo_name"].isin(list(test_smells["repo_name"]))]
tf


# In[120]:


test_smells.shape
w = test_smells[test_smells["repo_name"] == "fechbmaster_&_3DNIRmapper"]
w.shape


# In[121]:


vocabulary.shape
v = vocabulary[vocabulary["repo_name"] == "fechbmaster_&_3DNIRmapper"]
v.shape


# In[142]:


vocabulary[vocabulary["class_name"] == "TestCamera"]


# In[143]:


test_smells[test_smells["class_name"] == "TestCamera"]


# In[125]:


f = tf[tf["repo_name"] == "fechbmaster_&_3DNIRmapper"]
f.shape


# In[140]:


combined_data = f.merge(
    v,
    on=["repo_name", "file_name"],
    how="inner",
)

combined_data = combined_data.merge(
    w,
    on=["repo_name", "file_name"],
    how="inner",
)


# In[141]:


combined_data


# In[156]:


# h=test_flakiness[test_flakiness['repo_name']=='fechbmaster_&_3DNIRmapper']
test_flakiness
for i in test_flakiness.index:
    name = test_flakiness["class_name"][i]
    ind = name.rfind(".")
    test_flakiness["class_name"] = name[ind + 1 :]


# In[157]:


test_flakiness


# In[ ]:
