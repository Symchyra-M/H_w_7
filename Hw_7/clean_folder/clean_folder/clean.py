import re
import shutil
import sys
from pathlib import Path

# noralize
UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r",
               "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

TRANS = {}

# scan
jpeg_files = list()
png_files = list()
jpg_files = list()
txt_files = list()
docx_files = list()
folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()

registered_extensions = {"JPEG": jpeg_files,
                         "PNG": png_files,
                         "JPG": jpg_files,
                         "TXT": txt_files,
                         "DOCX": docx_files,
                         "ZIP": archives}

# noralize
# cтворємо ключі і значення
for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    # для маленьких
    TRANS[ord(key)] = value
    # для великих
    TRANS[ord(key.upper())] = value.upper()


def normalize(name):
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)
    return f"{new_name}.{'.'.join(extension)}"


# scan
def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ("JPEG", "JPG", "PNG", "TXT", "DOCX", "OTHER", "ARCHIVE"):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder / item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)


# main
def hande_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder / normalize(path.name))


def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize(path.name.replace(".zip", ''))

    archive_folder = root_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(path.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def get_folder_objects(root_path):
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass


def main():
    path = sys.argv[1]
    print(f"Start in {path}")
    folder_path = Path(path)

    scan(folder_path)

    for file in jpeg_files:
        hande_file(file, folder_path, "JPEG")

    for file in jpg_files:
        hande_file(file, folder_path, "JPG")

    for file in png_files:
        hande_file(file, folder_path, "PNG")

    for file in txt_files:
        hande_file(file, folder_path, "TXT")

    for file in docx_files:
        hande_file(file, folder_path, "DOCX")

    for file in others:
        hande_file(file, folder_path, "OTHERS")

    for file in archives:
        handle_archive(file, folder_path, "ARCHIVE")

    get_folder_objects(folder_path)


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")
    arg = Path(path)
    main(arg.resolve())
