from django.contrib.syndication.views import Feed
from .models import Entry

# res格式: http://www.geekpark.net/rss

class LatestEntriesFeed(Feed):
	title = "smileboyi的博客"
	link = "/siteblogs/"
	description = "smileboyi的最新博客文章！"

	# 订阅的数据
	def items(self):
		return Entry.objects.order_by('-created_time')[:5]

	# 订阅的标题
	def item_title(self, item):
		return item.title

	# 订阅的表示
	def item_description(self, item):
		return item.abstract
