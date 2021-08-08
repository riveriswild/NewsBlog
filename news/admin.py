from django.contrib import admin
from news.models import *

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Category)

# Register your models here.
