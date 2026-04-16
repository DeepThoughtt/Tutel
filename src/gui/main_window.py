import os
import threading
import tkinter

from src.singletons.assets import assets
from src.singletons.settings import settings
from src.singletons.localization import localization
from src.consts.languages import Languages
from src.business.app_business import AppBusiness
from src.entities.flags import Flags
from src.consts.icons import Icons
from src.utils.files import Files

class MainWindow(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.title(settings["appName"])
        self.iconbitmap()

        self.flags = Flags()
        self.iconbitmap(assets.icons[Icons.TUTEL])
        self.bind("<Button-1>", self.remove_focus_from_entries)
        self.minsize(700, 200)
        self.geometry("")

        self.build_menu()
        self.data_frame = tkinter.LabelFrame(self, text = localization["data"])
        self.data_frame.pack(fill = tkinter.BOTH, expand = True)

        self.directory_entry = tkinter.Entry(self.data_frame)
        self.directory_entry.insert(0, localization["directory"])
        self.directory_entry.pack(fill = tkinter.X)
        self.directory_entry.bind("<Button-1>", self.directory_focus_in)
        self.directory_entry.bind("<FocusOut>", self.directory_focus_out)

        self.from_ext_entry = tkinter.Entry(self.data_frame)
        self.from_ext_entry.insert(0, localization["convertFrom"])
        self.from_ext_entry.pack(fill = tkinter.X)
        self.from_ext_entry.bind("<Button-1>", self.from_ext_focus_in)
        self.from_ext_entry.bind("<FocusOut>", self.from_ext_focus_out)

        self.to_ext_entry = tkinter.Entry(self.data_frame)
        self.to_ext_entry.insert(0, localization["to"])
        self.to_ext_entry.pack(fill = tkinter.X)
        self.to_ext_entry.bind("<Button-1>", self.to_ext_focus_in)
        self.to_ext_entry.bind("<FocusOut>", self.to_ext_focus_out)

        self.check_frame = tkinter.Frame(self.data_frame)
        self.check_frame.pack()

        self.recursive_mode_flag = tkinter.IntVar()

        self.recursive_mode_check = tkinter.Checkbutton(
            master = self.check_frame, 
            text = localization["checkSubfolders"], 
            variable = self.recursive_mode_flag, 
            onvalue = 1, 
            offvalue = 0, 
            command = self.check_recursive_mode,
        )
        
        self.recursive_mode_check.grid(column = 0, row = 0)
        self.create_backups_flag = tkinter.IntVar()

        self.make_backups_check = tkinter.Checkbutton(
            master = self.check_frame, 
            text = localization["createBackupFolders"], 
            variable = self.create_backups_flag, 
            onvalue = 1, 
            offvalue = 0, 
            command = self.check_create_backups,
        )

        self.make_backups_check.grid(column = 1, row = 0)

        self.buttons_frame = tkinter.Frame(self)
        self.buttons_frame.pack()

        self.start_button = tkinter.Button(self.buttons_frame, text = localization["start"], command = self.start_conversion)
        self.start_button.grid(row = 0, column = 0)
        
        self.stop_button = tkinter.Button(self.buttons_frame, text = localization["stop"], command = self.stop_conversion)
        self.stop_button.grid(row = 0, column = 1)
        
        self.update_label = tkinter.Label(self, text = "")
        self.update_label.pack()

        self.version_label = tkinter.Label(self, text = f"v{settings['version']}", font = ("TkDefaultFont", 8))
        self.version_label.pack(anchor = "se", padx = 5, pady = 5)

        self.localized_widgets = {
            "data": self.data_frame,
            "checkSubfolders": self.recursive_mode_check,
            "createBackupFolders": self.make_backups_check,
            "start": self.start_button,
            "stop": self.stop_button,
        }
        
        self.exec_thread = None
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def remove_focus_from_entries(self, event):
        event.widget.focus_set()
        self.directory_entry.selection_clear()
        self.from_ext_entry.selection_clear()
        self.to_ext_entry.selection_clear()
    
    def directory_focus_in(self, event):
        self.directory_entry.delete(0, tkinter.END)
    
    def directory_focus_out(self, event):
        if self.directory_entry.get().strip() == "":
            self.directory_entry.delete(0, tkinter.END)
            self.directory_entry.insert(0, localization["directory"])
    
    def from_ext_focus_in(self, event):
        self.from_ext_entry.delete(0, tkinter.END)
    
    def from_ext_focus_out(self, event):
        if self.from_ext_entry_is_empty():
            self.from_ext_entry.delete(0, tkinter.END)
            self.from_ext_entry.insert(0, localization["convertFrom"])
    
    def to_ext_focus_in(self, event):
        self.to_ext_entry.delete(0, tkinter.END)
    
    def to_ext_focus_out(self, event):
        if self.to_ext_entry_is_empty():
            self.to_ext_entry.delete(0, tkinter.END)
            self.to_ext_entry.insert(0, localization["to"])
    
    def check_recursive_mode(self):
        self.flags.recursive_mode = self.recursive_mode_flag.get() == 1
         
    def check_create_backups(self):
        self.flags.create_backups = self.create_backups_flag.get() == 1
    
    def start_conversion(self):
        self.start_button.focus_set()
        
        if not self.flags.operation_in_progress:
            self.flags.operation_in_progress = True
            self.exec_thread = threading.Thread(target = self.thread)
            self.exec_thread.start()
            
    def stop_conversion(self):
        self.stop_button.focus_set()
        self.flags.operation_in_progress = False
        
    def on_close(self):
        self.flags.operation_in_progress = False
        self.destroy()
    
    def thread(self):
        directory = self.directory_entry.get().strip()
        from_ext = self.from_ext_entry.get().strip().lower()
        to_ext = self.to_ext_entry.get().strip().lower()
        
        if not os.path.isdir(directory):
            self.update_label.config(text = localization["invalidDirectory"])
            self.flags.operation_in_progress = False
            return
        
        if self.invalid_extensions(from_ext, to_ext):
            self.update_label.config(text = localization["noExtensionsFound"])
            self.flags.operation_in_progress = False
            return
    
        files_converted, stopped = AppBusiness.convert(directory, from_ext, to_ext, self.flags)
        self.update_label.config(text = self.get_update_label_text(stopped, files_converted))
        self.flags.operation_in_progress = False

    def invalid_extensions(self, from_ext, to_ext):
        return from_ext == "" or to_ext == "" or " " in from_ext or " " in to_ext or to_ext == localization["to"]
    
    def to_ext_entry_is_empty(self):
        return self.to_ext_entry.get().strip() == ""
    
    def from_ext_entry_is_empty(self):
        return self.from_ext_entry.get().strip() == ""
    
    def get_update_label_text(self, stopped, files_converted):
        if stopped:
            if files_converted == 1:
                return localization["conversionStoppedOneFileConverted"]
            else:
                return localization["conversionStoppedMultipleFilesConverted"].format(n = files_converted)
        
        if files_converted == 1:
            return localization["conversionCompletedOneFileConverted"]
        else:
            return localization["conversionCompletedMultipleFilesConverted"].format(n = files_converted)
        
    def english_language_selected(self):
        old_directory_text = localization["directory"]
        old_from_text = localization["convertFrom"]
        old_to_text = localization["to"]

        settings["language"] = Languages.ENGLISH
        Files.write_settings(settings)
        localization.set_language(settings["language"])
        self.translate_widgets(old_directory_text, old_from_text, old_to_text)

    def italian_language_selected(self):
        old_directory_text = localization["directory"]
        old_from_text = localization["convertFrom"]
        old_to_text = localization["to"]

        settings["language"] = Languages.ITALIAN
        Files.write_settings(settings)
        localization.set_language(settings["language"])
        self.translate_widgets(old_directory_text, old_from_text, old_to_text)

    def translate_widgets(self, old_directory_text, old_from_text, old_to_text):
        self.menu_bar.destroy()
        self.build_menu()

        for key, widget in self.localized_widgets.items():
            widget.config(text = localization[key])

        if self.directory_entry.get().strip() == old_directory_text:
            self.directory_entry.delete(0, tkinter.END)
            self.directory_entry.insert(0, localization["directory"])

        if self.from_ext_entry.get().strip() == old_from_text:
            self.from_ext_entry.delete(0, tkinter.END)
            self.from_ext_entry.insert(0, localization["convertFrom"])

        if self.to_ext_entry.get().strip() == old_to_text:
            self.to_ext_entry.delete(0, tkinter.END)
            self.to_ext_entry.insert(0, localization["to"])

        self.update_label.config(text = "")

    def build_menu(self):
        self.menu_bar = tkinter.Menu(self)
        self.languages_menu = tkinter.Menu(self.menu_bar, tearoff = 0)
        self.languages_menu.add_command(label = "English", command = self.english_language_selected)
        self.languages_menu.add_command(label = "Italiano", command = self.italian_language_selected)
        self.menu_bar.add_cascade(label = localization["language"], menu = self.languages_menu)
        self.config(menu = self.menu_bar)
