# Create your models here.
from django.db import models
# 导入内建的User模型。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone


class ArticlePost(models.Model):
    # 文章作者。参数 on_delete 用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)

    # 文章正文。保存大量文本使用 TextField
    body = models.TextField(max_length=10000, default='abc')

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将文章标题返回
        return self.title


class DailyData(models.Model):

    # 标题 参数 on_delete 用于指定数据删除的方式
    title = models.CharField(max_length=200)

    # article 参数 on_delete 用于指定数据删除的方式
    article = models.TextField()

    # article 参数 on_delete 用于指定数据删除的方式
    editor = models.CharField(max_length=100)

    # newssource 参数 on_delete 用于指定数据删除的方式
    newssource = models.CharField(max_length=100)

    # commentCount 参数 on_delete 用于指定数据删除的方式
    commentCount = models.CharField(max_length=100)

    # time 参数 on_delete 用于指定数据删除的方式
    time = models.CharField(max_length=100)

    # neg_pos 参数 on_delete 用于指定数据删除的方式
    neg_pos = models.CharField(max_length=100)

    # tags 参数 on_delete 用于指定数据删除的方式
    tags = models.CharField(max_length=100)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-time',)


    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将文章标题返回
        return self.title
