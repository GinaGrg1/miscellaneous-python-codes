import os
import re
from pathlib import Path
from shutil import copy, SameFileError, move
import subprocess

from zipfile import ZipFile, ZIP_DEFLATED

def get_file_info(filepath: str) -> dict:
  """
  Loop through the TimeLadder folder & create a dictionary where key is the original file path & value
  is its corresponding file that will be created.
  E.g {
   '.../TimeLadder-Period-202255.xml': '.../TimeLadder-Period-202288.xml'
  }
  """
  file_dict = dict()
  new_key = getArgument('new_key_name')

  original_files = filter(lambda filepath: filepath.is_file(), Path(filepath).glob('*'))
  for org_file in original_files:
    org_file_name = org_file.absolute()
    match_old_period = re.match(r'\w+-\w+-(?P<new_key>[0-9]+)--', org_file_name.stem)
    old_period = match_old_period.group('new_key')
    file_dict[str(org_file_name)] = str(org_file_name).replace(old_period, new_key)
  
  return file_dict

def copy_files(file_dict: dict) -> None:
  """
  Make the copy of the file in the same folder but with a different name.
  """
  for org_file_name, new_file_name in file_dict.items():
    try: 
      print(f"Copying {org_file_name} as {new_file_name}")
      copy(org_file_name, new_file_name)
    except SameFileError:
      print(f"This file already exists : {new_file_name}")
      pass
    
 def archive_files(path: str, files_to_zip: list) -> None:
  """
  path : main path where timeladder folders is.
  Here we are only interested in zipping & archiving the original files.
  
  After archiving into the `Archive` folder, they are deleted.
  """
  first_file_name = os.path.basename(files_to_zip[0])
  match = re.match(r'(?P<file_name>[\w+-]+)--', first_file_name)
  zip_file_name = f"{match.group('file_name')}.zip"
  
  print(f"\nWriting to zip file : {zip_file_name}")
  with ZipFile(f"./{zip_file_name}", 'w') as temp_zip:
    for file in files_to_zip:
      temp_zip.write(file, arcname=os.path.basename(file), compress_type=ZIP_DEFLATED)
  
  target_path = os.path.join(path, 'Archive')
  target_zip_path = os.path.join(target_path, zip_file_name)
  
  if os.path.exists(target_zip_path):
    print(f'Zip File Already Exists. Removing it. {target_zip_path}')
    Path(target_zip_path).unlink()
    
  move(f"./{zip_file_name}", target_path)
  
  print("\nFiles archived as .zip file. Removing the old files.\n")
  for old_file in files_to_zip:
    os.remove(old_file)
    
 def replace_using_sed(file_list: list) -> None:
  """
  file_list : List of files where we will make the replacements.
  One e.g:
      "/dbfs/mnt/ETL1/RG/GB/TimeLadders/GB/TimeLadder-Period-202102--GB_PETROL_IND_P.xml"
      
  """
  num_replace = "<NumMembers>" + getArgument('NumMembers') + "<\\/NumMembers>"
  cut_dt = "<CutOffDate>" + getArgument('CutOffDate') + "<\\/CutOffDate>"
  
  main_sed_cmd = 's/\\(<NumMembers>\\).*\\(<\\/NumMembers>\\)/'+num_replace+'/g; s/\\(<CutOffDate>\\).*\\(<\\/CutOffDate>\\)/'+cut_dt+'/g'
  
  for file_name in file_list:
    print(f"Replacing file : {file_name}")
    replace = subprocess.run(['sed', '-i', main_sed_cmd, file_name], stdout=subprocess.PIPE, universal_newlines=True)
    
    if replace.returncode != 0 :
      print(f"This file was not replaced. Please check : {file_name}")
      
if __name__ == '__main__':
  dbutils.widgets.removeAll()
  dbutils.widgets.text("new_key_name", "")
  dbutils.widgets.text("country", "")
  dbutils.widgets.text("NumMembers", "")
  dbutils.widgets.text("CutOffDate", "")
  
  time_ladder_path = f"../RG/TimeLadders/{getArgument('country').upper()}"
  
  file_dict = get_file_info(time_ladder_path)
  copy_files(file_dict)
  archive_files(time_ladder_path, list(file_dict.keys()))
  
  replace_using_sed(list(file_dict.values()))
  
  
