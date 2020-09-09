from redis import Redis
import json
from datetime import datetime
from os import environ
import logging
from uuid import uuid4, UUID
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

TASKS_KEY='tasks'
RESULTS_KEY='areas'

class Task:
    
    error = False
    
    def _consolidate(self):
        self._redis.hset(RESULTS_KEY, self.id, self.asdict())

    def __init__(self, redis, task_id=False):
        """Either loads a task from the results table (with task_id set), or waits for a new task to be added to the queue"""
        self._redis = redis
        if not task_id:
            self.task_body = json.loads(redis.blpop(TASKS_KEY)[1])
        else:
            res = self._redis.hget(RESULTS_KEY,task_id)
            if res:
                self.task_body = json.loads(res)
            else:
                return None

        self.id = self.task_body['id']
        logger.info(f"\t\t*[{self.id}] Fetched task.")

    def start(self):
        self.expires = datetime.now() + datetime.timedelta(seconds=60)
        self._consolidate()
        logger.info(f"\t\t*[{self.id}] Starting task, expiring at {self.expires}.")

    def done(self):
        self.expires = False
        self._consolidate()

    def is_expired(self):
        self.expires > datetime.now()

    def raise_error(self, message):
        self['error'] = message
        self._consolidate()

    def asdict(self):
        d = self.task_body
        if self.expires:
            d['expires'] = self.expires.isoformat()
        return d

    def __setitem__(self, key, value):
        self.task_body[key] = value
    
    def __getitem__(self, key):
        return self.task_body[key]