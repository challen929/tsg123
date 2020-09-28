from django.db import models
from django.core.validators import validate_comma_separated_integer_list
import datetime
from decimal import Decimal
# Create your models here.


# 会员管理
class Member(models.Model):
    """
    会员基本信息
    """
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)


class MemberState(models.Model):
    """
    会员状态信息
    """
    id = models.IntegerField(primary_key=True)
    begin_date = models.DateField()
    end_date = models.DateField()
    deposit = models.SmallIntegerField(default=0)
    name = models.CharField(max_length=10, null=True)
    parent = models.CharField(max_length=4, null=True)
    age_of_boy = models.CharField(null=True, max_length=10, validators=[validate_comma_separated_integer_list])
    age_of_girl = models.CharField(null=True, max_length=10, validators=[validate_comma_separated_integer_list])
    memo = models.CharField(max_length=50, null=True)
    referer = models.IntegerField(default=1000)
    state = models.SmallIntegerField()
    member = models.OneToOneField(to="Member", on_delete=models.CASCADE)
    type = models.ForeignKey(to="MemberType", on_delete=models.CASCADE)

    def state_set(self):
        self.state = (self.end_date - datetime.datetime.now().date()).days
        return self.state


class MemberType(models.Model):
    """
    会员类型：月卡，季卡，年卡，购书
    """
    name = models.CharField(max_length=4)
    days = models.SmallIntegerField()
    price = models.SmallIntegerField()
    discount = models.DecimalField(max_digits=3, decimal_places=2)


class MemberLog(models.Model):
    member = models.ForeignKey(to="MemberState", on_delete=models.CASCADE)
    type = models.CharField(max_length=10)  # 新增会员 交付押金 退还押金 续费会员 赠送会员 更换手机
    cart_id = models.IntegerField(null=True)
    phone = models.CharField(max_length=11, null=True)
    begin_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    deposit = models.SmallIntegerField(null=True)
    income = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    paid_by = models.CharField(max_length=6, null=True)
    created_time = models.DateTimeField(auto_now_add=True)


# 图书管理
class Book(models.Model):
    """
    童书基本信息
    """
    ISBN = models.CharField(max_length=16, primary_key=True)
    name = models.CharField(max_length=50)
    sets = models.SmallIntegerField(default=1)
    age_group = models.CharField(max_length=8, null=True)
    publisher = models.CharField(max_length=50, null=True)
    language = models.CharField(max_length=6, null=True)
    ori_price = models.DecimalField(max_digits=5, decimal_places=2)
    discount = models.DecimalField(max_digits=3, decimal_places=2)
    sell_price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    plus_price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    is_package = models.BooleanField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)

    def cal_price(self):
        self.sell_price = (self.ori_price * self.discount).quantize(Decimal("0.00"))
        self.plus_price = (self.sell_price * Decimal("0.88")).quantize(Decimal("0.00"))


class Stock(models.Model):
    """
    库存信息
    """
    ISBN = models.CharField(max_length=16, primary_key=True)
    parent_cate = models.CharField(max_length=10, null=True)
    sub_cate = models.CharField(max_length=10, null=True)
    book_size = models.CharField(max_length=4, null=True)
    total = models.SmallIntegerField(default=0)
    placed = models.SmallIntegerField(default=0)
    placed_on = models.CharField(max_length=5, null=True)
    stocked = models.SmallIntegerField(default=0)
    stocked_on = models.CharField(max_length=5, null=True)
    book = models.OneToOneField(to="Book", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class PurchaseBatch(models.Model):
    order_id = models.BigIntegerField()
    channel = models.CharField(max_length=10, default="京东")
    total_price_sale = models.DecimalField(max_digits=6, decimal_places=2)
    prom_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    coupon_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total_price_paid = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=4)
    progress = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_time = models.DateTimeField(auto_now_add=True)


class PurchaseDetail(models.Model):
    ISBN = models.CharField(max_length=16)
    package_id = models.CharField(max_length=16)
    price_sale = models.DecimalField(max_digits=5, decimal_places=2)
    price_paid = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.SmallIntegerField(default=1)
    is_sold = models.BooleanField(default=0)
    is_back = models.BooleanField(default=0)
    memo = models.CharField(max_length=20)
    created_time = models.DateTimeField(auto_now_add=True)
    batch = models.ForeignKey(to="PurchaseBatch", on_delete=models.CASCADE)
    book = models.ForeignKey(to="Book", on_delete=models.CASCADE)


class PackageMap(models.Model):
    package_id = models.CharField(max_length=16)
    book = models.ForeignKey(to="Book", on_delete=models.CASCADE)

    class Meta:
        unique_together=("package_id", "book")


# 借阅管理
class BorrowRecord(models.Model):
    member = models.ForeignKey(to="MemberState", on_delete=models.CASCADE)
    book = models.ForeignKey(to="Stock", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    return_time = models.DateTimeField(null=True)
    memo = models.CharField(max_length=50, null=True)
    damaged = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    update_time =  models.DateTimeField(auto_now=True)


class Cart(models.Model):
    book = models.ForeignKey(to="Book", on_delete=models.DO_NOTHING)
    member = models.ForeignKey(to="MemberState", on_delete=models.SET_DEFAULT, default=0)


class Order(models.Model):
    order_id = models.IntegerField()
    actually_paid = models.DecimalField(max_digits=5, decimal_places=2)
    created_time = models.DateTimeField(auto_now_add=True)
    purchase = models.ForeignKey(to="PurchaseDetail", on_delete=models.DO_NOTHING)
    member = models.ForeignKey(to="MemberState", on_delete=models.SET_DEFAULT, default=0)


# 价格走势
class ListenList(models.Model):
    product_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    created_date = models.DateField(auto_now_add=True)


class ListenAttr(models.Model):
    product_id = models.BigIntegerField()
    ori_price = models.DecimalField(max_digits=5, decimal_places=2)
    daily_price = models.DecimalField(max_digits=5, decimal_places=2)
    cut_price = models.DecimalField(max_digits=5, decimal_places=2)
    plus_price = models.DecimalField(max_digits=5, decimal_places=2)
    final_price = models.DecimalField(max_digits=5, decimal_places=2)
    prom = models.CharField(max_length=10)
    created_time = models.DateTimeField()
    detail = models.ForeignKey(to="ListenList", on_delete=models.CASCADE)

    class Meta:
        abstract=True


class HistoryPrice(ListenAttr):
    pass


class PrePrice(ListenAttr):
    pass


class CurrentPrice(ListenAttr):
    final_discount = models.DecimalField(max_digits=3, decimal_places=2)
    pre_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    bot_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    link = models.URLField(null=True)

