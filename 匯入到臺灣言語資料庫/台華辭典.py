from os.path import join
from django.conf import settings
from os import makedirs
from urllib.request import urlopen
import io
from csv import DictReader
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音相容教會羅馬字音標 import 臺灣閩南語羅馬字拼音相容教會羅馬字音標
from 臺灣言語工具.基本物件.公用變數 import 分字符號
from 臺灣言語工具.基本物件.公用變數 import 分詞符號
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.資料模型 import 外語表
import json


def 下載():
    語料目錄 = join(settings.BASE_DIR, '語料', '台華辭典')
    makedirs(語料目錄, exist_ok=True)
    with urlopen(
        'https://raw.githubusercontent.com/Taiwanese-Corpus/' +
        'Tinn-liong-ui_2000_taihoa-dictionary/master/' +
        '%E6%95%99%E8%82%B2%E9%83%A8%E5%BB%BA%E8%AD%B0%E7%94%A8%E5%AD%97/Taihoa.csv'
    ) as 資料檔案:
        全部資料csv = 資料檔案.read().decode('utf-8')
        with io.StringIO(全部資料csv) as 詞目:
            讀檔 = DictReader(詞目)
            輸出陣列 = []
            for 一逝 in 讀檔:
                輸出陣列.append(一逝)
            return 輸出陣列


def 匯入(陣列):
    for 一筆 in 陣列:
        匯入一筆(一筆)
    return


def 處理音標(音標):
    return (
        拆文分析器
        .建立句物件(文章粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音相容教會羅馬字音標, 音標))
        .轉音(臺灣閩南語羅馬字拼音相容教會羅馬字音標)
        .看型(物件分字符號=分字符號, 物件分詞符號=分詞符號)
    )


def 匯入一筆(一筆):
    # 12,a-bo2,a-bu2,阿母,;母親;媽媽;,mother,1884,Na
    # 華語, 英文都要照;拆開
    台語羅馬字 = 一筆['台語羅馬字'].strip()
    台語羅馬字2 = 一筆['台語羅馬字2'].strip()
    詞性 = 一筆['pos_h'].strip().strip(';')
    台語漢字 = 一筆['台語漢字'].strip()
    if 台語羅馬字2 == '':
        音標 = [
            處理音標(台語羅馬字)
        ]
    else:
        音標 = [
            處理音標(台語羅馬字), 處理音標(台語羅馬字2)
        ]
    for 華語 in 一筆['華語對譯'].strip(';').split(';'):
        存入外語表('華語', 音標, 台語漢字, 華語, 詞性)
    for 英文 in 一筆['英文'].strip(';').split(';'):
        if 英文:
            存入外語表('英語', 音標, 台語漢字, 英文, 詞性)
    return


def 存入外語表(外語語言, 音標, 台語漢字, 外語字, 詞性):
    公家 = {
        '收錄者': 來源表.objects.get_or_create(名='系統管理員')[0].編號(),
        '來源': 來源表.objects.get_or_create(名='台文華文線頂辭典')[0].編號(),
        '版權': 版權表.objects.get_or_create(版權='會使公開')[0].pk,
        '種類': '字詞',
        '語言腔口': '臺語',
        '著作所在地': '臺灣',
        '著作年': '2000',
    }
    外語內容 = {
        '外語語言': 外語語言,
        '外語資料': 外語字.strip(),
        '屬性': {'詞性': 詞性},
    }
    外語內容.update(公家)
    外語 = 外語表.加資料(外語內容)
    for 臺羅音標 in 音標:
        文本內容 = {
            '文本資料': 台語漢字,
            '音標資料': 臺羅音標,
        }
        文本內容.update(公家)
        外語.翻母語(文本內容)


def 列印辭典(陣列):
    列印陣列 = []
    for 一筆 in 陣列:
        列印陣列 += 列印一筆(一筆)
    with open('列印台華辭典.log', 'w') as outputfile:
        json.dump(列印陣列, outputfile, ensure_ascii=False)


def 列印一筆(一筆):
    # 12,a-bo2,a-bu2,阿母,;母親;媽媽;,mother,1884,Na
    # 華語, 英文都要照;拆開
    一筆陣列 = []
    台語羅馬字 = 一筆['台語羅馬字'].strip()
    台語羅馬字2 = 一筆['台語羅馬字2'].strip()
    臺字 = 一筆['台語漢字'].strip()
    if 台語羅馬字2 == '':
        音標 = [
            處理音標(台語羅馬字)
        ]
    else:
        音標 = [
            處理音標(台語羅馬字), 處理音標(台語羅馬字2)
        ]
    for 華字 in 一筆['華語對譯'].strip(';').split(';'):
        for 一音標 in 音標:
            一筆陣列.append({
                '臺字': 臺字,
                '羅馬': 一音標,
                '華字': 華字,
            })
    return 一筆陣列
