from django import forms
from .models import Themes, Comments


class CreateThemeForm(forms.ModelForm):
    title = forms.CharField(label='タイトル')

    class Meta:
        model = Themes
        fields = ('title',)


class DeleteThemeForm(forms.ModelForm):

    class Meta:
        model = Themes
        fields = []  # 削除ボタンだけを表示させる予定なので、fieldsは特に指定する必要ない


class PostCommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}),  # テキストエリアで指定
        )

    class Meta:
        model = Comments
        fields = ('comment', )
