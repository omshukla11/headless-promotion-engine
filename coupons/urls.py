from django.contrib import admin
from django.urls import path,include

#from .views import *
from .views import staticCoupenDetails, DynamicCoupenDetails, CouponVerify, VerifiedPayment, UpdateCouponCode
from .views import staticCoupenDetails, DynamicCoupenDetails, CouponVerify, VerifiedPayment,Coupenget,couponsList
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

urlpatterns =[
	path('static-create/', staticCoupenDetails.as_view()),
	path('dynamic-create/', DynamicCoupenDetails.as_view()),
    path('coupon-verify/', CouponVerify.as_view()),
    path('verified-payment/', VerifiedPayment.as_view()),
    path('change-code/', UpdateCouponCode.as_view()),
    path('coupen-get/',couponsList.as_view()),
]