import os
import datetime
import pymysql
import decimal

# t = datetime.date(year=2020, month=12, day=9)-datetime.datetime.now().date()
# print(t.days)

# d = round(decimal.Decimal("0.88")*decimal.Decimal("0.88"), 2)
# print(d, type(d))

# d = round(2.156, 2)
# d = decimal.Decimal("2.156").quantize(decimal.Decimal("0.00"))
# print(d, type(d))


# if __name__ == "__main__":
#     # 加载Django项目的配置信息
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tsg123.settings")
#     # 导入Django,并启动Django项目
#     import django
#     django.setup()
#
#     from books import models
#
#     pack_map = models.PackageMap.objects.filter(package_id="123").values_list("book_id")
#     print(pack_map)
#     # isbn_list = [isbn[0] for isbn in pack_map]
#     isbn_list=[]
#     for isbn in pack_map:
#         isbn_list.append(isbn[0])
#
#     print(isbn_list)
#     print("isbns:",",".join(isbn_list))


    # ret = models.MemberState.objects.get(id=1000)
    # ret = ret.end_date-ret.begin_date
    # print(ret.days)


    # obj = models.PrePrice.objects.all().values("created_time")[0]
    # print(obj, type(obj))
    #
    # cur_time = models.CurrentPrice.objects.values("created_time").all()[0]["created_time"]
    # now  = datetime.datetime.now()
    #
    # print(cur_time, now)
    # print((now - cur_time).seconds//3600)
    #
    # print(cur_time.date())


    # # 数据初始化导入
    # models.HistoryPrice.objects.all().delete()
    # models.PrePrice.objects.all().delete()
    # models.CurrentPrice.objects.all().delete()
    # models.ListenList.objects.all().delete()
    #
    # with open("D:/123/listenlist.txt", encoding='GB2312') as f:
    #     for line in f:
    #         product_id, name, created_date = line.strip().split("\t")
    #         models.ListenList.objects.create(product_id=product_id, name=name, created_date=created_date)
    #
    # with open("D:/123/historyprice.csv", encoding='GB2312') as f:
    #     for line in f:
    #         filed = line.strip().split(",")
    #         models.HistoryPrice.objects.create(
    #             product_id=filed[0],
    #             ori_price=filed[1],
    #             daily_price=filed[2],
    #             cut_price=filed[3],
    #             plus_price=filed[4],
    #             final_price=filed[5],
    #             prom=filed[6],
    #             created_time=datetime.datetime.strptime(filed[7], '%Y/%m/%d %H:%M'),
    #             detail_id=filed[0]
    #         )
    #
    # with open("D:/123/preprice.csv", encoding='GB2312') as f:
    #     for line in f:
    #         filed = line.strip().split(",")
    #         models.PrePrice.objects.create(
    #             product_id=filed[0],
    #             ori_price=filed[1],
    #             daily_price=filed[2],
    #             cut_price=filed[3],
    #             plus_price=filed[4],
    #             final_price=filed[5],
    #             prom=filed[6],
    #             created_time=datetime.datetime.strptime(filed[7], '%Y/%m/%d %H:%M'),
    #             detail_id=filed[0]
    #         )
    #
    # with open("D:/123/currentprice.csv", encoding='GB2312') as f:
    #     for line in f:
    #         filed = line.strip().split(",")
    #         models.CurrentPrice.objects.create(
    #             product_id=filed[0],
    #             ori_price=filed[1],
    #             daily_price=filed[2],
    #             cut_price=filed[3],
    #             plus_price=filed[4],
    #             final_price=filed[5],
    #             prom=filed[6],
    #             created_time=datetime.datetime.strptime(filed[7], '%Y/%m/%d %H:%M'),
    #             detail_id=filed[0],
    #             final_discount=float(filed[5]) / float(filed[1]),
    #             link='https://item.jd.com/{}.html'.format(filed[0])
    #         )




# with open("D:/123/currentprice.csv", encoding='GB2312') as f:
#     temp = 0
#     for line in f:
#         filed = line.strip().split(",")
#         # print(filed)
#         # dt = datetime.datetime.strptime(filed[7], '%Y/%m/%d %H:%M')
#         dt = datetime.datetime.strptime("2020-8-3", "%Y-%m-%d")
#         print(dt, type(dt))
#         temp += 1
#         if temp > 10:
#             break

# # 手动更新比上次，比最低
# conn = pymysql.connect(
#     host="localhost",
#     port=3306,
#     database="tsg123",
#     user="root",
#     password="123456",
#     charset="utf8"
# )
# cursor = conn.cursor()
# sql = 'update books_currentprice cur join books_preprice pre on cur.product_id=pre.product_id set cur.pre_price=cur.final_price-pre.final_price'
# cursor.execute(sql)
# conn.commit()
# cursor.close()
# sql2 = 'update books_currentprice cur join (select product_id, min(final_price) final_price from books_historyprice group by product_id) his on cur.product_id=his.product_id set cur.bot_price=cur.final_price-his.final_price'
# cursor = conn.cursor()
# cursor.execute(sql2)
# conn.commit()
# cursor.close()
# conn.close()


# SQL
# alter table books_memberlog auto_increment=158;

# delete from books_currentprice;
# insert into books_currentprice(
#     select id,
#            product_id,
#            ori_price,
#            daily_price,
#            cut_price,
#            plus_price,
#            final_price,
#            prom,
#            created_time,
#            0.00 as pre_price,
#            0.00 as bot_price,
#            detail_id,
#            0.01 as final_discount,
#            "1"  as link
#     from books_preprice
# );

# delete from books_preprice;
# insert into books_preprice(
#     select id,
#            product_id,
#            ori_price,
#            daily_price,
#            cut_price,
#            plus_price,
#            final_price,
#            prom,
#            created_time,
#            detail_id
#     from books_historyprice
#     where created_time > "2020-08-25"
# );

# delete from books_historyprice where created_time > "2020-08-25";


# try:
#     a=1/0
#     print(1)
# except Exception as e:
#     print(e)
