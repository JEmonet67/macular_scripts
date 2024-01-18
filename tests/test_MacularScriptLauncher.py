import src.MacularScriptLauncher as msl
import os

# TODO : Test de comparaison de csv obtenu par le script comparé à un csv test conservé
# TODO : Test sans path stim, sans path graph ou sans param=value
# TODO : Faire les tests des erreurs levées dans la classe MacularScriptLauncher
# TODO : Test simulation rétine : 1 seul str sans rien et n_stim=3, 1 sim avec graph/stim/params pas liste,
#  1 avec liste de longueur 1, 3 simulations avec graph, stim et param sous forme de liste.
# TODO : Que se passe t'il si n_sim = 0?

def test_init_macular_script_launcher():
    path_init_file = "/user/jemonet/home/Documents/These/Code/macular_scripts/config_macuscript_default.json"
    macuscript_launcher = msl.MacularScriptLauncher(path_init_file)

    dict_config_test = {'n_sim': 10, 'path_macufile': '/user/jemonet/home/Documents/These/Macular files/Session '
                                                      'retinocortical/RefactoredMacular/diSymGraph_pConnecParams/'
                                                      '9x3,15°_N41x15_nue0_1,86_nui0_12,66_horizWhiteBarMotion0,67x0,9°'
                                                      '_6dps_deltat0,0167_ampOPL0,025.json',
                        'path_macudata': '/user/jemonet/home/Documents/These/Data Macular/RefactoredMacular/'
                                         'diSymGraph_pConnecParams/41x15c/horizontal_white_bar/bar0,67x0,9°_6dps/'
                                         'ampGang/RC_RM_dSGpCP{id_sim}_'
                                         '{name_caract_sim}{value_caract_sim}{unit_caract_sim}_0f.csv',
                        'path_macustim': '/user/jemonet/home/Documents/These/stimuli/stim_'
                                         'database_newName/horizontal_motion/black_background_white_bar/'
                                         'horizontalScreen/2700x945/bar201x270/'
                                         'D187_motion30_trajX-191to2689_Y338to338_0f.mp4',
                        'params_dict': {'virtual_retina/relative_ampOPL': [0.00083, 0.004, 0.0079, 0.0119, 0.0159,
                                                                           0.0198, 0.0292, 0.0333, 0.0375, 0.0417]},
                        'id_sim': ['0012'],
                        'name_caract_sim': 'ampGang',
                        'unit_caract_sim': 'Hz',
                        'value_caract_sim': [1, 5, 10, 15, 20, 25, 35, 40, 45, 50]}

    assert macuscript_launcher.n_sim == 10
    assert macuscript_launcher.path_macufile == ""
    assert macuscript_launcher.path_macudata == ""
    assert macuscript_launcher.path_macustim == ""
    assert macuscript_launcher.path_macugraph == ""
    assert macuscript_launcher.params_dict == {}
    assert macuscript_launcher.dict_formatting_alias == {}
    assert macuscript_launcher.dict_config == dict_config_test

def test_check_params_dict():
    path_init_file = "/user/jemonet/home/Documents/These/Code/macular_scripts/config_macuscript_default.json"
    macuscript_launcher = msl.MacularScriptLauncher(path_init_file)

    dict_config_test = {'n_sim': 8, 'path_macufile': '/user/jemonet/home/Documents/These/Macular files/Session '
                                                     'retinocortical/RefactoredMacular/diSymGraph_pConnecParams/'
                                                     '9x3,15°_N41x15_nue0_1,86_nui0_12,66_horizWhiteBarMotion0,67x0,9°'
                                                     '_6dps_deltat0,0167_ampOPL0,025.json',
                        'path_macudata': '/user/jemonet/home/Documents/These/Data Macular/RefactoredMacular/'
                                         'diSymGraph_pConnecParams/41x15c/horizontal_white_bar/bar0,67x0,9°_6dps/'
                                         'ampGang/RC_RM_dSGpCP{id_sim}_'
                                         '{name_caract_sim}{value_caract_sim}{unit_caract_sim}_0f.csv',
                        'path_macustim': '/user/jemonet/home/Documents/These/stimuli/stim_'
                                         'database_newName/horizontal_motion/black_background_white_bar/'
                                         'horizontalScreen/2700x945/bar201x270/'
                                         'D187_motion30_trajX-191to2689_Y338to338_0f.mp4',
                        'params_dict': {'virtual_retina/relative_ampOPL': [0.00083, 0.004, 0.0079, 0.0119, 0.0159,
                                                                           0.0198, 0.0292, 0.0333],
                                        "BipolarGainControl/h_B": 6.11},
                        'id_sim': ['0012'],
                        'name_caract_sim': 'ampGang',
                        'unit_caract_sim': 'Hz',
                        'value_caract_sim': [1, 5, 10, 15, 20, 25, 35, 40]}

    macuscript_launcher.dict_config = dict_config_test
    assert macuscript_launcher.dict_config["params_dict"]['BipolarGainControl/h_B'] == 6.11


def test_change_dict_config():
    path_init_file = "/user/jemonet/home/Documents/These/Code/macular_scripts/config_macuscript_default.json"
    macuscript_launcher = msl.MacularScriptLauncher(path_init_file)

    dict_config_test = {'n_sim': 8, 'path_macufile': '/user/jemonet/home/Documents/These/Macular files/Session '
                                                      'retinocortical/RefactoredMacular/diSymGraph_pConnecParams/'
                                                      '9x3,15°_N41x15_nue0_1,86_nui0_12,66_horizWhiteBarMotion0,67x0,9°'
                                                      '_6dps_deltat0,0167_ampOPL0,025.json',
                        'path_macudata': '/user/jemonet/home/Documents/These/Data Macular/RefactoredMacular/'
                                         'diSymGraph_pConnecParams/41x15c/horizontal_white_bar/bar0,67x0,9°_6dps/'
                                         'ampGang/RC_RM_dSGpCP{id_sim}_'
                                         '{name_caract_sim}{value_caract_sim}{unit_caract_sim}_0f.csv',
                        'path_macustim': '/user/jemonet/home/Documents/These/stimuli/stim_'
                                         'database_newName/horizontal_motion/black_background_white_bar/'
                                         'horizontalScreen/2700x945/bar201x270/'
                                         'D187_motion30_trajX-191to2689_Y338to338_0f.mp4',
                        'params_dict': {'virtual_retina/relative_ampOPL': [0.00083, 0.004, 0.0079, 0.0119, 0.0159,
                                                                           0.0198, 0.0292, 0.0333]},
                        'id_sim': ['0012'],
                        'name_caract_sim': 'ampGang',
                        'unit_caract_sim': 'Hz',
                        'value_caract_sim': [1, 5, 10, 15, 20, 25, 35, 40]}

    macuscript_launcher.dict_config = dict_config_test
    assert macuscript_launcher.n_sim == 8
    assert macuscript_launcher.dict_config["params_dict"]['virtual_retina/relative_ampOPL'] == [0.00083, 0.004, 0.0079, 0.0119, 0.0159,
                                                                           0.0198, 0.0292, 0.0333]
    assert macuscript_launcher.dict_config["value_caract_sim"] == [1, 5, 10, 15, 20, 25, 35, 40]


def test_next_element():
    path_init_file = "/user/jemonet/home/Documents/These/Code/macular_scripts/config_macuscript_default.json"
    macuscript_launcher = msl.MacularScriptLauncher(path_init_file)

    for i in range(8):
        assert macuscript_launcher.next_element([1, 5, 10, 15, 20, 25, 35, 40], i) == [1, 5, 10, 15, 20, 25, 35, 40][i]

    assert macuscript_launcher.next_element(["Test1"], 5) == "Test1"
    assert macuscript_launcher.next_element("Test2", 0) == "Test2"


def test_refresh_dict_formatting_alias():
    path_init_file = "/user/jemonet/home/Documents/These/Code/macular_scripts/config_macuscript_default.json"
    macuscript_launcher = msl.MacularScriptLauncher(path_init_file)
    dict_formatting_alias0 = {
        'id_sim': '0012',
        'name_caract_sim': 'ampGang',
        'unit_caract_sim': 'Hz',
        'value_caract_sim': 1,
        'virtual_retina/relative_ampOPL_name': 'virtual_retina/relative_ampOPL',
        'virtual_retina/relative_ampOPL_value': "0,00083"
    }
    dict_formatting_alias7 = {
        'id_sim': '0012',
        'name_caract_sim': 'ampGang',
        'unit_caract_sim': 'Hz',
        'value_caract_sim': 40,
        'virtual_retina/relative_ampOPL_name': 'virtual_retina/relative_ampOPL',
        'virtual_retina/relative_ampOPL_value': "0,0333"
    }

    macuscript_launcher.refresh_dict_formatting_alias(0)
    assert macuscript_launcher.dict_formatting_alias == dict_formatting_alias0

    macuscript_launcher.refresh_dict_formatting_alias(7)
    assert macuscript_launcher.dict_formatting_alias == dict_formatting_alias7


def test_refresh_paths():
    # TODO test avec une liste de macugraph pour diversifier un peu plus le test, en faire un autre pour tester l'absence de stim/graph
    path_init_file = "/user/jemonet/home/Documents/These/Code/macular_scripts/config_macuscript_default.json"
    macuscript_launcher = msl.MacularScriptLauncher(path_init_file)

    macuscript_launcher.refresh_dict_formatting_alias(0)
    macuscript_launcher.refresh_paths(0)
    assert macuscript_launcher.path_macufile == '/user/jemonet/home/Documents/These/Macular files/Session ' \
                                                'retinocortical/RefactoredMacular/diSymGraph_pConnecParams/' \
                                                '9x3,15°_N41x15_nue0_1,86_nui0_12,66_horizWhiteBarMotion0,67x0,9°' \
                                                '_6dps_deltat0,0167_ampOPL0,025.json'
    assert macuscript_launcher.path_macudata == '/user/jemonet/home/Documents/These/Data Macular/RefactoredMacular/' \
                                                'diSymGraph_pConnecParams/41x15c/' \
                                                'horizontal_white_bar/bar0,67x0,9°_6dps/' \
                                                'ampGang/RC_RM_dSGpCP0012_ampGang1Hz_0f.csv'
    assert macuscript_launcher.path_macustim == '/user/jemonet/home/Documents/These/stimuli/stim_' \
                                                'database_newName/horizontal_motion/black_background_white_bar/' \
                                                'horizontalScreen/2700x945/bar201x270/' \
                                                'D187_motion30_trajX-191to2689_Y338to338_0f.mp4'
    assert macuscript_launcher.path_macugraph == ""


def test_create_non_existing_path():
    # TODO
    path_init_file = "/user/jemonet/home/Documents/These/Code/macular_scripts/config_macuscript_default.json"
    macuscript_launcher = msl.MacularScriptLauncher(path_init_file)
    path_macudata_file = "/user/jemonet/home/Documents/These/Data Macular/RefactoredMacular/" \
                    "diSymGraph_pConnecParams/41x15c/horizontal_white_bar/bar0,67x0,9°_6dps/" \
                    "ampGang/test/oui/test.py"

    path_macudata_dir = "/user/jemonet/home/Documents/These/Data Macular/RefactoredMacular/" \
                    "diSymGraph_pConnecParams/41x15c/horizontal_white_bar/bar0,67x0,9°_6dps/" \
                    "ampGang/test/oui"

    macuscript_launcher.create_non_existing_path(path_macudata_file)
    assert os.path.isdir(path_macudata_dir)


def test_path_file_to_path_dir():
    path_init_file = "/user/jemonet/home/Documents/These/Code/macular_scripts/config_macuscript_default.json"
    macuscript_launcher = msl.MacularScriptLauncher(path_init_file)
    path_macudata_file = "/user/jemonet/home/Documents/These/Data Macular/RefactoredMacular/" \
                    "diSymGraph_pConnecParams/41x15c/horizontal_white_bar/bar0,67x0,9°_6dps/" \
                    "ampGang/test/test.py"

    path_macudata_dir = "/user/jemonet/home/Documents/These/Data Macular/RefactoredMacular/" \
                    "diSymGraph_pConnecParams/41x15c/horizontal_white_bar/bar0,67x0,9°_6dps/" \
                    "ampGang/test/"

    assert macuscript_launcher.path_file_to_path_dir(path_macudata_file) == path_macudata_dir

def test_refresh_params_dict():
    path_init_file = "/user/jemonet/home/Documents/These/Code/macular_scripts/config_macuscript_default.json"
    macuscript_launcher = msl.MacularScriptLauncher(path_init_file)

    macuscript_launcher.refresh_params_dict(0)
    assert macuscript_launcher.params_dict == {'virtual_retina/relative_ampOPL': 0.00083}

    macuscript_launcher.refresh_params_dict(7)
    assert macuscript_launcher.params_dict == {'virtual_retina/relative_ampOPL': 0.0333}


def test_load_next_sim():
    path_init_file = "/user/jemonet/home/Documents/These/Code/macular_scripts/config_macuscript_default.json"
    macuscript_launcher = msl.MacularScriptLauncher(path_init_file)
    dict_formatting_alias0 = {
        'id_sim': '0012',
        'name_caract_sim': 'ampGang',
        'unit_caract_sim': 'Hz',
        'value_caract_sim': 1,
        'virtual_retina/relative_ampOPL_name': 'virtual_retina/relative_ampOPL',
        'virtual_retina/relative_ampOPL_value': "0,00083"
    }

    macuscript_launcher.load_next_sim(0)

    assert macuscript_launcher.params_dict == {'virtual_retina/relative_ampOPL': 0.00083}

    assert macuscript_launcher.dict_formatting_alias == dict_formatting_alias0


    assert macuscript_launcher.path_macufile == '/user/jemonet/home/Documents/These/Macular files/Session ' \
                                                'retinocortical/RefactoredMacular/diSymGraph_pConnecParams/' \
                                                '9x3,15°_N41x15_nue0_1,86_nui0_12,66_horizWhiteBarMotion0,67x0,9°' \
                                                '_6dps_deltat0,0167_ampOPL0,025.json'
    assert macuscript_launcher.path_macudata == '/user/jemonet/home/Documents/These/Data Macular/RefactoredMacular/' \
                                                'diSymGraph_pConnecParams/41x15c/' \
                                                'horizontal_white_bar/bar0,67x0,9°_6dps/' \
                                                'ampGang/RC_RM_dSGpCP0012_ampGang1Hz_0f.csv'
    assert macuscript_launcher.path_macustim == '/user/jemonet/home/Documents/These/stimuli/stim_' \
                                                'database_newName/horizontal_motion/black_background_white_bar/' \
                                                'horizontalScreen/2700x945/bar201x270/' \
                                                'D187_motion30_trajX-191to2689_Y338to338_0f.mp4'
    assert macuscript_launcher.path_macugraph == ""


def test_make_subprocess():
    path_init_file = "/user/jemonet/home/Documents/These/Code/macular_scripts/config_macuscript_default.json"
    macuscript_launcher = msl.MacularScriptLauncher(path_init_file)

    macuscript_launcher.load_next_sim(0)
    list_subprocess_test = ["macular-batch", "-r",
                       "-f", '/user/jemonet/home/Documents/These/Macular files/Session '
                             'retinocortical/RefactoredMacular/diSymGraph_pConnecParams/'
                             '9x3,15°_N41x15_nue0_1,86_nui0_12,66_horizWhiteBarMotion0,67x0,9°'
                             '_6dps_deltat0,0167_ampOPL0,025.json',
                       "-o", '/user/jemonet/home/Documents/These/Data Macular/RefactoredMacular/'
                             'diSymGraph_pConnecParams/41x15c/'
                             'horizontal_white_bar/bar0,67x0,9°_6dps/'
                             'ampGang/RC_RM_dSGpCP0012_ampGang1Hz_0f.csv',
                       "-s", '/user/jemonet/home/Documents/These/stimuli/stim_'
                             'database_newName/horizontal_motion/black_background_white_bar/'
                             'horizontalScreen/2700x945/bar201x270/'
                             'D187_motion30_trajX-191to2689_Y338to338_0f.mp4',
                       "-p", "virtual_retina/relative_ampOPL=0.00083"]

    assert macuscript_launcher.make_subprocess() == list_subprocess_test


#def test_run():
    # TODO


#def test_multiple_run():
    # TODO
