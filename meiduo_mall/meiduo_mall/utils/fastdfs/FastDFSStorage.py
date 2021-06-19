from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from fdfs_client.client import Fdfs_client, get_tracker_conf


@deconstructible
class FastDFSStorage(Storage):
    """自定义文件存储类"""

    def __init__(self, base_url=None, client_conf=None):
        """
        初始化
        :param base_url: 用于构造图片完整路径使用，图片服务器的域名
        :param client_conf: FastDFS客户端配置文件的路径
        """
        if base_url is None:
            base_url = settings.FDFS_URL
        self.base_url = base_url
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf

    def _open(self, name, mode='rb'):
        """
        用不到打开文件，所以省略。js传入后端的文件就是流文件
        """
        pass

    def _save(self, name, content):
        """
        在FastDFS中保存文件
        :param name: 传入的文件名
        :param content: 文件内容
        :return: 保存到数据库中的FastDFS的文件名
        """
        client = Fdfs_client(get_tracker_conf(self.client_conf))
        # client.upload_by_filename 该上方法传入的是绝对路径的文件，在storage保存的文件是带有文件后缀名的
        # upload_by_buffer传入的是content二进制文件，在storage保存后没有后缀名
        ret = client.upload_by_buffer(content.read())
        if ret.get("Status") != "Upload successed.":
            raise Exception("upload file failed")
        file_id = ret.get("Remote file_id")
        # python3中返回的file_id是bytes类型，返回是解码成str
        return file_id.decode()

    def url(self, name):
        """
        返回文件的完整URL路径
        :param name: 数据库中保存的文件名.也就是_save()方法返回的file_id
        :return: 完整的URL
        """
        return self.base_url + name

    def exists(self, name):
        """
        判断文件是否存在，FastDFS可以自行解决文件的重名问题
        所以此处返回False，告诉Django上传的都是新文件
        :param name:  文件名
        :return: False
        """
        return False
