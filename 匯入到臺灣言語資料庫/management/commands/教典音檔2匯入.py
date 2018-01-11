from csv import DictReader
from os.path import basename, join, dirname, abspath
from posix import listdir

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone


from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.基本物件.公用變數 import 分字符號
from 臺灣言語工具.基本物件.公用變數 import 分詞符號
from 臺灣言語工具.解析整理.解析錯誤 import 解析錯誤


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--匯入幾筆',
            type=int,
            default=100000,
            help='試驗用，免一擺全匯'
        )

    def handle(self, *args, **參數):
        call_command('顯示資料數量')

        'https://github.com/g0v/moedict-data-twblg/tree/master/uni'
        詞目 = {}
        with open(join(
            dirname(abspath(__file__)), '..', '..',
            '教育部閩南語常用詞辭典', '詞目總檔.csv'
        )) as 檔案:
            for 一筆 in DictReader(檔案):
                編號 = 一筆['主編碼'].strip()
                漢字 = 一筆['詞目'].strip()
                拼音 = 一筆['音讀'].strip().split('/')[0]
                try:
                    正規化臺羅 = (
                        拆文分析器
                        .建立句物件(文章粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音, 拼音))
                        .轉音(臺灣閩南語羅馬字拼音)
                        .看型(物件分字符號=分字符號, 物件分詞符號=分詞符號)
                    )
                    拆文分析器.對齊組物件(漢字, 正規化臺羅)
                    詞目[int(編號)] = (漢字, 正規化臺羅)
                except 解析錯誤:
                    pass
        公家內容 = {
            '收錄者': 來源表.objects.get_or_create(名='系統管理員')[0].編號(),
            '來源': 來源表.objects.get_or_create(名='臺灣閩南語常用詞辭典')[0].編號(),
            '版權': 版權表.objects.get_or_create(版權='會使公開')[0].pk,
            '種類': '字詞',
            '語言腔口': '臺語',
            '著作所在地': '臺灣',
            '著作年': str(timezone.now().year),
            '屬性': {'語者': '王秀容'}
        }
        音檔目錄 = join(settings.BASE_DIR, '語料', '教育部閩南語常用詞辭典wav')
        匯入數量 = 0
        for 路徑 in sorted(listdir(音檔目錄)):
            音檔路徑 = join(音檔目錄, 路徑)
            if 音檔路徑.endswith('.wav'):
                try:
                    音檔編號 = int(basename(音檔路徑).split('.')[0])
                except ValueError:
                    raise ValueError('有的音檔有重錄過')
                try:
                    (漢字, 拼音) = 詞目[音檔編號]
                except KeyError:  # 有的詞條尾仔提掉矣，親像編號5
                    continue
                else:
                    影音內容 = {'影音所在': 音檔路徑}
                    影音內容.update(公家內容)
                    影音 = 影音表.加資料(影音內容)
                    文本內容 = {
                        '文本資料': 漢字,
                        '音標資料': 拼音,
                    }
                    文本內容.update(公家內容)
                    影音.寫文本(文本內容)

                    匯入數量 += 1
                    if 匯入數量 == 參數['匯入幾筆']:
                        break

        call_command('顯示資料數量')
