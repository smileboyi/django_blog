from django.shortcuts import render
from . import models
from django.db.models import Q

import markdown, pygments

# https://www.cnblogs.com/kongzhagen/p/6640975.html
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# Create your views here.

# 返回当前page页的数据，和一个实例paginator
def make_paginator(objects,page,num=3):
	paginator = Paginator(objects,num)
	try:
		object_list = paginator.page(page)
	except PageNotAnInteger:
		object_list = paginator.page(1)
	except EmptyPage:
		object_list = paginator.page(paginator.num_pages)
	
	return object_list,paginator



# 通过传入实例paginator和当前page页,返回一个自定义分页页码（字典）
def pagination_data(paginator, page):
	if paginator.num_pages == 1:
		# 如果无法分页
		return {}
	# 当前页左边连续的页码号，初始值为空
	left = []
	right = []

	# 标示第 1 页页码后是否需要显示省略号
	left_has_more = False
	right_has_more = False

	# 标示是否需要显示第 1 页的页码号。
	# 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
	# 其它情况下第一页的页码是始终需要显示的。
	# 初始值为 False
	first = False

	# 标示是否需要显示最后一页的页码号。
	# 需要此指示变量的理由和上面相同。
	last = False

	# 获得用户当前请求的页码号
	try:
		page_number = int(page)
	except ValueError:
		page_number = 1
	except:
		page_number = 1

	total_pages = paginator.num_pages
	page_range = paginator.page_range

	if page_number == 1:
		# 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
		# 此时只要获取当前页右边的连续页码号，
		# 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
		# 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
		right = page_range[page_number:page_number + 4]

		# 如果最右边的页码号比最后一页的页码号减去 1 还要小，
		# 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
		if right[-1] < total_pages - 1:
			right_has_more = True

		# 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
		# 所以需要显示最后一页的页码号，通过 last 来指示
		if right[-1] < total_pages:
			last = True

	elif page_number == total_pages:
		# 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
		# 此时只要获取当前页左边的连续页码号。
		# 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
		# 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
		left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

		# 如果最左边的页码号比第 2 页页码号还大，
		# 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
		if left[0] > 2:
			left_has_more = True

		# 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
		# 所以需要显示第一页的页码号，通过 first 来指示
		if left[0] > 1:
			first = True
	else:
		# 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
		# 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
		left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
		right = page_range[page_number:page_number + 2]

		# 是否需要显示最后一页和最后一页前的省略号
		if right[-1] < total_pages - 1:
			right_has_more = True
		if right[-1] < total_pages:
			last = True

		# 是否需要显示第 1 页和第 1 页后的省略号
		if left[0] > 2:
			left_has_more = True
		if left[0] > 1:
			first = True

	data = {
		'left': left,
		'right': right,
		'left_has_more': left_has_more,
		'right_has_more': right_has_more,
		'first': first,
		'last': last,
	}
	return data



def index(request):
	entries = models.Entry.objects.all()
	page = request.GET.get('page',1)
	entry_list, paginator = make_paginator(entries, page)
	page_data = pagination_data(paginator, page)

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



def catagory(request,category_id):
	c = models.Category.objects.get(id=category_id)
	entries = models.Entry.objects.filter(category=c)

	page = request.GET.get('page',1)
	entry_list, paginator = make_paginator(entries, page)
	page_data = pagination_data(paginator, page)

	# 和index()用到的模板是一样的
	return render(request, 'blog/index.html', locals())


def tag(request,tag_id):
	t = models.Tag.objects.get(id=tag_id)
	if t.name == "全部":
			entries = models.Entry.objects.all()
	else:
			entries = models.Entry.objects.filter(tags=t)
	page = request.GET.get('page', 1)
	entry_list, paginator = make_paginator(entries, page)
	page_data = pagination_data(paginator, page)

	return render(request, 'blog/index.html', locals())



def search(request):
	# 如果是post请求，需要在模板表单里加入csrf_token
	keyword = request.GET.get('keyword',None)
	if not keyword:
		error_msg = '请输入关键字'
		return render(request,'blog/index.html',locals())

	# 从标题、正文、摘要里面查找关键字，获取包含关键字的文章
	entries = models.Entry.objects.filter(Q(title__icontains=keyword)
																				| Q(body__icontains=keyword)
																				| Q(abstract__icontains=keyword))
	# 数据的显示和index()方式一致
	page = request.GET.get('page', 1)
	entry_list, paginator = make_paginator(entries, page)
	page_data = pagination_data(paginator, page)

	return render(request, 'blog/index.html', locals())