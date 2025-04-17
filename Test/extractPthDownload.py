import os
import re
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(filename="pthDownload.log", level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_https_links_from_pth(directory="./"):
  """
  Extracts all URLs starting with 'https://' and ending with '.pth' from all files in the specified directory
  and saves them to pth.txt.

  Args:
    directory (str): The directory to search for files. Defaults to the current directory.
  """
  all_links = []

  # Walk through all directories and their files
  for root, _, files in os.walk(directory):
    for filename in files:
      if not filename.endswith('.py'):
        continue
      filepath = Path(root) / filename
      if not filepath.is_file() or not os.access(filepath, os.R_OK):
        logging.error(f"File {filepath} is not accessible")
        continue
      try:
        with open(filepath, 'r', encoding='utf-8') as f:
          for line in f:
            # Strip leading/trailing whitespace and check if it starts with https:// and ends with .pth
            cleaned_line = line.strip()
            # Use regex to find all strings starting with https:// and ending with .pth
            # Find URLs ending with .pth
            pth_matches = re.findall(r'(https://\S+\.pth)', cleaned_line)
            # Find URLs ending with .pt but not .pth
            pt_matches = re.findall(r'(https://\S+\.pt)(?!h)', cleaned_line)
            matches = pth_matches + pt_matches
            for match in matches:
              all_links.append(match)
      except Exception as e:
        logging.error(f"Error reading file {filepath}: {e}")

  output_filename = "pth.txt"
  try:
    with open(output_filename, 'w', encoding='utf-8') as outfile:
      for link in all_links:
        outfile.write(link + "\n")
    print(f"Successfully extracted {len(all_links)} links to {output_filename}")
  except Exception as e:
    logging.error(f"Error writing to file {output_filename}: {e}")

if __name__ == "__main__":
  extract_https_links_from_pth()