from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse


# 文章分类
class Category(models.Model):
  # verbose_nam='分类'可以简写为'分类'
  name = models.CharField('分类',max_length=128)

  def __str__(self):
    return self.name
  
  # 后台管理展示定制
  class Meta:
    # 给模型起个中文名字
    verbose_name = '博客分类'
    # verbose_name的复数形式，默认在后面加上's'
    verbose_name_plural = verbose_name


# 标签
class Tag(models.Model):
  name = models.CharField('标签',max_length=128)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = '博客标签'
    verbose_name_plural = verbose_name


# 文章
class Entry(models.Model):
  title = models.CharField('文章标题',max_length=128)
  # 外键可以是一个模型类
  author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)
  img = models.ImageField(upload_to='blog_img',null=True,blank=True,verbose_name='博客配图')
  body = models.TextField('正文',)
  abstract = models.TextField('摘要',max_length=256,null=True,blank=True)
  # 外键也可以是一个模型名
  visiting = models.PositiveIntegerField('访问量',default=0)
  category = models.ManyToManyField('Category',verbose_name='博客分类')
  tags = models.ManyToManyField('Tag',verbose_name='标签')
  # auto_now_add：为添加时的时间，修改对象不会变动
  created_time = models.DateTimeField('创建时间',auto_now_add=True)
  # auto_now：添加或修改对象，会更新时间
  modifyed_time = models.DateTimeField('修改时间',auto_now=True)

  def __str__(self):
    return self.title
  
  # 获取详情页地址（自定义方法）
  def get_absolute_url(self):
    return reverse('blog:blog_detail',kwargs={'blog_id':self.id})

  # 更新访问量（自定义方法）
  def increase_visiting(self):
    self.visiting += 1
    # update_fields：要保存的字段
    self.save(update_fields=['visiting'])
      
  class Meta:
    ordering = ['-created_time']
    verbose_name = '博客正文'
    verbose_name_plural = verbose_name