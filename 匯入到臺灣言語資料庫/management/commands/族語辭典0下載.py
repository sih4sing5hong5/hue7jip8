import json
from os import makedirs
from os.path import join, isfile
from random import randint
from time import sleep
from urllib.parse import quote
from urllib.request import urlopen, urlretrieve

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'https://github.com/thewayiam/ami_dict_crawler'

    def add_arguments(self, parser):
        parser.add_argument(
            '--下載幾筆',
            type=int,
            default=100000,
            help='試驗用，免一擺全匯'
        )

    def handle(self, *args, **參數):
        語料目錄 = join(settings.BASE_DIR, '族語辭典')
        makedirs(語料目錄, exist_ok=True)
        with urlopen(
            # 'https://github.com/thewayiam/ami_dict_crawler/raw/master/data/data.json'
            'https://github.com/Taiwanese-Corpus/ami_dict_crawler/raw/master/data/data.json'
        ) as 資料檔案:
            全部資料 = 資料檔案.read().decode('utf-8')
            資料 = json.loads(全部資料)
        with open(join(語料目錄, 'data.json'), 'w') as 檔案:
            檔案.write(全部資料)
        全部錄音檔 = []
        for 一筆 in 資料:
            錄音檔網址 = 一筆['pronounce']
            if 錄音檔網址 is not None:
                全部錄音檔.append(錄音檔網址)
            for 例句 in 一筆['examples']:
                錄音檔網址 = 例句['pronounce']
                if 錄音檔網址 is not None:
                    全部錄音檔.append(錄音檔網址)
        if len(全部錄音檔) != len(set(全部錄音檔)):
            raise RuntimeError('有仝網址的音檔')
        for 下載數量, 網址 in enumerate(全部錄音檔):
            所在 = join(語料目錄, 網址.split('/')[-1])
            if isfile(所在):
                print('{} 有矣'.format(所在))
            else:
                while True:
                    sleep(randint(33, 93))
                    print('掠 {} …'.format(所在))
                    try:
                        urlretrieve(quote(網址, safe='/:'), 所在)
                    except:
                        pass
                    else:
                        break
            if 下載數量 + 1 == 參數['下載幾筆']:
                break
