# Copyright 2021 The SODA Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
periodical task manager for metric collection tasks**
"""
from oslo_log import log

from delfin import manager
from delfin.coordination import ConsistentHashing
from delfin.task_manager.scheduler import schedule_manager
from delfin.task_manager.scheduler.schedulers.telemetry.job_handler \
    import FailedJobHandler
from delfin.task_manager.scheduler.schedulers.telemetry.job_handler \
    import JobHandler
from delfin.task_manager.tasks import telemetry

LOG = log.getLogger(__name__)


class MetricsTaskManager(manager.Manager):
    """manage periodical tasks"""

    RPC_API_VERSION = '1.0'

    def __init__(self, service_name=None, *args, **kwargs):
        self.telemetry_task = telemetry.TelemetryTask()
        super(MetricsTaskManager, self).__init__(*args, **kwargs)
        scheduler = schedule_manager.SchedulerManager()
        scheduler.start()
        JobHandler.schedule_boot_jobs()
        partitioner = ConsistentHashing()
        partitioner.start()
        partitioner.join_group()

    def assign_job(self, context, task_id):
        instance = JobHandler.get_instance(context, task_id)
        instance.schedule_job(task_id)

    def remove_job(self, context, task_id):
        instance = JobHandler.get_instance(context, task_id)
        instance.remove_job(task_id)

    def assign_failed_job(self, context, failed_task_id):
        instance = FailedJobHandler.get_instance(context, failed_task_id)
        instance.schedule_failed_job(failed_task_id)

    def remove_failed_job(self, context, failed_task_id):
        instance = FailedJobHandler.get_instance(context, failed_task_id)
        instance.remove_failed_job(failed_task_id)
