import csv
import os
import shutil
from pathlib import Path


class CsvUtil(object):

    def write_data(self, csv_file, data):
        if not csv_file.fieldnames:
            csv_file.fieldnames = list(data.keys())
            csv_file.writeheader()

        csv_file.writerow(data)

    def iterate(self, csv_path, encoding):
        with open(csv_path, "r", encoding=encoding) as fs:
            reader = csv.reader(fs)
            yield from reader

    def reset(self, path, *sub_files):
        if os.path.exists(path):
            shutil.rmtree(path)

        Path(path).mkdir()
        for subf in sub_files:
            Path(path, subf).mkdir()

    def open_csv(self, path, encoding):
        open_file = path.open('w', encoding=encoding)
        return csv.DictWriter(open_file, fieldnames=None, quoting=csv.QUOTE_ALL)

    def row_to_dict(self, line, elem_pos_dict):
        return {name: self.row_to_dict(line, value) if type(value) == dict else line[value]
                for name, value in elem_pos_dict.items()}
