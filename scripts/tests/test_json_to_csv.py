from scripts.json_to_csv import extract_JSON_info, ALL_SMELLS
from pathlib import Path
import pandas as pd


def test_SleepyTest_smell():
    json_path = Path(
        "../../data/Two_Samples_Per_Smell/SleepyTest/KD-Group___Carrier.Sample.json"
    )
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(
        json_info,
        columns=["repo_name", "test_file", "test_case", "test_function"] + ALL_SMELLS,
    )
    assert len(df[df.SleepyTest == True]) == 4

    json_path = Path(
        "../../data/Two_Samples_Per_Smell/SleepyTest/party98___Python-Parallel-Downloader.json"
    )
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(
        json_info,
        columns=["repo_name", "test_file", "test_case", "test_function"] + ALL_SMELLS,
    )
    assert len(df[df.SleepyTest == True]) == 15


def test_ObscureInLineSetup_smell():
    json_path = Path(
        "../../data/Two_Samples_Per_Smell/ObscureInLineSetup/apmechev___GRID_LRT.json"
    )
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(
        json_info,
        columns=["repo_name", "test_file", "test_case", "test_function"] + ALL_SMELLS,
    )
    assert len(df[df.ObscureInLineSetup == True]) == 1
    assert "test_stagingrc" in df.test_function[df.ObscureInLineSetup == True].to_list()

    json_path = Path(
        "../../data/Two_Samples_Per_Smell/ObscureInLineSetup/mit-crpg___OpenMOC.json"
    )
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(
        json_info,
        columns=["repo_name", "test_file", "test_case", "test_function"] + ALL_SMELLS,
    )
    assert len(df[df.ObscureInLineSetup == True]) == 3
    assert (
        "test_complement" in df.test_function[df.ObscureInLineSetup == True].to_list()
    )


def test_UnknownTest_smell():
    json_path = Path(
        "../../data/Two_Samples_Per_Smell/UnknownTest/bitcoin-core___HWI.json"
    )
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(
        json_info,
        columns=["repo_name", "test_file", "test_case", "test_function"] + ALL_SMELLS,
    )
    assert len(df[df.UnknownTest == True]) == 2
    assert "test_sign_msg" in df.test_function[df.UnknownTest == True].to_list()

    json_path = Path(
        "../../data/Two_Samples_Per_Smell/UnknownTest/PmagPy___PmagPy.json"
    )
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(
        json_info,
        columns=["repo_name", "test_file", "test_case", "test_function"] + ALL_SMELLS,
    )
    assert len(df[df.UnknownTest == True]) == 15
    assert (
        "test_propagate_ages_extra_location_rows"
        in df.test_function[df.UnknownTest == True].to_list()
    )
    assert "test_cmd_line" in df.test_function[df.UnknownTest == True].to_list()
    assert "test_guis" in df.test_function[df.UnknownTest == True].to_list()


def test_GeneralFixture_smell():
    json_path = Path(
        "../../data/Two_Samples_Per_Smell/GeneralFixture/fabioz___PyDev.Debugger.json"
    )
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(
        json_info,
        columns=["repo_name", "test_file", "test_case", "test_function"] + ALL_SMELLS,
    )
    # assert len(df[df.GeneralFixture == True]) == 15
    assert (
        "test___is_valid_py_file"
        in df.test_function[df.GeneralFixture == True].to_list()
    )
    assert (
        "test_finding_tests_with_regex_filters"
        not in df.test_function[df.GeneralFixture == True].to_list()
    )

    json_path = Path(
        "../../data/Two_Samples_Per_Smell/GeneralFixture/JohnVolk___PRMS-Python.json"
    )
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(
        json_info,
        columns=["repo_name", "test_file", "test_case", "test_function"] + ALL_SMELLS,
    )
    assert (
        "test_simulation_no_simdir"
        in df.test_function[df.GeneralFixture == True].to_list()
    )
    assert (
        "test_modify_params"
        not in df.test_function[df.GeneralFixture == True].to_list()
    )


def test_AssertionRoulette_smell():
    json_path = Path(
        "../../data/Two_Samples_Per_Smell/AssertionRoulette/DusanMadar___PySyncDroid.json"
    )
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(
        json_info,
        columns=["repo_name", "test_file", "test_case", "test_function"] + ALL_SMELLS,
    )
    # assert len(df[df.AssertionRoulette == True]) == 15
    assert "test_parser" not in df.test_function[df.AssertionRoulette == True].to_list()
    assert (
        "test_parser_unmatched"
        in df.test_function[df.AssertionRoulette == True].to_list()
    )

    json_path = Path(
        "../../data/Two_Samples_Per_Smell/AssertionRoulette/gapml___CV.json"
    )
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(
        json_info,
        columns=["repo_name", "test_file", "test_case", "test_function"] + ALL_SMELLS,
    )
    assert "test_008" not in df.test_function[df.AssertionRoulette == True].to_list()
    assert "test_038" in df.test_function[df.AssertionRoulette == True].to_list()


def test_RedundantAssertion_smell():
    json_path = Path(
        "../../data/Two_Samples_Per_Smell/RedundantAssertion/MarniTausen___Greenotyper.json"
    )
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(
        json_info,
        columns=["repo_name", "test_file", "test_case", "test_function"] + ALL_SMELLS,
    )
    assert len(df[df.RedundantAssertion == True]) == 4
    assert (
        "test_circular_hsv_figure"
        not in df.test_function[df.RedundantAssertion == True].to_list()
    )
    assert "test_defaults" in df.test_function[df.RedundantAssertion == True].to_list()

    json_path = Path(
        "../../data/Two_Samples_Per_Smell/RedundantAssertion/whiteclover___Choco.json"
    )
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(
        json_info,
        columns=["repo_name", "test_file", "test_case", "test_function"] + ALL_SMELLS,
    )
    assert (
        "test_check_not_found"
        not in df.test_function[df.RedundantAssertion == True].to_list()
    )
    assert "test_no_lookup" in df.test_function[df.RedundantAssertion == True].to_list()


def test_ConditionalTestLogic_smell():
    json_path = Path(
        "../../data/Two_Samples_Per_Smell/ConditionalTestLogic/fabioz___PyDev.Debugger.json"
    )
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(
        json_info,
        columns=["repo_name", "test_file", "test_case", "test_function"] + ALL_SMELLS,
    )
    # assert len(df[df.ConditionalTestLogic == True]) == 4
    assert (
        "test_search_on_jython"
        not in df.test_function[df.ConditionalTestLogic == True].to_list()
    )
    assert (
        "test_completion_sockets_and_messages"
        in df.test_function[df.ConditionalTestLogic == True].to_list()
    )

    json_path = Path(
        "../../data/Two_Samples_Per_Smell/ConditionalTestLogic/SUNCAT-Center___CatLearn.json"
    )
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(
        json_info,
        columns=["repo_name", "test_file", "test_case", "test_function"] + ALL_SMELLS,
    )
    assert (
        "test_pareto" not in df.test_function[df.ConditionalTestLogic == True].to_list()
    )
    assert (
        "test_constrained_ads"
        in df.test_function[df.ConditionalTestLogic == True].to_list()
    )


def test_DuplicateAssertion_smell():
    json_path = Path(
        "../../data/Two_Samples_Per_Smell/DuplicateAssertion/KD-Group___Half.Sample.json"
    )
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(
        json_info,
        columns=["repo_name", "test_file", "test_case", "test_function"] + ALL_SMELLS,
    )
    # assert len(df[df.DuplicateAssertion == True]) == 4
    assert (
        "test_mock_voltage_set_get"
        not in df.test_function[df.DuplicateAssertion == True].to_list()
    )
    assert (
        "test_mock_tau_set_get"
        in df.test_function[df.DuplicateAssertion == True].to_list()
    )

    json_path = Path(
        "../../data/Two_Samples_Per_Smell/DuplicateAssertion/ornlneutronimaging___NeuNorm.json"
    )
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(
        json_info,
        columns=["repo_name", "test_file", "test_case", "test_function"] + ALL_SMELLS,
    )
    assert (
        "test_setting_roi_x0_y0_x1_y1"
        not in df.test_function[df.DuplicateAssertion == True].to_list()
    )
    assert (
        "test_x_and_y_correctly_sorted"
        in df.test_function[df.DuplicateAssertion == True].to_list()
    )


def test_RedundantPrint_smell():
    json_path = Path(
        "../../data/Two_Samples_Per_Smell/RedundantPrint/al-niessner___DAWGIE.json"
    )
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(
        json_info,
        columns=["repo_name", "test_file", "test_case", "test_function"] + ALL_SMELLS,
    )
    # assert len(df[df.RedundantPrint == True]) == 4
    assert "test_schedule" not in df.test_function[df.RedundantPrint == True].to_list()
    assert "test_call" in df.test_function[df.RedundantPrint == True].to_list()

    json_path = Path(
        "../../data/Two_Samples_Per_Smell/RedundantPrint/Hoeppke___PyODESolver.json"
    )
    json_info = extract_JSON_info(json_path)
    df = pd.DataFrame(
        json_info,
        columns=["repo_name", "test_file", "test_case", "test_function"] + ALL_SMELLS,
    )

    assert (
        "test_convergence_rate"
        in df.loc[
            (df.RedundantPrint == True) & (df.test_case == "TestBDF6Example")
        ].test_function.to_list()
    )
    assert (
        "test_convergence_rate"
        not in df.loc[
            (df.RedundantPrint == True) & (df.test_case == "TestGaussLegendre")
        ].test_function.to_list()
    )
    assert "test_accuracy01" in df.test_function[df.RedundantPrint == True].to_list()
