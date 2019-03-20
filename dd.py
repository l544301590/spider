# -*-coding:utf-8-*-
import requests
import base64


def download_img(url, path):
    headers = {
        "Origin": "https://mp.weixin.qq.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Referer": "https://mp.weixin.qq.com/s?src=11&timestamp=1553059279&ver=1495&signature=Qsy5PbEgF0FvnCP*7s-tGwspFuEDRRc32nFuFda5fh-FL0tu4KLjF6L5ifSnk5uGD3PUuVWBhTIqtI37HfMgy6UEiEpaL5ZpH6*fRCyHAJ4yfAFoQB9EMPflu4gk--ca&new=1"
    }
    img = requests.get(url=url, headers=headers)
    img_data = img.content
    f = open(path, 'wb')
    f.write(img_data)
    f.close()


if __name__ == '__main__':
    url = "https://mmbiz.qpic.cn/mmbiz_png/7rGQr7yPGJrAfWFDSiaILj0glz8Kzbspo8QRlbZN3caoKgTGjHNb8wwLX8Glg9Ho1BOdYHP9FyaDRK1lf5YdNWQ/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1"
    path = "abc.png"
    download_img(url, path)

