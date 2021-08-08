from django.forms import ModelForm, CheckboxSelectMultiple
from news.models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


# форма добавления нового поста
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'postCategory', 'text']
        labels = {'author': 'Автор',
                  'title': 'Заголовок',
                  'postCategory': 'Категория',
                  'text': 'Текст',
                  }
        widgets = {'postCategory': CheckboxSelectMultiple}


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)  # вызываем этот же метод класса-родителя, чтобы
        # необходимые проверки и сохранение в модель User были выполнены
        basic_group = Group.objects.get(name='basic')  # получаем объект модели группы basic
        basic_group.user_set.add(user)  # через атрибут user_set, возвращающий список всех пользователей этой группы,
        # добавляем нового пользователя в эту группу
        return user  # требованием метода save() является возвращение объекта модели User по итогу выполнения функции.
