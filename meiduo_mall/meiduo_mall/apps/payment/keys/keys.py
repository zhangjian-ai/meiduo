import os


def get_str(path):
    with open(path, 'r') as r:
        return str(r.read())


base_path = os.path.dirname(os.path.abspath(__file__))

app_private_key_string = get_str(os.path.join(base_path, 'app_private_key.pem'))
alipay_public_key_string = get_str(os.path.join(base_path, 'alipay_public_key.pem'))
