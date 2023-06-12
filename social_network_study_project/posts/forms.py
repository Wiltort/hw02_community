#from django.contrib.auth import get_user_model
#from django.forms import ModelForm
from posts.models import Post, Group
from django import forms

#User = get_user_model()
#GR = Group.objects.values('title')

class PostForm(forms.ModelForm):
    group = forms.ModelChoiceField(required=False, queryset=Group.objects.all())
    text = forms.CharField(widget=forms.Textarea, required=True)
    class Meta:
        model = Post
        fields = ['group', 'text', 'image']


#class PostForm(ModelForm):
#   group = forms.CharField(required=False)
#    text = forms.CharField(widget=forms.Textarea, required=True)
