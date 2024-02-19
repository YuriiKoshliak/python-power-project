import sys
import re
import shutil
import gzip
import os
from pathlib import Path

# Він ще не готовий, працюю над ним


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()

folders_to_create = ["images", "documents", 'audio', 'video', 'archives', 'other']

main_folder_path = Path(input('Enter the path for sorting and cleaning: '))

images = ['.JPEG', '.PNG', '.JPG', '.SVG']
documents = ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX']
audio = ['.MP3', '.OGG', '.WAV', '.AMR']
video = ['.AVI', '.MP4', '.MOV', '.MKV']
archives = ['.ZIP', '.GZ', '.TAR']

found_extensions = set()

found_images = []
found_documents = []
found_audio = []
found_video = []
found_archives = []
found_other = []

def delete_empty_folders(path):

    deleted = set()
    
    for current_dir, subdirs, files in os.walk(path, topdown=False):

        still_has_subdirs = False
        for subdir in subdirs:
            if os.path.join(current_dir, subdir) not in deleted:
                still_has_subdirs = True
                break
    
        if not any(files) and not still_has_subdirs:
            os.rmdir(current_dir)
            deleted.add(current_dir)

    print(f'Наступні пусті папки були видалені: {deleted}\n' if len(deleted) != 0 else "Пустих папок не знайдено\n")

def normalize(name):
    try:
        base, extension = name.rsplit('.', 1)
        trans_name = base.translate(TRANS)
        good_name = re.sub(r'\W', "_", trans_name)
        return f'{good_name}.{extension}'
    except ValueError:
        trans_name = name.translate(TRANS)
        return re.sub(r'\W', "_", trans_name)
     

def unpack(archive_path, path_to_unpack):
    shutil.unpack_archive(archive_path, path_to_unpack)


def move_rename_file(path):
    k = 1
    extension = path.suffix
    base = normalize(path.stem)
    new_name = normalize(path.name)

    if extension.upper() in images:
        new_folder = "images"
        found_images.append(path.name)
    elif extension.upper() in documents:
        new_folder = "documents"
        found_documents.append(path.name)
    elif extension.upper() in audio:
        new_folder = "audio"
        found_audio.append(path.name)
    elif extension.upper() in video:
        new_folder = "video"
        found_video.append(path.name)
    elif extension.upper() in archives:
        if extension.upper() == '.GZ':
            try:
                with gzip.open(path, 'rb') as f_in:
                    os.mkdir(main_folder_path / 'archives' / base )
                    with open(main_folder_path / 'archives' / base / base, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                found_archives.append(path.name)        
                os.remove(path)
            except FileExistsError:
                print(f'Архів {path} не вдалося розпакувати, бо папка {base} вже існує.\n')
        else:
            unpack(path, main_folder_path / 'archives' / base)
            found_archives.append(path.name) 
            os.remove(path)

        return None
        
    else:
        new_folder = "other"
        found_extensions.add(extension.upper())
        found_other.append(path.name) 

    new_file_path = main_folder_path / new_folder / new_name

    def cykle_try(new_file_path):
        nonlocal k
        try:
            path.rename(new_file_path)
        except FileExistsError:
            k += 1
            print (f'Файл {new_file_path.name} вже існує в папці {new_folder}, назву буде змінено на {base}{k}\n')
            mega_name = new_file_path.with_stem(f'{base}{k}')
            try:
                path.rename(mega_name)
            except FileExistsError:
                cykle_try(mega_name.with_stem(f'{base}{k}'))

    cykle_try(new_file_path)



def monster_sort(path):
    
    for element in path.iterdir():
        if element.name not in folders_to_create:
            if element.is_dir():
                monster_sort(element)
            else:
                move_rename_file(element)
                


def sorting():
               
        for folder_name in folders_to_create:
            try:
                (main_folder_path / folder_name).mkdir()
            except FileExistsError:
                ...
        
        monster_sort(main_folder_path)

        delete_empty_folders(main_folder_path)

        print(f'У папці було знайдено дивні розширення: {found_extensions}.\
 Для вашої безпеки всі такі файли {found_other} було переміщено до папки "other".\n' if len(found_extensions) != 0 else "")
        
        print(f'''Відсортовані файли: 
              
              зображення: {found_images} 

              відеофайли: {found_video} 

              документи: {found_documents} 

              музика: {found_audio} 

              архіви: {found_archives} \n''')

        
        

if __name__ == "__main__":
    sorting()



