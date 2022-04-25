import tkinter as tk
import threading
import platform
import shutil
import os


class Tutel:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tutel")
        
        self.slash = "\\" if platform.system() == "Windows" else "/"
        self.root.iconbitmap(f".{self.slash}imgs{self.slash}tutel.ico")
        self.root.minsize(500, 160)
        self.root.geometry("")
        
        self.data_frame = tk.LabelFrame(self.root, text = "Data")
        self.data_frame.pack(fill = tk.BOTH, expand = True)
        
        self.directory_entry = tk.Entry(self.data_frame)
        self.directory_entry.insert(0, "Directory")
        self.directory_entry.pack(fill = tk.X)
        self.directory_entry.bind("<Button-1>", self.__directory_focus_in)
        self.directory_entry.bind("<FocusOut>", self.__directory_focus_out)
        
        self.from_entry = tk.Entry(self.data_frame)
        self.from_entry.insert(0, "Convert From...")
        self.from_entry.pack(fill = tk.X)
        self.from_entry.bind("<Button-1>", self.__from_focus_in)
        self.from_entry.bind("<FocusOut>", self.__from_focus_out)
        
        self.to_entry = tk.Entry(self.data_frame)
        self.to_entry.insert(0, "To...")
        self.to_entry.pack(fill = tk.X)
        self.to_entry.bind("<Button-1>", self.__to_focus_in)
        self.to_entry.bind("<FocusOut>", self.__to_focus_out)
        
        self.check_frame = tk.Frame(self.data_frame)
        self.check_frame.pack()
        
        self.recvar = tk.IntVar()
        self.recursive_mode_check = tk.Checkbutton(self.check_frame, text = "Check subfolders too", variable = self.recvar, onvalue = 1, offvalue = 0, command = self.__check_recursive_mode)
        self.recursive_mode_check.grid(column = 0, row = 0)
        
        self.backupvar = tk.IntVar()
        self.make_backups_check = tk.Checkbutton(self.check_frame, text = "Create backup folders", variable = self.backupvar, onvalue = 1, offvalue = 0, command = self.__check_create_backups)
        self.make_backups_check.grid(column = 1, row = 0)
        
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack()
        
        self.start_button = tk.Button(self.buttons_frame, text = "START", command = self.__start_conversion)
        self.start_button.grid(row = 0, column = 0)
        
        self.stop_button = tk.Button(self.buttons_frame, text = "STOP", command = self.__stop_conversion)
        self.stop_button.grid(row = 0, column = 1)
        
        self.update_label = tk.Label(self.root, text = "")
        self.update_label.pack()
        
        self.exec_thread = None
        self.make_backups = False
        self.recursive = False
        self.working = False
        
        self.root.protocol("WM_DELETE_WINDOW", self.__on_close)
        self.root.mainloop()
        
    
    def __directory_focus_in(self, event):
        self.directory_entry.delete(0, tk.END)
        
    
    def __directory_focus_out(self, event):
        if self.directory_entry.get().strip() == "":
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, "Directory")
    
    
    def __from_focus_in(self, event):
        self.from_entry.delete(0, tk.END)
        
    
    def __from_focus_out(self, event):
        if self.from_entry.get().strip() == "":
            self.from_entry.delete(0, tk.END)
            self.from_entry.insert(0, "Convert From...")
    
    
    def __to_focus_in(self, event):
        self.to_entry.delete(0, tk.END)
    
    
    def __to_focus_out(self, event):
        if self.to_entry.get().strip() == "":
            self.to_entry.delete(0, tk.END)
            self.to_entry.insert(0, "To...")
    
    
    def __check_recursive_mode(self):
        self.recursive = self.recvar.get() == 1
        
    
    def __check_create_backups(self):
        self.make_backups = self.backupvar.get() == 1
    
    
    def __start_conversion(self):
        self.start_button.focus_set()
        
        if not self.working:
            self.working = True
            self.exec_thread = threading.Thread(target = self.__thread)
            self.exec_thread.start()
            
    
    def __stop_conversion(self):
        self.stop_button.focus_set()
        self.working = False
        
    
    def __on_close(self):
        self.working = False
        self.root.destroy()
    
    
    def __thread(self):
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
    
        files_converted, stopped = self.__convert(directory, from_ext, to_ext)
        self.update_label.config(text = f"Conversion {'stopped' if stopped else 'completed'}, {files_converted} {'file' if files_converted == 1 else 'files'} converted")
        self.working = False
        
    
    def __convert(self, directory, from_ext, to_ext):
        converted_elements = 0
    
        if not self.recursive:
            filenames = set(next(os.walk(directory, topdown = True))[2])
            converted_elements, stopped = self.__convert_directory_content(directory, filenames, from_ext, to_ext)
            return converted_elements, stopped
            
        for path, directories, filenames in os.walk(directory):
            filenames = set(filenames)
            new_converted_elements, stopped = self.__convert_directory_content(path, filenames, from_ext, to_ext)
            converted_elements += new_converted_elements
            
            if stopped:
                return converted_elements, stopped
            
        return converted_elements, False
        
    
    def __convert_directory_content(self, directory, filenames, from_ext, to_ext):
        backup_directory = f"{directory}{self.slash}{from_ext}"
        converted_elements = 0
        
        for element in filenames:
            if not self.working:
                return converted_elements, True
                
            original_file = f"{directory}{self.slash}{element}"
            
            if element.lower().endswith(f".{from_ext}"):
                if self.make_backups:
                    if not os.path.exists(backup_directory):
                        os.mkdir(backup_directory)
                
                    shutil.copyfile(original_file, f"{backup_directory}{self.slash}{element}")
                
                filename = os.path.splitext(element)[0]
                new_name = self.__create_new_name(directory, filename, to_ext, filenames)
                os.rename(original_file, new_name)
                converted_elements += 1
                
                self.update_label.config(text = f"{converted_elements} {'file' if converted_elements == 1 else 'files'} converted")
        
        return converted_elements, False
        
    
    def __create_new_name(self, directory, filename, to_ext, directory_content):
        if f"{filename}.{to_ext}" not in directory_content:
            return f"{directory}{self.slash}{filename}.{to_ext}"
        
        n = 1
        while f"{filename}_{n}.{to_ext}" in directory_content:
            n += 1
        
        return f"{directory}{self.slash}{filename}_{n}.{to_ext}"


def main():
    Tutel()


if __name__ == "__main__":
    main()
    