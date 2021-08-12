from django.contrib import admin
from news.models import *

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'dateCreation')  # оставляем только имя и цену товара
    list_filter = ('author', 'dateCreation')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'author', 'dateCreation')  # тут всё очень похоже на фильтры из запросов в базу

admin.site.register(Post, NewsAdmin)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Category)

# Register your models here.
