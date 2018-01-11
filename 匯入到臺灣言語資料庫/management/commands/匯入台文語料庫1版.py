import json
from os.path import basename, dirname

from django.core.management.base import BaseCommand


from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.資料模型 import 資料表工具
from 程式.全漢全羅.匯入檔案揣資料夾 import 揣資料夾內的語料


class Command(BaseCommand):
    help = '匯入高明達聽拍的資料庫'

    def add_arguments(self, parser):
        parser.add_argument(
            'json資料夾所在',  type=str
        )
        parser.add_argument(
            'wav資料夾所在',  type=str
        )

    def handle(self, *args, **參數):
        self.stdout.write(資料表工具.顯示資料數量())
        公家內容 = {
            '收錄者': 來源表.objects.get_or_create(名='系統管理員')[0],
            '來源': {'名': '台文資料庫'},
            '版權': 版權表.objects.get_or_create(版權='會使公開')[0],
            '種類': '語句',
            '語言腔口': '閩南語',
            '著作所在地': '臺灣',
            '著作年': '2015',
        }
        try:
            for json檔名, wav檔名 in 揣資料夾內的語料(參數['json資料夾所在'], 參數['wav資料夾所在']):
                影音內容 = {'影音所在': wav檔名}
                影音內容.update(公家內容)
                影音 = 影音表.加資料(影音內容)
                with open(json檔名) as json檔案:
                    json資料 = json.load(json檔案)
                資料夾名 = basename(dirname(wav檔名))
                聲音檔名 = basename(wav檔名)
                for 一筆 in json資料:
                    一筆['文本資料'] = 一筆['漢字']
                    一筆['音標資料'] = 一筆['臺羅']
                    一筆['內容'] = 一筆['分詞']
                    一筆['語者'] = 語者照資料夾(資料夾名, 聲音檔名, 一筆['語者'])
                聽拍內容 = {'聽拍資料': json資料}
                聽拍內容.update(公家內容)
                影音.寫聽拍(聽拍內容)
        except KeyboardInterrupt as 錯誤:
            print(錯誤)
        self.stdout.write(資料表工具.顯示資料數量())


def 語者照資料夾(資料夾, 檔名, 語者):
    if 資料夾 in [
        'ALen&Tea',
        'DaAi_blktc',
        'DaAi_csgr',
        'DaAi_urs',
        'DaAi_vvrs',
        'LTS',
        'MH',
        'Neighbor',
    ]:
        return '{}-{}'.format(資料夾, 語者)
    if 資料夾 in ['Dream_State']:
        if 語者 == '主持人':
            return '{}-{}'.format(資料夾, 語者)
        return '{}-{}-{}'.format(資料夾, 檔名, 語者)
    if 資料夾 in [
        'FTVN-1',
        'FTVN-2',
        'FTVN-3',
        'FTVN-4',
        'PTSN-1',
        'PTSN-2',
        'PTSN-3',
    ]:
        return '{}-{}-{}'.format(資料夾, 檔名, 語者)
    if 資料夾 == 'TW03':
        return '{}-{}'.format(
            資料夾,
            檔名.split('0')[0].replace(' ', '_').strip('012345_')
        )
    if 資料夾 == 'EDU':
        return '{}-{}'.format(
            資料夾,
            檔名
        )
    raise RuntimeError('「{}」資料夾無設定'.format(資料夾))
