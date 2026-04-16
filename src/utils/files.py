import datetime
import json
import os
import sys
import pathlib

class Files:

    @staticmethod
    def get_data_base_path():
        # Windows
        if os.name == "nt":
            return pathlib.Path(os.getenv("APPDATA"))
        # MacOS
        elif sys.platform == "darwin":
            return pathlib.Path.home() / "Library" / "Application Support"
        # Linux
        else:
            return pathlib.Path.home() / ".local" / "share"
        
    @staticmethod
    def get_data_path():
        app_data_dir = Files.get_data_base_path() / "Tutel"
        app_data_dir.mkdir(parents = True, exist_ok = True) 
        return app_data_dir
    
    @staticmethod
    def get_resource_path(relative_path):
        # PyInstaller compatibility
        if hasattr(sys, "_MEIPASS"):
            return pathlib.Path(sys._MEIPASS) / relative_path
        
        return pathlib.Path(__file__).resolve().parent.parent.parent / relative_path

    @staticmethod
    def write_settings(settings):
        path = Files.get_data_path()
        path.mkdir(parents = True, exist_ok = True)
        file_path = path / "appsettings.json"

        with open(file_path, "w", encoding = "utf-8") as settings_file:
            json.dump(settings, settings_file, ensure_ascii = False, indent = 4)

    @staticmethod
    def write_crash_report(crash_report):
        path = Files.get_data_path() / "logs"
        path.mkdir(parents = True, exist_ok = True)
        now = datetime.datetime.now()
        file_path = path / f"crash_report_{now.strftime("%Y%m%d_%H%M%S")}.log"

        with open(file_path, "w", encoding = "utf-8") as crash_report_file:
            crash_report_file.write(crash_report)

    @staticmethod
    def read_settings():
        path = Files.get_data_path()
        path.mkdir(parents = True, exist_ok = True)
        file_path = path / "appsettings.json"

        # The file does not exist, so I copy the settings from the default settings file
        if  not file_path.is_file():
            default_settings = Files.read_default_settings()

            with open(file_path, "w", encoding = "utf-8") as settings_file:
                json.dump(default_settings, settings_file, ensure_ascii = False, indent = 4)
                return default_settings

        with open(file_path, "r", encoding = "utf-8") as settings_file:
            return json.load(settings_file)
        
    @staticmethod
    def read_default_settings():
        default_settings_path = Files.get_resource_path("assets/configs/default_appsettings.json")

        with open(default_settings_path, "r", encoding = "utf-8") as settings_file:
            return json.load(settings_file)
        
    @staticmethod
    def read_localization(language_code):
        path = Files.get_resource_path(f"l10n/{language_code}.json")

        with open(path, "r") as localization:
            return json.load(localization)
        
    @staticmethod
    def load_icon(icon_name):
        return Files.get_resource_path(f"assets/icons/{icon_name}")
