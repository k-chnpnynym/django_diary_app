from django import forms
from .models import Diary


class DiaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control-file', 'width': '500', 'height': '500'})
        self.fields['image'].required = False
        self.fields['text'].widget.attrs.update({'rows': 5})
        self.fields['title'].widget.attrs.update({'placeholder': 'タイトルを入力してください'})
        self.fields['date'].widget.attrs.update({'placeholder': '日付を選択してください', 'type': 'date'})
        self.fields['date'].required = True

        # enctypeを指定
        self.enctype = 'multipart/form-data'

    class Meta:
        model = Diary
        fields = ('date', 'title', 'text', 'image')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }
