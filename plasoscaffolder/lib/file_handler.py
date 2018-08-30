# -*- coding: utf-8 -*-
"""The file handler."""
import os
import pathlib
import shutil


class FileHandler:
  """Handles the creation of files."""

  @classmethod
  def CreateFilePath(cls, path: str, name: str, suffix: str) -> str:
    """Creates the file path from the directory path, filename and suffix.

    Args:
      path (str): path to the file directory.
      name (str): filename.
      suffix (str): suffix.

    Returns:
      str: the path to the file.
    """
    file_name = '{0:s}.{1:s}'.format(name, suffix)
    return os.path.join(path, file_name)

  @classmethod
  def _CreateFolder(cls, directory_path):
    """Creates a folder.

     This function should only to be called if the target folder does not yet
     exists or there will be an exception.

     Args:
       directory_path (str): path to the directory to create.
     """
    os.makedirs(directory_path)

  def CreateFile(
      self, directory_path: str, file_name: str, filename_suffix: str):
    """Creates a empty file.

    Args:
      directory_path (str): path to the directory the file should be created in.
      file_name (str): name of the new file.
      filename_suffix (str): suffix of the new file.

    Returns:
      str: path of the created file
    """
    file_path = self.CreateFilePath(
        directory_path, file_name, filename_suffix)

    if not os.path.exists(directory_path):
      self._CreateFolder(directory_path)

    pathlib.Path(file_path).touch()
    return file_path

  def CreateFileFromPath(self, file_path: str) -> str:
    """Creates a empty file.

    Args:
      file_path (str): path to the file.

    Returns:
      str: the path of the created file
    """
    self.CreateFolderForFilePathIfNotExist(file_path)
    pathlib.Path(file_path).touch()
    return file_path

  def CopyFile(self, source: str, destination: str) -> str:
    """Copies a file.

      Args:
        source (str): path of the file to copy
        destination (str): path to copy the file to.

      Returns:
        str: the path of the copied file
      """
    self.CreateFolderForFilePathIfNotExist(destination)
    shutil.copyfile(source, destination)
    return destination

  def CreateOrModifyFileWithContent(self, source: str, content: str):
    """Add content to a file and create the file and path if non existing.

    Args:
      source (str): path of the file to edit.
      content (str): content to append to the file.

    Returns:
      str: path of the edited file.
    """
    self.CreateFolderForFilePathIfNotExist(source)
    self.AddContent(source, content)

  def AddContent(self, source: str, content: str) -> str:
    """Add content to a file and create file if non existing.

    Args:
      source (str): path of the file to edit.
      content (str): content to append to the file.

    Returns:
      str: path of the edited file.
    """
    self.CreateFolderForFilePathIfNotExist(source)
    with open(source, 'a') as file_object:
      file_object.write(str(content))

    return source

  def CreateFolderForFilePathIfNotExist(self, file_path: str):
    """Creates folders for the given file if it does not exist.

    Args:
      file_path (str):  path to the file

    Returns:
      str: directory path of the created directory
    """
    directory_path = os.path.dirname(file_path)
    if not os.path.exists(directory_path):
      self._CreateFolder(directory_path)
    return directory_path