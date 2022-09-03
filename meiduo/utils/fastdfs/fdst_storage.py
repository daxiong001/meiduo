from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings


class FastDFSStorage(Storage):
    """自定义文件存储系统类"""

    def __init__(self, client_path=None, base_url=None):
        self.client_path = client_path or settings.FDFS_CLIENT_CONF
        self.base_url = base_url or settings.FDFS_BASE_URL

    def _open(self, name, mode='rb'):
        """
        用来打开文件，自定义文件存储系统的目的为了实现存储到远程图片服务器，不需要打开文件，所以重写不做任何操作
        :param name:
        :param mode:
        :return:
        """
        pass

    def _save(self, name, content):
        """
        文件储存时什么调用次方法，但是此方法默认是存储到本地，再次方法做事先文件存储到远程的服务器
        :param name:
        :param content:
        :return: file_id
        """
        # 1、创建fastdfs客户端
        client = Fdfs_client(self.client_path)
        # 2、通过客户端调用上传文件的方法上传文件到服务器
        ret = client.upload_by_buffer(content.read())
        # 3、判断文件是否上传成功
        if ret.get("Status") != 'Upload successed.':
            raise Exception('Upload file failed')
        # 4、返回file_id
        file_id = ret.get('Remote file_id')
        return file_id

    def exists(self, name):
        """
        当要进行上传时嗲用此方法判断文件是否已上传，如果没有上传才会嗲用save方法进行上传
        :param name:
        :return: true表示已存在不需要上传
        """
        return False

    def url(self, name):
        """
        访问图片就会调用此方法获取图片文件的绝对路径
        :param name: 访问图片的file_id
        :return:完整的图片访问路径
        """
        return self.base_url + name
