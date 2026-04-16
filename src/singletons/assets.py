from src.utils.files import Files

class Assets:

    def __init__(self):
        self.icons = {}

    def load_assets(self, assets_dict):
        self.icons = assets_dict["icons"]

assets = Assets()
