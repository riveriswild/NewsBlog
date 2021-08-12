from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, User, Comment, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
import logging


logger = logging.getLogger(__name__)


class NewsList(ListView):
    model = Post  # модель, объекты которой выводим
    template_name = 'posts.html'  # шаблон html
    context_object_name = 'posts'  # список со всеми объектами для образения через html
    ordering = ['-dateCreation']
    paginate_by = 4

    def get_context_data(self, *args,
                         **kwargs):  # метод для передачи переменных в шаблон, context - это словарь, ключи - переменные
        context = {**super().get_context_data(*args, **kwargs),
                   'categories': Category.objects.all(),
                   'is_not_author': not self.request.user.groups.filter(name='authors').exists()
                   }
        # заходим в
        # переменную запроса селф.реквест, вытасикваем текущего пользователя, через groups фильтруем по группе
        # авторы, проверяем есть ли он там
        return context

    def get_queryset(self):
        category_pk = self.request.GET.get('pk')  # тут еще возможно None надо
        if category_pk:
            return Post.objects.filter(postCategory__pk=category_pk).order_by('-dateCreation')
        return Post.objects.order_by('-dateCreation')


@login_required()
def upgrade_me(request):
    user = request.user  # получили объект текущего пользователя из переменной запроса
    authors_group = Group.objects.get(name='authors')  # вытаскиваем группу авторы из модели групп
    if not request.user.groups.filter(name='authors').exists():  # проверяем, находится ли пользователь в этой группе
        authors_group.user_set.add(user)  # добавляем
    return redirect('/posts/')  # перенаправляем на корневую стр сайта


# отдельный пост
class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = {**super().get_context_data(*args, **kwargs)}
        instance = self.get_object()
        id = self.kwargs.get('pk')  # это для категорий
        context['comments'] = instance.comment_set.all().order_by('dateCreation')
        context['categories'] = Post.objects.get(pk=id).postCategory.all()
        a = 'Категории: '
        for i in Post.objects.get(pk=id).postCategory.all().values('name'):
            a += (i['name'] + ' ')
        context['categories'] = a
        return context

    def get_object(self, *args, **kwargs):   # кэширование
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj


class PostSearch(ListView):
    model = Post  # модель, объекты которой выводим
    template_name = 'search.html'  # шаблон html
    context_object_name = 'posts'  # список со всеми объектами для образения через html
    ordering = ['-dateCreation']
    paginate_by = 4  # пагинация не работает из-за фильтра, попытаться поправить

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args,
                         **kwargs):  # метод для передачи переменных в шаблон, context - это словарь, ключи - переменные
        context = {
            **super().get_context_data(*args, **kwargs),  # получаем существующий контекст
            'filter': self.get_filter(),  # это для фильтра по постам
        }
        # context['time_now'] = datetime.utcnow()  # пока не в шаблоне
        return context


# создание поста
class PostCreate(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = ('news.add_post')
    template_name = 'post_create.html'
    form_class = PostForm


class PostUpdate(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = ('news.change_post')
    template_name = 'post_create.html'
    form_class = PostForm

    def get_object(self,
                   **kwargs):  # вместо queryset для получения инф об объекте, который редактируем: анные, которые
        # уже хранятся в товаре, будут взяты из метода get_object и заранее подставлены в формы.
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = ('news.delete_post')
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'


class CategoryDetailView(DetailView):
    template_name = 'category_detail.html'
    queryset = Category.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = {**super().get_context_data(*args, **kwargs)}
        instance = self.get_object()
        context['posts'] = instance.post_set.all().order_by('dateCreation')
        return context

@login_required()
def subscribe(request, **kwargs):
    pk = kwargs.get('pk')
    category = Category.objects.get(id=pk)
    if request.user not in category.subscribers.all():
        category.subscribers.add(request.user)
    return redirect('/posts/')

@login_required()
def unsubscribe(request, **kwargs):
    pk = kwargs.get('pk')
    category = Category.objects.get(id=pk)
    category.subscribers.remove(request.user)
    return redirect('/posts/')

# Create your views here.
