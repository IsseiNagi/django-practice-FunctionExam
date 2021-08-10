from django.shortcuts import render, redirect
from . import forms
from django.core.exceptions import ValidationError
from .models import UserActivateTokens

# Create your views here.


def home(request):
    return render(
        request, 'functionapp/home.html'
    )


def regist(request):
    regist_form = forms.RegistForm(request.POST or None)
    if regist_form.is_valid():
        try:
            regist_form.save()
            return redirect('functionapp:home')
        except ValidationError as e:
            regist_form.add_error('password', e)
    return render(
        request, 'functionapp/regist.html', context={
            'regist_form': regist_form
        }
    )


# トークン付きのURLから遷移したページで、実行する関数を定義する
def activate_user(request, token):

    # UserActivateTokensで指定したmanagerを呼び出すので、.objectsにする
    user_activate_token = UserActivateTokens.objects.activate_user_by_token(
        token)
    return render(request, 'functionapp/activate_user.html')
