import os
import datetime
import pymysql
from decimal import Decimal


if __name__ == "__main__":
    # 加载Django项目的配置信息
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tsg123.settings")
    # 导入Django,并启动Django项目
    import django
    django.setup()

    from books import models

    # 数据初始化导入

    # # 会员表：member memberstate
    # with open("D:/123/import_data/member.txt", encoding='GB2312') as f:
    #     for line in f:
    #         print(line)
    #         phone, member_id, created_time, type_id, begin_date, end_date, deposit,\
    #             parent, age_of_girl, age_of_boy, name, referer, state = line.strip().split("\t")
    #         models.Member.objects.create(
    #             id=int(member_id),
    #             phone=phone.strip(),
    #             created_time=datetime.datetime.strptime(created_time, "%Y/%m/%d %H:%M:%S")
    #         )
    #         models.MemberState.objects.create(
    #             id=member_id,
    #             begin_date=datetime.datetime.strptime(begin_date, '%Y/%m/%d').date(),
    #             end_date=datetime.datetime.strptime(end_date, '%Y/%m/%d').date(),
    #             deposit=deposit,
    #             name=name,
    #             parent=parent,
    #             age_of_boy=age_of_boy,
    #             age_of_girl=age_of_girl,
    #             referer=referer if referer else 1000,
    #             state=state,
    #             member_id=member_id,
    #             type_id=type_id
    #         )

    # # 童书表：book, stock   夏丏尊
    # with open("D:/123/import_data/book.txt", encoding='GB2312') as f:
    #     for line in f:
    #         isbn, name, sets, age_group, publisher, parent_cate, sub_cate, book_size,\
    #             language, ori_price, discount, sell_price, plus_price, \
    #             placed_on, placed, stocked_on, is_package = line.strip().split("\t")
    #         models.Book.objects.create(
    #             ISBN=isbn.strip(),
    #             name=name,
    #             sets = sets,
    #             age_group=age_group,
    #             publisher=publisher,
    #             language=language,
    #             ori_price=ori_price,
    #             discount=discount,
    #             plus_price=plus_price,
    #             sell_price=sell_price,
    #             is_package=is_package
    #
    #         )
    #         models.Stock.objects.create(
    #             ISBN=isbn.strip(),
    #             total=0,
    #             placed=placed,
    #             placed_on=placed_on,
    #             stocked=0,
    #             stocked_on=stocked_on,
    #             book_id=isbn.strip(),
    #             book_size=book_size,
    #             parent_cate=parent_cate,
    #             sub_cate=sub_cate
    #         )

    # # 进书批次表：purchasebatch
    # with open("D:/123/import_data/batch.txt", encoding='GB2312') as f:
    #     for line in f:
    #         # batch_id, order_id, channel, total_price_sale, prom_price, coupon_price, total_price_paid, discount, created_time
    #         fields = line.strip().split("\t")
    #         order_id = fields[1].strip()
    #         total_price_sale = Decimal(fields[3])
    #         prom_price = Decimal(fields[4])
    #         coupon_price = Decimal(fields[5])
    #         total_price_paid = total_price_sale - prom_price - coupon_price
    #         discount = (total_price_paid / total_price_sale).quantize(Decimal("0.0000"))
    #         created_time = datetime.datetime.strptime(fields[8], "%Y/%m/%d %H:%M:%S")
    #
    #         models.PurchaseBatch.objects.create(
    #             id=fields[0],
    #             order_id=order_id,
    #             channel=fields[2],
    #             total_price_sale=total_price_sale,
    #             prom_price=prom_price,
    #             coupon_price=coupon_price,
    #             total_price_paid=total_price_paid,
    #             discount=discount,
    #             created_time=created_time
    #         )

    # # 进书明细表：purchasedetail
    #     # with open("D:/123/import_data/detail.txt", encoding='GB2312') as f:
    #     #     for line in f:
    #     #         # id, isbn, package_id, price_sale, price_paid, created_time, batch_id, is_back, quantity
    #     #         fields = line.strip().split("\t")
    #     #         isbn = fields[1].strip()
    #     #         package_id = fields[2].strip()
    #     #         price_sale = Decimal(fields[3])
    #     #         price_paid = Decimal(fields[4])
    #     #         created_time = datetime.datetime.strptime(fields[5], "%Y/%m/%d %H:%M:%S")
    #     #
    #     #         models.PurchaseDetail.objects.create(
    #     #             id=fields[0],
    #     #             ISBN=isbn,
    #     #             package_id=package_id,
    #     #             price_sale=price_sale,
    #     #             price_paid=price_paid,
    #     #             quantity=fields[8],  # 只做标记用，不用于计算
    #     #             is_sold=0,
    #     #             is_back = fields[7],
    #     #             batch_id=fields[6],
    #     #             book_id=isbn,
    #     #             created_time=created_time
    #     #         )

    # 借阅记录表：borrowrecord
    with open("D:/123/import_data/borrow.txt", encoding='GB2312') as f:
        for line in f:
            # id, member_id, isbn, created_time, return_time, damaged, update_time
            fields = line.strip().split("\t")
            isbn = fields[2].strip()
            created_time = datetime.datetime.strptime(fields[3], "%Y/%m/%d %H:%M:%S") if fields[3] else None
            return_time = datetime.datetime.strptime(fields[4], "%Y/%m/%d %H:%M:%S") if fields[4] else None
            update_time = datetime.datetime.strptime(fields[6], "%Y/%m/%d %H:%M:%S") if fields[6] else None

            models.BorrowRecord.objects.create(
                id=fields[0],
                created_time=created_time,
                return_time=return_time,
                damaged=fields[5],
                book_id=isbn,
                member_id=fields[1],
                update_time=update_time
            )