# -*- encoding: utf-8 -*-
from ..lb_task import LbTask

from lazyblacksmith.extension.celery_app import celery_app
from lazyblacksmith.extension.esipy import esiclient
from lazyblacksmith.extension.esipy.operations import get_industry_systems
from lazyblacksmith.models import IndustryIndex
from lazyblacksmith.models import TaskState
from lazyblacksmith.models import db
from lazyblacksmith.utils.time import utcnow

from datetime import datetime
from email.utils import parsedate

import json
import pytz


@celery_app.task(name="update_industry_indexes", base=LbTask, bind=True)
def task_update_industry_indexes(self):
    """ Get the industry indexes list from API. """
    self.start()
    all_indexes = esiclient.request(get_industry_systems())
    insert_index_list = []

    if all_indexes.status == 200:
        for index in all_indexes.data:
            solar_system = index.solar_system_id

            for activity_index in index.cost_indices:
                row = {}
                row['solarsystem_id'] = solar_system
                row['activity'] = IndustryIndex.activity_string_to_activity(
                    activity_index.activity
                )
                row['cost_index'] = activity_index.cost_index
                insert_index_list.append(row)

        db.engine.execute("TRUNCATE TABLE %s" % IndustryIndex.__tablename__)
        db.engine.execute(
            IndustryIndex.__table__.insert(),
            insert_index_list
        )
        db.session.commit()
        self.end(TaskState.SUCCESS)
        
    else:
        self.end(TaskState.ERROR)

