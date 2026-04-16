from src.consts.languages import Languages
from src.utils.files import Files

class SettingsChecker:

    @staticmethod
    def fix_and_save(settings):
        default_settings = Files.read_default_settings()

        # If something is missing we add it back
        for setting_key in default_settings:
            if setting_key not in settings:
                settings[setting_key] = default_settings[setting_key]

        # We always update these at startup to be sure they are correct
        settings["version"] = default_settings["version"]
        settings["appName"] = default_settings["appName"]

        if not Languages.is_valid(settings["language"]):
            settings["language"] = default_settings["language"]

        if settings["createCrashReports"] not in [True, False]:
            settings["createCrashReports"] = default_settings["createCrashReports"]

        Files.write_settings(settings)
