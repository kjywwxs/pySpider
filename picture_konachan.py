import os
import requests
import re
import json
from log import logger
from tqdm import tqdm

'''
一个konachan网站的爬虫，获取图片以及图片信息,如tag,作者等信息
author: kjywwxs
updata:2023-5-30
'''


class KonachanImgSpider:
    # 图片存放文件夹
    dist_dir = "F:\\konachanPictures"
    # 图片详细信息存放文件夹(json文件，包含tag，作者等)
    dist_detail_info_dir = "F:\\konachanPictures\\detailInfo"

    def __init__(self):
        self.header = {
            'user-agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / '
                          '113.0.0.0Safari / 537.36Edg / 113.0.1774.50 '
        }
        # 本机开代理，端口号默认为10809
        self.proxy = {'https': '127.0.0.1:10809'}
        self.base_url = 'https://konachan.com/post'
        self.img_info_list = []

    def get_img_info_list(self, pages_start=1, pages_end=10):
        '''
        根据页数获得图片的info，每张图的info是一个字典，包含url,tag等信息
        :param pages_start: 开始页码，默认1
        :param pages_end: 结束页码，默认10
        '''
        img_info_list = []
        for page in range(pages_start, pages_end + 1):
            try:
                _resp = requests.get(self.base_url, params={"page": page}, headers=self.header, proxies=self.proxy)
                _json_img_list = re.findall(r"Post.register[(](.*)[)]", _resp.text)
                _dict_img_list = [json.loads(json_img) for json_img in _json_img_list]  # info列表，包含url,tag等信息
                logger.info('获取第{}页图片info成功，共{}张'.format(page, len(_dict_img_list)))
                img_info_list.extend(_dict_img_list)
            except:
                logger.info('获取第{}页图片info失败'.format(page))
        self.img_info_list = img_info_list

    def download_img_list(self):
        img_info_list = self.img_info_list
        logger.info('共{}张图片'.format(len(img_info_list)))
        for i, detail_info in enumerate(img_info_list):
            img_id = detail_info.get('id')
            img_url = detail_info.get('file_url')
            logger.info('开始下载第{}张,图片id：{},图片url：{}'.format(i + 1, img_id, img_url))
            # 如果已经存在，则不再下载
            if os.path.exists("F:\\konachanPictures\\detailInfo\\{}.json".format(img_id)):
                logger.info('第{}张已存在，跳过'.format(i + 1))
                continue
            self._download_img(img_url,
                               "F:\\konachanPictures\\{}".format(str(img_id) + self.get_img_type_from_url(img_url)))
            # 保存文件info为json
            self._save_img_info("F:\\konachanPictures\\detailInfo\\{}.json".format(img_id), json.dumps(detail_info))
            logger.info('第{}张下载保存成功'.format(i + 1))

    def _save_img_info(self, dist_detail_info_name, data):
        '''
        保存图片tag等信息
        :param dist_detail_info_dir: 保存目录以及文件名
        :param data: 要保存的json数据
        '''
        with open(dist_detail_info_name, "w") as f:
            f.write(data)

    def _download_img(self, url: str, fname: str):
        '''
        下载图片
        :param url: 图片url地址
        :param fname: 图片保存的文件位置+文件名
        :return:
        '''
        # 用流stream的方式获取url的数据
        resp = requests.get(url, stream=True, headers=self.header, proxies=self.proxy)
        # 拿到文件的长度，并把total初始化为0
        total = int(resp.headers.get('content-length', 0))
        # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作了
        with open(fname, 'wb') as file, tqdm(
                desc=fname,
                total=total,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)

    @staticmethod
    def get_img_type_from_url(url):
        return url[url.rfind('.'):]


if __name__ == '__main__':
    konachan_img_spider = KonachanImgSpider()
    konachan_img_spider.get_img_info_list(pages_start=1, pages_end=20)
    konachan_img_spider.download_img_list()
