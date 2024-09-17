# -*- coding: UTF-8 -*-
'''
@Project ：OneForAll 
@File    ：subdomain_worker.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/8/25 10:13 
@Comment ： 
'''
import json

import pymongo

from modules.database.consumer import RabbitMQConsumer
from modules.database.db import conn_db
from modules.heartbeat import Heartbeat
from oneforall import OneForAll
from config import settings
from config.log import logger
from common.task import Task

def oneforall(domain):
    test = OneForAll(target=domain)
    test.dns = False
    test.brute = True
    test.req = False
    test.takeover = False
    test.enrich = True
    test.run()
    results = test.datas
    return results

class Subdomain(Task):
    def __init__(self, task):
        self.task = task
        self.results = list()

        Task.__init__(self, task_id=task["task_id"])

    def do_scan(self):
        rs = oneforall(self.task["domain"])
        # 处理数据
        s = []
        for r in rs:
            s.append(r["subdomain"])
        s = set(list(s))
        for subdomain in s:
            self.results.append({
                "domain": self.task["domain"],
                "subdomain": subdomain,
                "source": "oneforall",
            })

    def save_db(self):
        logger.log('INFOR', f'Start save db results')
        if len(self.results) == 0:
            pass
        else:
            while True:
                # 存入数据库
                try:
                    db = conn_db("subdomain")
                    db.insert_many(self.results, ordered=False)
                    return
                except pymongo.errors.BulkWriteError as e:
                    for error in e.details['writeErrors']:
                        if error['code'] == 11000:  # E11000 duplicate key error collection，忽略重复主键错误
                            return
                            # print(f"Ignoring duplicate key error for document with _id {error['op']['_id']}")
                        else:
                            logger.log("ERROR", f"{error['code']}: {error['message']}")
                            logger.log("INFOR", "尝试重新save_db....")
                except Exception as e:
                    logger.log("ERROR", f"error：{e}")
                    logger.log("INFOR", "尝试重新save_db....")

    def run(self):
        self.receive_task()
        self.do_scan()
        self.save_db()
        self.finnish_task(time_escape="xxx", lens=len(self.results))


def run(task):
    """
    类调用统一入口

    @return:
    """
    sd = Subdomain(task)
    sd.run()

class SubdomainWorker(RabbitMQConsumer):
    def __init__(self, queue_name):
        super().__init__(queue_name)

    def task_handle(self):
        task = json.loads(self.message)
        run(task)

if __name__ == '__main__':
    # 启动心跳程序
    if settings.heart_beat_open == "true":
        hb = Heartbeat("心跳线程")
        hb.start()

    worker = SubdomainWorker("subdomain_oneforall_task")
    worker.start_consuming()
