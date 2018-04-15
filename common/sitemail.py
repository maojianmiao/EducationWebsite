# -*- coding: utf-8 -*-
# @Date    : 2018-02-15 00:18:31
# @Author  : linyuling
# @Version : $Id$
# @Notes   :


import smtplib
from email.mime.text import MIMEText
import logging


class sitemail(object):

    def __init__(self):
        self.msg_from = 'flaskadmin010@163.com'     #发送方邮件
        self.passwd = 'flaskadmin010'   #授权码
        #授权码和密码不是一个。密码：010010
        self.smtpserver = "smtp.163.com"
        self.timeout = 20       #登录超时时间

    def mail_server(self):
        try:
            self.s = smtplib.SMTP_SSL(self.smtpserver,465,self.timeout)
            self.s.login(self.msg_from, self.passwd)
            return True
        except Exception,e:
            logging.error(e)
            logging.critical(u'不能登录邮箱服务器！')
            return False

    def send(self,msg_to,title,content):
        msg = MIMEText(content)
        msg['Subject'] = title
        msg['From'] = self.msg_from
        msg['To'] = msg_to

        try:
            self.s.sendmail(self.msg_from,msg_to,msg.as_string())
            logging.info(u"发送成功")
            return True
        except Exception,e:
            logging.critical(u"发送失败")
            logging.critical(e)
            return False
    
    def quit(self):
        self.s.quit()

if __name__ == "__main__":
    m = sitemail()
    m.mail_server()
    m.send('396679681@qq.com','test','你好')
    m.quit