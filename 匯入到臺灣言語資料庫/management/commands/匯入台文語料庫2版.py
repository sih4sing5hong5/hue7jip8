import json

from django.core.management.base import BaseCommand


from 臺灣言語服務.models import 訓練過渡格式


class Command(BaseCommand):
    help = '匯入高明達聽拍的twisas資料庫'

    公家內容 = {
        '來源': '台文資料庫',
        '種類': '語句',
        '年代': '2018',
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '聽拍json',  type=str
        )

    def handle(self, *args, **參數):
        self.stdout.write('資料數量：{}'.format(訓練過渡格式.資料數量()))

        全部資料 = []
        匯入數量 = 0
        with open(參數['聽拍json']) as 檔案:
            for 資料 in json.load(檔案):
                全部資料.append(
                    訓練過渡格式(
                        影音所在=資料['影音所在'],
                        聽拍=資料['聽拍資料'],
                        **self.公家內容
                    )
                )

                匯入數量 += 1
                if 匯入數量 % 100 == 0:
                    self.stdout.write('匯入 {} 筆'.format(匯入數量))

        self.stdout.write('檢查格式了匯入')
        訓練過渡格式.加一堆資料(全部資料)

        self.stdout.write('資料數量：{}'.format(訓練過渡格式.資料數量()))
