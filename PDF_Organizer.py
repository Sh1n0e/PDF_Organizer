import os
import re
import platform
import datetime
import shutil

# ----------------- File Locations ----------------------------------------#
source = "/Users/Shawn/Downloads"
target = "/Users/Shawn/Documents/PDF"
# -------------------------------------------------------------------------#

#------------------ Parameters --------------------------------------------#
Extensions = ("pdf",)  # Use a tuple for multiple extensions
DATE_PATTERN = r".*(20\d\d)-?([01]\d)-?([0123]\d).*"
FOL_Sep = "/"
# -------------------------------------------------------------------------#

# ---------------------Methods to execute----------------------------------#
def getFolder(year, monthNum):  # Creating folders per month
    monthNames = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    monthFol = monthNames[int(monthNum) - 1]  # Convert month number to name
    return f"{year}/{monthFol}"


def get_file_date(folder, filename):
    matchObject = re.match(DATE_PATTERN, filename)
    if matchObject:
        year = matchObject.group(1)
        month = matchObject.group(2)
        print("Matched on file date pattern")
    else:
        dateCreate = creation_date(os.path.join(folder, filename))
        matchObject = re.match(DATE_PATTERN, dateCreate)
        if matchObject:
            year = matchObject.group(1)
            month = matchObject.group(2)
        else:
            year = "0"
            month = "0"
            print("Failed to get date for document: " + filename)
    return {"Year": year, "Month": month}


def creation_date(path_to_file):
    if platform.system() == 'Windows':
        timestamp = os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            timestamp = stat.st_birthtime
        except AttributeError:
            timestamp = stat.st_mtime
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


# -------------------------------------------------------------------------#

files = os.listdir(source)  # Get list of files in source directory
# Loops through entire Downloads folder and processes all pdf files
for file in files:
    if file.lower().endswith(Extensions):
        fileData = get_file_date(source, file)
        year = fileData["Year"]
        month = fileData["Month"]

        if year == "0" or month == "0":
            print("Unable to extract date: " + file)
            continue

        # Get folder name from dates
        folder = getFolder(year, month)

        # Creating target folder
        target_folder = os.path.join(target, folder)
        if not os.path.exists(target_folder):
            print("Creating Folder: " + target_folder)
            os.makedirs(target_folder)  # Corrected to makedirs

        # Move pdf if it doesn't exist
        sourceFile = os.path.join(source, file)
        targetFile = os.path.join(target_folder, file)
        if not os.path.exists(targetFile):
            print("Moving File: " + file)
            shutil.move(sourceFile, targetFile)
        else:
            # If it exists and sizes are the same, delete it
            if os.stat(sourceFile).st_size == os.stat(targetFile).st_size:
                print("Duplicate File detected, Deleting: " + file)
                os.remove(sourceFile)
            else:
                print("Duplicate File, different size: " + file)
