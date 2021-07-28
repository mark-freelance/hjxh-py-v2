import hashlib


def _encode_item(key: str, val: str) -> str:
    j = '-'.join([len(key).__format__('02d'), key])
    k = '-'.join([len(val).__format__('04d'), val])
    v = ':'.join([j, k])
    return v


def _encode_params(d: dict) -> str:
    return ';'.join(_encode_item(k, d[k]) for k in sorted(d))


def gen_md5(s: str) -> str:
    hl = hashlib.md5()
    hl.update(s.encode(encoding='utf-8'))
    s2 = hl.hexdigest()
    # print('MD5加密前为 ：' + s)
    # print('MD5加密后为 ：' + s2)
    return s2


def get_sign(d: dict, secret: str) -> str:
    a = _encode_params(d) + secret
    return gen_md5(a)
