from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib import messages
from .models import Themes, Comments
from django.http import Http404
from django.core.cache import cache
from django.http import JsonResponse

# Create your views here.


def create_theme(request):
    create_theme_form = forms.CreateThemeForm(request.POST or None)
    if create_theme_form .is_valid():

        # 現在ログインしているユーザーを取得して、外部キー要素に代入
        create_theme_form.instance.user = request.user
        create_theme_form.save()
        messages.success(request, '掲示板を作成しました')
        return redirect('boards:list_themes')

    return render(request, 'boards/create_theme.html', context={
        'create_theme_form': create_theme_form,
    })


def list_themes(request):
    themes = Themes.objects.fetch_all_themes()  # ThemeManagerの関数をobjectsで呼び出す
    return render(request, 'boards/list_themes.html', context={
        'themes': themes
    })


def edit_theme(request, id):
    # idを引数に取ってThemesモデルから該当themeを取得する
    theme = get_object_or_404(Themes, id=id)
    # themeのuser.idが編集リクエストを投げているユーザーidと異なる場合は404エラーを出す
    if theme.user.id != request.user.id:
        raise Http404
    edit_theme_form = forms.CreateThemeForm(
        request.POST or None, instance=theme)  # CreateThemeFormを使い回す
    if edit_theme_form.is_valid():
        edit_theme_form.save()
        messages.success(request, '掲示板を更新しました')
        return redirect('boards:list_themes')
    return render(
        request, 'boards/edit_theme.html', context={  # フォームとidを引数で渡す
            'edit_theme_form': edit_theme_form,
            'id': id,
        }
    )


def delete_theme(request, id):
    theme = get_object_or_404(Themes, id=id)
    if theme.user.id != request.user.id:
        raise Http404
    delete_theme_form = forms.DeleteThemeForm(request.POST or None)
    if delete_theme_form.is_valid():  # csrfトークンのチェックだけ
        theme.delete()
        messages.success(request, '掲示板を削除しました')
        return redirect('boards:list_themes')
    return render(
        request, 'boards/delete_theme.html', context={
            'delete_theme_form': delete_theme_form,
        }
    )


# Commentsモデルを使ってテーマにコメント投稿をする
def post_comments(request, theme_id):
    #  キャッシュにデータがあった場合は取り出す
    # 第１引数の名前でキャッシュに値がセットされていたら取り出す。なければdefault第２引数''ブランクを返す。
    saved_comment = cache.get(
        f'saved_comment-theme_id={theme_id}-user_id={request.user.id}',
        ''
    )
    post_comment_form = forms.PostCommentForm(
        request.POST or None,
        # saved_commentを、コメントの初期値として指定する
        initial={'comment': saved_comment},
        )

    # そのままsaveすると、該当テーマやユーザーの情報がないので、テーマをまず取得する
    theme = get_object_or_404(Themes, id=theme_id)

    # 投稿されたコメントを取得する Commentsのマネージャークラスを新たに作成して、fetch_by_theme_idメソッドを定義する
    comments = Comments.objects.fetch_by_theme_id(theme)

    if post_comment_form.is_valid():

        # ユーザーがログインしていなかったら404エラーを出す
        if not request.user.is_authenticated:
            raise Http404
        # 取得したテーマ・ユーザーの情報をインスタンスにセットする
        post_comment_form.instance.theme = theme
        post_comment_form.instance.user = request.user

        post_comment_form.save()

        # コメントを保存したので、キャッシュを削除する
        cache.delete(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}')

        return redirect('boards:post_comments', theme_id=theme_id)
    return render(
        request, 'boards/post_comments.html', context={
            'post_comment_form': post_comment_form,
            'theme': theme,
            'comments': comments,
        }
    )


def save_comment(request):
    if request.is_ajax:
        comment = request.GET.get('comment')
        theme_id = request.GET.get('theme_id')

        # コメントの一時保存。第１引数をキーに、第２引数をキャッシュに格納する
        if comment and theme_id:
            cache.set(
                f'saved_comment-theme_id={theme_id}-user_id={request.user.id}',
                comment
            )
            # JavaScriptのalert(json.message)でメッセージを表示
            return JsonResponse({'message': '一時保存しました'})
