from django.shortcuts import render
from .serializers import *
from .models import Coupens, Dynamic_coupens, Static_coupens
from rest_framework import status,permissions,viewsets,generics,mixins
import uuid
from rest_framework.response import Response
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
import pandas as pd
import numpy as np
from django.db.models import Q
from datetime import date,datetime, timedelta
import datetime

User = get_user_model()
from datetime import date
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
		lengthofcode = request.data['lengthofcode']
		limit_coupens = request.data['limit_coupens']
		postdata = Coupens.objects.create(name=name,valid_date=valid_date, is_static=True,cart_limit = cart_limit,category = category,amount_limit=amount_limit,percent_limit=percent_limit,numberOfcoupens=numberOfcoupens,lengthofcode=lengthofcode)
		data = Static_coupens.objects.create(coupens=postdata,limit_coupens=limit_coupens,code=code)
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
		#users = request.data['users']
		csv_file = request.FILES['csv']
		if not csv_file.name.endswith('.csv'):
			return Response('THIS IS NOT A CSV FILE')
		df = pd.read_csv(csv_file)
		users_id = []
		for i,j in enumerate(df['visited']):
			print(i,"==",j)
			if j>3:
				print("this is perfect i ",i)
				print("This is value of j",j)
				users_id.append(i)
	

		postdata = Coupens.objects.create(name=name, valid_date=valid_date, is_static=False,cart_limit = cart_limit,category = category,amount_limit=amount_limit,percent_limit=percent_limit,numberOfcoupens=numberOfcoupens,lengthofcode=lengthofcode)
		for i in users_id:
			id_yas = df['user_id'][i]
			temp = User.objects.get(id=id_yas)
			data = Dynamic_coupens.objects.create(coupens=postdata,user=temp,is_used=False)
			print(data.generate_code())

		return JsonResponse({'success': 'created'}, status=status.HTTP_201_CREATED)
	
class CouponVerify(APIView):

	#permission_classes = [permissions.IsAuthenticated]
	
	def post(self, request, *args, **kwargs):
		cart_value = request.data['cartvalue']
		code = request.data['couponcode']
		final_discount = -1
		try:
			dynamic = Dynamic_coupens.objects.get(code = code)
			if(dynamic.is_used==False):
				if(int(dynamic.coupens.cart_limit)<=cart_value):
					final_discount = cart_value * (float(dynamic.coupens.percent_limit)*0.01)
					final_discount = min(final_discount, float(dynamic.coupens.amount_limit))
					return JsonResponse({'finaldiscount': final_discount, 'final_cart_value': (cart_value-final_discount)}, status=status.HTTP_202_ACCEPTED)
				else:
					return JsonResponse({'error': 'Cart value is less than expected'}, status=status.HTTP_400_BAD_REQUEST)
			else:
				return JsonResponse({'error': 'Coupon already used'}, status=status.HTTP_400_BAD_REQUEST)
		except:
			try:
				static = Coupens.objects.get(code = code)
				if(static.limit_coupens>0):
					if(static.coupens.cart_limit<=cart_value):
						final_discount = cart_value * (float(static.coupens.percent_limit)*0.01)
						final_discount = min(final_discount, float(static.coupens.amount_limit))
						return JsonResponse({'finaldiscount': final_discount, 'final_cart_value': (cart_value-final_discount)}, status=status.HTTP_202_ACCEPTED)
					else:
						return JsonResponse({'error': 'Cart value is less than expected'}, status=status.HTTP_400_BAD_REQUEST)
				else:
					return JsonResponse({'error': 'Total redemption exceeded'}, status=status.HTTP_403_FORBIDDEN)
			except:
				return JsonResponse({'error': 'No Coupon Code found'}, status=status.HTTP_204_NO_CONTENT)
			
class VerifiedPayment(APIView):

	permission_classes = [permissions.IsAuthenticated]
	
	def post(self, request, *args, **kwargs):
		code = request.data['couponcode']
		try:
			dynamic = Dynamic_coupens.objects.get(code = code)
			dynamic.is_used = True
			dynamic.save()
			return JsonResponse({'success': 'Dynamic coupon used'}, status=status.HTTP_202_ACCEPTED)
		except:
			try:
				static = Coupens.objects.get(code = code)
				static.limit_coupens = static.limit_coupens - 1
				static.save()
				return JsonResponse({'success': 'Static coupon used'}, status=status.HTTP_202_ACCEPTED)
			except:
				return JsonResponse({'error': 'No Coupon Code found'}, status=status.HTTP_204_NO_CONTENT)


class Coupenget(APIView):
	permission_classes = [permissions.IsAuthenticated]


	def get(self, request, *args, **kwargs):
		coupens =  Coupens.objects.all()
		
		return Response("Done")


class couponsList(generics.ListCreateAPIView):
	queryset = Coupens.objects.all()
	serializer_class = coupensgetSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Coupens.objects.all()

        


class UpdateCouponCode(APIView):

	def post(self, request, *args, **kwargs):
		oldcode = request.data['oldcode']
		newcode = request.data['newcode']
		try:
			static = Static_coupens.objects.get(code = oldcode)
			try:
				temp = Static_coupens.objects.get(code = newcode)
				try:
					temp = Dynamic_coupens.objects.get(code = newcode)
				except:
					return JsonResponse({'Select another code as a coupon for this already exists'}, status=status.HTTP_226_IM_USED)
			except:
				static.code = newcode
				static.save()
				return JsonResponse({'success': 'Coupon Code changed'}, status=status.HTTP_200_OK)
		except:
			return JsonResponse({'error': 'No Code Found'}, status=status.HTTP_400_BAD_REQUEST)
