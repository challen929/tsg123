import json
import re
import requests
import pymysql
import datetime

from books import models


class Listen:

    def prepare(self):
        pre_values = models.PrePrice.objects.values()
        for values in pre_values:
            del values['id']
            models.HistoryPrice.objects.create(**values)

        models.PrePrice.objects.all().delete()

        cur_values = models.CurrentPrice.objects.values()
        for values in cur_values:
            del values["id"]
            del values["final_discount"]
            del values["pre_price"]
            del values["bot_price"]
            del values["link"]
            models.PrePrice.objects.create(**values)

        models.CurrentPrice.objects.all().delete()

    def download(self, excepts=False):
        if excepts:
            remove_ids = models.CurrentPrice.objects.values_list("product_id")
            book_ids = models.ListenList.objects.exclude(product_id__in=remove_ids).values_list("product_id")
        else:
            book_ids = models.ListenList.objects.values_list("product_id")
        for book_id in book_ids:
            res1 = requests.get('https://p.3.cn/prices/mgets?pduid=421958664&skuIds=J_%s' % book_id[0])
            res2 = requests.get(
                'https://wq.jd.com/commodity/promo/get?skuid=%s' % book_id[0]
            )
            content1 = json.loads(res1.content)[0]  # 字典
            content2 = res2.content.decode("utf-8") # 字符串
            temp = re.search("每满(\d+)元，可减(\d+)元现金", content2)
            if temp:
                a = int(temp.group(1))
                b = int(temp.group(2))
                prom_memo = "%s-%s" % (a, b)
                prom_discount = (a-b)/a
            else:
                prom_memo = "100-0"
                prom_discount = 1
            ori_price = float(content1.get('m'))
            daily_price = float(content1.get('op'))
            cut_price = float(content1.get('p')) if float(content1.get('p', '0')) > 0 else daily_price
            plus_price = float(content1.get('tpp')) if float(content1.get('tpp', '0')) > 0 else daily_price
            final_price = min(cut_price, plus_price) * prom_discount
            models.CurrentPrice.objects.create(
                product_id=book_id[0],
                ori_price=ori_price,
                daily_price=daily_price,
                cut_price=cut_price,
                plus_price=plus_price,
                final_price=final_price,
                prom=prom_memo,
                created_time=datetime.datetime.now(),
                detail_id=book_id[0],
                final_discount=final_price / ori_price,
                link='https://item.jd.com/{}.html'.format(book_id[0])
            )

    def update(self):
        conn = pymysql.connect(
            host="localhost",
            port=3306,
            database="tsg123",
            user="root",
            password="123456",
            charset="utf8"
        )
        cursor = conn.cursor()
        sql = 'update books_currentprice cur join books_preprice pre on cur.product_id=pre.product_id set cur.pre_price=cur.final_price-pre.final_price'
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        sql2 = 'update books_currentprice cur join (select product_id, min(final_price) final_price from books_historyprice group by product_id) his on cur.product_id=his.product_id set cur.bot_price=cur.final_price-his.final_price'
        cursor = conn.cursor()
        cursor.execute(sql2)
        conn.commit()
        cursor.close()
        conn.close()
