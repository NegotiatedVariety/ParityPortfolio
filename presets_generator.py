import json

class Preset:
    """

    """
    def __init__(self, name, domestic_stock, international_stock, bonds, money_market):
        """

        """
        self._preset_dict = {
            "preset_name": name,
            "domestic_stock": domestic_stock,
            "international_stock": international_stock,
            "bonds": bonds,
            "money_market": money_market
        }

    def get_preset_dict(self):
        """

        """
        return self._preset_dict


class PresetList:
    """

    """

    def __init__(self):
        self._preset_dict = {}
        self._preset_list = []

    def add_preset(self, name, domestic_stock, international_stock, bonds, money_market):
        """

        """
        if name in self._preset_dict:
            overwrite = input("Warning:" + name + " already exists in JSON. Overwrite? (y/n)")

            if overwrite == "n":
                return

        else:
            self._preset_dict[name] = Preset(name, domestic_stock, international_stock, bonds, money_market)

    def delete_preset(self, name):
        """

        """
        del self._preset_dict[name]

    def save_as_json(self, file_name):
        """

        """
        self._preset_list.clear()

        for preset in self._preset_dict.values():
            self._preset_list.append(preset.get_preset_dict())

        with open(file_name, "w") as outfile:
            json.dump(self._preset_list, outfile)

    def read_json(self, file_name):
        """

        """

        with open(file_name, "r") as infile:
            preset_list = json.load(infile)

        self._preset_dict.clear()

        for preset in preset_list:
            self._preset_dict[preset["preset_name"]] = Preset(preset["preset_name"], preset["domestic_stock"], preset["international_stock"], preset["bonds"], preset["money market"])
