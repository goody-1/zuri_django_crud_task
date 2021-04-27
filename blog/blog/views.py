from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, \
    UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import auth

from .models import Post
from .forms import NewUserForm


from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes




# Create your views here.


class BlogListView(ListView):
    model = Post  
    template_name = "home.html"

class BlogDetailView(DetailView):
    model = Post
    template_name='post_detail.html'

class BlogCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = ['title', 'author', 'body']

class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'body']

class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')


def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username = request.POST['username'])
                return render (request,'registration/signup.html', {'error':'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render (request,'registration/signup.html', {'error':'Password does not match!'})
    else:
        print("an error occured")
        return render(request,'registration/signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password = request.POST['password'])
        if user is not None:
            print('login')
            auth.login(request,user)
            return redirect('home')
        else:
            return render (request,'registration/login.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request,'registration/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('home')

   
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password_reset/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset/password_reset.html", context={"password_reset_form":password_reset_form})