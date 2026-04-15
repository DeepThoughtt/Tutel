import os
import shutil

class AppBusiness:

    @staticmethod
    def convert(directory, from_ext, to_ext, flags):
        converted_elements = 0

        if not flags.recursive_mode:
            filenames = set(next(os.walk(directory, topdown = True))[2])
            converted_elements, stopped = AppBusiness.convert_directory_content(directory, filenames, from_ext, to_ext, flags)
            return converted_elements, stopped
        
        for path, directories, filenames in os.walk(directory):
            filenames = set(filenames)
            new_converted_elements, stopped = AppBusiness.convert_directory_content(path, filenames, from_ext, to_ext, flags)
            converted_elements += new_converted_elements

            if stopped:
                return converted_elements, stopped
            
        return converted_elements, False
    
    @staticmethod
    def convert_directory_content(directory, filenames, from_ext, to_ext, flags):
        backup_directory = f"{directory}/{from_ext}_backup_folder"
        converted_elements = 0
        
        for element in filenames:
            if not flags.operation_in_progress:
                return converted_elements, True
                
            original_file = f"{directory}/{element}"
            
            if element.lower().endswith(f".{from_ext}"):
                if flags.create_backups:
                    if not os.path.exists(backup_directory):
                        os.mkdir(backup_directory)
                
                    shutil.copyfile(original_file, f"{backup_directory}/{element}")
                
                filename = os.path.splitext(element)[0]
                new_name = AppBusiness.create_new_file_name(directory, filename, to_ext, filenames)
                os.rename(original_file, new_name)
                converted_elements += 1

        return converted_elements, False
    
    @staticmethod
    def create_new_file_name(directory, filename, to_ext, directory_content):
        if f"{filename}.{to_ext}" not in directory_content:
            return f"{directory}/{filename}.{to_ext}"
        
        n = 1
        while f"{filename}_{n}.{to_ext}" in directory_content:
            n += 1
        
        return f"{directory}/{filename}_{n}.{to_ext}"
