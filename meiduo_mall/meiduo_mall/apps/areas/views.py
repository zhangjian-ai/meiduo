from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .models import Area
from .serializers import AreaSerializer, SubsAreaSerializer


class AreasViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """查询地址，就是查询所有和查询单一。这里继承视图集，其父类已经帮我们实现两种查询方法
    同时也是严格按照restful风格编写的。查所有/areas  ;查单一 /areas/(?P<id>\d+)
pip    """

    # 由于我们将查所有和查单一的序列化器和模型对象不一样，所以我们重写以下方法作为判断

    # GenericAPIView get_queryset  负责返回查询集
    def get_queryset(self):
        if self.action == 'list':
            return Area.objects.filter(parent=None)
        else:
            return Area.objects.all()

    # GenericAPIView get_serializer_class  负责返回序列化器类，指明视图使用的序列化器
    def get_serializer_class(self):
        if self.action == 'list':
            return AreaSerializer
        else:
            return SubsAreaSerializer
