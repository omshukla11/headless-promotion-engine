from rest_framework import serializers
from .models import Coupens,Static_coupens,Dynamic_coupens

class coupensSerializer(serializers.ModelSerializer):
	class Meta:
		model = Coupens
		fields='__all__'

class statictSerializer(serializers.ModelSerializer):
	class Meta:
		model = Static_coupens
		fields=['code']

class coupensgetSerializer(serializers.ModelSerializer):
	coupens_static = serializers.SerializerMethodField('get_coupen_static')
	def get_coupen_static(self,obj):
		ser = Static_coupens.objects.filter(coupens=obj).values_list('code','limit_coupens')
		try:
			print(ser[0][1])
			if ser[0][1] !=0:
				return ser[0][0]
			else:
				return ''
		except:
			return ''
	dynamic_coupen = serializers.SerializerMethodField('get_dynamic_static')
	def get_dynamic_static(self,obj):
		ser = Dynamic_coupens.objects.filter(coupens=obj).values_list('code')
		try:
			print(ser[0][0])
			return ser[0][0]
		except:
			return ""
	class Meta:
		model = Coupens
		fields=['name','percent_limit','amount_limit','valid_date','coupens_static','dynamic_coupen','cart_limit']


# class coupensSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Coupons
# 		fields='__all__'

# class coupensSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Coupons
# 		fields='__all__'
# 		
