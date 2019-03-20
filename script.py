# -*-coding:utf-8-*-
import os
import time
import bs4


IMG_ROOT = ""
POST_IMG_DIR = os.path.join(IMG_ROOT, "post")


def get_folder_of_today():
    # get date info
    t = time.localtime(time.time())
    year, month, day = t[0], t[1], t[2]

    # if these paths do not exist, create them
    dir_year = os.path.join(POST_IMG_DIR, str(year))
    if not os.path.exists(dir_year):
        os.mkdir(dir_year)
    dir_month = os.path.join(dir_year, str(month))
    if not os.path.exists(dir_month):
        os.mkdir(dir_month)
    dir_day = os.path.join(dir_month, str(day))
    if not os.path.exists(dir_day):
        os.mkdir(dir_day)

    return dir_day


def save_img():
    t = time.localtime(time.time())
    h, m, s = str(t[3]), str(t[4]), str(t[5])
    h = h if len(h) == 2 else "0" + h
    m = m if len(m) == 2 else "0" + m
    s = s if len(s) == 2 else "0" + s
    fn = h + m + s + ".jpg"
    path = os.path.join(get_folder_of_today(), fn)






if not POST_IMG_DIR:
    os.mkdir(POST_IMG_DIR)

time.localtime()