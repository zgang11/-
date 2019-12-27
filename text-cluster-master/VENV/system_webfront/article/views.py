from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

# 导入 HttpResponse 模块
from django.http import HttpResponse
from .models import ArticlePost


# 视图函数


def article_list(request):
    ## 取出所有博客文章
    # articles = ArticlePost.objects.all()

    ## render函数：载入模板，并返回context对象

    article_list = ArticlePost.objects.all()

    # 每页显示2篇文章
    paginator = Paginator(article_list, 5)

    # 获取 url 中的页码
    page = request.GET.get('page')

    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {'articles': articles}

    return render(request, 'article/list.html', context)


# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    # 需要传递给模板的对象
    context = {'article': article}
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)


# 情感分析
def analyse_list(request):
    article_list = ArticlePost.objects.all()

    # 每页显示2篇文章
    paginator = Paginator(article_list, 5)

    # 获取 url 中的页码
    page = request.GET.get('page')

    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {'articles': articles}
    return render(request, 'article/scencetence_analyse.html', context)


# 热点话题
def hot_topic(request):
    article_list = ArticlePost.objects.all()

    # 每页显示5篇文章
    paginator = Paginator(article_list, 5)

    # 获取 url 中的页码
    page = request.GET.get('page')

    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {'articles': articles}

    return render(request, 'article/hot_topic.html', context)


# 用户管理
def user_manage(request):
    return render(request, 'article/user_manage.html')


# 关于
def about(request):
    return render(request, 'article/about.html')
