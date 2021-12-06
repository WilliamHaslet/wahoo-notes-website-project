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
    #document_classes = forms.ModelChoiceField(queryset=Profile.objects.all())

    class Meta:
        model = Document
        fields = ('title', 'document', 'document_class', )
        exclude = ('profile', )
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(DocumentForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['document_class'].queryset = user.profile.classes.all()