from django.shortcuts import render, get_object_or_404, redirect
#from django.http import HttpResponse
from .models import Post, Group
#from django.views.generic.edit import CreateView
from .forms import PostForm
#from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

User = get_user_model()

def index(request):
    #запрос к БД сортировка по убыванию и вывод всех
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list,10)
    #Разбиваем паджинатором по 10 постов
    page_number = request.GET.get('page')
    # variable in url with number of page
    page = paginator.get_page(page_number)
    return render(
        request,
        "index.html",
        {'page': page, 'paginator': paginator}
        )

def group_posts(request, slug):
    # функция get_object_or_404 получает по заданным критериям объект из базы данных 
    # или возвращает сообщение об ошибке, если объект не найден
    group = get_object_or_404(Group, slug=slug)

    # Метод .filter позволяет ограничить поиск по критериям. Это аналог добавления
    # условия WHERE group_id = {group_id}
    posts = Post.objects.filter(group=group).order_by("-pub_date").all()
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "group.html", 
        {"group": group, "page": page, 'paginator': paginator}
        )

@login_required()
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            return redirect('index')
        return render(request, 'new.html', {'form':form})
    form = PostForm()
    return render(request, 'new.html', {'form':form, 'Edit': False})

def profile(request, username):
        # тут тело функци
        Author = get_object_or_404(User, username = username)
        post_list = Post.objects.filter(author = Author).order_by('-pub_date').all()
        post_num = post_list.count()
        paginator = Paginator(post_list,10)
        #Разбиваем паджинатором по 10 постов
        page_number = request.GET.get('page')
        # variable in url with number of page
        page = paginator.get_page(page_number)
        return render(
            request,
            'profile.html',
            {'Author':Author, 'page': page, 'paginator': paginator, 'post_num':post_num}
            )
 
 
def post_view(request, username, post_id):
        # тут тело функции
        Author = get_object_or_404(User, username = username)
        post_list = Post.objects.filter(author = Author).order_by('-pub_date').all()
        post_num = post_list.count()
        p = get_object_or_404(post_list, id = post_id)
        return render(
            request,
            'post.html',
            {'Author':Author, 'post': p, 'post_num':post_num}
            )
        

@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    #form = PostForm(instance = post, initial=[{'group': 'post.group', 'text':'hjshdjshdsjhdsdhsjhjsh'}])
    if request.user != post.author:
         redirect('post', username= username, post_id = post_id)
         #raise PermissionError("Вы не можете редактировать этот пост")
        # тут тело функции. Не забудьте проверить, 
        # что текущий пользователь — это автор записи.
        # В качестве шаблона страницы редактирования укажите шаблон создания новой записи
        # который вы создали раньше (вы могли назвать шаблон иначе)
    if (request.method == 'POST'):
        form = PostForm(request.POST, instance = post)
               
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            return redirect('post', username= username, post_id = post_id)
        return render(request, 'new.html', {'form':form, 'Edit': True, 'post':post})
    form = PostForm(instance=post)
    return render(request, 'new.html', {'form':form, 'Edit': True, 'post': post})
