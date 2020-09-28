import datetime
import json
from decimal import Decimal

from django.shortcuts import render, redirect, HttpResponse
from django.db.models import F, Q, Count, Max, Min, Sum
from books import models
from utils.mypage import Page
from utils.listen import Listen

# Create your views here.


# 首页
def home(request):
    return render(request, "home.html")


# 会员管理
def member_list(request):
    """会员列表"""
    obj_all = models.MemberState.objects.all()

    # 每次请求时更新state
    for obj in obj_all:
        state_old = obj.state
        state_new = obj.state_set()
        if state_old == state_new:
            break
        else:
            obj.save()

    # 搜索列表
    keyword = request.GET.get("keyword")
    path = request.path_info
    if keyword and keyword.strip():
        if keyword[0:4].isdigit():
            obj_all = models.MemberState.objects.filter(member__phone__contains=keyword.strip())

    # 分页处理
    total_count = obj_all.count()
    page_num = request.GET.get("page")
    page_obj = Page(path, page_num, total_count, request.GET, per_page=10, page_max=11)
    obj_show = obj_all[page_obj.start:page_obj.end]
    page_html = page_obj.page_html()

    return render(request, "member_list.html", {"member_list": obj_show, "page_html": page_html})


def member_edit(request):
    """编辑会员"""
    if request.method == "POST":
        # 获取referer页面URL，以便编辑完成后返回
        ref = request.GET.get("ref")

        # 获取编辑后的字段内容
        edit_id = request.POST.get("id")
        phone = request.POST.get("phone")
        end_date = datetime.datetime.strptime(request.POST.get("enddate"), "%Y-%m-%d").date()
        deposit = int(request.POST.get("deposit"))
        parent = request.POST.get("parent")
        name = request.POST.get("name")
        age_of_girl = request.POST.get("girl")
        age_of_boy = request.POST.get("boy")
        memo = request.POST.get("memo")

        edit_obj = models.MemberState.objects.get(id=edit_id)
        # 修改手机号码
        if edit_obj.member.phone != phone:
            member_obj = models.Member.objects.get(id=edit_id)
            member_obj.phone = phone
            member_obj.save()
            models.MemberLog.objects.create(
                type="更换手机",
                member_id=edit_id,
                phone=phone
            )
        if edit_obj.end_date < end_date:
            models.MemberLog.objects.create(
                type="赠送会员",
                member_id=edit_id,
                begin_date=edit_obj.end_date,
                end_date=end_date
            )
        if edit_obj.deposit != deposit:
            models.MemberLog.objects.create(
                type="交付押金",
                deposit=deposit,
                income=deposit-edit_obj.deposit,
                member_id=edit_id
            )
        # 修改其他字段
        edit_obj.end_date = end_date
        edit_obj.deposit = deposit
        edit_obj.parent = parent
        edit_obj.name = name
        edit_obj.age_of_girl = age_of_girl
        edit_obj.age_of_boy = age_of_boy
        edit_obj.memo = memo
        # 将修改提交到数据库
        edit_obj.save()
        return redirect(ref)
    edit_id = request.GET.get("id")
    if edit_id:
        edit_obj = models.MemberState.objects.get(id=edit_id)
        type_list = models.MemberType.objects.all()
        return render(request, "member_edit.html", {"member_obj": edit_obj})
    else:
        return HttpResponse("要编辑的数据不存在")


def member_renew(request):
    """续费会员"""
    if request.method == "POST":
        ref = request.GET.get("ref")

        edit_id = request.POST.get("id")
        type_id = request.POST.get("typeid")
        price = request.POST.get("price")
        begin_date = datetime.datetime.strptime(request.POST.get("begindate"), "%Y-%m-%d").date()
        give_days = request.POST.get("give")
        memo = request.POST.get("memo")

        type_obj = models.MemberType.objects.get(id=type_id)
        add_days = type_obj.days + int(give_days)
        end_date = begin_date + datetime.timedelta(days=add_days)

        edit_obj = models.MemberState.objects.get(id=edit_id)
        edit_obj.type_id = type_id
        edit_obj.begin_date = begin_date
        edit_obj.end_date = end_date
        edit_obj.memo = memo
        # 将修改提交到数据库
        edit_obj.save()
        models.MemberLog.objects.create(
            type="续费会员",
            begin_date=begin_date,
            end_date=end_date,
            cart_id=type_id,
            income=price.strip(),
            member_id=edit_id
        )
        return redirect(ref)
    edit_id = request.GET.get("id")
    if edit_id:
        edit_obj = models.MemberState.objects.get(id=edit_id)
        type_list = models.MemberType.objects.all()
        return render(request, "member_renew.html", {"member_obj": edit_obj, "type_list": type_list})
    else:
        return HttpResponse("要编辑的数据不存在")


def member_add(request):
    """添加会员"""
    if request.method == "POST":
        phone = request.POST.get("phone")
        type_id = request.POST.get("typeid")
        price = request.POST.get("price")
        give_days = request.POST.get("give")
        deposit = request.POST.get("deposit")
        memo = request.POST.get("memo")
        referer = request.POST.get("referer")

        type_obj = models.MemberType.objects.get(id=type_id)
        add_days = type_obj.days + int(give_days)
        begin_date = datetime.datetime.now().date()
        end_date = begin_date + datetime.timedelta(days=add_days)

        member_obj = models.Member.objects.create(phone=phone)
        models.MemberState.objects.create(
            id=member_obj.id,
            begin_date=begin_date,
            end_date=end_date,
            deposit=deposit,
            memo=memo,
            referer=referer,
            state=add_days,
            member=member_obj,
            type=type_obj
        )
        models.MemberLog.objects.create(
            type="新增会员",
            phone=phone,
            begin_date=begin_date,
            end_date=end_date,
            cart_id=type_id,
            income=price.strip(),
            member_id=member_obj.id
        )
        if int(deposit)>0:
            models.MemberLog.objects.create(
                type="交付押金",
                deposit=deposit,
                income=deposit.strip(),
                member_id=member_obj.id
            )
        return redirect("/member_list/")
    type_list = models.MemberType.objects.all()
    return render(request, "member_add.html", {"type_list": type_list})


# 童书管理
def book_list(request):
    keyword = request.GET.get("keyword")
    path = request.path_info
    """童书列表"""
    if keyword:
        obj_all = models.Book.objects.filter(name__contains=keyword)
    else:
        obj_all = models.Book.objects.order_by("created_time").reverse()

    # 计算售价和会员价
    # for obj in obj_all:
    #     obj.cal_price()
    #     obj.save()

    # 分页处理
    total_count = obj_all.count()
    page_num = request.GET.get("page")
    page_obj = Page(path, page_num, total_count, request.GET, per_page=10, page_max=11)
    obj_show = obj_all[page_obj.start:page_obj.end]
    page_html = page_obj.page_html()

    return render(request, "book_list.html", {"book_list": obj_show, "page_html": page_html})


def book_add(request):
    """新增童书"""
    lang_list = ["注音版", "文字版", "双语版", "英文版", "无字版", "其他"]
    age_list = ["0-3岁", "3-6岁", "7-10岁", "11-14岁", "15-18岁", "其他"]
    package_id = request.GET.get("package_id")

    if request.method == "POST":
        isbn = request.POST.get("ISBN")
        name = request.POST.get("name")
        is_package = request.POST.get("isPackage")
        sets = request.POST.get("sets")
        age_group = request.POST.get("ageGroup")
        publisher = request.POST.get("publisher")
        language = request.POST.get("Lang")
        ori_price = request.POST.get("oriPrice")
        discount = request.POST.get("discount")

        # 添加到book表
        new_book = models.Book.objects.create(
            ISBN=isbn,
            name=name,
            is_package=is_package,
            sets=sets,
            age_group=age_group,
            publisher=publisher,
            language=language,
            ori_price=Decimal(ori_price),
            discount=Decimal(discount),
        )
        new_book.cal_price()
        new_book.save()

        # 添加到stock表
        new_stock = models.Stock.objects.create(
            ISBN=isbn,
            book_id=isbn
        )
        return redirect("/book_list/")
    pack_obj = models.Book.objects.get(ISBN=package_id) if package_id else None
    avg_price = (pack_obj.ori_price / pack_obj.sets).quantize(Decimal("0.00")) if package_id else ""
    return render(request, "book_add.html", {"pack_obj": pack_obj, "avg_price": avg_price, "lang_list": lang_list, "age_list": age_list})


# 库存管理
def stock_list(request):
    keyword = request.GET.get("keyword")
    path = request.path_info
    """库存列表"""
    if keyword and keyword.strip():
        if keyword[0:5].isdigit():
            obj_all = models.Stock.objects.filter(ISBN=keyword.strip())
        else:
            obj_all = models.Stock.objects.filter(book__name__contains=keyword.strip())
    else:
        obj_all = models.Stock.objects.order_by("created_time").reverse()

    # 分页处理
    total_count = obj_all.count()
    page_num = request.GET.get("page")
    page_obj = Page(path, page_num, total_count, request.GET, per_page=10, page_max=11)
    obj_show = obj_all[page_obj.start:page_obj.end]
    page_html = page_obj.page_html()
    return render(request, "stock_list.html", {"stock_list": obj_show, "page_html": page_html})


def stock_edit(request):
    """编辑库存信息"""
    if request.method == "POST":
        isbn = request.POST.get("ISBN")
        parent_cate = request.POST.get("parentCate")
        sub_cate = request.POST.get("subCate")
        book_size = request.POST.get("bookSize")
        placed_on = request.POST.get("placedOn")
        placed = int(request.POST.get("placed"))
        stocked_on = request.POST.get("stockedOn")

        edit_obj = models.Stock.objects.get(ISBN=isbn)
        edit_obj.parent_cate = parent_cate
        edit_obj.sub_cate = sub_cate
        edit_obj.book_size = book_size
        edit_obj.placed_on = placed_on
        edit_obj.placed = placed
        edit_obj.stocked_on = stocked_on
        edit_obj.stocked = edit_obj.total - placed
        edit_obj.save()

        referer = request.GET.get("referer")
        print(referer)
        return redirect(referer)
    edit_id = request.GET.get("id")
    edit_obj = models.Stock.objects.get(ISBN=edit_id)
    return render(request, "stock_edit.html", {"edit_obj": edit_obj})


def stock_update(request):
    stock_objs = models.Stock.objects.all()
    for stock in stock_objs:
        total = models.PurchaseDetail.objects.filter(is_sold=0, is_back=0, ISBN=stock.ISBN).aggregate(
            count=Count("id")
        )["count"]
        stock.total = total if total else 0
        stock.stocked = total - stock.placed
        stock.save()
    return redirect("/stock_list/")


# 采购管理
def purchase_batch(request):
    """采购批次列表"""
    obj_all = models.PurchaseBatch.objects.all().order_by("created_time").reverse()
    total_count = obj_all.count()

    page_num = request.GET.get("page")
    page_obj = Page("/purchase_batch/", page_num, total_count, per_page=10, page_max=11)

    obj_show = obj_all[page_obj.start:page_obj.end]
    page_html = page_obj.page_html()
    return render(request, "purchase_batch.html", {"batch_list": obj_show, "page_html": page_html})


def purchase_add(request):
    """新增（合并）进书批次订单"""
    # 从url获取batch_id,用于判断新增还是合并
    batch_id = request.GET.get("batch_id")

    if request.method == "POST":
        order_id = request.POST.get("orderId")
        channel = request.POST.get("channel")
        total_price_sale = Decimal(request.POST.get("salePrice"))
        prom_price = Decimal(request.POST.get("promPrice"))
        coupon_price = Decimal(request.POST.get("couponPrice"))
        total_price_paid = total_price_sale - prom_price - coupon_price
        discount = (total_price_paid / total_price_sale).quantize(Decimal("0.0000"))
        if batch_id:
            # 合并
            batch_obj = models.PurchaseBatch.objects.get(id=batch_id)
            batch_obj.total_price_sale += total_price_sale
            batch_obj.prom_price += prom_price
            batch_obj.coupon_price += coupon_price
            batch_obj.total_price_paid += total_price_paid
            batch_obj.discount = (batch_obj.total_price_paid / batch_obj.total_price_sale).quantize(Decimal("0.0000"))
            batch_obj.save()
        else:
            # 新增
            models.PurchaseBatch.objects.create(
                order_id=order_id,
                channel=channel,
                total_price_sale=total_price_sale,
                prom_price=prom_price,
                coupon_price=coupon_price,
                total_price_paid=total_price_paid,
                discount=discount
            )

        return redirect("/purchase_batch/")

    batch_obj = models.PurchaseBatch.objects.get(id=batch_id) if batch_id else None
    return render(request, "purchase_add.html", {"batch_obj": batch_obj})


def purchase_detail(request):
    batch_id = request.GET.get("batch_id")
    batch_obj = models.PurchaseBatch.objects.get(id=batch_id)
    obj_all = models.PurchaseDetail.objects.filter(batch_id=batch_id).values(
        "ISBN", "batch_id", "book__name", "book__is_package", "package_id", "price_sale", "price_paid", "is_sold", "memo"
    ).annotate(
        quantity=Count("batch_id"), created_time=Min("created_time"), id=Min("id")
    ).order_by("created_time").reverse()
    total_count = obj_all.count()

    page_num = request.GET.get("page")
    page_obj = Page("/purchase_detail/", page_num, total_count, request.GET, per_page=10, page_max=11)

    obj_show = obj_all[page_obj.start:page_obj.end]
    page_html = page_obj.page_html()

    return render(request, "purchase_detail.html", {"purchase_list": obj_show, "batch_obj": batch_obj, "page_html": page_html})


def purchase_add2(request):
    # 对套装录入单本时，url附带package_id
    package_id = request.GET.get("package_id", "0")
    batch_id = request.GET.get("batch_id")

    if request.method == "POST":
        # 录入单本时，url附带batch_id
        batch_obj = models.PurchaseBatch.objects.get(id=batch_id)
        # 录入套装时，url附带is_package=1
        is_package = request.GET.get("is_package", 0)

        # isbn支持多项输入，以逗号分割
        isbn_list = request.POST.get("ISBN").split(",")
        # 录入包的单本时，取包的ISBN，否则取0
        package_id = package_id if package_id else 0
        price_sale = request.POST.get("salePrice")
        quantity = int(request.POST.get("quantity"))
        memo = request.POST.get("memo")

        for isbn in isbn_list:
            # isbn多余1个时，循环添加
            if isbn:
                stock_obj = models.Stock.objects.get(ISBN=isbn)
                for i in range(quantity):
                    # 数量大于1时，循环重复添加
                    new_obj = models.PurchaseDetail.objects.create(
                        ISBN=isbn,
                        package_id=package_id,
                        price_sale=Decimal(price_sale),
                        price_paid=Decimal("0.00"),
                        quantity=quantity,  # 只做标记用，不用于计算
                        is_sold=0,
                        batch_id=batch_id,
                        book_id=isbn,
                    )
                    # 计算实付单价
                    new_obj.price_paid = (new_obj.price_sale*new_obj.batch.discount).quantize(Decimal("0.00"))
                    new_obj.save()
                    # 计算该批次录入进度
                    if is_package == 0:
                        batch_obj.progress += new_obj.price_sale
                        batch_obj.save()
                    # 库存总量+1
                    stock_obj.total += 1
                    stock_obj.stocked += 1
                    stock_obj.save()
                if package_id != "0":
                    try:
                        models.PackageMap.objects.create(package_id=package_id, book_id=isbn)
                    except Exception:
                        pass
            else:
                break
        return redirect("/purchase_detail/?batch_id=%s" % batch_id)
    avg_price = 0
    quantity = 1
    isbns = ""
    if package_id != "0":
        # 录入包的单本时，单价和数量默认填充
        pack_obj = models.PurchaseDetail.objects.filter(ISBN=package_id, batch_id=batch_id, book__is_package=1)[0]
        avg_price = (pack_obj.price_sale / pack_obj.book.sets).quantize(Decimal("0.00"))
        quantity = pack_obj.quantity
        # 录入过包数据的，自动填充包含的书籍isbn
        pack_map = models.PackageMap.objects.values_list("book_id").filter(package_id=package_id)
        isbn_list = [isbn[0] for isbn in pack_map]
        isbns = ",".join(isbn_list)
    return render(request, "purchase_add2.html", {"avg_price": avg_price, "quantity": quantity, "isbns": isbns})


def purchase_update(request):
    batch_list = models.PurchaseBatch.objects.all()
    for batch in batch_list:
        progress = batch.purchasedetail_set.filter(book__is_package=0).aggregate(
            progress=Sum("price_sale")
        )["progress"]
        print(progress)
        batch.progress = progress if progress else 0
        batch.save()
    return redirect("/purchase_batch/")


# 借阅管理
def borrow_record(request):
    """借阅记录"""
    # 获取全部待还的书籍 和 最近归还的书籍，按更新时间倒序
    yesterday = datetime.datetime.now() - datetime.timedelta(hours=6)
    obj_all = models.BorrowRecord.objects.filter(
        Q(return_time__isnull=True) | Q(return_time__gt=yesterday)
    ).order_by("update_time").reverse()

    # 处理还书请求，筛选对应书籍的待还借阅记录并返回，以完成还书操作
    if request.method == "POST":
        bid_list = []
        for i in range(1, 6):
            book_id = request.POST.get("ISBN%s" % i)
            if book_id:
                bid_list.append(book_id)
            else:
                break
        obj_all = models.BorrowRecord.objects.filter(book_id__in=bid_list, return_time__isnull=True).order_by("created_time").reverse()

    # 分页处理
    total_count = obj_all.count()
    page_num = request.GET.get("page")
    page_obj = Page("/borrow_record/", page_num, total_count, request.GET, per_page=10, page_max=11)
    obj_show = obj_all[page_obj.start:page_obj.end]
    page_html = page_obj.page_html()

    return render(request, "borrow_record.html", {"record_list": obj_show, "page_html": page_html})


def borrow_ret(request):
    """还书操作"""
    # 获取归还图书对应的借阅记录，添加还书时间和备注
    now = datetime.datetime.now()
    ret_id = request.POST.get("id")
    memo = request.POST.get("memo").strip()
    record_obj = models.BorrowRecord.objects.get(id=ret_id)
    record_obj.return_time = datetime.datetime.now()
    record_obj.memo = record_obj.memo+" "+memo if record_obj.memo else memo
    record_obj.save()

    # 返回相应数据给ajax；完成页面的局部刷新
    ret = {"now": now.strftime("%Y-%m-%d %H:%M:%S"), "memo": record_obj.memo}
    ret_str = json.dumps(ret)
    return HttpResponse(ret_str)


def borrow_bor(request):
    """借书操作"""
    member_id = request.POST.get("memberid")
    for i in range(1, 6):
        book_id = request.POST.get("ISBN%s" % i)
        if book_id:
            models.BorrowRecord.objects.create(member_id=member_id, book_id=book_id)
        else:
            break
    return redirect("/borrow_record/")


def borrow_edit_memo(request):
    """编辑借还书备注"""
    record_id = request.POST.get("recordId")
    memo = request.POST.get("memo")
    edit_obj = models.BorrowRecord.objects.get(id=record_id)
    edit_obj.memo = memo
    edit_obj.save()
    # 返回相应数据给ajax；完成页面的局部刷新
    return HttpResponse(memo)


def cart_list(request):
    """扫码录入isbn,自动添加对应书籍到cart表"""
    today = datetime.datetime.now().date()
    if request.method == "POST":
        isbn = request.POST.get("isbn")
        member_id = request.POST.get("member_id")
        member_id = int(member_id) if member_id else 1
        new_obj = models.Cart.objects.create(book_id=isbn, member_id=member_id)
        is_active = 1 if new_obj.member.end_date > today else 0
        trele = """<tr>
            <td style="display: none">{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>
                <button class="del_sel">删除</button>
            </td>
        </tr>""".format(
            new_obj.id, new_obj.book_id, new_obj.book.name, new_obj.book.sets,
            new_obj.book.ori_price, new_obj.book.sell_price, new_obj.book.plus_price,
            new_obj.member_id, new_obj.book.stock.total
        )
        if member_id >= 1000:
            cart_objs = models.Cart.objects.all()
            for cart in cart_objs:
                cart.member_id = member_id
                cart.save()
        summary = models.Cart.objects.values("member_id").annotate(
            ori_price=Sum("book__ori_price"),
            sell_price = Sum("book__sell_price"),
            plus_price = Sum("book__plus_price"),
        )[0]
        need_paid = str(summary["plus_price"]) if is_active == 1 else str(summary["sell_price"])
        price = {"ori_price": str(summary["ori_price"]), "sell_price": str(summary["sell_price"]), "plus_price": str(summary["plus_price"]), "need_paid": need_paid}
        data = {"trele": trele, "price": price}
        data_str = json.dumps(data)
        return HttpResponse(data_str)

    obj_list = models.Cart.objects.all()
    if len(obj_list):
        first_obj = obj_list.first()
        is_active = 1 if first_obj.member.end_date > today else 0
        summary = models.Cart.objects.values("member_id").annotate(
            ori_price=Sum("book__ori_price"),
            sell_price=Sum("book__sell_price"),
            plus_price=Sum("book__plus_price"),
        )[0]
        summary["need_paid"] = summary["plus_price"] if is_active == 1 else summary["sell_price"]
    else:
        summary = {"ori_price": "0.00", "sell_price": "0.00", "plus_price": "0.00", "need_paid": "0.00"}
    return render(request, "cart_list.html", {"book_list": obj_list, "summary": summary})


def cart_del(request):
    """删除cart数据"""
    del_id = request.POST.get("del_id")
    price = {"ori_price": "0.00", "sell_price": "0.00", "plus_price": "0.00", "need_paid": "0.00"}
    if del_id == "0":
        # 清空购物车
        models.Cart.objects.all().delete()
        trele = """<tr id="none">
            <td colspan="9" class="text-center">暂时没有数据</td>
        </tr>"""
    else:
        # 删除对应行记录
        models.Cart.objects.get(id=del_id).delete()
        if models.Cart.objects.exists():
            trele = ""
            summary = models.Cart.objects.values("member_id").annotate(
                ori_price=Sum("book__ori_price"),
                sell_price=Sum("book__sell_price"),
                plus_price=Sum("book__plus_price"),
            )[0]
            need_paid = str(summary["plus_price"]) if summary["member_id"] >= 1000 else str(summary["sell_price"])
            price = {"ori_price": str(summary["ori_price"]), "sell_price": str(summary["sell_price"]),
                     "plus_price": str(summary["plus_price"]), "need_paid": need_paid}
        else:
            # 如果购物车为空，返回提示行
            trele = """<tr id="none">
                <td colspan="9" class="text-center">暂时没有数据</td>
            </tr>"""
    data = {"trele": trele, "price": price}
    data_str = json.dumps(data)
    return HttpResponse(data_str)


def cart_submit(request):
    """提交订单"""
    today = datetime.datetime.now().date()
    need_paid = request.POST.get("needPaid")
    actually_paid = request.POST.get("actuallyPaid")
    ratio = Decimal(actually_paid) / Decimal(need_paid)
    cart_objs = models.Cart.objects.all()
    is_active = 1 if cart_objs.first().member.end_date > today else 0
    # 获取当前最大的订单id
    order_id = models.Order.objects.aggregate(order_id=Max("order_id"))["order_id"]
    order_id = (order_id+1) if order_id else 1
    # 循环将cart表数据放入order表
    for cart in cart_objs:
        # 获取当前书籍对应的最早一条进书记录
        purchase_id = models.PurchaseDetail.objects.filter(ISBN=cart.book_id, is_sold=0).aggregate(purchase_id=Min("id"))["purchase_id"]
        print(purchase_id)
        purchase_obj = models.PurchaseDetail.objects.get(id=purchase_id)
        # 添加到订单
        models.Order.objects.create(
            order_id=order_id,
            actually_paid=((cart.book.plus_price if is_active == 1 else cart.book.sell_price) * ratio).quantize(Decimal("0.00")),
            purchase_id=purchase_id,
            member_id=cart.member_id
        )
        # 对应的进书记录，出售状态设置is_sold=1
        purchase_obj.is_sold = 1
        purchase_obj.save()
        if cart.book.is_package == 1:
            pack_map = models.PackageMap.objects.values_list("book_id").filter(package_id=cart.book_id)
            for isbn in pack_map:
                purchase_id = models.PurchaseDetail.objects.filter(ISBN=isbn[0], is_sold=0).aggregate(purchase_id=Min("id"))["purchase_id"]
                purchase_obj = models.PurchaseDetail.objects.get(id=purchase_id)
                # 添加到订单
                models.Order.objects.create(
                    order_id=order_id,
                    actually_paid=((purchase_obj.book.plus_price if is_active == 1 else purchase_obj.book.sell_price) * ratio).quantize(Decimal("0.00")),
                    purchase_id=purchase_id,
                    member_id=cart.member_id
                )
                # 对应的进书记录，出售状态设置is_sold=1
                purchase_obj.is_sold = 1
                purchase_obj.save()
        # 修改库存信息

    cart_objs.delete()
    order_objs = models.Order.objects.filter(order_id=order_id, purchase__book__is_package=0)
    member_obj = order_objs[0].member
    return render(request, "print_ticket.html", {"order_objs": order_objs, "member_obj": member_obj,
                                                 "need_paid":need_paid, "actually_paid": actually_paid,
                                                 "is_active":is_active})


def order_list(request):
    obj_all = models.Order.objects.all().order_by("id").reverse()
    # 分页处理
    total_count = obj_all.count()
    page_num = request.GET.get("page")
    page_obj = Page("/order_list/", page_num, total_count, request.GET, per_page=10, page_max=11)
    obj_show = obj_all[page_obj.start:page_obj.end]
    page_html = page_obj.page_html()

    return render(request, "order_list.html", {"order_list": obj_show, "page_html": page_html})


# 监听管理
def listen_list(request):
    """价格比对列表"""
    # sign标记是否允许更新：如果上次更新时间在12个小时之前，则允许更新sign=1
    now = datetime.datetime.now()
    if models.CurrentPrice.objects.exists():
        cur_time = models.CurrentPrice.objects.values("created_time").all()[0]["created_time"]
    else:
        cur_time = now

    sign = 0 if cur_time.date() == now.date() and (now - cur_time).seconds / 3600 < 12 else 1

    obj_all = models.CurrentPrice.objects.order_by("final_discount")     # 不能对decimal字段过滤？

    # 分页处理
    total_count = obj_all.count()
    page_num = request.GET.get("page")
    page_obj = Page("/listen_list/", page_num, total_count, request.GET, per_page=10, page_max=11)
    obj_show = obj_all[page_obj.start:page_obj.end]
    page_html = page_obj.page_html()

    return render(request, "listen_list.html", {"listen_list": obj_show, "page_html": page_html, "sign": sign})


def listen_update(request):
    # 下载最新价格数据
    rerun = request.GET.get("rerun")
    listen = Listen()
    try:
        if rerun:
            # 接续下载价格数据
            listen.download(excepts=True)
        else:
            # 准备current、pre、history表
            listen.prepare()
            # 下载最新价格数据
            listen.download()
        # 更新对比价格
        listen.update()
    except Exception as e:
        return HttpResponse(str(e))
    return redirect("/listen_list/")


def listen_add(request):
    """添加书目到监听列表"""
    msg = ""
    error_msg = '<p class="text-danger text-center">ID和名称不能为空</p>'
    success_msg = '<p class="text-success text-center">提交成功</p>'
    if request.method == "POST":
        # 获取要添加的书籍商品id,和名称，添加到表
        product_id = request.POST.get("productid")
        name = request.POST.get("name")
        if product_id and name:
            try:
                models.ListenList.objects.create(product_id=product_id, name=name)
                msg = success_msg
            except Exception:
                # 添加失败时提示信息
                msg = '<p class="text-danger text-center">商品ID重复</p>'
        else:
            msg = error_msg
    return render(request, "listen_add.html", {"msg": msg})


def print_ticket(request):
    return render(request, "print_ticket.html")