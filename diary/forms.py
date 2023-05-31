from django import forms

from .models import Diary, Comment


class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ('date', 'title', 'tags', 'text', 'image', 'video', 'image_video')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple,
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }



class DiaryStaffForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ('date', 'title', 'tags', 'text', 'image', 'video', 'image_video', 'secret')
        widgets = {
            'tags': forms.CheckboxSelectMultiple,
        }



class DiaryCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)



class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'コメントを編集してください。'}))
    submit = forms.CharField(widget=forms.HiddenInput(), initial='更新')