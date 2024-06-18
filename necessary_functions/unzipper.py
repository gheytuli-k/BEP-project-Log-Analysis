import zipfile
from typing import Dict, List

def unzip(source_path:str, destination_path:str, files:Dict[str, List[str]]) -> None:
    """
    Unzips the given log files of the workflow jobs and stores them in the destination path.

    :param source_path: The path to the source zip file
    :param destination_path: The path to store the extracted files
    :param files: The files to extract from the zip file
    :return: None
    """
    files_to_extract = []
    for folder, file in files.items():
        for f in file:
            files_to_extract.append(folder+"/"+f+".txt")

    with zipfile.ZipFile(source_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file in files_to_extract:
                zip_ref.extract(file, destination_path)



