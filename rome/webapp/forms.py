from django import forms
from .models import Comment, UserProfile
from django.contrib.auth.forms import AuthenticationForm

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'title', 'content']
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'content': forms.Textarea(attrs={'class': 'form-control form-control-sm'}),
        }
        
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm'}))
    
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'last_name', 'address', 'phone_number', 'email']