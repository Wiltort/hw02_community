from django.shortcuts import render, get_object_or_404, redirect
#from django.http import HttpResponse
from .models import Post, Group
from django.views.generic.edit import CreateView
from .forms import PostForm
#from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


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
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    return render(request, "group.html", {"group": group, "posts": posts})

#class new(CreateView):
#   template_name = 'new.html'
#    form_class = NewPostForm
 #   success_url = reverse_lazy('index')

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
    return render(request, 'new.html', {'form':form})