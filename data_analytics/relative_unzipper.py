'''
Usage:
Download files from moodle
Pass the path to the folder containing CSI WiFILogs.zip
If path contains backslashes (windows), end path with two backslashes (to escape escape char)
If path contains forward slashes (osx), path must end with one or more forward slashes

See example below if __name__ == "__main__":

Output:
If there is a file ending in Logs.zip, it will be extracted to a folder with the same name
If that folder contains zips with ar relevant room name (B-002, B-003 or B-004 in the name,
they will be extracted to folders named the room which the files describe
'''

import glob
import os
import zipfile


def unzipper_outer(outer_path):
    outer_path = fix_windows_path(outer_path)

    for filepath in glob.iglob(outer_path + "*Logs.zip"):
        filepath = fix_windows_path(filepath)

        # get last part of path
        filename = os.path.basename(os.path.normpath(filepath))

        # remove file extension and use as folder to extract zip to
        filename = str(filename.split(".")[0])

        # create folder using name of zip
        if not os.path.exists(outer_path + filename):
            os.makedirs(outer_path + filename)

        print("extracting", filename + ".zip", "to", outer_path + filename)
        archive = zipfile.ZipFile(filepath)
        archive.extractall(outer_path + filename)

        # relative path has . at start, so use [1] and add . to start of inner path
        if filepath[0:2] == "..":
            inner_path = str(".." + filepath.split(".")[2])
        elif filepath[0] == ".":
            inner_path = str("." + filepath.split(".")[1])
        else:
            inner_path = str(filepath.split(".")[0])

        inner_path += "/"

        # extract inner zips
        unzipper_inner(inner_path, "B-02")
        unzipper_inner(inner_path, "B-03")
        unzipper_inner(inner_path, "B-04")


def unzipper_inner(path, new_folder):
    path = fix_windows_path(path)
    # print("path", path)

    if not os.path.exists(path + new_folder):
        os.makedirs(path + new_folder)

    for filename in glob.iglob(path + "*.zip"):
        if new_folder in filename:
            filename = fix_windows_path(filename)
            print("extracting", filename)

            archive = zipfile.ZipFile(filename)
            archive.extractall(path+new_folder)


def fix_windows_path(string):
    new_string = ""
    for i in range(len(string)):
        # two backslashes need to escape escape char
        if string[i] == "\\":
            new_string += "/"
        else:
            new_string += string[i]

    # print(new_string)
    return new_string


if __name__ == "__main__":
    # change path here
    unzipper_outer("./data/")

    # examples
    # unzipper_outer(r"C:/Users/conor/Documents/college (ucd)/semester 3 research comp47360/test//")
    # unzipper_outer(r"C:\Users\conor\Documents\college (ucd)\semester 3 research comp47360\test\\")
