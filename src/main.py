import traceback

from src.consts.icons import Icons
from src.singletons.assets import assets
from src.singletons.localization import localization
from src.singletons.settings import settings
from src.gui.main_window import MainWindow
from src.utils.files import Files
from src.utils.settings_checker import SettingsChecker

def main():
    SettingsChecker.fix_and_save(settings)
    localization.set_language(settings["language"])

    assets.load_assets({
        "icons": {
            Icons.TUTEL: Files.load_icon(Icons.TUTEL),
        },
    })

    main_window = MainWindow()
    main_window.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        if settings["createCrashReports"]:
            Files.write_crash_report(traceback.format_exc())
