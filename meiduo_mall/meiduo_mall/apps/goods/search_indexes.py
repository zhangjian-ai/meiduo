from haystack import indexes

from .models import SKU


class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """
    SKU索引数据模型
    """

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        """重写并返回建立索引的模型类"""
        return SKU

    def index_queryset(self, using=None):
        """返回要建立索引的查询集"""
        return self.get_model().objects.filter(is_launched=True)
