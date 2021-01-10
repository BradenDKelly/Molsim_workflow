import os

__all__ = ["make_folder"]

def make_folder(folderName):
    """
    Makes a folder in the current directory.
    This could be modified to make a folder in a 
    specified directory.

    Parameters
    ----------
    folderName : string
        name of the folder to be created

    Returns
    -------
    Makes a folder

    """
    try:
        os.makedirs(folderName)
    except OSError as e:
        if e.errno != errno.EExist:
            raise
            

