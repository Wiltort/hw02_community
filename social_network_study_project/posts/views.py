from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse
from .models import Post, Group

def index(request):
    #запрос к БД сортировка по убыванию и вывод первых 10
    latest = Post.objects.order_by('-pub_date')[:10]
    #собираем тексты постов в один, разделяя новой строкой
    return render(request,"index.html",{"posts": latest})

def group_posts(request, slug):
    # функция get_object_or_404 получает по заданным критериям объект из базы данных 
    # или возвращает сообщение об ошибке, если объект не найден
    group = get_object_or_404(Group, slug=slug)

    # Метод .filter позволяет ограничить поиск по критериям. Это аналог добавления
    # условия WHERE group_id = {group_id}
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    return render(request, "group.html", {"group": group, "posts": posts})