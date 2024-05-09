import requests
from lxml import etree
import pandas as pd

if __name__ == '__main__':
    resLs = []
    for page in range(335):
        page += 1
        url = f"https://news.fx678.com/column/forex/{page}"
        headers = {
            'Cookie': '__bid_n=18e5bdda2a84384817dcf2; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218e5bdda2c5180a-09b59f7fe507cb8-4c657b58-1166400-18e5bdda2c61e93%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fcn.bing.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThlNWJkZGEyYzUxODBhLTA5YjU5ZjdmZTUwN2NiOC00YzY1N2I1OC0xMTY2NDAwLTE4ZTViZGRhMmM2MWU5MyJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218e5bdda2c5180a-09b59f7fe507cb8-4c657b58-1166400-18e5bdda2c61e93%22%7D; tfstk=fXHm_XtyajPbpx70AQ2XEmHovkO8hZw_oVBTWRUwazz7Mjnv1OVar2QO_tWZZP0rrry_HxpiszuzkqhxX3wiD2qtSctbbPuZSPhvwpnjcRwwJPvppmGubqNrsrPV4hrTXDpAysijcRs52NRKam1gIhdOIRuaU7rgfR5abVrPazZ_bZyau3mrs88dFSCtBIVT-MhICEAfxhri0zXE2jqV0PJQ0OPSFkPmvmzus5DumS4Uwzgorxu-bxHbNLB7C0hnSfueysUqtk0u9jYhn20bb42xLhObN5kiIuGWS14n_mhI_7x23020o5k-zMC7nfujISGcfHiz34GQRSRWPuDxp54QZa8q2044tfjym_5EEr6_4hHl11N4Vu4K5Qg5mgMupdtkq6JuguZ2p3xl11N4Vu4pq3fhZSr70pC..; Hm_lvt_d25bd1db5bca2537d34deae7edca67d3=1711450595,1711451993,1711452802,1711528980; Hm_lpvt_d25bd1db5bca2537d34deae7edca67d3=1711528980; XSRF-TOKEN=eyJpdiI6Ikp2blkwSjNaTlZ2b2YzdE9vQWZSRGc9PSIsInZhbHVlIjoiMUM3WmZONlVCbU1zZE1nQlwvNGhhejVlMEhka1NoRHR0ZW5Ba05XQVhSSXFreUZFYmM4MWNnTUdPSlRya3dOYkUiLCJtYWMiOiI3ODU4YTdjMGQ3MDhlZDgxOTk5MzUzN2FkYjY0YTllZmExODAyMzgwNzAwZTQ4NTJiZjJiM2FiNzJlNTdmZDE0In0%3D; laravel_session=eyJpdiI6ImlxWkxncWNueHdGZEdBcnNSK05VV1E9PSIsInZhbHVlIjoiaElKUGtiVTJ2WklOUmlmZUhkMk1idEx6aGFhVVlMSWU3YmkzMzMyT1c4bmZSRzFTRHhpMHJOZ3NPVnRqVUhudSIsIm1hYyI6IjVlYTEyMjllYzRlYTgzZWVjZGUxZDRkOTFjNjdhYzAyMTRiM2QzZjUwYjhiYjQ3MTU3ZTNlZGE4MmIyNzJhNWYifQ%3D%3D',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        }
        #发送请求
        response = requests.get(url=url, headers=headers).text
        #数据解析
        tree = etree.HTML(response)
        titles = tree.xpath('//ul[@class="list"]//h3/text()')
        contents = tree.xpath('//ul[@class="list"]//p/text()')
        times = tree.xpath('//ul[@class="list"]//i/text()')
        for title, content, time in zip(titles, contents, times):
            dic = {
                '时间': time,
                '标题': title,
                '概要': content
            }
            resLs.append(dic)
    df = pd.DataFrame(resLs)
    df.to_csv('D:\汇通财经新闻文本.csv', index=False)
