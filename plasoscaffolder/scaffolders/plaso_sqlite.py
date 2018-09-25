# -*- coding: utf-8 -*-

"""The scaffolder interface classes."""
import os
import sqlite3

from typing import Dict
from typing import Iterator
from typing import Tuple

from plasoscaffolder.scaffolders import interface
from plasoscaffolder.scaffolders import plaso
from plasoscaffolder.scaffolders import manager


class PlasoSQLiteScaffolder(plaso.PlasoPluginScaffolder):
  """The plaso SQLite plugin scaffolder.

  Attributes:
    database_name (str): name of the test SQLite database for the plugin.
    database_schema (dict): a dict containing all table names (keys) and the SQL
        statement used to create the table (value), derived from the test
        database.
    data_types (dict): a dict containing all the data types generated for the
        parser, the key is the name for each SQL statement run against the
        database and the value is the data type used for each generated event
        resulting from that SQL statement.
    queries (dict): a dict containing query name and SQL statements or queries
        run against the database.
    query_columns (dict): for each SQL statement run against the database, with
        the key being query name and value being a list of all SQL column names
        that are returned for each query.
    required_tables (list): a list of all required tables needed for the plugin
        to parse this particular database.
    timestamp_columns (dict): a dict containing a list of all columns with
        timestamp values, with query names as the key.
  """

  # The name of the plugin or parser this scaffolder provides.
  NAME = 'sqlite'
  DESCRIPTION = 'Provides a scaffolder to generate a plaso SQLite plugin.'

  SCHEMA_QUERY = (
      'SELECT tbl_name, sql '
      'FROM sqlite_master '
      'WHERE type = "table" AND tbl_name != "xp_proc" '
      'AND tbl_name != "sqlite_sequence"')

  # Filenames of templates.
  TEMPLATE_PARSER_FILE = 'sqlite_plugin.jinja2'
  TEMPLATE_PARSER_TEST = 'sqlite_plugin_test.jinja2'
  TEMPLATE_FORMATTER_FILE = 'sqlite_plugin_formatter.jinja2'
  TEMPLATE_FORMATTER_TEST = 'sqlite_plugin_formatter_test.jinja2'

  # Questions, a list that contains all the needed questions that the
  # user should be prompted about before the plugin or parser is created.
  # Each element in the list should be of the named tuple question.
  QUESTIONS = [
      interface.Question(
          'queries', 'Query name and SQL queries to extract data',
          ('Define the name of the SQL query as well as the actual '
           'SQL queries this plugin will execute'), dict),
      interface.Question(
          'required_tables', 'List of required tables',
          'Define a list of all required tables.', list)]

  def __init__(self):
    """Initializes the plaso SQLite plugin scaffolder."""
    super(PlasoSQLiteScaffolder, self).__init__()
    self.database_name = ''
    self.database_schema = {}
    self.data_types = {}
    self.queries = {}
    self.query_columns = {}
    self.required_tables = []
    self.timestamp_columns = {}

  def _GetQueryColumns(self, query: str) -> Iterator[str]:
    """Generates column names from a SQL statement.

    Args:
      query (str): a SQL query.

    Yields:
      str: a column name extracted from a SQL statement.
    """
    _, _, query_string = query.lower().partition('select')
    query_column_string, _, _ = query_string.partition('from')

    for column in query_column_string.split(','):
      _, _, column_alias = column.partition(' as ')
      column = column_alias or column

      _, _, column = column.rpartition('.')

      if not column:
        continue

      yield column.strip()

  def _GetSchema(self, database_path: str) -> Dict[str, str]:
    """Returns the schema of a SQLite database as a dict.

    Args:
      database_path (str): full path to the SQLite database.

    Returns:
      dict: containing:
        str: name of a table in the
        str:  SQL command that was used to create the table.

    Raises:
      sqlite3.DatabaseError: if the database cannot be read.
    """
    database = sqlite3.connect(database_path)
    try:
      database.row_factory = sqlite3.Row
      cursor = database.cursor()

      sql_results = cursor.execute(self.SCHEMA_QUERY)

      schema = {
          table_name: ' '.join(query.split())
          for table_name, query in sql_results}

    except sqlite3.DatabaseError:
      database.close()
      raise

    return schema

  def GetJinjaContext(self) -> Dict[str, object]:
    """Returns a dict that can be used as a context for Jinja2 templates.

    Returns:
      dict: containing:
        str: name of Jinja argument.
        object: Jinja argument value.
    """
    context = super(PlasoSQLiteScaffolder, self).GetJinjaContext()
    context['database_name'] = self.database_name
    context['database_schema'] = self.database_schema
    context['data_types'] = self.data_types
    context['queries'] = self.queries
    context['query_columns'] = self.query_columns
    context['required_tables'] = self.required_tables
    context['timestamp_columns'] = self.timestamp_columns
    return context

  def GenerateFiles(self) -> Iterator[Tuple[str, str]]:
    """Generates files required for the SQLite plugin.

    Yields:
      tuple: file name and content of the file to be written to disk.
    """
    _, _, database_name = self.test_file.rpartition(os.sep)
    self.database_name = database_name

    self.data_types = {}
    sql_columns = {}
    timestamp_columns = {}

    for query_name, query in self.queries.items():
      self.data_types[query_name] = '{0:s}:{1:s}'.format(
          self._output_name.lower().replace('_', ':'), query_name.lower())
      timestamp_columns[query_name] = []
      sql_columns[query_name] = []

      for column in self._GetQueryColumns(query):
        if 'time' in column:
          timestamp_columns[query_name].append(column.strip())
        sql_columns[query_name].append(column)

    self.query_columns = sql_columns
    self.timestamp_columns = timestamp_columns

    self.database_schema = self._GetSchema(self.test_file)

    for name, content in super(PlasoSQLiteScaffolder, self).GenerateFiles():
      yield name, content


manager.ScaffolderManager.RegisterScaffolder(PlasoSQLiteScaffolder)
