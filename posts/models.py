from django.db import models
# Create your models here.
class Account(models.Model):
	phone=models.CharField(max_length=20, null=False, blank=False)
	dateOfBirth=models.DateField( null=False, blank=False)
	sex=models.CharField(max_length=10, null=False, blank=False)
	username=models.CharField(max_length=100, null=True, blank=True)
	password=models.CharField(max_length=100, null=False, blank=False)
	hashpassword=models.CharField(max_length=1000, null=False, blank=False)
	confirmationCode=models.CharField(max_length=10, null=False, blank=False)
	confirmationStatus=models.CharField(max_length=2)
	onlineStatus=models.CharField(max_length=2)
	createdDate=models.DateTimeField (null=False, blank=False)
	followers = models.IntegerField(null=True, blank=True)
class postType(models.Model):
	pType=models.CharField(max_length=50)
class Post(models.Model):
	author = models.ForeignKey(Account, on_delete=models.CASCADE)
	hashtag=models.CharField(max_length=255)
	date=models.DateTimeField()
	editDate=models.DateTimeField(null=True, blank=True)
	trueValue=models.IntegerField()
	falseValue=models.IntegerField()
class Post_content(models.Model):
	post=models.ForeignKey(Post, on_delete=models.CASCADE)
	text=models.TextField()
	img_id=models.TextField(null=True, blank=True)
	vid_id=models.TextField(null=True, blank=True)
class saved_posts(models.Model):
	username=models.ForeignKey(Account, on_delete=models.CASCADE)
	post=models.ForeignKey(Post, on_delete=models.CASCADE)
	date=models.DateTimeField()
class graphics(models.Model):
	post=models.ForeignKey(Post, on_delete=models.CASCADE)
	graphicsName=models.CharField(max_length=10000000,null=True, blank=True)
class Video_content(models.Model):
	post=models.ForeignKey(Post, on_delete=models.CASCADE)
	videoName=models.CharField(max_length=10000000, null=True, blank=True)
class Comment(models.Model):
	post=models.ForeignKey(Post, on_delete=models.CASCADE)
	commentor=models.ForeignKey(Account, on_delete=models.CASCADE)
	comment=models.TextField(null=True, blank=True)
	imageComment=models.TextField(null=True, blank=True)
	videoComment=models.TextField(null=True, blank=True)
	lightType=models.CharField(max_length = 10)
	date=models.DateTimeField(null = True, blank =True)
class GenuineBlogers(models.Model):
	username = models.ForeignKey(Account, on_delete=models.CASCADE)
	date=models.DateField()
class Follows(models.Model):
	username = models.ForeignKey(Account, on_delete = models.CASCADE)
	bloger = models.TextField()