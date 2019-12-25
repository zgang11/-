# 引入path
from django.urls import path
from . import views

# 正在部署的应用的名称
app_name = 'article'

urlpatterns = [
    # 目前还没有urls
    path('article-list/', views.article_list, name='article_list'),
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    path('analyse-list/', views.analyse_list, name='analyse-list'),
    path('hot-topic/', views.hot_topic, name='hot-topic'),
    path('user-manage/', views.user_manage, name="user-manage"),
    path('about/', views.about, name="about")
]
