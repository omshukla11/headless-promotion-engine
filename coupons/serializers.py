from rest_framework import serializers
from .models import Coupens

class coupensSerializer(serializers.ModelSerializer):
	class Meta:
		model = Coupens
		fields='__all__'


# class coupensSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Coupons
# 		fields='__all__'

# class coupensSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Coupons
# 		fields='__all__'
# 		