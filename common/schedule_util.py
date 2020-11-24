import time
import os
import sched
import psutil
import json
import logging
import re
from logging.handlers import RotatingFileHandler

schedule = sched.scheduler(time.time, time.sleep)


def enter_(inc, task):
    task()
    schedule.enter(inc, 0, enter_, [inc, task])


def task():
    print('test task function')

# 定时任务函数
def schedule_(interval, task_func):
    if interval is None:
        interval=10
    schedule.enter(0, 0, enter_, [interval, task_func])
    schedule.run()


if __name__ == '__main__':
    print(schedule_(10, task_func=task))