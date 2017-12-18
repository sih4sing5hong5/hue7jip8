from csv import DictReader, DictWriter
import json

from django.core.management import call_command
from django.core.management.base import BaseCommand


from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音相容教會羅馬字音標 import 臺灣閩南語羅馬字拼音相容教會羅馬字音標


class Command(BaseCommand):
    公家 = {
        '收錄者': 來源表.objects.get_or_create(名='系統管理員')[0].編號(),
        '來源': 來源表.objects.get_or_create(名='辨識計劃')[0].編號(),
        '版權': 版權表.objects.get_or_create(版權='會使公開')[0].pk,
        '種類': '字詞',
        '語言腔口': '臺語',
        '著作所在地': '臺灣',
        '著作年': '2017',
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '常用詞csv',
        )
        parser.add_argument(
            '辭典json',
        )
        parser.add_argument(
            '語言模型詞表',
        )
        parser.add_argument(
            '--匯入幾筆',
            type=int,
            default=10000000,
            help='試驗用，免一擺全匯'
        )

    def handle(self, *args, **參數):
        call_command('顯示資料數量')
        結果 = []
        無對著的 = []
        台華辭典 = self._辭典台華對應(參數['辭典json'], 參數['語言模型詞表'])
        for (漢字, 臺羅, 頻次nc) in self._csv的index(參數['常用詞csv']):
            if (漢字, 臺羅) in 台華辭典:
                結果.append((漢字, 臺羅, 頻次nc, 台華辭典[(漢字, 臺羅)]))
            else:
                無對著的.append((漢字, 臺羅, 頻次nc))
        self._輸出對著結果(結果)
        self._輸出無揣著(無對著的)
        print(len(台華辭典), len(結果))

    def _輸出對著結果(self, 結果):
        with open('台華有對應.csv', 'w') as 常用詞csv:
            fieldnames = ['漢字', '臺羅', '頻次nc', '華語']
            writer = DictWriter(常用詞csv, fieldnames=fieldnames)

            writer.writeheader()
            for 漢字, 臺羅, 頻次nc, 華語陣列 in 結果:
                for 華語 in 華語陣列:
                    writer.writerow({
                        '漢字': 漢字,
                        '臺羅': 臺羅,
                        '頻次nc': 頻次nc,
                        '華語': 華語,
                    })

    def _輸出無揣著(self, 結果):
        with open('台華無對著.csv', 'w') as 常用詞csv:
            fieldnames = ['漢字', '臺羅', '頻次nc']
            writer = DictWriter(常用詞csv, fieldnames=fieldnames)

            writer.writeheader()
            for 漢字, 臺羅, 頻次nc, in 結果:
                writer.writerow({
                    '漢字': 漢字,
                    '臺羅': 臺羅,
                    '頻次nc': 頻次nc,
                })

    def _buaih(self):
        匯入數量 = 0
        for 漢字, 臺羅, 頻次nc, 華語 in 結果:
            外語內容 = {
                '外語語言': '華語',
                '外語資料': 華語,
            }
            外語內容.update(self.公家)
            外語 = 外語表.加資料(外語內容)
            文本內容 = {
                '文本資料': 漢字,
                '音標資料': 臺羅,
            }
            文本內容.update(self.公家)
            外語.翻母語(文本內容)
            匯入數量 += 1
            if 匯入數量 == 參數['匯入幾筆']:
                break
        call_command('顯示資料數量')

    def _csv的index(self, 常用詞csv所在):
        with open(常用詞csv所在) as 常用詞csv:
            for 一逝 in DictReader(常用詞csv):
                臺羅 = 一逝['臺羅'].strip()
                數字調 = (
                    拆文分析器
                    .分詞句物件(文章粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音, 臺羅))
                    .轉音(臺灣閩南語羅馬字拼音相容教會羅馬字音標)
                )
                yield 一逝['台語漢字'].strip(), 數字調.看型('-'), 一逝['頻次nc']

    def _辭典台華對應(self, 辭典json所在, 語言模型詞表所在):
        詞表 = set()
        with open(語言模型詞表所在) as 語言模型詞表:
            for 一逝 in 語言模型詞表.readlines():
                詞表.add(一逝.split()[0])
        資料 = {}
        with open(辭典json所在) as 辭典json:
            for 一條 in json.load(辭典json):
                華字 = 一條['華字']
                if 華字 in 詞表:
                    漢字 = 文章粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音相容教會羅馬字音標, 一條['臺字'])
                    臺羅 = 文章粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音相容教會羅馬字音標, 一條['羅馬'])
                    數字調 = (
                        拆文分析器
                        .分詞句物件(文章粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音, 臺羅))
                        .轉音(臺灣閩南語羅馬字拼音相容教會羅馬字音標)
                    )
                    標準 = 數字調.看型('-')
                    try:
                        資料[(漢字, 標準)].append(華字)
                    except KeyError:
                        資料[(漢字, 標準)] = [華字]
        return 資料
