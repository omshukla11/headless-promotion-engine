from django.db import models
from account.models import *
# Create your models here.

class Coupens(models.Model):
	name = models.CharField(max_length=255,blank=True,null=True)
	is_static = models.BooleanField(default=False)
	cart_limit = models.TextField(blank=True,null=True)
	category = models.TextField(blank=True,null=True)
	amount_limit - models.TextField(blank=True,null=True)
	percent_limit - models.TextField(blank=True,null=True)
	valid_date = models.DateField(blank=True,null=True)
	create_date = models.DateField(auto_now_add=True)
	code = models.CharField(blank=True,null=True)


class Static_coupens(models.Model):

	coupens = models.ForeignKey(Coupens,related_name='coupens_static')
	limit_coupens  = models.IntegerField(blank=True,null=True)


class Dynamic_coupens(models.Model):

	coupens = models.ForeignKey(Coupens,related_name='coupens_dynamic')
	user = models.ForeignKey(User,related_name="coupen_user")
	valid_date = models.DateField(null=True, blank=True)
	is_used = models.BooleanField(default=False)





