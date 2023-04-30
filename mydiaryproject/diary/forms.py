from django import forms
from .models import Diary, Comment


class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ('date', 'title', 'text', 'image', 'tags')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }



class DiaryStaffForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ('date', 'title', 'text', 'image', 'tags', 'secret')



class DiaryCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
