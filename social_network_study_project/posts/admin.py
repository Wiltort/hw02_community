from django.contrib import admin
from .models import Post, Group
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ("text", "pub_date", "author", "group") 
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("text",) 
    # добавляем возможность фильтрации по дате
    list_filter = ("pub_date",) 

class GroupAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "description")

# при регистрации модели Post источником конфигурации для неё назначаем класс PostAdmin
admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)