from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, \
    UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.shortcuts import get_object_or_404

from django.utils import timezone

from .models import Post
from .forms import PostForm, CommentForm


from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes



# print(User); print(help(User))
# Create your views here.


class BlogListView(ListView):
    model = Post  

    class Meta:
        ordering = ['-published_date']
        filtering = ['published_date__lte=timezone.now()']
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    template_name = "home.html"

class BlogDetailView(DetailView):
    model = Post
    template_name='post_detail.html'

class BlogCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    form_class = PostForm
    # fields = ['title', 'body']
    redirect_field_name = 'blog/post_detail.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    form = PostForm
    fields = ['title', 'body']

class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')


# def post_new(request):
#     form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})


def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(email = request.POST['email']) and User.objects.get(username = request.POST['username'])
                return render (request,'registration/signup.html', {'error':'Email is already taken!'})

            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], email=request.POST['email'],  password=request.POST['password1'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render (request,'registration/signup.html', {'error':'Password does not match!'})
    else:
        print("an error occured")
        return render(request,'registration/signup.html')

# def signup(request):
#     if request.method == 'POST':
#         form = NewUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = NewUserForm()
#     return render(request, 'registration/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        if form.is_valid():
            user = auth.authenticate(username=request.POST['username'], password = request.POST['password'])
            if user is not None:
                auth.login(request,user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('home')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
 
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
					'site_name': 'Goody\'s Blog',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'goody@admin.tech' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
                    
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset/password_reset.html", context={"password_reset_form":password_reset_form})


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)