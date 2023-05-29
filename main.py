import requests
import re


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # header = {
    #     'cookie':'cf_clearance=U1zhR6wWKJGM8wtzE446Y_TwHdmnww6thcqwXP9Z5T4-1684851168-0-250; forum_post_last_read_at="2023-05-23T16:12:59+02:00"; country=US; blacklisted_tags=[""]; konachan.net=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWIzMzc0NDJiMTliMDdmNTFhODMwOTI2NmIwZDI1M2FlBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMTd3R3VIdVFiSGxoUWtyMUhNdHkrUXR1bzBVNmZaQ2dNUlA0WHZqK1JVdVU9BjsARg==--da1d65aee5e7c8d34310ee063ab255516b336eb0; vote=1; __utma=20658210.1185020988.1684851181.1684851181.1684851181.1; __utmc=20658210; __utmz=20658210.1684851181.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=20658210.1.10.1684851181',
    #     'user-agent':'Mozilla / 5.0(Windows NT 10.0;Win64;) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 113.0.0.0Safari / 537.36Edg / 113.0.1774.50'
    # }
    #
    # res = requests.get('https://konachan.net/post?page=1',verify=False)
    header = {
        'user-agent':'Mozilla / 5.0(Windows NT 10.0;Win64;) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 113.0.0.0Safari / 537.36Edg / 113.0.1774.50'
    }

    res_html = requests.get('https://www.bilibili.com/video/BV1w84y1u777/')
    print(type(res_html.text))
    string_re = re.findall('window.__playinfo__=(.*?)</script>', res_html.text)[0]
    import json
    json_data = json.loads(string_re)
