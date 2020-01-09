from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

# 导入 HttpResponse 模块
from django.http import HttpResponse
from .models import ArticlePost, DailyData
from django.db.models import Q
import time
import datetime


# 视图函数


def article_list(request):
    # 根据GET请求中查询条件
    # 返回不同排序的对象数组

    article_list = DailyData.objects.all().order_by('-total_views')
    order = 'total_views'
    paginator = Paginator(article_list, 10)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    # 需要传递给模板（templates）的对象

    # 数据传递
    day_0 = datetime.date.today()
    day_0_ = str(day_0).split('-')
    day_0_0 = day_0_[0] + '年' + day_0_[1] + '月' + day_0_[2] + '日'
    data_0 = DailyData.objects.filter(time_s=day_0_0).count()
    x = [str(day_0)]
    y = [data_0]
    for i in range(1, 7):
        name_1 = day_0 - datetime.timedelta(days=i)
        name_1_ = str(name_1).split('-')
        name_1_1 = name_1_[0] + '年' + name_1_[1] + '月' + name_1_[2] + '日'
        data = DailyData.objects.filter(time_s=name_1_1).count()
        x.insert(0, str(name_1))
        y.insert(0, data)

    # 折线图数据
    xAxis = x
    yAxis = y

    Topic = DailyData.objects.all().count()
    todayTopic = data_0

    context = {'articles': articles, 'order': order, 'xAxis': xAxis, 'yAxis': yAxis, 'Topic': Topic,
               'todayTopic': todayTopic}

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
    paginator = Paginator(article_list, 7)

    # 获取 url 中的页码
    page = request.GET.get('page')

    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)

    # 折线图数据后台获取
    # 当天
    day_0 = datetime.date.today()
    day_0_ = str(day_0).split('-')
    day_0_0 = day_0_[0] + '年' + day_0_[1] + '月' + day_0_[2] + '日'
    data_0_pos = DailyData.objects.filter(Q(neg_pos='1') & Q(time_s=day_0_0)).count()
    data_0_neg = DailyData.objects.filter(Q(neg_pos='-1') & Q(time_s=day_0_0)).count()
    # 前一天
    day_1 = day_0 - datetime.timedelta(days=1)
    day_1_ = str(day_1).split('-')
    day_1_1 = day_1_[0] + '年' + day_1_[1] + '月' + day_1_[2] + '日'
    data_1_pos = DailyData.objects.filter(Q(neg_pos='1') & Q(time_s=day_1_1)).count()
    data_1_neg = DailyData.objects.filter(Q(neg_pos='-1') & Q(time_s=day_1_1)).count()
    # 前两天
    day_2 = day_0 - datetime.timedelta(days=2)
    day_2_ = str(day_2).split('-')
    day_2_2 = day_2_[0] + '年' + day_2_[1] + '月' + day_2_[2] + '日'
    data_2_pos = DailyData.objects.filter(Q(neg_pos='1') & Q(time_s=day_2_2)).count()
    data_2_neg = DailyData.objects.filter(Q(neg_pos='-1') & Q(time_s=day_2_2)).count()
    # 前三天
    day_3 = day_0 - datetime.timedelta(days=3)
    day_3_ = str(day_3).split('-')
    day_3_3 = day_3_[0] + '年' + day_3_[1] + '月' + day_3_[2] + '日'
    data_3_pos = DailyData.objects.filter(Q(neg_pos='1') & Q(time_s=day_3_3)).count()
    data_3_neg = DailyData.objects.filter(Q(neg_pos='-1') & Q(time_s=day_3_3)).count()
    # 前四天
    day_4 = day_0 - datetime.timedelta(days=4)
    day_4_ = str(day_4).split('-')
    day_4_4 = day_4_[0] + '年' + day_4_[1] + '月' + day_4_[2] + '日'
    data_4_pos = DailyData.objects.filter(Q(neg_pos='1') & Q(time_s=day_4_4)).count()
    data_4_neg = DailyData.objects.filter(Q(neg_pos='-1') & Q(time_s=day_4_4)).count()
    # 前五天
    day_5 = day_0 - datetime.timedelta(days=5)
    day_5_ = str(day_5).split('-')
    day_5_5 = day_5_[0] + '年' + day_5_[1] + '月' + day_5_[2] + '日'
    data_5_pos = DailyData.objects.filter(Q(neg_pos='1') & Q(time_s=day_5_5)).count()
    data_5_neg = DailyData.objects.filter(Q(neg_pos='-1') & Q(time_s=day_5_5)).count()
    # 前六天
    day_6 = day_0 - datetime.timedelta(days=6)
    day_6_ = str(day_6).split('-')
    day_6_6 = day_6_[0] + '年' + day_6_[1] + '月' + day_6_[2] + '日'
    data_6_pos = DailyData.objects.filter(Q(neg_pos='1') & Q(time_s=day_6_6)).count()
    data_6_neg = DailyData.objects.filter(Q(neg_pos='-1') & Q(time_s=day_6_6)).count()

    xAxis = [str(day_6), str(day_5), str(day_4), str(day_3), str(day_2), str(day_1), str(day_0)]
    data_pos = [data_6_pos, data_5_pos, data_4_pos, data_3_pos, data_2_pos, data_1_pos, data_0_pos]
    data_neg = [data_6_neg, data_5_neg, data_4_neg, data_3_neg, data_2_neg, data_1_neg, data_0_neg]

    # 饼图数据后台获取
    companyNames = ['积极', '消极', '中立']
    articles = paginator.get_page(page)
    middle = DailyData.objects.filter(neg_pos='0').count()
    pos = DailyData.objects.filter(neg_pos='1').count()
    neg = DailyData.objects.filter(neg_pos='-1').count()
    series_data = [{'value': pos, 'name': '积极'}, {'value': neg, 'name': '消极'}, {'value': middle, 'name': '中立'}]
    # 需要传递给模板（templates）的对象
    context = {'articles': articles, "series_data": series_data, "companyNames": companyNames, 'xAxis': xAxis,
               'data_pos': data_pos, 'data_neg': data_neg}
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
