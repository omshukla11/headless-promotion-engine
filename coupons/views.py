from django.shortcuts import render
from .serializers import *
from .models import Coupens
from rest_framework import status,permissions,viewsets
import uuid
# Create your views here.
class staticCoupenDetails(viewsets.ModelViewSet):
	queryset = Coupens.objects.all()
	serializer_class = coupensSerializer
	permission_classes = [permissions.IsAuthenticated]

	def post(self,request):
		name = request.POST.get('name')
		is_static = request.POST.get('is_static')
		cart_limit = request.POST.get('cart_limit')
		category = request.POST.get('category')
		amount_limit = request.POST.get('amount_limit')
		percent_limit = request.POST.get('percent_limit')
		valid_date = request.POST.get('valid_date')
		code = request.POST.get('code')
		numberOfcoupens = request.POST.get('numberOfcoupens')
		lengthofcode = request.POST.get('lengthOfCode')
		limit_coupens = request.POST.get('limit_coupens')

		postdata = Coupens.objects.create(name=name,is_static=is_static,cart_limit = cart_limit,category = category,amount_limit=amount_limit,percent_limit=percent_limit,code=code,numberOfcoupens=numberOfcoupens,lengthOfCode=lengthofcode)

		data = Static_coupens.objects.create(coupens=postdata,limit_coupens=limit_coupens)

		ser = coupensSerializer(postdata).data

		return Response(ser)


class DynamicCoupenDetails(viewsets.ModelViewSet):
	queryset = Coupens.objects.all()
	serializer_class = coupensSerializer
	permission_classes = [permissions.IsAuthenticated]

	def post(self,request):
		name = request.POST.get('name')
		is_static = request.POST.get('is_static')
		cart_limit = request.POST.get('cart_limit')
		category = request.POST.get('category')
		amount_limit = request.POST.get('amount_limit')
		percent_limit = request.POST.get('percent_limit')
		valid_date = request.POST.get('valid_date')
		#code = request.POST.get('code')
		numberOfcoupens = request.POST.get('numberOfcoupens')
		lengthofcode = request.POST.get('lengthOfCode')
		#limit_coupens = request.POST.get('limit_coupens')
		user = request.POST.get('user')

		postdata = Coupens.objects.create(name=name,is_static=is_static,cart_limit = cart_limit,category = category,amount_limit=amount_limit,percent_limit=percent_limit,code=code,numberOfcoupens=numberOfcoupens,lengthOfCode=lengthofcode)

		data = Dynamic_coupens.objects.create(coupens=postdata,user=user)

		ser = coupensSerializer(postdata).data

		return Response(ser)









