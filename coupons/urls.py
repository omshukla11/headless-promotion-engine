from django.contrib import admin
from django.urls import path,include

#from .views import *
from . import views
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'static-coupen-create', views.staticCoupenDetails)

urlpatterns =[
	path('', include(router.urls)),
]