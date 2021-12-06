from django import forms
from django.contrib.auth.models import User
from .models import Profile, Document, Class

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['computing_id', 'year']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        #document_class = forms.ModelChoiceField(queryset=Profile.classes.all())
        #document_class = forms.ModelChoiceField(queryset=Class.objects.all())
        fields = ('title', 'document', 'document_class',)
        exclude = ('profile', )