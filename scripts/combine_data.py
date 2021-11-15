# -*- coding: utf-8 -*-

"""
This script combines the test smell, vocabulary, and flakiness data all into a single csv
"""
import os
from typing import List

import requests
from pathlib import Path
import pandas as pd
from numpy import random
from time import sleep
from tqdm import tqdm
from bs4 import UnicodeDammit
from typeguard import typechecked

DATA_FOLDER: Path = Path("..", "data")
VOCABULARY_DATA_FILE: Path = Path("vocabulary", "data_file.csv")
TEST_SMELLS_DATA_FILE: Path = Path("repos_csvs", "merged_csvs.csv")
TEST_FLAKINESS_DATA_FILE: Path = Path("python_flaky_tests", "active_repos_clean.csv")
OUTPUT_DATA_FILE: Path = Path("oracle", "oracle.csv")
REPOS_DIR: Path = Path("repos")


# From file path in vocabulary dataframe (ex: https://github.com/tensorflow/tensorflow)
# get the repo_name (tensorflow/tensorflow)
@typechecked
def get_repo_name_from_url(url: str) -> str:
    parts = url.split("/")
    return parts[-2] + "_&_" + parts[-1]


# replace the '/' with '_&_' in the file_names in the test_flakiness data (ex: tests/unit/test_geometry.py becomes
# tests_&_unit_&_test_geometry.py)
@typechecked
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
    test_smells_df_: pd.DataFrame = pd.read_csv(test_smell_data_file, index_col=0)

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

    # find downloaded repos
    repos_path: Path = Path.joinpath(DATA_FOLDER, REPOS_DIR)

    # get the direct subdirectories from the repos directory in order to find the names of all projects
    all_repos: List[str] = [f.name for f in os.scandir(repos_path) if f.is_dir()]

    # filter dataframe to keep only repos that appear as a subdirectory (downloaded repos)
    test_flakiness_df_ = test_flakiness_df_[
        test_flakiness_df_["repo_name"].isin(all_repos)
    ]

    test_flakiness_df_["file_name"] = test_flakiness_df_["file_name"].astype(str)

    # keep releavant columns only
    test_flakiness_df_ = test_flakiness_df_[
        ["repo_name", "file_name", "class_name", "func_name", "flaky"]
    ]

    return test_flakiness_df_.copy()


if __name__ == "__main__":
    vocabulary: pd.DataFrame = create_vocabulary_df()
    test_smells: pd.DataFrame = create_test_smells_df()
    test_flakiness: pd.DataFrame = create_test_flakiness_df()

    # Merge vocabulary and flakiness first
    test_info: pd.DataFrame = vocabulary.merge(
        test_flakiness,
        on=["repo_name", "file_name", "class_name", "func_name"],
        how="inner",
    )

    # Add test smells where appropriate
    test_info_and_flakiness: pd.DataFrame = test_smells.merge(
        test_info, on=["repo_name", "file_name", "class_name", "func_name"], how="right"
    )

    # Add False for test smells that are empty
    test_info_and_flakiness.fillna(False, inplace=True)

    # Save the results
    test_info_and_flakiness.to_csv(str(Path(DATA_FOLDER, OUTPUT_DATA_FILE)))
