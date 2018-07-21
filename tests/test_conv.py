from unittest import mock

from csv2neo4jcsv import Csv2Neo4jCsv, Neo4jImportHandler

import unittest

from csv_util import CsvUtil


class TestConfigurable(unittest.TestCase):

    def test_basic_impl(self):

        class DataImportMock(Neo4jImportHandler):

            def import_graph(self, neo4j_admin, node_paths, link_paths):
                pass

        class CsvMock(CsvUtil):

            def write_data(self, csv_file, data):
                pass

            def reset(self, path, *sub_files):
                pass

            def iterate(self, csv_path, encoding):
                yield from [
                    ['nd_1', 'nd_2', '1'],
                    ['nd_2', 'nd_3', '2'],
                    ['nd_3', 'nd_1', '3']
                ]

            def open_csv(self, path, encoding, **kwargs):
                return [f'stub {path}']

        class MockedCsv2Neo4j(Csv2Neo4jCsv, CsvMock,DataImportMock):

            def __init__(self):
                super().__init__(
                    src={
                        'path': "src/of/node",
                        'encoding': 'shift-jis',
                    },
                    model={
                        'node_1': 0,
                        'node_2': 1,
                        'attr_1': 2,
                    },
                    dst={
                        'encoding': 'utf-8',
                        'node_path': 'dst/of/nodes',
                        'link_path': 'dst/of/links',
                        'csv_files': {
                            'node': ['NODE'],
                            'link': ['LINK']
                        }
                    },
                    dbms={
                        'base_path': 'path/to/database',
                        'neo4j_admin': 'bin/neo4j-admin.bat'
                    }
                )

            def init(self):
                return {}

            def converter(self, row, **kwargs):
                return [
                    ('NODE', 2),
                    ('LINK', 3)
                ]

        test = MockedCsv2Neo4j()
        test.run()
        test.convert_to_csv()

        test.import_to_database()


if __name__ == '__main__':
    unittest.main()
