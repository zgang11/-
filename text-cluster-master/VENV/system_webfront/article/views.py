from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

# 导入 HttpResponse 模块
from django.http import HttpResponse
from .models import ArticlePost, DailyData
from django.db.models import Q


# 视图函数


def article_list(request):
    # 根据GET请求中查询条件
    # 返回不同排序的对象数组
    if request.GET.get('order') == 'total_views':
        article_list = DailyData.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        article_list = DailyData.objects.all()
        order = 'normal'

    paginator = Paginator(article_list, 10)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {'articles': articles, 'order': order}

    return render(request, 'article/list.html', context)


# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    article = DailyData.objects.get(id=id)
    # 需要传递给模板的对象
    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    context = {'article': article}
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)


# 情感分析
def analyse_list(request):
    article_list = DailyData.objects.all()

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
    search = request.GET.get('search')
    order = request.GET.get('order')
    # 用户搜索逻辑
    if search:
        if order == 'total_views':
            # 用 Q对象 进行联合搜索
            article_list = DailyData.objects.filter(
                Q(title__icontains=search) |
                Q(article__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = DailyData.objects.filter(
                Q(title__icontains=search) |
                Q(article__icontains=search)
            )
    else:
        # 将 search 参数重置为空
        search = ''
        if order == 'total_views':
            article_list = DailyData.objects.all().order_by('-total_views')
        else:
            article_list = DailyData.objects.all()

    # 每页显示5篇文章
    paginator = Paginator(article_list, 10)

    # 获取 url 中的页码
    page = request.GET.get('page')

    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {'articles': articles, 'order': order, 'search': search}

    return render(request, 'article/hot_topic.html', context)


# 用户管理
def user_manage(request):
    return render(request, 'article/user_manage.html')


# 关于
def about(request):
    return render(request, 'article/about.html')
