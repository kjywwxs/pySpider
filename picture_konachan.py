import os
import requests
import re
import json
from log import logger

'''
一个konachan网站的爬虫，获取图片以及图片信息,如tag,作者等信息
'''
# 图片存放文件夹
dist_dir = ""
# 图片详细信息存放文件夹(json文件，包含tag，作者等)
dist_detail_info_dir = ""

if __name__ == '__main__':

    header = {
        'user-agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / '
                      '113.0.0.0Safari / 537.36Edg / 113.0.1774.50 '
    }
    # 本机开代理，端口号默认为10809
    proxy = {'https': '127.0.0.1:10809'}
    # 爬10页
    for i in range(1, 11):
        param = {
            "page": i
        }

        resp = requests.get('https://konachan.com/post', params=param, headers=header, proxies=proxy)
        json_img_list = re.findall(r"Post.register[(](.*)[)]", resp.text)

        dict_img_list = [json.loads(json_img) for json_img in json_img_list]  # 包含图片（详细信息）
        # id_url_img_list = [(dict_img.get('id'),dict_img.get('file_url')) for dict_img in dict_img_list]
        print('获取第{}页图片url成功，共{}张'.format(i, len(dict_img_list)))

        for j, detail_info in enumerate(dict_img_list):
            print('开始下载第{}张'.format(j + 1))
            img_id = detail_info.get('id')
            # 如果已经存在，则不再下载
            if os.path.exists("F:\\konachanPictures\\detailInfo\\{}.json".format(img_id)):
                print('第{}张已存在，跳过'.format(j + 1))
                continue
            resp = requests.get(detail_info.get('file_url'), headers=header, proxies=proxy)
            print('第{}张下载成功'.format(j + 1))
            with open("F:\\konachanPictures\\detailInfo\\{}.json".format(img_id), "w") as f:
                f.write(json.dumps(detail_info))
            with open("F:\\konachanPictures\\{}.jpg".format(img_id), "wb") as f:
                f.write(resp.content)
            print('第{}张保存成功'.format(j + 1))
