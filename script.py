# -*-coding:utf-8-*-
import os
import time


IMG_ROOT = ""
POST_IMG_DIR = os.path.join(IMG_ROOT, "post")

if not POST_IMG_DIR:
    os.mkdir(POST_IMG_DIR)

time.localtime()