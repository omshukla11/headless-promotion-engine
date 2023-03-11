from django.db import models
from accounts.models import *
import uuid
# Create your models here.

class Coupens(models.Model):
	company = models.ForeignKey(AdminProfile, on_delete=models.CASCADE,blank=True,null=True)
	name = models.CharField(max_length=255,blank=True,null=True)
	is_static = models.BooleanField(default=False, null=True)
	cart_limit = models.TextField(blank=True,null=True)
	category = models.TextField(blank=True,null=True)
	amount_limit = models.TextField(blank=True,null=True)
	percent_limit = models.TextField(blank=True,null=True)
	valid_date = models.DateField(blank=True,null=True)
	create_date = models.DateField(auto_now_add=True)
	numberOfcoupens = models.IntegerField(blank=True,null=True)
	lengthofcode = models.IntegerField(blank=True,null=True)



class Static_coupens(models.Model):
	code = models.CharField(max_length=50,blank=True,null=True,unique=True)
	coupens = models.ForeignKey(Coupens,related_name='coupens_static',on_delete=models.CASCADE)
	limit_coupens  = models.IntegerField(blank=True,null=True)


class Dynamic_coupens(models.Model):
	code = models.TextField(blank=True, null=True, unique=True)
	coupens = models.ForeignKey(Coupens,related_name='coupens_dynamic',on_delete=models.CASCADE)
	user = models.ForeignKey(User,related_name="coupen_user",on_delete=models.CASCADE)
	is_used = models.BooleanField(default=False)

	def generate_code(self):
		username = self.user.username
		length_of_code = self.coupens.lengthofcode
		generated_code = ''
		if(int(length_of_code)>len(username)):
			generated_code = f"{username}{uuid.uuid4().hex[:int(length_of_code)-len(username)]}"
		else:
			generated_code = f"{username[:int(length_of_code)]}"
		self.code = generated_code
		try:
			self.save()
		except:
			return None
		return generated_code
	
	def refer_friend(self, email):
		if(self.coupens.numberOfcoupens>0):
			user = User.objects.get(email = email)
			referral = Dynamic_coupens.objects.create(user=user, coupens=self.coupens)
			referral.generate_code()
			return referral
		else:
			return None