"""一些支持方法，比如加密"""
import hashlib
from utils.log import logger
from zipfile import ZipFile

class EncryptError(Exception):
    pass


def sign(sign_dict, private_key=None, encrypt_way='MD5'):
    """传入待签名的字典，返回签名后字符串
    1.字典排序
    2.拼接，用&连接，最后拼接上私钥
    3.MD5加密"""
    dict_keys = sorted(sign_dict.keys())

    string = ''
    for key in dict_keys:
        if sign_dict[key] is None:
            pass
        else:
            string += '{0}={1}&'.format(key, sign_dict[key])
    string = string[0:len(string) - 1].replace(' ', '')

    return encrypt(string, salt=private_key, encrypt_way=encrypt_way)


def encrypt(string, salt='', encrypt_way='MD5'):
    u"""根据输入的string与加密盐，按照encrypt方式进行加密，并返回加密后的字符串"""
    string += salt
    if encrypt_way.upper() == 'MD5':
        hash_string = hashlib.md5()
    elif encrypt_way.upper() == 'SHA1':
        hash_string = hashlib.sha1()
    else:
        logger.exception(EncryptError('请输入正确的加密方式，目前仅支持 MD5 或 SHA1'))
        return False

    hash_string.update(string.encode())
    return hash_string.hexdigest()


def unzip(abs_file, ext_path):
    zip_file = ZipFile(abs_file)
    for name in zip_file.namelist():
        zip_file.extract(name, ext_path)
    zip_file.close()


if __name__ == '__main__':
    logger.info(encrypt('Crowd@ad123', '', 'MD5'))
    zjk = {'ZJK': 'YES', 'OK': '365  DAYS', 'WHO': 'EVERYONE', 'WHERE': 'SEA', 'DAYS': 'SOME', 'PASS': None}
    logger.info(sign(zjk, private_key='张'))

