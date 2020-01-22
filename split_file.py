from fsplit.filesplit import FileSplit
from pathlib import Path
import myconf

split_folder = myconf.split_folder

Path(split_folder).mkdir(parents=True, exist_ok=True)
FileSplit(file=myconf.file_path, splitsize=myconf.number_of_lines_in_splitted_file,
				output_dir=split_folder).split()
