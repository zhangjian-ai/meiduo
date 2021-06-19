from fdfs_client.client import Fdfs_client,get_tracker_conf


# 上传图片
path = get_tracker_conf('/Users/zhangjian/PycharmProjects/meiduo/meiduo_mall/meiduo_mall/utils/fastdfs/client.conf')
client = Fdfs_client(path)

ret = client.upload_by_filename('/Users/zhangjian/Documents/icon/4567.jpeg')

if __name__ == '__main__':
    print(ret)
    print(type(ret))
    print(type(ret.get('Remote file_id')))