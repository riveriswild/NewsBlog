from django.urls import path
from news.views import NewsList, NewsDetail, PostSearch, PostCreate, PostDelete, PostUpdate, upgrade_me, \
    CategoryDetailView, subscribe, unsubscribe
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(NewsList.as_view()), name='posts'),
    path('<int:pk>', NewsDetail.as_view(), name='post'),
    path('search/', PostSearch.as_view(), name='search'),
    path('add/', PostCreate.as_view(), name='add'),
    path('create/<int:pk>', PostUpdate.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDelete.as_view(), name='post_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('category/<int:pk>', cache_page(60 * 5)(CategoryDetailView.as_view()), name='category'),
    path('subscribe/<int:pk>', subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe, name='unsubscribe')

]
