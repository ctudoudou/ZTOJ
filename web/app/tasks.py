#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/12 下午9:47
# @Author  : tudoudou
# @File    : tasks.py.py
# @Software: PyCharm

# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import ast

from celery import Celery
import requests
from app.models import Example, Submits

app = Celery('tasks', backend='redis://localhost', broker='redis://localhost')


@app.task
def problem_add(token, language, code, sample):
    result = requests.post('http://127.0.0.1:2333/add',
                           {'token': str(token), 'language': language, 'code': code, 'sample': sample})
    # TODO eval之后要去掉
    fresult = eval(result.content.decode())['s1']
    print(fresult)
    print(type(fresult))
    error = fresult['error']
    stdout = fresult['stdout']
    time = fresult['time']
    temp = Example.objects.filter(id=token).update(error=error, stdout=stdout, time=time)
    return 0


@app.task
def problem_submit(token, language, code, time, memory, sample):
    result = requests.post('http://127.0.0.1:2333/judge',
                           {'token': token, 'language': language, 'code': code, 'time': time, 'memory': memory,
                            'sample': sample})
    result = result.content.decode()
    try:
        result= float(result)
    except:
        result = ['0','1','Code Error', 'Memory Overflow', 'Time Overflow', 'Compile Error', 'Unknown Error'].index(result)
    temp = Submits.objects.filter(id=token).update(pass_field=result)
    return result
