# -*- coding: utf-8 -*-
# @Date    : 2018-02-21 17:45:31
# @Author  : linyuling
# @Version : $Id$
# @Notes   :


from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64
import logging
#生成公钥和私钥
def generate_keys():
    #伪随机书生成器
    generator = Random.new().read
    #rsa算法对象
    rsa = RSA.generate(1024, generator)

    private_key = rsa.exportKey()
    publick_key = rsa.publickey().exportKey()

    print private_key
    print 
    print publick_key

#加密：对字符串先进行RSA加密，再进行base64加密
def encrypt_string(string):
    rsakey = RSA.importKey(publick_key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    text = cipher.encrypt(string)
    text = base64.urlsafe_b64encode(text)
    logging.info('encrypt:',text)
    return text
#解密：对加密字符串先进行base64解密，再进行RSA解密
def decrypt_string(string):
    rsakey = RSA.importKey(private_key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    text = base64.urlsafe_b64decode(string)
    text =cipher.decrypt(text,"ERROR")
    logging.info('decrypt:',text)
    return text

private_key = """-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgQCYSuiTFcR2c/GbBCW+aMR1x6avvN6+I7V9i6hPsOZdMImtZOG9
u849siJGUO5tCjV93Niz8ig1+n39TCjm0AMR9WUn44sqEpwPb2jV/rroiNR7+GgW
iceVuK7KGvwOdqdSg4Lb7Qzw71hrYpjGk2scRWy8yl/mo/UNYolnZXBntQIDAQAB
AoGASlBjZUK9979kKmy/rkaZd4/ROvhDCS2LppO7sgd0ogzJYh9UOK2oWlrOdtmP
Pw44RA68gDKuhIiTakL7woXGuP/4AqKRZ/kkvlHlu3poL1Ve4vxcz8fWRW4GOL3Q
AOGMWoUe2RRVI54S1UcSB5VrvkMMqE3B9GWJqCD7osGn5AECQQDCUbaFSN5x/ekd
fV9XHsZ/t4vEww/yjU7Y3Rhhxk+HuX2MwujSZixzEBExoCJnm7QA9HN8250KqMqm
bi2z1N71AkEAyKIinD/XcDrT8YHRhsKTNsF8fMerlaycNIv/HZYzWH03iqva/+Wf
imp1dQTyn+Nbuav4yP/2q8n9bB9LQy5twQJAWzLKfMd0Tv+h9ssugc7ZznswR8pc
o7OaO8GYfdr63HI78GJRrt1xIxd5WlcTjpjO5FvWD9VqYORTJ8UyAeJ4OQJAGssM
NDGSY7p3c1kS0hxJ7JYKOd+wWlyiv6GygBD+6mJOeIZayLGxjJqK9QWkIRYLuc/t
eWo1VtuyrC3Br0cUAQJAPD7jDSE5anYHWp4vY9bjuRcZWOzd0poihg3MbiVYdkiK
uDHo+8Y54GydtYLtuxEhpkhQH5uNaVm/FN0NgFY7dA==
-----END RSA PRIVATE KEY-----"""

publick_key = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCYSuiTFcR2c/GbBCW+aMR1x6av
vN6+I7V9i6hPsOZdMImtZOG9u849siJGUO5tCjV93Niz8ig1+n39TCjm0AMR9WUn
44sqEpwPb2jV/rroiNR7+GgWiceVuK7KGvwOdqdSg4Lb7Qzw71hrYpjGk2scRWy8
yl/mo/UNYolnZXBntQIDAQAB
-----END PUBLIC KEY-----"""

if __name__ == "__main__":
    s = b"Hello Wrold"
    #a = encryptString(s)
    b = decrypt_string('c_vg8YWLCbbGNZgwSCvFQ-JqOmv3LGHytubItdHSurxQBZjJCPOJE-GwqPuX2QxoUasbFdxOYlJnRrTGxTuI4HHaOjdyrdhTxUXMVvkIUh3pws2_VQ7NYXSUieCKRGzdSLqfKwxFjlZxATD6FRiFzTgtKIl6jrJFNzwRDe5UCUk=')
    print b