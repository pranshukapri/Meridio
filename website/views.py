from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.views import generic
from django.views.generic import View
from django.contrib.auth.models import User,Permission
from django.core.mail import send_mail
from .models import Profile,SharedObjects,Network,Request,Conversation
from .forms import UserForm
import random,datetime
# Create your views here.

#Declaring Global lists
AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
flag = False
#Declraing Methods
def index(request):
	user = User.objects.all()
	total = len(user)
	template = loader.get_template('website/index.html') 
	context = {"total":total}
	return HttpResponse(template.render(context,request))

class UserFormView(View):
	form_class = UserForm
	template_name = 'website/registration_form.html'
	def get(self,request):
		form = self.form_class(None)
		return render(request,self.template_name,{'form':form})

	def post(self,request):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = form.save(commit = False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()
			profile = Profile(user=user,contrib=0)
			profile.save()
			user = authenticate(username=username,password=password)
			if user is not None:
				if user.is_active:
					login(request,user)
					request.session['curr_user']=username
					return redirect('website:index')

		return render(request,self.template_name,{'form':form})

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				request.session['curr_user']=username
				return redirect('website:index')
			else:
				return render(request,'website/login.html',{'error_message':'Your account has been disabled'})
		else:
			return render(request,'website/login.html',{'error_message':'Invalid login'})
	return render(request,'website/login.html',{})

def logout_user(request):
	if "curr_user" in request.session:
		del request.session['curr_user']
	logout(request)
	form = UserForm(request.POST or None)
	context = {
		"form":form,
	}
	return render(request,'website/login.html',context)

def change_password(request):
	if request.method == 'POST':
		try:
			user = request.POST['forgot_user']
			user_object = User.objects.get(username = user)
			user_email = user_object.email
			new_password = "@#"+user+"&"+str(random.randint(1,100000))+"$"
			user_object.set_password(new_password)
			user_object.save()
			send_mail(
			    'Wizzy Downloader : Change Password',
			    'Your new password is : '+new_password,
			    'abhijitroy996@gmail.com',
			    [user_email],
			    fail_silently=False,
			)
			#print(user_object.password+" "+user_object.username+" "+new_password)
			return render(request,'website/login.html',{'error_message':'Password Reset'})
		except Exception as e:
			print("Exception : "+str(e))
			return render(request,'website/login.html',{'error_message':'Please check your Username'})

def profile(request):
	if not request.user.is_authenticated():
		return render(request,'website/login.html',{'error_message':'Login to Access Feature'})
	template=loader.get_template('website/profile.html')
	user = User.objects.get(username=request.session['curr_user'])
	profile = user.profile
	share = None
	sent_req = Request.objects.filter(user=user)
	recieved_req = Request.objects.filter(friend_pk=user.pk)
	network = Network.objects.filter(user=user)
	network_list=[]
	for item in network:
		friend = User.objects.get(pk=item.friend_pk)
		network_list.append(friend)
	try:
		share = user.sharedobjects_set.all()
	except Exception as e:
		share=None
	context={'user':user,'profile':profile,'share':share,'sent_req':sent_req,'recieved_req':recieved_req,'network_list':network_list}
	return HttpResponse(template.render(context,request))

def update_profile(request):
	userObj = User.objects.get(username=request.session['curr_user'])
	sent_req=Request.objects.filter(user=userObj)
	recieved_req=Request.objects.filter(friend_pk=userObj.pk)
	network = Network.objects.filter(user=userObj)
	network_list=[]
	for item in network:
		friend = User.objects.get(pk=item.friend_pk)
		network_list.append(friend)
	profile = userObj.profile
	firstname = request.POST['firstname']
	lastname = request.POST['lastname']
	bio = request.POST['userbio']
	location = request.POST['userloc']
	bday = request.POST['bday']
	share = None
	try:
		share = userObj.sharedobjects_set.all()
	except Exception as e:
		share=None
	#print(len(request.POST["avatar"]))
	#print(len(request.FILES["avatar"]))
	try:
		file_length = len(request.POST['avatar'])
	except:
		file_length = len(request.FILES['avatar'])
	if file_length !=0 :		
		profile.avatar = request.FILES['avatar']
		file_type = profile.avatar.url.split(".")[-1]
		file_type = file_type.lower()
		if file_type not in IMAGE_FILE_TYPES:
			context={'user':userObj,'profile':profile,'share':share,'sent_req':sent_req,'recieved_req':recieved_req,'network_list':network_list,'error_message':'Image type Not Supported'}
			return render(request,'website/profile.html',context)
	userObj.first_name = firstname
	userObj.last_name = lastname
	profile.bio = bio
	profile.location = location
	#Convert to datetime type
	try:
		#print('In the correct block')
		profile.birth_date = datetime.datetime.strptime(bday, '%B %d, %Y')
		profile.birth_date = profile.birth_date.date()
	except Exception as e:
		#print('In the IN correct block')
		try:
			profile.birth_date = datetime.datetime.strptime(bday, '%b. %d, %Y')
			profile.birth_date = profile.birth_date.date()
		except:
			profile.birth_date = bday
	print("BirthDate = "+str(profile.birth_date))
	#See if field is null or not
	userObj.save()
	profile.save()
	return render(request,'website/profile.html',{'user':userObj,'profile':profile,'share':share,'sent_req':sent_req,'recieved_req':recieved_req,'network_list':network_list,'error_message':'PROFILE UPDATED'})

def add_share(request):
	user = User.objects.get(username=request.session['curr_user'])
	sent_req=Request.objects.filter(user=user)
	recieved_req=Request.objects.filter(friend_pk=user.pk)
	network = Network.objects.filter(user=user)
	network_list=[]
	for item in network:
		friend = User.objects.get(pk=item.friend_pk)
		network_list.append(friend)
	profile = user.profile
	share = None
	try:
		share = user.sharedobjects_set.all()
	except Exception as e:
		share=None
	name = request.POST['sharedItemName']
	share_object = SharedObjects(user=user,name=name,num_download=0,date_added=datetime.datetime.now().date())
	if len(request.FILES['uploadedfile'])!=0 :
		share_object.upload_obj = request.FILES['uploadedfile']
		share_object.save()
	else:
		context={'user':user,'profile':profile,'share':share,'sent_req':sent_req,'recieved_req':recieved_req,'network_list':network_list,'error_message':'NO FILE SELECTED'}
		return render(request,'website/profile.html',context)		
	share = user.sharedobjects_set.all()
	context={'user':user,'profile':profile,'share':share,'sent_req':sent_req,'recieved_req':recieved_req,'network_list':network_list,'error_message':'Files have been added to your Repository'}
	return render(request,'website/profile.html',context)

def remove_share(request):
	removeName = request.POST['pk']
	user = User.objects.get(username=request.session['curr_user'])
	sent_req=Request.objects.filter(user=user)
	recieved_req=Request.objects.filter(friend_pk=user.pk)
	network = Network.objects.filter(user=user)
	network_list=[]
	for item in network:
		friend = User.objects.get(pk=item.friend_pk)
		network_list.append(friend)
	profile = user.profile
	s = user.sharedobjects_set.get(pk=removeName)
	s.delete()
	share = user.sharedobjects_set.all()
	context={'user':user,'profile':profile,'share':share,'sent_req':sent_req,'recieved_req':recieved_req,'network_list':network_list,'error_message':'File has been REMOVED'}
	return render(request,'website/profile.html',context)

def sharingzone(request,page_id):	
	if not request.user.is_authenticated():
		return render(request,'website/login.html',{'error_message':'Login to Access Feature'})
	if flag == True:
		request.session['null_search']="No such user found"
	start = (int(page_id)-1)*40
	userList = User.objects.all()
	length = int(len(userList)/40)
	next_page = int(page_id)+1
	prev_page=-1
	if int(page_id)!=1:		
		prev_page = int(page_id)-1
	if int(page_id) >= length:
		next_page=-1
	if len(userList)-start < 40:
		userList = userList[start:]
	else:
		userList = userList[start:start+40]
	if(length-int(page_id) > 5):
		length = int(page_id)+5
	context={'userList':userList,'next_page':next_page,'prev_page':prev_page,'range':range(int(page_id),length+1)}
	return render(request,'website/sharing_zone.html',context)

def repository(request,user_id):
	user = get_object_or_404(User , username=user_id)
	logged_user = get_object_or_404(User , username=request.session["curr_user"])
	shared_obj = user.sharedobjects_set.all()
	friend_status = "Send Request"
	list1 = len(Network.objects.filter(user=logged_user,friend_pk=user.pk,friend_name=user.username))
	list2 = len(Request.objects.filter(user=logged_user,friend_pk=user.pk,friend_name=user.username))
	if user.username == request.session['curr_user']:
		friend_status = "My Profile"
	if(list1 != 0):
		friend_status = "Friend"
	elif(list2!=0):
		friend_status = "Request Sent"
	context={'username':user_id,'shared_obj':shared_obj,'user':user,'status':friend_status}
	return render(request,'website/repository.html',context)

def download(request,user_id,object_key):
	#print(user_id+" "+object_key)
	user = get_object_or_404(User,username=user_id)
	object_name = user.sharedobjects_set.get(pk=object_key)
	object_name.num_download+=1
	object_name.save()
	filename = object_name.upload_obj.url.split('/')[-1]
	response = HttpResponse(object_name.upload_obj.file, content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=%s' % filename
	return response

def search(request):
	user_name = request.GET["searchtext"]
	try:
		flag=False
		user = get_object_or_404(User,username=user_name)
	except Exception as e:
		flag=True
		return redirect("website:sharing_zone",page_id=1)
	return redirect("website:repository",user_name)

def preview(request,user_id,object_key):
	user = get_object_or_404(User,username=user_id)
	object_name = user.sharedobjects_set.get(pk=object_key)
	object_name.views+=1
	context={"file":object_name}
	object_name.save()
	return render(request,'website/preview.html',context)

def friend_request(request,user_id):
	sender = User.objects.get(username=request.session['curr_user'])
	reciever = User.objects.get(username=user_id)
	frnd_rqst = Request(user=sender,friend_pk=reciever.pk,friend_name=user_id)
	frnd_rqst.save()
	print("Request sent")
	return redirect("website:repository",user_id=user_id)

def remove_request(request,decision):
	sender = request.POST['sender']
	reciever = request.POST['reciever']
	user = User.objects.get(username=sender)
	friend = User.objects.get(username=reciever)
	req = Request.objects.get(user=user,friend_pk=friend.pk,friend_name=friend.username)
	req.delete()
	if decision == 'accept':
		network1 = Network(user=user,friend_pk=friend.pk,friend_name=friend.username,last_conversation=datetime.datetime.now().date())
		network2 = Network(user=friend,friend_pk=user.pk,friend_name=user.username,last_conversation=datetime.datetime.now().date())
		network1.save()
		network2.save()
		try:
			req = Request.objects.filter(user=friend,friend_pk=user.pk,friend_name=user.username)
		except Exception as e:
			req = None
		if len(req) !=0 and req!=None:
			req[0].delete()
	return redirect("website:profile")

def message_app(request,chat_id):
	if not request.user.is_authenticated():
		return render(request,'website/login.html',{'error_message':'Login to Access Feature'})
	chat_id = int(chat_id)
	user = User.objects.get(username=request.session['curr_user'])
	#in order_by the hyphen means descending order
	network = Network.objects.filter(user=user).order_by("-last_conversation")
	network_list = []
	if(len(network) == 0):
		context={'network_list':network_list,'chat_id':chat_id,'is_empty':"Repo is empty"}
		return render(request,'website/message_app.html',context)
	itr = 0
	for item in network:
		friend = User.objects.get(pk=item.friend_pk)
		network_map = {'network':item,'friend':friend,'chat_id':itr}
		network_list.append(network_map)
		itr = itr+1
	#print(chat_id)
	sent_message_list = network_list[chat_id]["network"].conversation_set.all().order_by("conv_time")
	cross_item = Network.objects.get(user=network_list[chat_id]["friend"],friend_pk=user.pk,friend_name=user.username)
	#print(cross_item)
	recieved_message_list = cross_item.conversation_set.all().order_by("conv_time")
	message_list = sent_message_list | recieved_message_list
	message_list = sorted(message_list,key=lambda item:item.conv_time)
	context={'network_list':network_list,'chat_id':chat_id,'message_list':message_list}
	return render(request,'website/message_app.html',context)

def chat_insert(request,chat_id):
	print(chat_id)
	text = request.POST['chat_text']
	target_name = request.POST['chat_target']
	target = User.objects.get(username=target_name)
	target_pk = target.pk
	user = User.objects.get(username=request.session["curr_user"])
	network1 = Network.objects.get(user=user,friend_pk=target_pk,friend_name=target_name)
	network2 = Network.objects.get(user=target,friend_pk=user.pk,friend_name=user.username)
	network1.last_conversation = datetime.datetime.now()
	network2.last_conversation = datetime.datetime.now()
	time_now = datetime.datetime.now()
	converse = Conversation(network=network1,conversation=text,conv_time=time_now)
	converse.save()
	network1.save()
	network2.save()
	return redirect('website:app_message',0)

def chat_change(request,chat_id):
	return redirect('website:app_message',chat_id)





