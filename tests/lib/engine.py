# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Test class for the scaffolder engine"""
import os
import unittest

from plasoscaffolder.definitions import interface as definition_interface
from plasoscaffolder.definitions import manager as definition_manager
from plasoscaffolder.lib import engine
from plasoscaffolder.lib import errors
from plasoscaffolder.scaffolders import interface as scaffolder_interface


class AwesomeScaffolder(scaffolder_interface.Scaffolder):
  """Awesome test scaffolder."""
  NAME = 'Awesome'
  DESCRIPTION = 'This is a really awesome thing.'
  QUESTIONS = [
      scaffolder_interface.Question('test1', 'a', 'b', str),
      scaffolder_interface.Question('test2', 'a', 'b', str),
      scaffolder_interface.Question('test3', 'a', 'b', str)]

  def GenerateFiles(self):
    """Empty file generator."""
    return iter(())

  def GetFilesToCopy(self):
    """Empty files to copy generator."""
    return iter(())


class NotWrongDefinition(definition_interface.ScaffolderDefinition):
  """Definition for the not so wrong project."""
  NAME = 'N/A'

  def ValidatePath(self, root_path: str) -> bool:
    """Validate a path to the test project."""
    if 'wrong' in root_path:
      return False

    if 'error' in root_path:
      return False

    return True


class ScaffolderEngineTest(unittest.TestCase):
  """Test case for the scaffolder engine functions. """

  @classmethod
  def setUpClass(cls):
    definition_manager.DefinitionManager.RegisterDefinition(NotWrongDefinition)

  def testSetModuleName(self):
    """Test setting the module name."""
    test_engine = engine.ScaffolderEngine()
    test_name = 'foobar'

    test_engine.SetModuleName(test_name)

    module_name = getattr(test_engine, '_module_name', 'N/A')
    self.assertEqual(module_name, test_name.title())

    test_name = 'some module this is'
    expected_module_name = 'SomeModuleThisIs'
    expected_file_name = 'some_module_this_is'

    test_engine.SetModuleName(test_name)
    module_name = getattr(test_engine, '_module_name', 'N/A')
    file_name = getattr(test_engine, '_file_name_prefix', 'N/A')

    self.assertEqual(expected_module_name, module_name)
    self.assertEqual(expected_file_name, file_name)

  def testSetProjectRootPath(self):
    """Test setting the root path to a project."""
    test_engine = engine.ScaffolderEngine()

    # Test a path that will fail.
    path = os.path.join(os.path.curdir, 'wrong path')
    with self.assertRaises(errors.NoValidDefinition):
      test_engine.SetProjectRootPath(path)

    path = 'this is absolutely the correct path'
    test_engine.SetProjectRootPath(path)

    root_path = getattr(test_engine, '_definition_root_path', '')
    project = getattr(test_engine, '_definition', '')

    self.assertEqual(root_path, path)
    self.assertEqual(project, NotWrongDefinition.NAME)

  def testSetScaffolder(self):
    """Test setting the scaffolder of a scaffolder engine."""
    test_engine = engine.ScaffolderEngine()
    test_scaffolder = AwesomeScaffolder()

    test_engine.SetScaffolder(test_scaffolder)

    self.assertTrue(hasattr(test_engine, '_scaffolder'))
    self.assertIsInstance(
        getattr(test_engine, '_scaffolder', None), scaffolder_interface.Scaffolder)

  def testStoreScaffolderAttribute(self):
    """Test storing attributes in a scaffolder."""
    test_engine = engine.ScaffolderEngine()
    test_scaffolder = AwesomeScaffolder()
    test_engine.SetScaffolder(test_scaffolder)

    test_string1 = 'Test String'
    test_string2 = 'Part of the scaffolder'
    test_string3 = 'I\'m stored in the scaffolder!'

    test_engine.StoreScaffolderAttribute('test1', test_string1, str)
    with self.assertRaises(errors.ScaffolderNotConfigured):
      test_scaffolder.RaiseIfNotReady()

    test_engine.StoreScaffolderAttribute('test2', test_string2, str)
    with self.assertRaises(errors.ScaffolderNotConfigured):
      test_scaffolder.RaiseIfNotReady()

    test_engine.StoreScaffolderAttribute('test3', test_string3, str)
    self.assertIsNone(test_scaffolder.RaiseIfNotReady())

    scaffolder_attributes = getattr(test_scaffolder, '_attributes', {})
    test1_attr = scaffolder_attributes.get('test1', '')
    test2_attr = scaffolder_attributes.get('test2', '')
    test3_attr = scaffolder_attributes.get('test3', '')

    self.assertEqual(test1_attr, test_string1)
    self.assertEqual(test2_attr, test_string2)
    self.assertEqual(test3_attr, test_string3)

  def testEngineNotReady(self):
    """Test if the engine is fully configured."""
    test_engine = engine.ScaffolderEngine()
    with self.assertRaises(errors.EngineNotConfigured):
      _ = list(test_engine.GenerateFiles())

    path = 'this is absolutely the correct path'
    test_engine.SetProjectRootPath(path)

    with self.assertRaises(errors.EngineNotConfigured):
      _ = list(test_engine.GenerateFiles())

    test_engine.SetModuleName('TestBarWithFoo')
    with self.assertRaises(errors.EngineNotConfigured):
      _ = list(test_engine.GenerateFiles())

    with self.assertRaises(errors.ScaffolderNotConfigured):
      test_engine.StoreScaffolderAttribute('test1', 'foobar', str)

    test_engine.SetScaffolder(AwesomeScaffolder())
    with self.assertRaises(errors.EngineNotConfigured):
      _ = list(test_engine.GenerateFiles())

    test_string1 = 'Test String'
    test_string2 = 'Part of the scaffolder'
    test_string3 = 'I\'m stored in the scaffolder!'
    test_engine.StoreScaffolderAttribute('test1', test_string1, str)
    test_engine.StoreScaffolderAttribute('test2', test_string2, str)
    test_engine.StoreScaffolderAttribute('test3', test_string3, str)

    self.assertListEqual(list(test_engine.GenerateFiles()), [])


if __name__ == '__main__':
  unittest.main()
