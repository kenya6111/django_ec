import datetime
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class ItemQuerySet(models.QuerySet):
    def search(self,**kwargs):
        queryset = self;
        # 各条件に基づいてフィルタリングを適用
        if kwargs.get("product_name"):
            queryset = queryset.filter(name__icontains=kwargs["product_name"])
        if kwargs.get("star_from"):
            queryset = queryset.filter(star__gte=kwargs["star_from"])
        if kwargs.get("star_to"):
            queryset = queryset.filter(star__lte=kwargs["star_to"])
        if kwargs.get("price_from"):
            queryset = queryset.filter(price__gte=kwargs["price_from"])
        if kwargs.get("price_to"):
            queryset = queryset.filter(price__lte=kwargs["price_to"])

        # is_sale と is_not_sale の条件を確認
        is_sale = kwargs.get("is_sale")
        is_not_sale = kwargs.get("is_not_sale")
        if is_sale is not None and is_not_sale is not None:
            pass  # 両方が指定されている場合はフィルタを適用しない
        elif is_sale is not None:
            queryset = queryset.filter(is_sale=True)
        elif is_not_sale is not None:
            queryset = queryset.filter(is_sale=False)

        # 作成日の範囲条件を追加
        if kwargs.get("create_date_from"):
            queryset = queryset.filter(created_at__gte=kwargs["create_date_from"])
        if kwargs.get("create_date_to"):
            queryset = queryset.filter(created_at__lte=kwargs["create_date_to"])

        return queryset
class PurchaseDetaiQuerySet(models.QuerySet):
    def search(self,**kwargs):
        queryset = self;

        if kwargs.get("create_date_from"):
            queryset = queryset.filter(created_at__gte=kwargs["create_date_from"])
        if kwargs.get("create_date_to"):
            queryset = queryset.filter(created_at__lte=kwargs["create_date_to"])

        return queryset

class ItemModel(models.Model):
    name = models.CharField(max_length=100)
    star = models.IntegerField(null=True, blank=True, default=1)
    price = models.IntegerField(null=True, blank=True, default=1)
    image = models.ImageField(upload_to='')
    is_sale = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    # content = models.TextField()
    # author = models.CharField(max_length=100)
    # readText = models.TextField(null=True, blank=True, default='a')
    def __str__(self):
        return self.name +" id:"+ str(self.id)
    class Meta:
        db_table = 'items'

    objects = ItemQuerySet.as_manager()

class CartModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def item_num_sum (self):
        return sum(item.quantity for item in self.cart_items.all())
    @property
    def item_price_sum(self):
        return sum(item.item.price*0.6*item.quantity if item.item.is_sale else item.item.price*item.quantity for item in self.cart_items.all())

class CartItemModel(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "cart_id:" + str(self.cart.id) + ", item_id:"+str(self.item.id)+", quantity:"+str(self.quantity)

class CheckoutModel(models.Model):
    cart = models.OneToOneField(CartModel, on_delete=models.SET_NULL, related_name='checkout', null=True, blank=True)
    first_name = models.CharField(max_length=50,blank=True, null=True)
    last_name = models.CharField(max_length=50,blank=True, null=True)
    user_name = models.CharField(max_length=50,blank=True, null=True)
    email = models.EmailField(max_length=100,blank=True, null=True)
    address1 = models.CharField(max_length=100,blank=True, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100,blank=True, null=True)
    state = models.CharField(max_length=100,blank=True, null=True)
    zip_code = models.CharField(max_length=20,blank=True, null=True)

    name_on_card = models.CharField(max_length=100,blank=True, null=True)
    credit_number=models.CharField(max_length=100,null=True,blank=True)
    credit_expiration = models.CharField(max_length=10,blank=True, null=True)
    cvv = models.PositiveSmallIntegerField(blank=True, null=True)
    total_price = models.BigIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)

class PurchaseDetailModel(models.Model):
    checkout = models.ForeignKey(CheckoutModel, on_delete=models.CASCADE, related_name='purchase_details')
    item_name = models.CharField(max_length=100)
    item_price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    is_sale = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PurchaseDetaiQuerySet.as_manager()


class PromotionCodeModel(models.Model):
    promote_code = models.CharField(max_length=100)
    discount_amount = models.IntegerField(default=0)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return str(self.promote_code) +": "+ str(self.discount_amount)


