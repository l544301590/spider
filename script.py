# -*-coding:utf-8-*-
import os
import time
import bs4
import requests
import re
import sys
from requests_toolbelt.multipart import MultipartEncoder
import json


DOMAIN = "https://myhomie.chinaxueyun.com/"
UPLOAD_IMG_API = "http://myhomie.chinaxueyun.com/info_platform/public/index.php/post/Index/uploadImg"
UPLAOD_VD_API = "http://myhomie.chinaxueyun.com/info_platform/public/index.php/post/Index/uploadVideo"
SEND_POST_API = "http://myhomie.chinaxueyun.com/info_platform/public/index.php/post/Index/sendPost"


def get_query_dict(url):
    tmp = url.split("?")
    if len(tmp) <= 1:
        return None
    query_list = tmp[1].split("&")
    d = {q.split("=")[0]: q.split("=")[1] for q in query_list}
    return d


def disable_webp(url):
    """remove "tp=webp" from the url"""

    d = get_query_dict(url)
    if d is None:
        return url
    if d.get("tp"):
        del d["tp"]
    query_list = []
    for key, value in d.items():
        query_list.append(key + "=" + value)
    query_str = "&".join(query_list)
    res = url.split("?")[0] + "?" + query_str
    return res


# def get_folder_of_today():
#     """use today's date string to create a folder and return the name of it"""
#
#     # get date info
#     t = time.localtime(time.time())
#     year, month, day = str(t[0]), str(t[1]), str(t[2])
#     year = year if len(year) == 4 else "0" + year
#     month = month if len(month) == 2 else "0" + month
#     day = day if len(day) == 2 else "0" + day
#     date = year + month + day
#
#     # if the path do not exist, create it
#     dir_date = POST_IMG_DIR + str(date) + "/"
#     if not os.path.exists(dir_date):
#         os.mkdir(dir_date)
#
#     return dir_date


def get_img_data(wx_img_url):
    """return the binary data of the image, given wechat img url"""

    # get image bin data TODO Un-comment 'origin'
    headers = {
        "Origin": "https://mp.weixin.qq.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    }  # the header may be not important
    img = requests.get(url=disable_webp(wx_img_url), headers=headers)
    img_data = img.content

    # # give the image a file name
    # d = get_query_dict(wx_img_url)
    # fmt = d["wx_fmt"]  # jpg or png or jpeg
    # fn = str(time.time()) + "." + fmt  # use timestamp to name file
    #
    # # get the whole path name on server and request url
    # path = get_folder_of_today() + fn
    # new_img_url = DOMAIN + path
    #
    # # save the image
    # f = open(path, 'wb')
    # f.write(img_data)
    # f.close()

    return img_data


def upload_img(img_data):
    """upload the img given image data, return the complete url"""

    data = MultipartEncoder({
        'img': ('abc.jpg', img_data)
    })
    headers = {
        "Content-Type": data.content_type,
        "Cookie": "PHPSESSID=2oek5ov42u3vj8lnsblkn6srj2"
    }
    response = requests.post(url=UPLOAD_IMG_API, data=data, headers=headers)
    res = json.loads(response.text.encode('utf-8').decode('utf-8-sig'))
    if res["status_code"] == "0":
        print("Cannot recognize the image data!")
        exit(0)
    return DOMAIN + res["link"]


def modify_src(html):
    """modify the html to make sure all the images can be shown in browser"""

    # if the attribute src and data-src both exist,
    # there will be two same images with different file names
    soup = bs4.BeautifulSoup(html, "lxml")
    for img in soup.find_all("img"):
        if img.get("src"):
            if re.match("https://mmbiz.qpic.cn/", img["src"]):
                img["src"] = upload_img(img["src"])
        if img.get("data-src"):
            if re.match("https://mmbiz.qpic.cn/", img["data-src"]):
                img["data-src"] = upload_img(img["data-src"])
                img["src"] = img["data-src"]
    return soup.prettify()


def send_post(post_type, title, cate, content):
    data = {
        "post_type": post_type,
        "title": title,
        "cate": cate,
        "content": content
    }
    requests.post(data=data, header={"Cookie": "PHPSESSID=2oek5ov42u3vj8lnsblkn6srj2"})

if __name__ == '__main__':
    # url = sys.argv[1]
    url = "https://mp.weixin.qq.com/s?src=11&timestamp=1553088601&ver=1496&signature=xRnJpMlUM6Zdb0j57OLkOuL3yZHu90CzwzMiNwycd-xr*rzabd4wqqPyAkDJEqUzrULVcK9ckfCTo31qSnr7F4tBpLX64J831dWpLCzEyaD8DhbEQmFElH8GAfH7pRGe&new=1"
    final_html = modify_src(requests.get(url).content)
    send_post('1', 'testest', 'test', final_html)

