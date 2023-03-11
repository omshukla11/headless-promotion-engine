from rest_framework import serializers
from .models import Coupens, Static_coupens, Dynamic_coupens

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupens
        fields = '__all__'

class StaticCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Static_coupens
        fields = '__all__'

class DynamicCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dynamic_coupens
        fields = '__all__'