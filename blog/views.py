from django.shortcuts import render
from . import models

import markdown, pygments

# Create your views here.

def index(request):
	entries = models.Entry.objects.all()
	# locals()返回一个包含当前作用域里面的所有变量和它们的值的字典
	return render(request,'blog/index.html',locals())


def detail(request,blog_id):
	entry = models.Entry.objects.get(id=blog_id)
	entry.increase_visiting()

	md = markdown.Markdown(extensions=[
		'markdown.extensions.extra',
		'markdown.extensions.codehilite',
		'markdown.extensions.toc',
	])
	entry.body = md.convert(entry.body)
	entry.toc = md.toc

	return render(request,'blog/detail.html',locals())