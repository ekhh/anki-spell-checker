from functools import partial, wraps
from aqt.operations import QueryOp
from aqt.utils import showWarning
from datetime import date
import requests as req
from aqt import mw
import subprocess
import zipfile
import pickle
import platform
import shutil
import os
import sys
import aqt

from .const import *


def refreshLanguages(*args):
    p = mw.web.page().profile()
    p.setSpellCheckEnabled(False)
    p.setSpellCheckLanguages({})
    p.setSpellCheckLanguages(getDictionaries())
    p.setSpellCheckEnabled(getUserData("status", default=True))


def getDictionaries():
    dicts = []
    for file in os.listdir(DICT_DIR):
        if file.endswith(".bdic"):
            dicts.append(file.removesuffix(".bdic"))
    return dicts


def background_op(func=None, /, *, success=None, with_progress= None, label=None):
    if not func:
        return partial(background_op, success=success, with_progress=with_progress, label=label)

    @wraps(func)
    def wrapper(*args, **kwargs):
        def noop(*args, **kwargs):
            pass

        if success:
            op = QueryOp(parent=mw, op=partial(func, *args, **kwargs), success=success)
        else:
            op = QueryOp(parent=mw, op=partial(func, *args, **kwargs), success=noop)
        if with_progress:
            return op.with_progress(label=label).run_in_background()
        else:
            return op.run_in_background()
    return wrapper


@background_op(success=refreshLanguages, with_progress=True, label="Compiling user dictionaries...")
def compileUserDictionaries(*args, **kwargs):
    for dic in os.listdir(USER_DICT_PATH):
        if dic.endswith((".dic", ".txt")):
            compileUserDictionary(dic.split(".")[0])


@background_op(success=refreshLanguages)
def compilePersonal(*args):
    compileUserDictionary("personal")


def compileUserDictionary(name, *args):
    base = os.path.join(USER_DICT_PATH, name)
    tmp_files = []
    if os.path.isfile(base + ".txt"):
        with open(base + ".txt", "rb") as f:
            line_count = sum(1 for _ in f)
        with open(base + ".txt", 'r') as in_file, open(base + ".dic", 'w') as out_file:
            out_file.write(str(line_count) + "\nWeirdBugFix\n")
            for line in in_file:
                out_file.write(line)
            tmp_files.append(out_file.name)
    if not os.path.isfile(base + ".dic"):
        return
    if not os.path.isfile(base + ".aff"):
        unique_chars = set()
        with open(base + ".dic", 'r') as file:
            for line in file:
                for char in line:
                    unique_chars.add(char)
        content = f"SET UTF-8\nTRY {''.join(unique_chars)}\n"
        with open(base + ".aff", 'w') as file:
            file.write("".join(content))
            tmp_files.append(file.name)
    compileBDIC(USER_DICT_PATH, name, remove=False)
    for f in tmp_files:
        os.remove(f)


@background_op(with_progress=False, label="Spell checker:\nDownloading binaries for dictionary conversion...")
def checkConversionBinaries(*args):
    done_file = os.path.join(BINS_PATH, "verified")
    if not os.path.isfile(done_file):
        zip_loc = [BINS_PATH, "bins.zip"]
        downloadToFile(URL_BINARIES, *zip_loc)
        with zipfile.ZipFile(os.path.join(*zip_loc), 'r') as zip_ref:
            for zip_info in zip_ref.infolist():
                if zip_info.is_dir():
                    continue
                zip_info.filename = os.path.basename(zip_info.filename)
                zip_ref.extract(zip_info, BINS_PATH)
        os.remove(os.path.join(*zip_loc))
        saveWrite(done_file, str(date.today()), mode="w")


def compileBDIC(path, name, remove=False):
    command = [BIN_PATH, os.path.join(path, name)]
    if os.name != 'nt':
        mode = os.stat(BIN_PATH).st_mode
        mode |= (mode & 0o444) >> 2  # copy R bits to X
        os.chmod(BIN_PATH, mode)
    res = subprocess.run(command, shell=False, capture_output=True, text=True)
    if remove:
        ex = [".dic", ".aff"]
        for e in ex:
            os.remove(os.path.join(path, name + e))
    print(f"Compiled {name}")

    if res.returncode != 0:
        aqt.mw.taskman.run_on_main(
            lambda: showWarning(f"The requested dictionary ({name}) could not be compiled. Process output:\n{res.stdout}"))
    else:
        try:
            shutil.move(os.path.join(path, name + ".bdic"), os.path.join(DICT_DIR, name + ".bdic"))
        except OSError as e:
            print(e)
            if name == "personal":
                compilePersonal()
            else:
                aqt.mw.taskman.run_on_main(
                    lambda: showWarning(f"Error: The requested dictionary ({name}) could not be compiled."))


def download(url):
    try:
        res = req.get(url)
    except ConnectionError as error:
        showWarning(
            "An internet connection is not available. Error: {error}")
        return None
    if res.status_code != 200:
        showWarning(f"Access to {url} has failed. Status code: {res.status_code}.")
    return res


def openPath(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def downloadToFile(url, loc, name):
    res = download(url)
    if res is None:
        return None
    saveMkdir(loc)
    save_path = os.path.join(loc, name)
    saveWrite(save_path, res.content)

    return save_path


def setUserData(name, data):
    path = os.path.join(USER_PATH, name + ".pck")
    try:
        with open(path, "w+b") as f:
            pck = pickle.dumps(data)
            f.write(pck)
    except IOError as err:
        showWarning(f"Could not write to user_files. Error: {err}")


def getUserData(name, default=None):
    if default is None:
        default = []
    path = os.path.join(USER_PATH, name + ".pck")
    if not os.path.isfile(path):
        return default
    try:
        with open(path, "rb") as f:
            pck = f.read()
            return pickle.loads(pck)
    except IOError as err:
        showWarning(f"Could not read user_files. Error: {err}")
        return default


def saveMkdir(path):
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as error:
        showWarning(f"Could not create the data directory. Error: {error}")


def saveWrite(path, content, mode="w+b"):
    try:
        with open(path, mode) as f:
            f.write(content)
    except IOError as error:
        showWarning(f"Could not write content to disk. Error: {error}")

def saveWriteUnique(path, content:str, mode="a+"):
    try:
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write("")

        with open(path, "r") as f:
            existing_lines = set(line.strip() for line in f.readlines())

        new_content = content.strip()
        if new_content in existing_lines:
            return False

        with open(path, mode) as f:
            f.write(content)
        return True

    except Exception as error:
        showWarning(f"Could not write content to disk. Error: {error}")
        return False
