import itertools
import contextlib

from pathlib import Path
import subprocess
from csv_util import CsvUtil


class Neo4jImportHandler:

    def import_graph(self, neo4j_admin, node_paths, link_paths):
        subprocess.call([neo4j_admin, 'import']
                        + [f'--nodes {pth} ' for pth in node_paths]
                        + [f'--relationships {pth}' for pth in link_paths]
                        )


def make_paths(base_path, file_names):
    return {
        name: Path(base_path, name).with_suffix('.csv')
        for name in file_names
    }


class Csv2Neo4jCsv(CsvUtil, Neo4jImportHandler):

    def __init__(self, *, src, model, dst, dbms):
        super().__init__()
        self.src = src
        self.dst = dst
        self.dbms = dbms
        self.model = model

        self.node_paths = make_paths(dst['node_path'], dst['csv_files']['node'])
        self.link_paths = make_paths(dst['link_path'], dst['csv_files']['link'])

    def init(self):
        raise NotImplementedError

    def converter(self, row, **kwargs):
        raise NotImplementedError

    @contextlib.contextmanager
    def open_dst_csvs(self):
        all_paths = {**self.node_paths, **self.link_paths}

        yield {
            name: super(Csv2Neo4jCsv, self).open_csv(all_paths, self.dst['encoding'])
            for name, path in all_paths.items()
        }

    def convert_to_csv(self):
        rows = super().iterate(self.src['path'], self.src['encoding'])
        rows = (super(Csv2Neo4jCsv, self).row_to_dict(row, self.model) for row in rows)

        init_state = self.init()
        graph_data = (self.converter(row, **init_state) for row in rows)

        with self.open_dst_csvs() as csvs:
            for name, data in itertools.chain.from_iterable(graph_data):
                super().write_data(csvs[name], data)

    def import_to_database(self):
        neo4j_admin = str(Path(self.dbms["base_path"], self.dbms["neo4j_admin"]).absolute())
        super().import_graph(neo4j_admin, node_paths=self.node_paths, link_paths=self.link_paths)

    def run(self):
        self.convert_to_csv()
        self.import_to_database()
