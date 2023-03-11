from django.shortcuts import render
from .serializers import *
from .models import Coupens, Dynamic_coupens, Static_coupens
from rest_framework import status,permissions,viewsets,generics,mixins
import uuid
from rest_framework.response import Response
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

User = get_user_model()

# Create your views here.
class staticCoupenDetails(mixins.CreateModelMixin, generics.GenericAPIView):
	queryset = Coupens.objects.all()
	serializer_class = coupensSerializer
	permission_classes = [permissions.IsAuthenticated]

	def post(self,request):
		name = request.data['name']
		is_static = request.data['is_static']
		if(is_static!=True):
			return JsonResponse({'error': 'Hit the other API for Dynamic Coupons'}, status=status.HTTP_400_BAD_REQUEST)
		cart_limit = request.data['cart_limit']
		category = request.data['category']
		amount_limit = request.data['amount_limit']
		percent_limit = request.data['percent_limit']
		valid_date = request.data['valid_date']
		code = request.data['code']
		numberOfcoupens = request.data['numberOfcoupens']
		lengthofcode = request.data['lengthOfCode']
		limit_coupens = request.data['limit_coupens']
		postdata = Coupens.objects.create(name=name,valid_date=valid_date, is_static=True,cart_limit = cart_limit,category = category,amount_limit=amount_limit,percent_limit=percent_limit,code=code,numberOfcoupens=numberOfcoupens,lengthofcode=lengthofcode)
		data = Static_coupens.objects.create(coupens=postdata,limit_coupens=limit_coupens)
		ser = coupensSerializer(postdata).data
		return JsonResponse(ser, status=status.HTTP_201_CREATED)


class DynamicCoupenDetails(mixins.CreateModelMixin, generics.GenericAPIView):
	queryset = Coupens.objects.all()
	serializer_class = coupensSerializer
	permission_classes = [permissions.IsAuthenticated]

	def post(self,request):
		name = request.data['name']
		is_static = request.data['is_static']
		if(is_static==True):
			return JsonResponse({'error': 'Hit the other API for Static Coupons'}, status=status.HTTP_400_BAD_REQUEST)
		cart_limit = request.data['cart_limit']
		category = request.data['category']
		amount_limit = request.data['amount_limit']
		percent_limit = request.data['percent_limit']
		valid_date = request.data['valid_date']
		numberOfcoupens = request.data['numberOfcoupens']
		lengthofcode = request.data['lengthofcode']
		users = request.data['users']
		postdata = Coupens.objects.create(name=name, valid_date=valid_date, is_static=False,cart_limit = cart_limit,category = category,amount_limit=amount_limit,percent_limit=percent_limit,numberOfcoupens=numberOfcoupens,lengthofcode=lengthofcode)
		for user_email in users:
			temp = User.objects.get(email=user_email)
			data = Dynamic_coupens.objects.create(coupens=postdata,user=temp,is_used=False)
			print(data.generate_code())

		return JsonResponse({'success': 'created'}, status=status.HTTP_201_CREATED)
	
class CouponVerify(APIView):

	permission_classes = [permissions.IsAuthenticated]
	
	def post(self, request, *args, **kwargs):
		pass