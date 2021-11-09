from scripts.json_to_csv import extract_JSON_info, ALL_SMELLS
from pathlib import Path
import pandas as pd


def test_SleepyTest_smell():
    json_path = Path('../../data/Two_Samples_Per_Smell/SleepyTest/KD-Group___Carrier.Sample.json')
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(json_info, columns=["repo_name", "test_file", "test_case", 'test_function'] + ALL_SMELLS)
    assert len(df[df.SleepyTest == True]) == 4

    json_path = Path('../../data/Two_Samples_Per_Smell/SleepyTest/party98___Python-Parallel-Downloader.json')
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(json_info, columns=["repo_name", "test_file", "test_case", 'test_function'] + ALL_SMELLS)
    assert len(df[df.SleepyTest == True]) == 15


def test_ObscureInLineSetup_smell():
    json_path = Path('../../data/Two_Samples_Per_Smell/ObscureInLineSetup/apmechev___GRID_LRT.json')
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(json_info, columns=["repo_name", "test_file", "test_case", 'test_function'] + ALL_SMELLS)
    assert len(df[df.ObscureInLineSetup == True]) == 1
    assert 'test_stagingrc' in df.test_function[df.ObscureInLineSetup == True].to_list()

    json_path = Path('../../data/Two_Samples_Per_Smell/ObscureInLineSetup/mit-crpg___OpenMOC.json')
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(json_info, columns=["repo_name", "test_file", "test_case", 'test_function'] + ALL_SMELLS)
    assert len(df[df.ObscureInLineSetup == True]) == 3
    assert 'test_complement' in df.test_function[df.ObscureInLineSetup == True].to_list()


def test_UnknownTest_smell():
    json_path = Path('../../data/Two_Samples_Per_Smell/UnknownTest/bitcoin-core___HWI.json')
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(json_info, columns=["repo_name", "test_file", "test_case", 'test_function'] + ALL_SMELLS)
    assert len(df[df.UnknownTest == True]) == 2
    assert 'test_sign_msg' in df.test_function[df.UnknownTest == True].to_list()

    json_path = Path('../../data/Two_Samples_Per_Smell/UnknownTest/PmagPy___PmagPy.json')
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(json_info, columns=["repo_name", "test_file", "test_case", 'test_function'] + ALL_SMELLS)
    assert len(df[df.UnknownTest == True]) == 15
    assert 'test_propagate_ages_extra_location_rows' in df.test_function[df.UnknownTest == True].to_list()
    assert 'test_cmd_line' in df.test_function[df.UnknownTest == True].to_list()
    assert 'test_guis' in df.test_function[df.UnknownTest == True].to_list()


def test_GeneralFixture_smell():
    json_path = Path('../../data/Two_Samples_Per_Smell/GeneralFixture/fabioz___PyDev.Debugger.json')
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(json_info, columns=["repo_name", "test_file", "test_case", 'test_function'] + ALL_SMELLS)
    # assert len(df[df.GeneralFixture == True]) == 15
    assert 'test___is_valid_py_file' in df.test_function[df.GeneralFixture == True].to_list()
    assert 'test_finding_tests_with_regex_filters' not in df.test_function[df.GeneralFixture == True].to_list()

    json_path = Path('../../data/Two_Samples_Per_Smell/GeneralFixture/JohnVolk___PRMS-Python.json')
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(json_info, columns=["repo_name", "test_file", "test_case", 'test_function'] + ALL_SMELLS)
    assert 'test_simulation_no_simdir' in df.test_function[df.GeneralFixture == True].to_list()
    assert 'test_modify_params' not in df.test_function[df.GeneralFixture == True].to_list()


def test_AssertionRoulette_smell():
    json_path = Path('../../data/Two_Samples_Per_Smell/AssertionRoulette/DusanMadar___PySyncDroid.json')
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(json_info, columns=["repo_name", "test_file", "test_case", 'test_function'] + ALL_SMELLS)
    # assert len(df[df.AssertionRoulette == True]) == 15
    assert 'test_parser' not in df.test_function[df.AssertionRoulette == True].to_list()
    assert 'test_parser_unmatched' in df.test_function[df.AssertionRoulette == True].to_list()

    json_path = Path('../../data/Two_Samples_Per_Smell/AssertionRoulette/gapml___CV.json')
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(json_info, columns=["repo_name", "test_file", "test_case", 'test_function'] + ALL_SMELLS)
    assert 'test_008' not in df.test_function[df.AssertionRoulette == True].to_list()
    assert 'test_038' in df.test_function[df.AssertionRoulette == True].to_list()


def test_RedundantAssertion_smell():
    json_path = Path('../../data/Two_Samples_Per_Smell/RedundantAssertion/MarniTausen___Greenotyper.json')
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(json_info, columns=["repo_name", "test_file", "test_case", 'test_function'] + ALL_SMELLS)
    assert len(df[df.RedundantAssertion == True]) == 4
    assert 'test_circular_hsv_figure' not in df.test_function[df.RedundantAssertion == True].to_list()
    assert 'test_defaults' in df.test_function[df.RedundantAssertion == True].to_list()

    json_path = Path('../../data/Two_Samples_Per_Smell/RedundantAssertion/whiteclover___Choco.json')
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(json_info, columns=["repo_name", "test_file", "test_case", 'test_function'] + ALL_SMELLS)
    assert 'test_check_not_found' not in df.test_function[df.RedundantAssertion == True].to_list()
    assert 'test_no_lookup' in df.test_function[df.RedundantAssertion == True].to_list()