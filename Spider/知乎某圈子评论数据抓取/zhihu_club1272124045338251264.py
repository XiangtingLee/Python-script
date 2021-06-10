import re
import os
import json
import math
import requests

class ZhiHu(object):
    def __init__(self):
        self.base_url = "https://www.zhihu.com/api/v4/clubs/tags/1272124045338251264/posts?limit={1}&offset={0}"
        self.s = requests.session()
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"}

    def _detect(self):
        resp = self.s.get(self.base_url.format(0, 10), headers=self.headers)
        try:
            total = resp.json()["paging"]["totals"]
        except:
            total = 0
        print("total detect count: %s"%total)
        return total

    def get_all_data(self, page_lim : int = 100):
        data = []
        total = self._detect()
        method = "get"
        if os.path.exists("data.json"):
            with open("data.json", "r", encoding='UTF-8') as data_file:
                file_data = json.load(data_file)
            if len(file_data) == total:
                data += file_data
                print("total get count: %s" % len(data))
                return data
        if total:
            all_page = math.ceil(total / 100)
            for page in range(all_page):
                start = page * 100
                url = self.base_url.format(start, page_lim)
                print("start req: %s"%url)
                resp = self.s.get(url, headers=self.headers)
                try:
                    data += resp.json()["data"]
                except:
                    print("page %s no data!"%(page+1))
                    data += []
            with open("data.json", "w+", encoding='UTF-8') as f:
                f.writelines(json.dumps(data, indent=2, ensure_ascii=False))
            print("total download count: %s" % len(data))
            return data


    def ana(self, all_data):
        sup_keys = ["计算机", "软件", "数字媒体", "网络工程", "物联网"]
        sup_content = []
        for data in all_data:
            # 替换换行
            content = data["content"][0]["content"].replace("<br>", "\n")
            uid = data["author"]["id"]
            cid = data["id"]
            # 筛选关键字
            for key in sup_keys:
                if content.count(key):
                    sup_content.append((uid, content, cid))
                    break
        for uid, content, cid in sup_content:
            result = re.search("3[7-9]\d\.\d|3[7-9]\d", content)
            if result:
                # print(uid, cid)
                # print(result.group(0))
                print(cid,"\n", content,"\n","\n")

    def run(self):
        data = self.get_all_data()
        self.ana(data)


if __name__ == "__main__":
    z = ZhiHu()
    z.run()