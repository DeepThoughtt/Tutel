from src.utils.files import Files

class Localization:

    def set_language(self, language_code):
        self.localization = Files.read_localization(language_code)

    def __getitem__(self, label):
        return self.localization.get(label, "[MISSING LOCALIZATION]")

localization = Localization()
