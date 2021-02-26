import os
from zipfile import ZipFile, ZIP_DEFLATED
import shutil


def zip_hier_xmls(country, zip_path):
  """
  zip_path = '/dbfs/mnt/<some-path>/<some-folder>/'
  """
  files_to_zip = [zip_path+file for file in os.listdir(zip_path) if file.startswith(country)]
  
  with ZipFile('./test.zip', 'w') as my_zip:
    for file_name in files_to_zip:
      my_zip.write(file_name, arcname=os.path.basename(file_name), compress_type=ZIP_DEFLATED)
  
  shutil.move('./test.zip', '/dbfs/mnt/<some-path>/<some-folder>/')
