from django.shortcuts import render, redirect
from . import forms
from django.core.exceptions import ValidationError
from .models import UserActivateTokens
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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


def user_login(request):
    login_form = forms.LoginForm(request.POST or None)

    if login_form.is_valid():
        email = login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, 'ログイン完了しました')
                return redirect('functionapp:home')
            else:
                messages.warning(request, 'ユーザーがアクティブではありません')
        else:
            messages.warning(request, 'IDかパスワードが間違っています')
    return render(request, 'functionapp/user_login.html', context={
        'login_form': login_form,
    })


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'ログアウトしました')
    return redirect('functionapp:home')
