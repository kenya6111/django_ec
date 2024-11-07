import datetime
from django.db import models

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
        return self.name
    class Meta:
        db_table = 'items'

    objects = ItemQuerySet.as_manager()