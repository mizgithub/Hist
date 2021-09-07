from django.shortcuts import render, redirect
from django.http import HttpResponse
import hashlib
import datetime
import random
import os
# Create your views here.
#from .models import Post_table
from .models import Account, postType,Post, Post_content, saved_posts,graphics,Video_content, Comment, GenuineBlogers,Follows 
import json
from django.http import JsonResponse
import sys;
''''from googlevoice import Voice'''
# from twilio.rest import Client
# from twilio.http.http_client import TwilioHttpClient
# from twilio.rest import TwilioRestClient
# from requests import Request, Session
# from twilio.http import HttpClient
# from twilio.http.response import Response
# from requests import Request, Session, hooks

# from twilio.http import HttpClient
# from twilio.http.response import Response
# from twilio.http.request import Request as TwilioRequest
# import logging
# from twilio.compat import urlencode
class postBundle():
	"""docstring for postBundle"""
	def __init__(self,post_text, post_date,truevalue,falsevalue,author, pid, graphCont, is_graphics, moreThanOne,numGraphics, videoName, is_video, is_self, is_saved,light, color_title, seemore):
		self.postType=postType
		self.post_text= post_text
		self.post_date=post_date
		self.truevalue=truevalue
		self.falsevalue=falsevalue
		self.author=author
		self.pid=pid
		self.graphCont=graphCont
		self.is_graphics=is_graphics
		self.moreThanOne=moreThanOne
		self.numGraphics=numGraphics
		self.videoName=videoName
		self.is_video=is_video
		self.is_self=is_self
		self.is_saved=is_saved
		self.light=light
		self.is_post=True
		self.color_title=color_title
		self.saved_id="null"
		self.seemore=seemore
class profile():
	def __init__(self, idnum,username, birthdate, sex, phonenumber, isGenuine, followers, isFollowed):
		self.idnum = idnum
		self.username=username
		self.birthdate=birthdate
		self.sex=sex
		self.phonenumber=phonenumber
		self.isGenuine = isGenuine
		self.followers = followers
		self.isFollowed= isFollowed
class genuineBloger():
	def __init__(self,idnum, username, followers, date, isFollowed):
		self.idnum = idnum
		self.username=username
		self.followers=followers
		self.date=date
		self.isFollowed=isFollowed
def sendSMS(code, phonenumber):
	account_sid = 'AC61d3592b9a7252a7e742ba55d77b006f'
	auth_token = '40eda593cbea82b040292cb42f66e37d'
	#proxy_client = TwilioHttpClient()
	#proxy_client.session.proxies = {'https': os.environ['https_proxy']}

	#client = Client(account_sid, auth_token, http_client=proxy_client)
	client = Client(account_sid, auth_token)
	message = client.messages \
	                .create(
	                     body=code,
	                     from_='+13155414480',
	                     to=phonenumber
	                 )

	print(message.sid)

def setcolorSession(request, color, value):
	request.session[color]=value
	request.session.modified=True
def getcolorSession(request, color):
	is_checked=request.session[color]
	return is_checked
def setsession(request,username):
	request.session['histusername']=username
	request.session.modified=True
def delsession(request):
	del	request.session['histusername']
	request.session.modified=True
def logout(request):
	del	request.session['histusername']
	request.session.modified=True
	return redirect(splash)
def getsession(request):
	username=request.session.get('histusername')
	return username
def splash(request):
	return render(request,"splash.html",{})
def createAccountPage(request):
	return render(request, "createAccount.html", {})
def signup(request):
	
	phone = request.POST.get('phone')
	birthDate=request.POST.get('birthdate')
	sex=request.POST.get('sex')
	passw=request.POST.get('password')
	hashpassw=hashlib.md5(passw.encode())
	date=datetime.datetime.now()
	n=random.randint(100000,999999)
	code="H"+str(n)
	obj=Account.objects.filter(phone=phone)
	if obj and obj[0].phone == phone:
		return render(request, "createAccount.html", {"message": "Phone number is already registered"})
	else:
		acc=Account(phone=phone, dateOfBirth=birthDate, sex=sex, password=passw, hashpassword= hashpassw, confirmationCode= code, confirmationStatus= '1', onlineStatus='0', createdDate=date, followers=0)
		acc.save()
		obj=Account.objects.latest('id')
		user="Hi"+str(obj.id)
		accObj=Account.objects.filter(pk=obj.id)
		accObj.update(username=user)
		setsession(request, user)
		#sendSMS(code, phone)
		return render(request, "accountConfirmation.html", {"username": user})
	
def accountConfirmation(request):
	username=getsession(request)
	return render(request, "accountConfirmation.html", {"username": username})
def deleteColorSetting(request):
	request.session['green']="nochecked"
	request.session['blue']="nochecked"
	request.session['red']="nochecked"
	request.session.modified=True
def changeColorSetting(request):
	deleteColorSetting(request)
	color=request.POST.getlist('color')
	for c in color:
		print(c)
		setcolorSession(request, c, "checked")
	url= request.POST.get('url')
	if url=="home":
		return redirect(home)
	elif url=="blogers":
		response=blogers(request)
		return response
	elif url=="savedPosts":
		return redirect(savedPosts)
def home(request):
	postType=""
	color=""
	hashTag=""
	poster=""
	color=[]
	green=""
	red=""
	blue=""
	if getcolorSession(request, 'green') == "checked":
		color.append("#00ff00")
		green="checked"
	if getcolorSession(request, "blue") == "checked":
		color.append("#0000ff")
		blue="checked"
	if getcolorSession(request, "red") == "checked":
		color.append("#ff0000")
		red="checked"
	if request.POST:
		request.POST.get('postType')
		if request.POST.get('postType')!=None and request.POST.get('postType')!="All":
			postType=request.POST.get('postType')
		if request.POST.get('hashTag')!=None:
			hashTag=request.POST.get('hashTag')
		if request.POST.get('username')!=None:
			poster=request.POST.get('username')
	try:
		username=getsession(request)
		if username!=None and username!="":
			post_col=getPostedData(request,username,postType,color,hashTag,poster)
			if(post_col!=None):
				posttype=getpostTypes()
				return render(request, "home.html", {"posts": post_col, "username": username,"types": posttype, "green":green, "blue":blue, "red":red, "genuineBlogers":getGenuineBlogers()})	
		else:
			return redirect(splash)
	except ValueError as error:
		print(error)
		return redirect(splash)
def newpost(request):
	images, videos, text, ptype="","","",""
	if request.POST:
		text=request.POST.get('text')
		textList=text.split(" ")
		hashTag=""
		for t in textList:
			if len(t)>1 and t[0]=="#":
				hashTag+=t+";"
		username=getsession(request)
		if  username!=None and username!="":
			account=Account.objects.filter(username=username)[0]
			postdate=datetime.datetime.now()
			post_obj=Post(author=account, hashtag=hashTag,date=postdate,trueValue=0,falseValue=0)
			post_obj.save()
			latest_post_obj=Post.objects.latest('id')
			postCont_obj=Post_content(post=latest_post_obj,text= text,img_id="",vid_id="")
			postCont_obj.save()
			if request.FILES:
				if len(request.FILES.getlist('images'))!=0:
					images=request.FILES.getlist('images')
					for im in images:
						gObj=graphics(post=latest_post_obj)
						gObj.save()
						obj=graphics.objects.latest('id')
						graphicsname="hist_img_"+str(hex(obj.id))+"."+str(im.name.split(".")[1].lower())
						status=handle_uploaded_file(im, 'posts/static/uploaded_graphics/'+graphicsname)
						if status:
							graphics.objects.filter(pk=obj.id).update(graphicsName=graphicsname)
				if len(request.FILES.getlist('vid'))!=0:
					video=request.FILES['vid']
					vObj=Video_content(post=latest_post_obj)
					vObj.save()
					obj=Video_content.objects.latest('id')
					videoname="hist_video_"+str(hex(obj.id))+"."+str(video.name.split(".")[1].lower())
					status=handle_uploaded_file(video, 'posts/static/uploaded_videos/'+videoname)
					if status:
						Video_content.objects.filter(pk=obj.id).update(videoName=videoname)
	return redirect(home)
def handle_uploaded_file(filesource, filename):
	status=False
	with open(filename,'wb+') as dest:
		for chunk in filesource.chunks():
			dest.write(chunk)
		status=True
	return status
def Histers_In_your_region(request):
	username = getsession(request)
	accObj =  Account.objects.filter(username = username)[0]
	countryCode = accObj.phone[:4]
	print(countryCode)
	accObj = Account.objects.filter(phone__contains = countryCode). exclude(username = username).order_by('-followers')
	if request.POST:
		last_hister_id = request.POST.get("last_hister_id")
		accObj = accObj.filter(id__lt = last_hister_id)
	histerInYourRegion = []
	counter = 0
	for acc in accObj:
		counter += 1
		if counter > 10:
			break
		histerInYourRegion.append(getprofile(request,acc.username))
	return render(request, "showHistersInRegion.html", {"histers": histerInYourRegion, "username":username,"genuineBlogers":getGenuineBlogers()})
def savePost(request):
	postId=request.GET.get('postId')
	username=getsession(request)
	if postId!=None and username!=None:
		postObj=Post.objects.get(pk=postId)
		accObj=Account.objects.filter(username=username)[0]
		saveddate=datetime.datetime.now()
		savedPostObj=saved_posts(username=accObj, post=postObj, date=saveddate)
		savedPostObj.save()
	return redirect(savedPosts)
def savedPosts(request):
	username=getsession(request)
	postCollection=[]
	colorType=[]
	post_col={"ob0":"null"}
	green=""
	red=""
	blue=""
	last_post_id=""
	maxNumOfPosts=5
	if request.POST:
		last_post_id = request.POST.get('last_post_id')
	print("last post id=",last_post_id)
	if last_post_id !="":
		maxNumOfPosts=5
	if getcolorSession(request, 'green') == "checked":
		colorType.append("#00ff00")
		green="checked"
	if getcolorSession(request, "blue") == "checked":
		colorType.append("#0000ff")
		blue="checked"
	if getcolorSession(request, "red") == "checked":
		colorType.append("#ff0000")
		red="checked"
	if username!=None:
		savedPostObj=saved_posts.objects.filter(username__username=username).order_by('-id')
		if last_post_id!="":
			savedPostObj=savedPostObj.filter(id__lt = last_post_id)
		numberOfPosts=0
		for saved in savedPostObj:
			colorcount=0
			is_graphics=False
			moreThanOne=False
			numGraphics=0
			is_video=False
			graphcont=[]
			graphcontText=""
			postObj=Post.objects.get(pk=saved.post.id)
			postContObj=Post_content.objects.filter(post__id=postObj.id)[0]
			graphObj=graphics.objects.filter(post__id = postObj.id)
			for g in graphObj:
				numGraphics+=1
			for g in graphObj:
				graphcont.append(g.graphicsName)
				graphcontText+=";;"+g.graphicsName
				break
			if len(graphcont)>0:
				is_graphics=True
			if numGraphics>1:
				moreThanOne=True
				numGraphics-=1
			vidObj=Video_content.objects.filter(post__id=postObj.id)
			videoname=""
			if len(vidObj)!=0:
				videoname=vidObj[0].videoName
				is_video=True
			color, color_title=getcolor(postObj.id)
			for c in colorType:
				if c == color:
					colorcount+=1
			if colorcount > 0:
				numberOfPosts +=1
				if numberOfPosts > maxNumOfPosts:
					break
				text=postContObj.text
				if len(text)>0:
					textList=text.split()
					for t in textList:
						if len(t) > 1 and t[0] == "#":
							ht=t.replace("#", "%23")
							text=text.replace(t, "<a href='/search?hashTag="+ht+"'>"+t+"</a>")
				textline= text.split("\n")
				sampleText=text
				seemore=False
				if len(textline) > 5:
					sampleText=str("\n".join(textline[:5]))
					seemore=True
				if last_post_id !="" and last_post_id!=None:
					key="ob"+str(numberOfPosts)
					pbtext=str(sampleText)+"\tSaved on "+str(saved.date.date())+" : Posted on "+str(postObj.date.date())+"\t"+str(postObj.author.username)+"\t"+str(postObj.id)+"\t"+str(graphcontText)+"\t"+str(is_graphics)+"\t"+str(moreThanOne)+"\t"+str(numGraphics)+"\t"+str(videoname)+"\t"+str(is_video)+"\tFalse\tTrue"+"\t"+str(color)+"\t"+str(color_title)+"\t"+str(saved.id)+"\t"+str(seemore)
					post_col[key]=pbtext
				
				pB=postBundle(sampleText, "Saved on "+str(saved.date.date())+" : Posted on "+str(postObj.date.date()),postObj.trueValue,postObj.falseValue,postObj.author.username, postObj.id, graphcont, is_graphics, moreThanOne, numGraphics, videoname, is_video, False, True, color, color_title, seemore)
				pB.saved_id=saved.id
				print("saved id",saved.id)
				postCollection.append(pB)
	if last_post_id !="":
		return HttpResponse(json.dumps(post_col))
	return render(request,"savedPosts.html", {"posts":postCollection,"username":username,"types": getpostTypes(),"green":green, "blue": blue, "red":red, "genuineBlogers":getGenuineBlogers()})
def removeFromSavedPosts(request):
	postId=request.GET.get('postId')
	username = getsession(request)
	if username != None and username != "":
		saved_posts.objects.filter(post__id=postId).delete()
	return redirect(savedPosts)
def getPostText(request):
	post_text=""
	if request.POST:
		postId=request.POST.get('postId')
		postContent=Post_content.objects.filter(post__id=postId)[0]
		post_text=postContent.text
	return HttpResponse(post_text)
def editPostText(request):
	if request.POST:
		postId=request.POST.get('postId')
		text=request.POST.get('editposttext')
		Post.objects.filter(id=postId).update(editDate=datetime.datetime.now())
		Post_content.objects.filter(post__id= postId).update(text=text);
	return redirect(blogers)
def getPostedData(request,username, postType, colorType, hashTag, poster):
	post_col=[]
	try:
		print("gpd",username)
		postCont=Post_content.objects.filter(post__author__username=username)
		followed = Follows.objects.filter(username__username=username)
		if len(followed) >0:
			for f in followed:
				print("gpdbloger",f.bloger)
				postCont = postCont | Post_content.objects.filter(post__author__username=f.bloger)
		postCont = postCont.order_by("-id")
		numberOfPosts=0
		for posts in postCont:
			is_self=False
			is_saved=False
			is_video=False
			is_graphics=False
			moreThanOne=False
			numGraphics=0
			graphcont=[]
			if posts.post.author.username == username:
				is_self=True
			savedObj=saved_posts.objects.filter(post__id=posts.post.id, username__username=username)
			if len(savedObj)>0:
				is_saved=True
			videoname=""
			vidObj=Video_content.objects.filter(post__id = posts.post.id)
			if len(vidObj)!=0:
				videoname=vidObj[0].videoName
				is_video=True
			graphObj=graphics.objects.filter(post__id = posts.post.id)
			for g in graphObj:
				numGraphics+=1
			for g in graphObj:
				graphcont.append(g.graphicsName)
				break
			if len(graphcont)>0:
				is_graphics=True
			if numGraphics>1:
				moreThanOne=True
				numGraphics-=1
			color, color_title=getcolor(posts.post.id)
			is_color=0
			for c in colorType:
				if color == c:
					is_color+=1
			if is_color>0:
				numberOfPosts+=1
				if numberOfPosts > 10:
					break
				text=posts.text
				if len(text)>0:
					textList=text.split()
					for t in textList:
						if len(t) > 1 and t[0] == "#":
							ht=t.replace("#", "%23")
							text=text.replace(t, "<a href='/search?hashTag="+ht+"'>"+t+"</a>")
				textline=text.split("\n")
				sampleText=text
				seemore=False
				if len(textline) > 5:
					for t in textline[:5]:
						sampleText="\n".join(textline[:5])
					print(sampleText)
					seemore=True
				pB=postBundle(sampleText, posts.post.date, posts.post.trueValue, posts.post.falseValue, posts.post.author.username, posts.post.id, graphcont, is_graphics, moreThanOne, numGraphics, videoname, is_video, is_self, is_saved, color, color_title, seemore)
				post_col.append(pB)
		return post_col
	except:
		print("Exceptions/mizanu")
		return post_col
def getBlogerPost(request,username, postType, colorType, hashTag, poster):
	post_col=[]
	try:
		postCont=""
		postCont=Post_content.objects.all().order_by('-id')
		if hashTag!="" and hashTag!=None:
			postCont=postCont.filter(text__contains=hashTag).order_by('-id')
		if poster!="" and poster!=None:
			print("the poster",poster)
			postCont=postCont.filter(post__author__username=poster).order_by('-id')
		numberOfPosts=0
		for posts in postCont:
			is_self=False
			is_saved=False
			is_video=False
			is_graphics=False
			moreThanOne=False
			numGraphics=0
			graphcont=[]
			if posts.post.author.username == username:
				is_self=True
			savedObj=saved_posts.objects.filter(post__id=posts.post.id, username__username=username)
			if len(savedObj)>0:
				is_saved=True
			videoname=""
			vidObj=Video_content.objects.filter(post__id = posts.post.id)
			if len(vidObj)!=0:
				videoname=vidObj[0].videoName
				is_video=True
			graphObj=graphics.objects.filter(post__id = posts.post.id)
			for g in graphObj:
				numGraphics+=1
			for g in graphObj:
				graphcont.append(g.graphicsName)
				break
			if len(graphcont)>0:
				is_graphics=True
			if numGraphics>1:
				moreThanOne=True
				numGraphics-=1
			color, color_title=getcolor(posts.post.id)
			is_color=0
			for c in colorType:
				if color == c:
					is_color+=1
			if is_color>0:
				numberOfPosts+=1
				if numberOfPosts > 10:
					break
				text=posts.text
				if len(text)>0:
					textList=text.split()
					for t in textList:
						if len(t) > 1 and t[0] == "#":
							ht=t.replace("#", "%23")
							text=text.replace(t, "<a href='/search?hashTag="+ht+"'>"+t+"</a>")
				textline=text.split("\n")
				sampleText=text
				seemore=False
				if len(textline) > 5:
					for t in textline[:5]:
						sampleText="\n".join(textline[:5])
					print(sampleText)
					seemore=True
				pB=postBundle(sampleText, posts.post.date, posts.post.trueValue, posts.post.falseValue, posts.post.author.username, posts.post.id, graphcont, is_graphics, moreThanOne, numGraphics, videoname, is_video, is_self, is_saved, color, color_title, seemore)
				post_col.append(pB)
		return post_col
	except:
		print("Exceptions/mizanu")
		return post_col
def getSearchedPost(request,username, postType, colorType, hashTag, poster):
	post_col=[]
	try:
		postCont=""
		postCont=Post_content.objects.all().order_by('-id')
		if hashTag!="" and hashTag!=None:
			postCont=postCont.filter(text__contains=hashTag).order_by('-id')
		if poster!="" and poster!=None:
			print("the poster",poster)
			postCont=postCont.filter(post__author__username=poster).order_by('-id')
		numberOfPosts=0
		for posts in postCont:
			is_self=False
			is_saved=False
			is_video=False
			is_graphics=False
			moreThanOne=False
			numGraphics=0
			graphcont=[]
			if posts.post.author.username == username:
				is_self=True
			savedObj=saved_posts.objects.filter(post__id=posts.post.id, username__username=username)
			if len(savedObj)>0:
				is_saved=True
			videoname=""
			vidObj=Video_content.objects.filter(post__id = posts.post.id)
			if len(vidObj)!=0:
				videoname=vidObj[0].videoName
				is_video=True
			graphObj=graphics.objects.filter(post__id = posts.post.id)
			for g in graphObj:
				numGraphics+=1
			for g in graphObj:
				graphcont.append(g.graphicsName)
				break
			if len(graphcont)>0:
				is_graphics=True
			if numGraphics>1:
				moreThanOne=True
				numGraphics-=1
			color, color_title=getcolor(posts.post.id)
			is_color=0
			for c in colorType:
				if color == c:
					is_color+=1
			if is_color>0:
				numberOfPosts+=1
				if numberOfPosts > 10:
					break
				text=posts.text
				if len(text)>0:
					textList=text.split()
					for t in textList:
						if len(t) > 1 and t[0] == "#":
							ht=t.replace("#", "%23")
							text=text.replace(t, "<a href='/search?hashTag="+ht+"'>"+t+"</a>")
				textline=text.split("\n")
				sampleText=text
				seemore=False
				if len(textline) > 5:
					for t in textline[:5]:
						sampleText="\n".join(textline[:5])
					print(sampleText)
					seemore=True
				pB=postBundle(sampleText, posts.post.date, posts.post.trueValue, posts.post.falseValue, posts.post.author.username, posts.post.id, graphcont, is_graphics, moreThanOne, numGraphics, videoname, is_video, is_self, is_saved, color, color_title, seemore)
				post_col.append(pB)
		return post_col
	except:
		print("Exceptions/mizanu")
		return post_col
def seemoreText(request):
	pid= request.POST.get('pid')
	postCont=Post_content.objects.filter(post__id=pid)[0]
	text=postCont.text
	if len(text)>0:
		textList=text.split()
		for t in textList:
			if len(t) > 1 and t[0] == "#":
				ht=t.replace("#", "%23")
				text=text.replace(t, "<a href='/search?hashTag="+ht+"'>"+t+"</a>")
	return HttpResponse(text)
def get_more_search(request,username, postType, colorType, hashTag, poster,last_post_id):
	post_col=[]
	try:
		postCont=""
		postCont=Post_content.objects.filter(post__id__lt=last_post_id).order_by('-id')
		if hashTag!="" and hashTag!=None:
			postCont=postCont.filter(text__contains=hashTag)
		if poster!="" and poster!=None:
			print("the poster",poster)
			postCont=postCont.filter(post__author__username=poster).order_by('-id')
		if len(postCont) > 2:
			postCont=postCont[:2]
		numberOfPosts=0
		for posts in postCont:
			is_self=False
			is_saved=False
			is_video=False
			is_graphics=False
			moreThanOne=False
			numGraphics=0
			graphcont=[]
			if posts.post.author.username == username:
				is_self=True
			savedObj=saved_posts.objects.filter(post__id=posts.post.id, username__username=username)
			if len(savedObj)>0:
				is_saved=True
			videoname=""
			vidObj=Video_content.objects.filter(post__id = posts.post.id)
			if len(vidObj)!=0:
				videoname=vidObj[0].videoName
				is_video=True
			graphObj=graphics.objects.filter(post__id = posts.post.id)
			for g in graphObj:
				numGraphics+=1
			for g in graphObj:
				graphcont.append(g.graphicsName)
				break
			if len(graphcont)>0:
				is_graphics=True
			if numGraphics>1:
				moreThanOne=True
				numGraphics-=1
			color, color_title=getcolor(posts.post.id)
			is_color=0
			for c in colorType:
				if color == c:
					is_color+=1
			if is_color>0:
				numberOfPosts+=1
				if numberOfPosts > 10:
					break
				text=posts.text
				if len(text)>0:
					textList=text.split()
					for t in textList:
						if len(t) > 1 and t[0] == "#":
							ht=t.replace("#", "%23")
							text=text.replace(t, "<a href='/search?hashTag="+ht+"'>"+t+"</a>")
				pB=postBundle(text, posts.post.date, posts.post.trueValue, posts.post.falseValue, posts.post.author.username, posts.post.id, graphcont, is_graphics, moreThanOne, numGraphics, videoname, is_video, is_self, is_saved, color, color_title, True)
				post_col.append(pB)
		return post_col
	except:
		print("Exceptions/mizanu")
		return post_col
def get_more_posts(request):
	post_col={"ob":"null"}
	username=getsession(request);
	last_post_id = request.POST.get('last_post_id')
	print(last_post_id)
	poster=request.POST.get("poster")
	colorType=[]
	if getcolorSession(request, 'green') == "checked":
		colorType.append("#00ff00")
	if getcolorSession(request, "blue") == "checked":
		colorType.append("#0000ff")
	if getcolorSession(request, "red") == "checked":
		colorType.append("#ff0000")
	try:
		followed = Follows.objects.filter(username__username=username)
		postCont = Post_content.objects.filter(post__author__username=username)
		if len(followed) > 0:
			for f in followed:
				postCont = postCont | Post_content.objects.filter(post__author__username=f.bloger)
		postCont = postCont.filter(post__id__lt = last_post_id). order_by("-id")
		key="ob"
		counter=1
		numberOfPosts=0
		for posts in postCont:
			is_self=False
			is_saved=False
			is_video=False
			is_graphics=False
			moreThanOne=False
			numGraphics=0
			graphcont=""
			if posts.post.author.username == username:
				is_self=True
			savedObj=saved_posts.objects.filter(post__id=posts.post.id, username__username=username)
			if len(savedObj)>0:
				is_saved=True
			videoname=""
			vidObj=Video_content.objects.filter(post__id = posts.post.id)
			if len(vidObj)!=0:
				videoname=vidObj[0].videoName
				is_video=True
			graphObj=graphics.objects.filter(post__id = posts.post.id)
			for g in graphObj:
				numGraphics+=1
			for g in graphObj:
				graphcont+=";;"+g.graphicsName
				break
			if len(graphcont)>0:
				is_graphics=True
			if numGraphics>1:
				moreThanOne=True
				numGraphics-=1
			color, color_title=getcolor(posts.post.id)
			colorcount=0
			for c in colorType:
				if c == color:
					colorcount+=1
			if colorcount > 0:
				numberOfPosts+=1
				if numberOfPosts > 5:
					break;
				text=posts.text
				if len(text)>0:
					textList=text.split()
					for t in textList:
						if len(t) > 1 and t[0] == "#":
							ht=t.replace("#", "%23")
							text=text.replace(t, "<a href='/search?hashTag="+ht+"'>"+t+"</a>")
				#PbText=posts.text+"\t"+posts.post.date+"\t"+posts.post.author.username+"\t"+posts.post.id+"\t"+graphcont+"\t"+is_graphics+"\t"+moreThanOne+"\t"+str(numGraphics)+"\t"+videoname+"\t"+is_video+"\t"+is_self+"\t"+is_saved+"\t"+color+"\t"+color_title;
				pB=str(text)+"\t"+str(posts.post.date)+"\t"+str(posts.post.author.username)+"\t"+str(posts.post.id)+"\t"+str(graphcont)+"\t"+str(is_graphics)+"\t"+str(moreThanOne)+"\t"+str(numGraphics)+"\t"+str(videoname)+"\t"+str(is_video)+"\t"+str(is_self)+"\t"+str(is_saved)+"\t"+str(color)+"\t"+str(color_title)
				key="ob"+str(counter)
				counter+=1
				post_col[key]=pB
		return HttpResponse(json.dumps(post_col))
	except:
		print("Mizanu Exceptions")
		return HttpResponse("error")
def get_more_bloger_posts(request):
	post_col={"ob":"null"}
	username=getsession(request);
	last_post_id = request.POST.get('last_post_id')
	print(last_post_id)
	poster=request.POST.get("poster")
	colorType=[]
	if getcolorSession(request, 'green') == "checked":
		colorType.append("#00ff00")
	if getcolorSession(request, "blue") == "checked":
		colorType.append("#0000ff")
	if getcolorSession(request, "red") == "checked":
		colorType.append("#ff0000")
	try:
		postCont=""
		postCont = Post_content.objects.filter(post__id__lt = last_post_id).order_by('-id')
		if poster!="" and poster!=None:
			postCont=postCont.filter(post__author__username = poster)
		key="ob"
		counter=1
		numberOfPosts=0
		for posts in postCont:
			is_self=False
			is_saved=False
			is_video=False
			is_graphics=False
			moreThanOne=False
			numGraphics=0
			graphcont=""
			if posts.post.author.username == username:
				is_self=True
			savedObj=saved_posts.objects.filter(post__id=posts.post.id, username__username=username)
			if len(savedObj)>0:
				is_saved=True
			videoname=""
			vidObj=Video_content.objects.filter(post__id = posts.post.id)
			if len(vidObj)!=0:
				videoname=vidObj[0].videoName
				is_video=True
			graphObj=graphics.objects.filter(post__id = posts.post.id)
			for g in graphObj:
				numGraphics+=1
			for g in graphObj:
				graphcont+=";;"+g.graphicsName
				break
			if len(graphcont)>0:
				is_graphics=True
			if numGraphics>1:
				moreThanOne=True
				numGraphics-=1
			color, color_title=getcolor(posts.post.id)
			colorcount=0
			for c in colorType:
				if c == color:
					colorcount+=1
			if colorcount > 0:
				numberOfPosts+=1
				if numberOfPosts > 5:
					break;
				text=posts.text
				if len(text)>0:
					textList=text.split()
					for t in textList:
						if len(t) > 1 and t[0] == "#":
							ht=t.replace("#", "%23")
							text=text.replace(t, "<a href='/search?hashTag="+ht+"'>"+t+"</a>")
				#PbText=posts.text+"\t"+posts.post.date+"\t"+posts.post.author.username+"\t"+posts.post.id+"\t"+graphcont+"\t"+is_graphics+"\t"+moreThanOne+"\t"+str(numGraphics)+"\t"+videoname+"\t"+is_video+"\t"+is_self+"\t"+is_saved+"\t"+color+"\t"+color_title;
				pB=str(text)+"\t"+str(posts.post.date)+"\t"+str(posts.post.author.username)+"\t"+str(posts.post.id)+"\t"+str(graphcont)+"\t"+str(is_graphics)+"\t"+str(moreThanOne)+"\t"+str(numGraphics)+"\t"+str(videoname)+"\t"+str(is_video)+"\t"+str(is_self)+"\t"+str(is_saved)+"\t"+str(color)+"\t"+str(color_title)
				key="ob"+str(counter)
				counter+=1
				post_col[key]=pB
		return HttpResponse(json.dumps(post_col))
	except:
		print("Mizanu Exceptions")
		return HttpResponse("error")
def getallImages(request):
	try:
		post_id=request.POST['post_id']
		print("hello there",post_id)
		graphObj = graphics.objects.filter(post__id=int(post_id))
		images="";
		for obj in graphObj:
			images+=obj.graphicsName+";"
		return HttpResponse(images)
	except:
		print('Exceptions')
		return HttpResponse("error")
def getpostTypes():
	obj=postType.objects.all()
	posttype=[]
	for o in obj:
		posttype.append(o.pType)
	print(posttype)
	return posttype
def getcolor(postId):
	commentObj = Comment.objects.filter(post__id = postId)
	number_of_green=0
	number_of_red=0
	for c in commentObj:
		if c.lightType == "green":
			number_of_green+=1
		elif c.lightType == "red":
			number_of_red+=1
	color = "#0000ff"
	color_title="Does not classified as True or False information"
	"""if number_of_red + number_of_green >=100:
		if number_of_green - (number_of_green/4) > number_of_red:
			color = "#00ff00"
		elif number_of_red -(number_of_red/8) > number_of_green:
			color="#ff0000"""
	if number_of_green > number_of_red:
		color="#00ff00"
		color_title="Classified as True information"
	elif number_of_red > number_of_green:
		color="#ff0000"
		color_title="Classified as False information"
	return color, color_title
def getLight(request):
	postId = request.POST.get('postId')
	username = getsession(request)
	commentObj=Comment.objects.filter(post__id = postId)
	green_counter=0
	greenResult=""
	gyou=""
	gcomm=""
	red_counter=0
	redResult=""
	ryou=""
	rcomm=""
	for comment in commentObj:
		if comment.lightType == "green":
			green_counter+=1
			if comment.commentor.username == username:
				gyou="you"
				if comment.comment !=None or comment.imageComment !=None or comment.videoComment != None:
					gcomm="1"
				else:
					gcomm="0"
		elif comment.lightType == "red":
			red_counter+=1
			if comment.commentor.username == username:
				ryou="you"
				if comment.comment !=None or comment.imageComment != None or comment.videoComment !=None:
					rcomm="1"
				else:
					rcomm="0"
	if green_counter > 0:
		if gyou == "you":
			green_counter -=1
		votes=changeNumberToString(green_counter)
		if green_counter == 0:
			votes=""
		greenResult=gyou+","+gcomm+","+votes
	if red_counter > 0:
		if ryou == "you":
			red_counter -=1
		rvotes = changeNumberToString(red_counter)
		if red_counter == 0:
			rvotes =""
		redResult=ryou+","+rcomm+","+rvotes
	result= greenResult+";"+redResult;
	return HttpResponse(result)
def getLightStatus(postId):
	postId = request.POST.get('postId')
	username = getsession(request)
	commentObj=Comment.objects.filter(post__id = postId)
	green_counter=0
	greenResult=""
	gyou=False
	gcomm=False
	red_counter=0
	redResult=""
	ryou=False
	rcomm=False

	for comment in commentObj:
		if comment.lightType == "green":
			green_counter+=1
			if comment.commentor.username == username:
				gyou=True
				if comment.comment !=None or comment.imageComment !=None or comment.videoComment != None:
					gcomm=False
				else:
					gcomm=True
		elif comment.lightType == "red":
			red_counter+=1
			if comment.commentor.username == username:
				ryou=True
				if comment.comment !=None or comment.imageComment != None or comment.videoComment !=None:
					rcomm="1"
				else:
					rcomm="0"
	greenVote=""
	redVote = ""
	if green_counter > 0:
		greenVote = changeNumberToString(green_counter)
		if gyou:
			greenVote = "You, "+greenVote
		
	if red_counter > 0:
		redVote = changeNumberToString(red_counter)
		if ryou:
			redVote = "You ,"+redVote
	return greenVote, gcomm, redVote, rcomm
def changeNumberToString(num):
	stringnum=""
	if num >= 1000:
		stringnum = str(num/1000)+"k"
	elif num >= 1000000:
		stringnum = str(num/1000000)+"m"
	elif num >=1000000000:
		stringnum = str(num/1000000000)+"b"
	elif num >= 1000000000000:
		stringnum = str(num/1000000000000)+"t"
	else:
		stringnum=str(num)
	return stringnum
def switchLight(request):
	try:
		postId = request.POST.get('postId')
		lightType = request.POST.get('lightType')
		username = getsession(request)
		print(lightType, username, postId)
		commObj=Comment.objects.filter(commentor__username = username, post__id = postId)
		if len(commObj) > 0:
			if commObj[0].lightType == lightType:
				commObj.delete()
			else:
				commObj.delete()
				accObj=Account.objects.filter(username=username)[0]
				postObj=Post.objects.filter(id=postId)[0]
				commObj = Comment(post= postObj, commentor= accObj, lightType= lightType)
				commObj.save()
		else:
			accObj=Account.objects.filter(username=username)[0]
			postObj=Post.objects.filter(id=postId)[0]
			commObj = Comment(post= postObj, commentor= accObj, lightType= lightType)
			commObj.save()
	except:
		print("Exception")
	return HttpResponse("OK")
def writePostComment(request):
	if request.POST:
		username=getsession(request)
		postId=request.POST.get('postId')
		comment=request.POST.get('comment')
		lightType=request.POST.get('lighttype')
		date=datetime.datetime.now()
		Comment.objects.filter(commentor__username=username, post__id=postId).update(comment=comment, date=date)
	return HttpResponse("OK")
def getPostComments(request):
	username=getsession(request)
	postId=request.POST.get('postId')
	comment=""
	commObj= Comment.objects.filter(post__id = postId).order_by('-id')
	for comm in commObj:
		if comm.comment !=None:
			comment+=";"+comm.commentor.username+"#$3histcomma"+comm.comment+"#$3histcommaOn "+str(comm.date.date())
	return HttpResponse(comment)
def blogers(request):
	post_col=[]
	posttype=[]
	username=getsession(request)
	postType=""
	hashTag=""
	hister=""
	green=""
	red=""
	blue=""
	colorType=[]
	if getcolorSession(request, 'green') == "checked":
		colorType.append("#00ff00")
		green="checked"
	if getcolorSession(request, "blue") == "checked":
		colorType.append("#0000ff")
		blue="checked"
	if getcolorSession(request, "red") == "checked":
		colorType.append("#ff0000")
		red="checked"
	if request.POST:
		if request.POST.get('color')!=None:
			color=request.POST.get('color')
	if request.GET.get('username')!=None:
		hister=request.GET.get('username')
	if request.POST.get('username')!=None:
		hister=request.POST.get('username')
		print("username", hister)
	if hister == "":
		hister=username
	if hister == username:
		try:
			if username!=None and username!="":
				post_col=getBlogerPost(request,username,postType,colorType,hashTag,hister)
				if post_col!=None:
					posttype=getpostTypes()
					profile=getprofile(request,hister)
		except:
			post_col=[]
			posttype=[]
		return render(request, "blogers.html", {"posts": post_col, "profile": getprofile(request,hister), "is_you":True, "username": username, "types": posttype, "green":green, "blue": blue,"red":red, "genuineBlogers":getGenuineBlogers()})
	else:
		try:
			post_col=getBlogerPost(request,username,postType,colorType,hashTag,hister)
			if post_col!=None:
				posttype=getpostTypes()
				profile=hister
		except:
			post_col=[]
			posttype=[]
	return render(request, "blogers.html", {"posts": post_col, "profile": hister, "is_you":False,"username":username,"green": green, "blue":blue,"red":red, "isFollowed": is_followed(username, hister),"genuineBlogers":getGenuineBlogers(), "isGenuine":getprofile(request, hister).isGenuine})
def is_followed(username, hister):
	print("isFollowed",username, hister)
	isFollowed = "Follow"
	follObj = Follows.objects.filter(username__username = username, bloger=hister)
	if len(follObj) > 0:
		isFollowed = "Unfollow"
	return isFollowed
def get_data(request):
	return HttpResponse("helow world")
def showProfile(request):
	username=getsession(request)
	profile=""
	if username != None and username != "":
		profile=getprofile(request,username)
	return render(request, "user_profile.html", {"profile": profile, "username":username,"genuineBlogers":getGenuineBlogers()})
def getprofile(request,username):
	accObjc=Account.objects.filter(username=username)[0]
	isGenuine = False
	genuineBlogers = GenuineBlogers.objects.filter(username__username = username)
	if len(genuineBlogers)>0:
		isGenuine = True
	isFollowed = False
	you = getsession(request)
	follObj = Follows.objects.filter(username__username = you, bloger = username)
	if len(follObj) > 0:
		isFollowed = True
	prof=profile(accObjc.id,accObjc.username, accObjc.dateOfBirth, accObjc.sex, accObjc.phone, isGenuine, accObjc.followers,isFollowed)
	return prof
def search(request):
	post_col=[]
	colorType={"#00ff00", "#0000ff", "#ff0000"}
	username=getsession(request)
	posttype = getpostTypes()
	if request.GET:
		hashTag=request.GET.get('hashTag')
		print("search hashtag", hashTag)
		if len(hashTag) > 1 and hashTag[0] == "#":
			if request.GET.get("last_post_id"):
				print(request.GET.get("last_post_id"))
				post_col=get_more_search(request, username, None, colorType, hashTag, None, request.GET.get("last_post_id"))
				if len(post_col) == 0:
					pB=postBundle("", "", "", ""," ", "", "", "", "", "", "", "", "", "", "","", True)
					pB.is_post = False
					pB.text=True
					post_col.append(pB)
					return render(request, "searchResult.html", {"posts": post_col, "username": username,"types": posttype, "hashTag": hashTag, "more": False, "genuineBlogers":getGenuineBlogers()})
			else:
				post_col=getSearchedPost(request,username,None,colorType,hashTag,None)
		author=Account.objects.filter(username = hashTag)
		for auth in author:
			pB=postBundle("", "", "", "", auth.username, "", "", "", "", "", "", "", "", "", "","", True)
			pB.is_post = False
			pB.text=False
			post_col.append(pB)
	if len(post_col) == 0:
		pB=postBundle(True, "", "", "","", "", "", "", "", "", "", "", "", "", "","", True)
		pB.is_post=False
		pB.text=True
		post_col.append(pB)
		return render(request, "searchResult.html", {"posts": post_col, "username": username,"types": posttype, "hashTag": hashTag,"more":False, "genuineBlogers":getGenuineBlogers()})
	return render(request, "searchResult.html", {"posts": post_col, "username": username,"types": posttype, "hashTag": hashTag, "more": True, "genuineBlogers":getGenuineBlogers()})	
def login(request):
	user=request.POST.get('username')
	passw=request.POST.get('password')
	print(user, passw)
	try:
		obj=Account.objects.filter(username=user) | Account.objects.filter(phone=user)
		obj=obj[0]
		print(obj.phone)
		confirmationStatus=obj.confirmationStatus
		if (obj.username==user or obj.phone==user) and passw==obj.password:
			setsession(request, obj.username)
			setcolorSession(request, "green","checked")
			setcolorSession(request, "blue","checked")
			setcolorSession(request, "red","checked")
			if confirmationStatus=='1':
				return redirect(home)
			else:
				return redirect(accountConfirmation)
		else:
			return render(request, "splash.html",{"message": "Wrong username and or Password"})		
	except:
		return render(request, "splash.html",{"message": "Wrong username and or Password"})						
def deletePost(request):
	postId=request.GET.get("postId")
	username=getsession(request);
	if username !=None and username!="":
		graphObj=graphics.objects.filter(post__id=postId)
		for obj in graphObj:
			_delete_file("posts/static/uploaded_videos/"+obj.graphicsName)
		vidObj=Video_content.objects.filter(post__id=postId)
		if len(vidObj)>0:
			_delete_file("posts/static/uploaded_video/"+vidObj[0].videoName)
		print(postId)
		Post.objects.filter(id=int(postId)).delete()
	return redirect(blogers)
def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)
def setest(request):
	username=getsession(request)
	return render(request, "setest.html",{"username":username})
def performAccountConfirmation(request):
	username=getsession(request)
	confcode=request.POST.get('confcode')
	print(username)
	try:
		obj=Account.objects.filter(username=username)
		obj=obj[0]
		if str(obj.confirmationCode)==str(confcode):
			Account.objects.filter(pk=obj.id).update(confirmationStatus='1')
			return redirect(home)
		else:
			return render(request,"accountConfirmation.html", {"message": "Enter the correct confirmation code. If you have no the code click on Resend","username": username})
	except:
			return render(request,"accountConfirmation.html", {"message": "Enter the correct confirmation code. If you have no the code click on Resend","username":username})
def updateGeniuneBlogers(request):
	print(datetime.datetime.now().date())
	users = Account.objects.all()
	for user in users:
		green, blue, red=0,0,0
		user_posts=Post.objects.filter(author__username = user.username)
		for post in user_posts:
			color, _ = getcolor(post.id)
			if color == "#00ff00":
				green+=1
			elif color == "#0000ff":
				blue+=1
			else:
				red+=1
		if green > 1 and red == 0:
			gbobj=GenuineBlogers.objects.filter(username__username = user.username)
			if len(gbobj) == 0:
				genuineBObj = GenuineBlogers(username=user, date=datetime.datetime.now().date())
				genuineBObj.save()
		elif red > 0:
			gbobj=GenuineBlogers.objects.filter(username__username = user.username)
			gbobj.delete()

	genuineBObj = GenuineBlogers.objects.all()
	blogers=[]
	for gb in genuineBObj:
		blogers.append(gb)

	return render(request, "admin_update_genuine_blogers_list_histxcxhupdating.html", {"blogers": blogers})
def getGenuineBlogers():
	genuineBObj = GenuineBlogers.objects.all()
	blogers=[]
	counter=0
	for gb in genuineBObj:
		counter += 1
		if counter > 5:
			break
		accObj = Account.objects.filter(username = gb.username.username)[0]
		genBlog = genuineBloger(gb.id,gb.username.username, accObj.followers, gb.date, False)
		blogers.append(genBlog)
	return blogers
def allGenuineBlogers(request):
	user = getsession(request)
	genuineBObj = GenuineBlogers.objects.all().order_by('-id')
	if request.POST:
		last_genuine_bloger_id= request.POST.get("last_genuine_bloger_id")
		genuineBObj = GenuineBlogers.objects.filter(id__lt = last_genuine_bloger_id).order_by('-id')
	blogers=[]
	counter=0;
	for gb in genuineBObj:
		if gb.username.username != user:
			isFollowed="Follow"
			followedObj = Follows.objects.filter(username__username=user, bloger = gb.username.username)
			if len(followedObj) > 0:
				isFollowed = "Unfollow"
			accObj = Account.objects.filter(username = gb.username.username)[0]
			genBlog = genuineBloger(gb.id,gb.username.username, accObj.followers, gb.date, isFollowed)
			counter+=1
			if counter > 10:
				break
			blogers.append(genBlog)
	return render(request, "All_genuine_blogers.html", {"genuineBlogers": blogers, "username":user,"topgenuineBlogers":getGenuineBlogers()})
def follow(request):
	if request.POST:
		try:
			user=getsession(request)
			bloger=request.POST.get('bloger')
			AccObj = Account.objects.filter(username=user)[0]
			fObject= Follows(username = AccObj, bloger=bloger)
			fObject.save()
			gbObj=Account.objects.filter(username = bloger)[0]
			numOf_followers = int(gbObj.followers) + 1
			Account.objects.filter(username=bloger).update(followers = numOf_followers)
			return HttpResponse("ok")
		except:
			return HttpResponse("no")
	return HttpResponse("no")
def unfollow(request):
	if request.POST:
		try:
			user=getsession(request)
			bloger=request.POST.get('bloger')
			fObject=Follows.objects.filter(username__username=user, bloger=bloger)
			fObject.delete()
			gbObj=Account.objects.filter(username = bloger)[0]
			numOf_followers = int(gbObj.followers) - 1
			Account.objects.filter(username=bloger).update(followers = numOf_followers)
			return HttpResponse("ok")
		except:
			return HttpResponse("no")
	return HttpResponse("no")