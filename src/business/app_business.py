import os
import shutil
import pathlib

class AppBusiness:

    @staticmethod
    def convert(directory, from_ext, to_ext, flags):
        directory = pathlib.Path(directory)
        converted_elements = 0

        if not flags.recursive_mode:
            filenames = {p.name for p in directory.iterdir() if p.is_file()}
            converted_elements, stopped = AppBusiness.convert_directory_content(directory, filenames, from_ext, to_ext, flags)
            return converted_elements, stopped
        
        for path, directories, filenames in os.walk(directory):
            path = pathlib.Path(path)
            filenames = set(filenames)
            new_converted_elements, stopped = AppBusiness.convert_directory_content(path, filenames, from_ext, to_ext, flags)
            converted_elements += new_converted_elements

            if stopped:
                return converted_elements, stopped
            
        return converted_elements, False
    
    @staticmethod
    def convert_directory_content(directory, filenames, from_ext, to_ext, flags):
        backup_directory = directory / f"{from_ext}_backup_folder"
        converted_elements = 0
        
        for element in filenames:
            if not flags.operation_in_progress:
                return converted_elements, True
            
            if not element.lower().endswith(f".{from_ext}"):
                continue
                
            original_file = directory / element

            if flags.create_backups:
                backup_directory.mkdir(exist_ok = True)
                shutil.copyfile(original_file, backup_directory / element)
            
            filename = pathlib.Path(element).stem
            new_name = AppBusiness.create_new_file_name(directory, filename, to_ext, filenames)
            original_file.rename(new_name)
            converted_elements += 1

        return converted_elements, False
    
    @staticmethod
    def create_new_file_name(directory, filename, to_ext, directory_content):
        if f"{filename}.{to_ext}" not in directory_content:
            return directory / f"{filename}.{to_ext}"
        
        n = 1
        while f"{filename}_{n}.{to_ext}" in directory_content:
            n += 1
        
        return directory / f"{filename}_{n}.{to_ext}"
