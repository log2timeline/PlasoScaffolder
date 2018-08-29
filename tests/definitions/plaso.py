# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Test class for the plaso project."""
import os
import unittest

from plasoscaffolder.lib import definitions
from plasoscaffolder.definitions import plaso


class PlasoProjectTest(unittest.TestCase):
  """Test case for the plaso project definition. """

  def testPlasoProject(self):
    """Test plaso project definitions."""
    test_path = os.path.join(os.path.dirname(
        os.path.dirname(os.path.dirname(__file__))), 'test_data')

    project_test = plaso.PlasoProject()
    self.assertEqual(project_test.NAME, definitions.DEFINITION_PLASO)

    self.assertTrue(project_test.ValidatePath(os.path.join(
        test_path, 'PlasoPath')))

    self.assertFalse(project_test.ValidatePath(os.path.join(
        test_path, 'PlasoFailPath1')))

    self.assertFalse(project_test.ValidatePath(os.path.join(
        test_path, 'PlasoFailPath2')))


if __name__ == '__main__':
  unittest.main()
