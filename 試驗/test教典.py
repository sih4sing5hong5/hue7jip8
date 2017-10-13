from django.test.testcases import TestCase
from 匯入到臺灣言語資料庫.教育部閩南語常用詞辭典.教典 import 教典


class 教典試驗(TestCase):

    def setUp(self):
        self.一月日詞目 = {
            '主編碼': '6',
            '屬性': '1',
            '詞目': '一月日',
            '音讀': 'tsi̍t gue̍h-ji̍t/tsi̍t ge̍h-li̍t',
            '文白屬性': '0',
            '部首': '',
        }
        self.一日月華語 = {
            'kokgi_no': '9',
            'n_no': '6',
            'kokgi': '一個月',
            'kokgi_v': '一個月',
        }
        self.一教典 = 教典()

    def test下載詞目正確(self):
        詞目總檔陣列 = self.一教典.下載詞目總檔()
        self.assertEqual(詞目總檔陣列[4], self.一月日詞目)
        self.assertEqual(len(詞目總檔陣列), 25881)

    def test下載華語正確(self):
        華語檔陣列 = self.一教典.下載對應華語檔()
        self.assertEqual(華語檔陣列[8], self.一日月華語)
        self.assertEqual(len(華語檔陣列), 30416)

    def test取得一臺羅一華語(self):
        臺羅華陣列 = self.一教典.取得臺羅對照華語()
        有揣到 = False
        for 一物件 in 臺羅華陣列:
            if 一物件['臺字'] == '一刀兩斷':
                有揣到 = True
                self.assertEqual(一物件, {
                    '臺字': '一刀兩斷',
                    '羅馬': 'it-to-lióng-tuān',
                    '華字': '一刀兩斷',
                })
        self.assertTrue(有揣到)

    def test取得多臺羅一華語(self):
        臺羅華陣列 = self.一教典.取得臺羅對照華語()
        數量 = 0
        for 一物件 in 臺羅華陣列:
            if 一物件['臺字'] == '一月日':
                數量 += 1
        self.assertEqual(數量, 2)

    def test取得一臺羅多華語(self):
        臺羅華陣列 = self.一教典.取得臺羅對照華語()
        數量 = 0
        for 一物件 in 臺羅華陣列:
            if 一物件['羅馬'] == 'tsi̍t' and 一物件['臺字'] == '一':
                數量 += 1
        self.assertEqual(數量, 2)

    def test取得一臺羅一華語去空白(self):
        臺羅華陣列 = self.一教典.取得臺羅對照華語()
        有揣到 = False
        for 一物件 in 臺羅華陣列:
            if 一物件['臺字'] == '介紹' and 一物件['華字'].startswith('引進'):
                有揣到 = True
                self.assertEqual(一物件, {
                    '臺字': '介紹',
                    '羅馬': 'kài-siāu',
                    '華字': '引進',
                })
        self.assertTrue(有揣到)

    def test不要出現無華字的臺字(self):
        臺羅華陣列 = self.一教典.取得臺羅對照華語()
        有揣到 = False
        for 一物件 in 臺羅華陣列:
            if 一物件['臺字'] == '戇的也有一項會。':
                有揣到 = True
        self.assertFalse(有揣到)

    def test最後一個華字(self):
        臺羅華陣列 = self.一教典.取得臺羅對照華語()
        有揣到 = False
        for 一物件 in 臺羅華陣列:
            if 一物件['臺字'] == '肥朒朒':
                有揣到 = True
                self.assertEqual(一物件, {
                    '臺字': '肥朒朒',
                    '羅馬': 'puî-tsut-tsut',
                    '華字': '肥嘟嘟',
                })
        self.assertTrue(有揣到)

    def test排序後最後一個華字(self):
        臺羅華陣列 = self.一教典.取得臺羅對照華語()
        有揣到 = False
        for 一物件 in 臺羅華陣列:
            if 一物件['臺字'] == '短打':
                有揣到 = True
        self.assertTrue(有揣到)
