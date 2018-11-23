# -*- coding: utf-8 -*-
# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Job to execute secret processing task."""

from __future__ import unicode_literals

# TODO: import from turbinia.evidence the needed files, eg:
# from turbinia.evidence import FilteredTextFile
from turbinia.jobs import interface
from turbinia.jobs import manager

# TODO: if needed import parts from turbinia.workers.


class SecretProcessingJob(interface.TurbiniaJob):
  """Need to add some description here."""

  # The types of evidence that this Job will process
  # TODO: Fill this out.
  evidence_input = []
  evidence_output = []

  NAME = 'SecretProcessingJob'

  def create_tasks(self, evidence):
    """Create task.

    Args:
      evidence: List of evidence object to process

    Returns:
        A list of tasks to schedule.
    """
    # TODO: Fill in the tasks.
    tasks = []
    return tasks


manager.JobsManager.RegisterJob(SecretProcessingJob)
