from django import forms
from .models import Document

#Website form
#from .models import Document

#Trial 2 stack overflow

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

'''
#Trial 1
class DocumentForm(forms.FileField):
    class Meta:
        model = Document
        fields = ('description', 'document', )

#Django form

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
'''