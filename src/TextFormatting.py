import re


class TextFormatting:
    """Character string that contains some substring "{alias_format}" to replace.

    Each substring "{alias_format}" have different alias name and all are present as keys in a formatting dictionary.
    They are associated to a value corresponding to a str used to replace it and formate the string.

    Parameters
    ----------
    str_to_form : str
        String chain with "{alias_format}" to formate.

    formatting_dict : dict
        Dictionary that associate "alias_format" keys to string to add in the string to form.

    """
    def __init__(self, str_to_form, formatting_dict={}):
        self.formatting_dict = formatting_dict
        self.str_to_form = str_to_form
        self.formatting_reg = re.compile("("+re.escape("{")+".*?"+re.escape("}")+")")

    @property
    def str_to_form(self):
        """Getter for the str_to_form attribute."""
        return self._str_to_form

    @str_to_form.setter
    def str_to_form(self, text):
        """Setter for the str_to_form attribute. Check that it is a str."""

        if type(text) != str:
            raise TypeError("Text to form have to be a string.")
        self._str_to_form = text

    @property
    def formatting_dict(self):
        """Getter for the formatting_dict attribute."""
        return self._formatting_dict

    @formatting_dict.setter
    def formatting_dict(self, dictionary):
        """Setter for the str_to_form attribute. Check that it is a dict."""
        if type(dictionary) != dict:
            raise TypeError("Formatting dict have to be a dictionary.")
        self._formatting_dict = dictionary

    def to_str(self):
        """Formate the string_to_form attribute based on the formatting dictionary.

        Each "{alias_format}" present in the str are replace by the value of the alias_format key in the formatting
        dictionary. If no corresponding key is in the dictionary, the "{alias_format}" is kept and a warning launch.

        Returns
        ----------
        formatted_str : str
            Str formatted with all "{alias_format}" replaced.

        """
        formatted_str = self.str_to_form
        list_formatting_alias = self.formatting_reg.findall(self.str_to_form)

        for alias in list_formatting_alias:
            try:
                formatted_str = formatted_str.replace(alias, f"{self.formatting_dict[alias[1:-1]]}")
            except KeyError:
                print(f"Warning : The key {alias} doesn't exist in the formatting dict.")

        return formatted_str

    def __repr__(self):
        return self.to_str()
