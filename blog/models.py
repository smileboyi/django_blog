from django.db import models
from django.contrib.auth.models import User


# 文章分类
class Category(models.Model):
  name = models.CharField('分类',max_length=128)

  def __str__(self):
    return self.name
  
  class Meta:
    verbose_name = '博客分类'
    verbose_name_plural = verbose_name

