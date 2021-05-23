from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Comment

# Create your forms here.

# class NewUserForm(UserCreationForm):
# 	email = forms.EmailField(required=True, help_text="Required. Inform a valid email address.")

# 	class Meta:
# 		model = User
# 		fields = ("username", "email", "password1", "password2")

# 	def save(self, commit=True):
# 		user = super(NewUserForm, self).save(commit=False)
# 		user.email = self.cleaned_data['email']
# 		if commit:
# 			user.save()
# 		return user

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title', 'body')
        

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('author', 'text',)