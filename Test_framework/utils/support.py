"""一些支持方法，比如簽名、加密"""
import hashlib
from utils.log import logger


class EncryptError(Exception):
    pass

# 簽名函數
def sign(sign_dict, private_key=None, encrypt_way='MD5'):
    """傳入待簽名的字典，返回簽名後字符串
    1.字典排序
    2.拼接，用&連接，最後拼接上私鑰
    3.MD5加密"""
    dict_keys = sign_dict.keys()
    dict_keys.sort()

    string = ''
    for key in dict_keys:
        if sign_dict[key] is None:
            pass
        else:
            string += '{0}={1}&'.format(key, sign_dict[key])
    string = string[0:len(string) - 1]
    string = string.replace(' ', '')

    return encrypt(string, salt=private_key, encrypt_way=encrypt_way)

# 加密函數
def encrypt(string, salt='', encrypt_way='MD5'):
    u"""根據輸入的string與加密鹽，按照encrypt方式進行加密，並返回加密後的字符串"""
    string += salt
    if encrypt_way.upper() == 'MD5':
        hash_string = hashlib.md5()
    elif encrypt_way.upper() == 'SHA1':
        hash_string = hashlib.sha1()
    else:
        logger.exception(EncryptError('請輸入正確的加密方式，目前僅支持 MD5 或 SHA1'))
        return False

    hash_string.update(string.encode())
    return hash_string.hexdigest()

if __name__ == '__main__':
    print(encrypt('100000307111111'))