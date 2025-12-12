import src.TextFormatting as tf


def test_create_text_formatting():
    """Test to check TextFormatting can be created and to display their attributes."""
    dict_formatting = {"num_sim": "0012",
                       "name_caract_sim": "ampGang",
                       "unit_caract_sim": "Hz",
                       "values_caract_sim": 1
                       }

    path_macudata = "~/Documents/These/Data Macular/RefactoredMacular/diSymGraph_pConnecParams/" \
                    "41x15c/horizontal_white_bar/bar0,67x0,9°_6dps/ampGang/RC_RM_dSGpCP{num_sim}_{name_caract_sim}" \
                    "{value_caract_sim}{unit_caract_sim}_0f.csv"

    text_formatting = tf.TextFormatting(path_macudata, dict_formatting)
    assert text_formatting.str_to_form == path_macudata
    assert text_formatting.formatting_dict == dict_formatting


def test_modify_text_formatting_params():
    """Test to check that getters for TextFormatting are working"""
    dict_formatting = {"num_sim": "0012",
                       "name_caract_sim": "ampGang",
                       "unit_caract_sim": "Hz",
                       "values_caract_sim": 1
                       }
    dict_formatting2 = {"num_sim": "0011",
                        "name_caract_sim": "barSpeed",
                        "unit_caract_sim": "dps",
                        "values_caract_sim": 6
                        }

    path_macudata = "~/Documents/These/Data Macular/RefactoredMacular/diSymGraph_pConnecParams/" \
                    "41x15c/horizontal_white_bar/bar0,67x0,9°_6dps/ampGang/RC_RM_dSGpCP{num_sim}_{name_caract_sim}" \
                    "{value_caract_sim}{unit_caract_sim}_0f.csv"
    path_macudata2 = "~/Documents/These/Data Macular/RefactoredMacular/diSymGraph_pConnecParams/" \
                     "41x15c/horizontal_white_bar/bar0,67x0,9°_6dps/ampGang/RC_RM_dSGpCP{num_sim}_{name_caract_sim}" \
                     "{value_caract_sim}{unit_caract_sim}_3f.csv"

    text_formatting = tf.TextFormatting(path_macudata, dict_formatting)
    text_formatting.str_to_form = path_macudata2
    text_formatting.formatting_dict = dict_formatting2
    assert text_formatting.str_to_form == path_macudata2
    assert text_formatting.formatting_dict == dict_formatting2


def test_to_str():
    """Test to verify that the to_str() allow to well formate the str."""
    dict_formatting = {"num_sim": "0012",
                       "name_caract_sim": "ampGang",
                       "unit_caract_sim": "Hz",
                       "value_caract_sim": 1
                       }

    path_macudata = "~/Documents/These/Data Macular/RefactoredMacular/diSymGraph_pConnecParams/" \
                    "41x15c/horizontal_white_bar/bar0,67x0,9°_6dps/ampGang/RC_RM_dSGpCP{num_sim}_{name_caract_sim}" \
                    "{value_caract_sim}{unit_caract_sim}_0f.csv"

    text_formatting = tf.TextFormatting(path_macudata, dict_formatting)
    assert text_formatting.to_str() == "~/Documents/These/Data Macular/RefactoredMacular/" \
                                       "diSymGraph_pConnecParams/41x15c/horizontal_white_bar/bar0,67x0,9°_6dps/" \
                                       "ampGang/RC_RM_dSGpCP0012_ampGang1Hz_0f.csv"
