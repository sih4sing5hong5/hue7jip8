import io
import json
from os.path import join

from django.core.management import call_command
from django.test.testcases import TestCase
from setuptools.py31compat import TemporaryDirectory


from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.models import 訓練過渡格式


class 匯入2版單元試驗(TestCase):
    def setUp(self):
        self.兩句 = [{
            "影音所在": "/home/ciciw/git/gi2_liau7_khoo3/音檔/MH/MaternalHome-003.wav",
            "聽拍資料": [
                {
                    "內容": "a1 khuann2-tio3 tsau9 gin1-na2 hong3 khi7-hu7 honnh4",
                    "口語臺羅": "a1 khuann2-tio3 tsau9 gin1-na2 hong3 khi7-hu7 honnh4",
                    "本調臺羅": "--ah4 khuann3-tioh8 tsau9 gin2-a2 hong9 khi1-hu7--honnh4",
                    "漢字": "啊看著（查某）囡仔（予人）欺負乎",
                    "結束時間": 125.706,
                    "語者": "高欣欣",
                    "開始時間": 123.242
                },
                {
                    "內容": "i7 to3 tshe3 be3-tiau5 ah4",
                    "口語臺羅": "i7 to3 tshe3 be3-tiau5 ah4",
                    "本調臺羅": "i1 to7 tse7 be7-tiau5--ah4",
                    "漢字": "伊就坐袂牢矣",
                    "結束時間": 127.084,
                    "語者": "高欣欣",
                    "開始時間": 125.706
                },
            ]
        }]

        self.兩檔 = [
            {
                "影音所在": "/home/ciciw/git/gi2_liau7_khoo3/音檔/MH/MaternalHome-003.wav",
                "聽拍資料": [
                    {
                        "內容": "a1 khuann2-tio3 tsau9 gin1-na2 hong3 khi7-hu7 honnh4",
                        "口語臺羅": "a1 khuann2-tio3 tsau9 gin1-na2 hong3 khi7-hu7 honnh4",
                        "本調臺羅": "--ah4 khuann3-tioh8 tsau9 gin2-a2 hong9 khi1-hu7--honnh4",
                        "漢字": "啊看著（查某）囡仔（予人）欺負乎",
                        "結束時間": 125.706,
                        "語者": "高欣欣",
                        "開始時間": 123.242
                    },
                ],
            },
            {
                "影音所在": "/home/ciciw/git/gi2_liau7_khoo3/音檔/MH/MaternalHome-003.wav",
                "聽拍資料": [
                    {
                        "內容": "a1 khuann2-tio3 tsau9 gin1-na2 hong3 khi7-hu7 honnh4",
                        "口語臺羅": "a1 khuann2-tio3 tsau9 gin1-na2 hong3 khi7-hu7 honnh4",
                        "本調臺羅": "--ah4 khuann3-tioh8 tsau9 gin2-a2 hong9 khi1-hu7--honnh4",
                        "漢字": "啊看著（查某）囡仔（予人）欺負乎",
                        "結束時間": 125.706,
                        "語者": "高欣欣",
                        "開始時間": 123.242
                    },
                    {
                        "內容": "i7 to3 tshe3 be3-tiau5 ah4",
                        "口語臺羅": "i7 to3 tshe3 be3-tiau5 ah4",
                        "本調臺羅": "i1 to7 tse7 be7-tiau5--ah4",
                        "漢字": "伊就坐袂牢矣",
                        "結束時間": 127.084,
                        "語者": "高欣欣",
                        "開始時間": 125.706
                    },
                ]
            }
        ]

    def test_匯入數量(self):
        with TemporaryDirectory() as 資料夾:
            聲音檔所在 = join(資料夾, 'audio.wav')
            資料檔所在 = join(資料夾, 'twisas2.json')
            with open(聲音檔所在, 'wb') as 檔案:
                檔案.write(聲音檔.對參數轉(2, 16, 1, b'khiau2' * 16000).wav格式資料())
            self.兩檔[0]['影音所在'] = 聲音檔所在
            self.兩檔[1]['影音所在'] = 聲音檔所在
            with open(資料檔所在, 'wt') as 檔案:
                json.dump(self.兩檔, 檔案)
            with io.StringIO() as out:
                call_command('匯入台文語料庫2版', 資料檔所在, stdout=out)
        self.assertEqual(訓練過渡格式.資料數量(), 2)

    def test_匯入內容(self):
        with TemporaryDirectory() as 資料夾:
            聲音檔所在 = join(資料夾, 'audio.wav')
            資料檔所在 = join(資料夾, 'twisas2.json')
            with open(聲音檔所在, 'wb') as 檔案:
                檔案.write(聲音檔.對參數轉(2, 16, 1, b'khiau2' * 16000).wav格式資料())
            self.兩句[0]['影音所在'] = 聲音檔所在
            with open(資料檔所在, 'wt') as 檔案:
                json.dump(self.兩句, 檔案)
            with io.StringIO() as out:
                call_command('匯入台文語料庫2版', 資料檔所在, stdout=out)
        self.assertEqual(訓練過渡格式.objects.get().聽拍, self.兩句[0]['聽拍資料'])
