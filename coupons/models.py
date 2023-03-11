from django.db import models
from accounts.models import *
# Create your models here.

class Coupens(models.Model):
	name = models.CharField(max_length=255,blank=True,null=True)
	is_static = models.BooleanField(default=False)
	cart_limit = models.TextField(blank=True,null=True)
	category = models.TextField(blank=True,null=True)
	amount_limit = models.TextField(blank=True,null=True)
	percent_limit = models.TextField(blank=True,null=True)
	valid_date = models.DateField(blank=True,null=True)
	create_date = models.DateField(auto_now_add=True)
	code = models.CharField(max_length=50,blank=True,null=True,unique=True)
	numberOfcoupens = models.IntegerField(blank=True,null=True)
	lengthofcode = models.IntegerField(blank=True,null=True)



class Static_coupens(models.Model):

	coupens = models.ForeignKey(Coupens,related_name='coupens_static',on_delete=models.CASCADE)
	limit_coupens  = models.IntegerField(blank=True,null=True)


class Dynamic_coupens(models.Model):

	coupens = models.ForeignKey(Coupens,related_name='coupens_dynamic',on_delete=models.CASCADE)
	user = models.ForeignKey(User,related_name="coupen_user",on_delete=models.CASCADE)
	is_used = models.BooleanField(default=False)





