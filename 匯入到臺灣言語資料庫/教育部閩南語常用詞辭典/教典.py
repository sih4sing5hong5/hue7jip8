from django.conf import settings
from os.path import join
from os import makedirs
from urllib.request import urlopen
import io
from csv import DictReader
import json


class 教典():
    對應華語檔 = ('https://raw.githubusercontent.com/g0v/' +
             'moedict-data-twblg/master/uni/' +
             '%E5%B0%8D%E6%87%89%E8%8F%AF%E8%AA%9E.csv')
    詞目總檔 = ('https://raw.githubusercontent.com/g0v/' +
            'moedict-data-twblg/master/uni/' +
            '%E8%A9%9E%E7%9B%AE%E7%B8%BD%E6%AA%94.csv')

    def 下載對應華語檔(self):
        return self.下載(self.對應華語檔)

    def 下載詞目總檔(self):
        return self.下載(self.詞目總檔)

    def 下載(self, 下載網址):
        print('下載', 下載網址)
        語料目錄 = join(settings.BASE_DIR, '語料', '教典')
        makedirs(語料目錄, exist_ok=True)
        with urlopen(下載網址) as 資料檔案:
            全部資料csv = 資料檔案.read().decode('utf-8')
            with io.StringIO(全部資料csv) as 詞目:
                讀檔 = DictReader(詞目)
                輸出陣列 = []
                for 一逝 in 讀檔:
                    輸出陣列.append(一逝)
                return 輸出陣列

    def 取得臺羅對照華語(self):
        詞目總檔 = self.下載詞目總檔()
        對應華語檔 = self.下載對應華語檔()
        對應華語檔.sort(key=lambda x: int(x['n_no']))
        臺羅華結果 = []
        華語迴圈索引 = 0
        for 一詞目 in 詞目總檔:
            # 一臺多華分成多個詞
            # 多臺一華分成多個詞
            臺字 = 一詞目['詞目'].strip()
            臺編號 = 一詞目['主編碼'].strip()

            臺編號數字 = int(臺編號)
            for 索引, 一逝 in enumerate(對應華語檔[華語迴圈索引:], start=華語迴圈索引):
                n_no數字 = int(一逝['n_no'])
                if 一逝['n_no'] == 臺編號:
                    # 找到了同樣臺字主編碼的華字
                    華字 = 一逝['kokgi'].strip()
                    羅馬陣列 = 一詞目['音讀'].strip().split('/')
                    for 一羅馬 in 羅馬陣列:
                        臺羅華結果.append({
                            '臺字': 臺字,
                            '羅馬': 一羅馬,
                            '華字': 華字,
                        })
                elif 臺編號數字 < n_no數字:
                    # 已經沒有同樣臺字主編碼的華字
                    華語迴圈索引 = 索引
                    break
#                 elif 臺編號數字 > n_no數字:
#                     # 詞目總檔跳號
#                     # 原因：https://github.com/g0v/moedict-data-twblg/issues/10
#                     # 『對應華語的抓取是在詞目總檔更新前，所以可能已經改版』
#                     # 例：
#                     # 詞目：50637氣候 50639貨幣
#                     # 華語：26259,50637,氣候 26260,50638,帶領 26261,50639,貨幣
#                     # 詞目是50637，結束時，華語索引指到50638
#                     # 狀況：當詞目是50639，華語索引應該跳過50638
#                    continue
        return 臺羅華結果

    def 列印辭典(self):
        臺羅華結果 = self.取得臺羅對照華語()
        with open('列印教典.log', 'w') as outputfile:
            json.dump(臺羅華結果, outputfile, ensure_ascii=False, indent=2)
