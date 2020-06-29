from django import forms
from django.contrib.auth.models import User
from .models import Question, MyProfile, PostComment


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'option_one', 'option_two', 'option_three']


class UserUpdate(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['email']


class ProfileUpdate(forms.ModelForm):
    description = forms.CharField(label='description', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '', 'rows':'3', 'cols':'45'}))
    class Meta:
        model = MyProfile
        fields = ['image', 'birth_date', 'phone_number', 'city', 'state', 'description']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Text goes here!!!', 'rows':'5', 'cols':'45'}))
    class Meta:
        model = PostComment
        fields = ['comment']
