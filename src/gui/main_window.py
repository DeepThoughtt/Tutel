import os
import threading
import tkinter

from src.business.app_business import AppBusiness
from src.entities.flags import Flags

class MainWindow(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.title("Tutel")
        self.iconbitmap()

        self.flags = Flags()
        base_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_path, "..", "..", "imgs", "tutel.ico")

        self.iconbitmap(icon_path)
        self.bind("<Button-1>", self.remove_focus_from_entries)
        self.minsize(500, 160)
        self.geometry("")

        self.data_frame = tkinter.LabelFrame(self, text = "Data")
        self.data_frame.pack(fill = tkinter.BOTH, expand = True)

        self.directory_entry = tkinter.Entry(self.data_frame)
        self.directory_entry.insert(0, "Directory")
        self.directory_entry.pack(fill = tkinter.X)
        self.directory_entry.bind("<Button-1>", self.directory_focus_in)
        self.directory_entry.bind("<FocusOut>", self.directory_focus_out)

        self.from_entry = tkinter.Entry(self.data_frame)
        self.from_entry.insert(0, "Convert From...")
        self.from_entry.pack(fill = tkinter.X)
        self.from_entry.bind("<Button-1>", self.from_focus_in)
        self.from_entry.bind("<FocusOut>", self.from_focus_out)

        self.to_entry = tkinter.Entry(self.data_frame)
        self.to_entry.insert(0, "To...")
        self.to_entry.pack(fill = tkinter.X)
        self.to_entry.bind("<Button-1>", self.to_focus_in)
        self.to_entry.bind("<FocusOut>", self.to_focus_out)

        self.check_frame = tkinter.Frame(self.data_frame)
        self.check_frame.pack()

        self.recursive_mode_flag = tkinter.IntVar()

        self.recursive_mode_check = tkinter.Checkbutton(
            master = self.check_frame, 
            text = "Check subfolders too", 
            variable = self.recursive_mode_flag, 
            onvalue = 1, 
            offvalue = 0, 
            command = self.check_recursive_mode
        )
        
        self.recursive_mode_check.grid(column = 0, row = 0)
        self.create_backups_flag = tkinter.IntVar()

        self.make_backups_check = tkinter.Checkbutton(
            master = self.check_frame, 
            text = "Create backup folders", 
            variable = self.create_backups_flag, 
            onvalue = 1, 
            offvalue = 0, 
            command = self.check_create_backups
        )

        self.make_backups_check.grid(column = 1, row = 0)

        self.buttons_frame = tkinter.Frame(self)
        self.buttons_frame.pack()

        self.start_button = tkinter.Button(self.buttons_frame, text = "START", command = self.start_conversion)
        self.start_button.grid(row = 0, column = 0)
        
        self.stop_button = tkinter.Button(self.buttons_frame, text = "STOP", command = self.stop_conversion)
        self.stop_button.grid(row = 0, column = 1)
        
        self.update_label = tkinter.Label(self, text = "")
        self.update_label.pack()
        
        self.exec_thread = None
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def remove_focus_from_entries(self, event): 
        event.widget.focus_set()
        self.directory_entry.selection_clear()
        self.from_entry.selection_clear()
        self.to_entry.selection_clear()
    
    def directory_focus_in(self, event):
        self.directory_entry.delete(0, tkinter.END) 
    
    def directory_focus_out(self, event):
        if self.directory_entry.get().strip() == "":
            self.directory_entry.delete(0, tkinter.END)
            self.directory_entry.insert(0, "Directory")
    
    def from_focus_in(self, event):
        self.from_entry.delete(0, tkinter.END)
    
    def from_focus_out(self, event):
        if self.from_entry.get().strip() == "":
            self.from_entry.delete(0, tkinter.END)
            self.from_entry.insert(0, "Convert From...")
    
    def to_focus_in(self, event):
        self.to_entry.delete(0, tkinter.END)
    
    def to_focus_out(self, event):
        if self.to_entry.get().strip() == "":
            self.to_entry.delete(0, tkinter.END)
            self.to_entry.insert(0, "To...")
    
    def check_recursive_mode(self):
        self.flags.recursive_mode = self.recursive_mode_flag.get() == 1
         
    def check_create_backups(self):
        self.flags.create_backups = self.create_backups_flag.get() == 1
    
    def start_conversion(self):
        self.start_button.focus_set()
        
        if not self.working:
            self.working = True
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
        from_ext = self.from_entry.get().strip().lower()
        to_ext = self.to_entry.get().strip().lower()
        
        if not os.path.isdir(directory):
            self.update_label.config(text = "Invalid directory, retry")
            self.working = False
            return
        
        if from_ext == "" or to_ext == "" or " " in from_ext or " " in to_ext or to_ext == "To...":
            self.update_label.config(text = "No extensions found, retry")
            self.working = False
            return
    
        files_converted, stopped = AppBusiness.convert(directory, from_ext, to_ext, self.flags)
        self.update_label.config(text = f"Conversion {'stopped' if stopped else 'completed'}, {files_converted} {'file' if files_converted == 1 else 'files'} converted")
        self.working = False
