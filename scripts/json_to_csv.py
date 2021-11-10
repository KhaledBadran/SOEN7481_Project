# %%

from dataclasses import dataclass
import json
from pathlib import Path
from typing import List, Optional, Dict

import pandas as pd
from dataclasses_json import dataclass_json, LetterCase
import glob
import os
import tqdm


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DetectorResult:
    name: str
    has_smell: bool
    detail: Optional[int] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TestCaseResult:
    name: str
    detector_results: List[DetectorResult]
    number_of_methods: Optional[int] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FileResult:
    name: str
    test_cases: List[TestCaseResult]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Result:
    result: List[FileResult]


TRUE_FALSE_SMELLS = [
    "EmptyTest",
    "ExceptionHandling",
    "IgnoredTest",
    "MagicNumberTest",
    "SleepyTest",
    "SuboptimalAssert",
    "RedundantPrint",
]

ALL_SMELLS = [
    "AssertionRoulette",
    "ConditionalTestLogic",
    "ConstructorInitialization",
    "DefaultTest",
    "DuplicateAssertion",
    "EmptyTest",
    "ExceptionHandling",
    "GeneralFixture",
    "IgnoredTest",
    "LackCohesion",
    "MagicNumberTest",
    "ObscureInLineSetup",
    "RedundantAssertion",
    "RedundantPrint",
    "SleepyTest",
    "SuboptimalAssert",
    "TestMaverick",
    "UnknownTest",
]


def find_true_functions(smell_details: List[List]) -> List[str]:
    """
    Given the details from a true/false smell, this method returns the functions that have the smell
    """
    return [item[0] for item in smell_details if item[1] == "true"]


def find_ObscureInLineSetup_functions(smell_details: List[List]) -> List[str]:
    """
    Given the details from an ObscureInLineSetup smell, this method returns the functions that have the smell
    """
    return [item[0] for item in smell_details if len(item[1]) >= 11]


def find_UnknownTest_functions(smell_details: List[List]) -> List[str]:
    """
    Given the details from an UnknownTest smell, this method returns the functions that have the smell
    """
    return [item[0] for item in smell_details if item[1] == "0"]


def find_LackCohesion_functions(smell_details: Dict) -> List[str]:
    """
    Given the details from an LackCohesion smell, this method returns the functions that have the smell
    """
    func_names = list()
    threshold = smell_details["threshold"]
    cosine_similarity_scores = smell_details["cosineSimilarityScores"]

    for cosine_similarity_score in cosine_similarity_scores:
        # if the similarity is lower than the threshold, append both functions (similar functions)
        if cosine_similarity_score[2] < threshold:
            func_names.append(cosine_similarity_score[0])
            func_names.append(cosine_similarity_score[1])

    return list(set(func_names))


def find_GeneralFixture_functions(smell_details: List[List]) -> List[str]:
    """
    Given the details from an GeneralFixture smell, this method returns the functions that have the smell
    """
    return [item[0] for item in smell_details if len(item[1]) > 0]


def find_AssertionRoulette_functions(smell_details: Dict) -> List[str]:
    """
    Given the details from an AssertionRoulette smell, this method returns the functions that have the smell
    """
    assertion_calls: List = smell_details["assertionCallsInTests"]
    assertion_statements: List = smell_details["assertStatementsInTests"]

    func_names = list()

    for assertion_call in assertion_calls:
        calls = assertion_call[1].replace("]", "").replace("[", "").split(",")
        if len(calls) > 1:
            func_names.append(assertion_call[0])

    for assertion_statement in assertion_statements:
        statements = assertion_statement[1].replace("]", "").replace("[", "").split(",")
        if len(statements) > 1:
            func_names.append(assertion_statement[0])

    return list(set(func_names))


def find_RedundantAssertion_functions(smell_details: Dict) -> List[str]:
    """
    Given the details from an RedundantAssertion smell, this method returns the functions that have the smell
    """
    redundant_calls: List = smell_details["testMethodHaveRedundantAssertCall"]
    redundant_statements: List = smell_details["testMethodHaveRedundantAssertStatement"]

    func_names = list()
    func_names += [call[0] for call in redundant_calls if call[1] != "0"]
    func_names += [
        statement[0] for statement in redundant_statements if statement[1] != "0"
    ]

    return list(set(func_names))


def find_ConditionalTestLogic_functions(smell_details: Dict) -> List[str]:
    """
    Given the details from an ConditionalTestLogic smell, this method returns the functions that have the smell
    """
    all_functions: List = (
        smell_details["testHasConditionalTestLogic"]
        + smell_details["testHasComprehension"]
    )

    return list({item[0] for item in all_functions if item[1] == "true"})


def find_DuplicateAssertion_functions(smell_details: Dict) -> List[str]:
    """
    Given the details from an ConditionalTestLogic smell, this method returns the functions that have the smell
    """
    all_functions: List = (
        smell_details["testHasDuplicateAssertCall"]
        + smell_details["testHasDuplicateAssertStatement"]
    )

    return list({item[0] for item in all_functions if item[1] == "true"})


def create_class_function_dict() -> dict:
    return dict((test_smell, False) for test_smell in ALL_SMELLS)


def find_smelly_functions(test_smell: str, test_smell_details) -> List[str]:
    if test_smell in TRUE_FALSE_SMELLS:
        return find_true_functions(test_smell_details)
    elif test_smell == "ObscureInLineSetup":
        return find_ObscureInLineSetup_functions(test_smell_details)
    elif test_smell == "UnknownTest":
        return find_UnknownTest_functions(test_smell_details)
    elif test_smell == "LackCohesion":
        return find_LackCohesion_functions(test_smell_details)
    elif test_smell == "GeneralFixture":
        return find_GeneralFixture_functions(test_smell_details)
    elif test_smell == "AssertionRoulette":
        return find_AssertionRoulette_functions(test_smell_details)
    elif test_smell == "RedundantAssertion":
        return find_RedundantAssertion_functions(test_smell_details)
    elif test_smell == "ConditionalTestLogic":
        return find_ConditionalTestLogic_functions(test_smell_details)
    elif test_smell == "DuplicateAssertion":
        return find_DuplicateAssertion_functions(test_smell_details)

    return []


def extract_JSON_info(path_to_json_file: Path) -> List:
    with path_to_json_file.open() as f:
        json_str = f.read()

    json_root = json.loads(json_str)
    if isinstance(json_root, list):
        json_root = {"result": json_root}
        result = Result.from_json(json.dumps(json_root))
    else:
        result = Result.from_json(json_str)
    json_info = []
    for test_file, test_case in (
        (tf, tc) for tf in result.result for tc in tf.test_cases
    ):
        test_case_functions = {}
        test_case_information = [path_to_json_file.stem, test_file.name, test_case.name]

        detector_results = sorted(test_case.detector_results, key=lambda dr: dr.name)

        smelly_results = (result for result in detector_results if result.has_smell)

        for detector_result in smelly_results:

            smelly_functions = find_smelly_functions(
                detector_result.name, detector_result.detail
            )

            for smelly_function in smelly_functions:

                if smelly_function not in test_case_functions.keys():
                    test_case_functions[smelly_function] = create_class_function_dict()

                test_case_functions[smelly_function][detector_result.name] = True

        for test_case_function, test_smells in test_case_functions.items():
            # line =
            line = test_case_information.copy()
            line.append(test_case_function)
            for test_smell in test_smells:
                line.append(test_smells[test_smell])
            # lines.append(line)
            json_info.append(line.copy())

    return json_info.copy()


def save_to_csv(data: List, output_dir: Path, file_name: str) -> None:
    if len(data) != 0:
        df = pd.DataFrame(
            data,
            columns=["repo_name", "test_file", "test_case", "test_function"]
            + ALL_SMELLS,
        )
        df.to_csv(output_dir / f"{file_name}.csv", index=False)

    return


def parse_JSON_to_csv(json_files_dir: Path, csv_file_dir: Path) -> None:
    JSON_FILE_PATHS = [
        p for p in json_files_dir.iterdir() if p.is_file() and p.suffix == ".json"
    ]

    count = 0
    REPO_DATA_FRAMES = []
    REPO_RESULTS = []

    for json_file_path in JSON_FILE_PATHS:
        json_data = extract_JSON_info(json_file_path)
        save_to_csv(json_data, csv_file_dir, json_file_path.stem)
        count += 1 if len(json_data) != 0 else 0

    print(f"Converted {count} JSON file(s).")


def main():
    json_dir = Path("../data/repos_jsons")
    csv_dir = Path("../data/repos_csvs")
    parse_JSON_to_csv(json_dir, csv_dir)


# JSON_FILES_DIR = Path("../data/sample_jsons")
# CSV_FILES_DIR = Path("../data/sample_csvs")
# Aggregation below
# aggregated_lines = []
# for repo_df, result in zip(REPO_DATA_FRAMES, REPO_RESULTS):
#     if len(repo_df) == 0:
#         continue
#     repo_name = repo_df["repo_name"][0]
#     repo_test_file_count = len(result.result)
#     repo_test_case_count = sum(len(tf.test_cases) for tf in result.result)
#     repo_test_method_count = sum(
#         tc.number_of_methods for tf in result.result for tc in tf.test_cases
#     )
#     line = [
#         repo_name,
#         repo_test_file_count,
#         repo_test_case_count,
#         repo_test_method_count,
#     ]
#
#     for smell in ALL_SMELLS:
#         line.append(sum(repo_df[smell]))
#     aggregated_lines.append(line)
#
# aggregated_df = pd.DataFrame(
#     aggregated_lines,
#     columns=["repo_name", "test_file_count", "test_case_count", "test_method_count"]
#     + ALL_SMELLS,
# )
# aggregated_df.to_csv(CSV_FILES_DIR / "aggregated.csv", index=False)
# print("Aggregated result generated")
#
# # def aggregate_csvs_to_one_csv():
# #     DETECTOR_OUTPUT = Path("../data/sample_csvs")
# file_path = os.path.join(CSV_FILES_DIR, "combined_csv.csv")
#
# # remove the file of already exists
# if os.path.exists(file_path):
#     os.remove(file_path)
#
# df_list = []
# all_files = glob.glob(os.path.join(CSV_FILES_DIR, "*.csv"))
#
# for csv_file in tqdm.tqdm(all_files):
#     df = pd.read_csv(csv_file)
#     df_list.append(df)
# result = pd.concat(df_list)
# result = result.reset_index(drop=True)
# print(result.shape)
# result.to_csv(file_path, index=False)


if __name__ == "__main__":
    main()
