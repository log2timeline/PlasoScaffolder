# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the Timesketch index analyzer scaffolder."""
import unittest

from plasoscaffolder.scaffolders import timesketch_index


class TimesketchIndexScaffolderTest(unittest.TestCase):
  """Test class for the Timesketch index analyzer plugin scaffolder."""

  maxDiff = None

  def testTimesketchIndexScaffolder(self):
    """Test the Timesketch index analyzer scaffolder."""
    scaffolder = timesketch_index.TimesketchIndexScaffolder()
    scaffolder.SetOutputName('testing')

    file_copy_paths = [x for _, x in scaffolder.GetFilesToCopy()]
    self.assertEqual(file_copy_paths, [])

    files_generated = dict(scaffolder.GenerateFiles())

    expected_files = frozenset([
        'timesketch/lib/analyzers/testing.py',
        'timesketch/lib/analyzers/testing_test.py',
        'timesketch/lib/analyzers/__init__.py'])
    self.assertEqual(set(files_generated.keys()), expected_files)

    expected_parser_init_addition = (
        '# TODO: put in alphabetical order.\nfrom '
        'timesketch.lib.analyzers import testing')
    self.assertEqual(
        expected_parser_init_addition,
        files_generated['timesketch/lib/analyzers/__init__.py'])

    with open('test_data/timesketch_testing_plugin.py', 'r') as fh:
      expected_parser_content = fh.read()
    self.assertEqual(
        expected_parser_content,
        files_generated['timesketch/lib/analyzers/testing_test.py'])


if __name__ == '__main__':
  unittest.main()
