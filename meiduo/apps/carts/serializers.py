from rest_framework import serializers
from meiduo.apps.goods.models import SKU


class CartSerializer(serializers.Serializer):
    """购物车序列化器"""
    sku_id = serializers.IntegerField(min_value=1, label="商品sku_Id")
    count = serializers.IntegerField(label="购买数量")
    selected = serializers.BooleanField(default=True, label="商品勾选状态")

    def validate_sku_id(self, value):
        try:
            SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError("sku_id不存在")
