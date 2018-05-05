# -*- coding: utf-8 -*-
# @Date    : 2018-02-13 23:20:15
# @Author  : linyuling
# @Version : $Id$
# @Notes   :

from models.__init__ import init_db,db_session
from models.users import users
from models.course import course
from models.comment import comment
from models.video import video
from models.video_record import video_record
from models.category import category, category_to_course
import urllib2
from models.note import note
#from change_email import change_email
import hashlib
#from moviepy.editor import VideoFileClip
from sqlalchemy import desc,asc,func
from models.user_to_course import user_to_course, collect
from models.course_rate import course_rate
from models.change_email import change_email
from common.api import to_mp4
from models.jitang import jitang
#import imageio
import glob
import re
import chardet
#imageio.plugins.ffmpeg.download()
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def hash_string(string):
    if not string:
        string = ""
    #sha1加密
    m = hashlib.sha1()
    m.update(string)
    #返回加密的16进制数
    return m.hexdigest()

def send_url(url):
    data = urllib2.urlopen(url).read()
    print data
    return data


def create_category():
    categorys = [u'文化艺术',
                 u'编程开发',
                 u'体育运动',
                 u'工业类',
                 u'语言学习',
                 u'通识教育',]

    for c in categorys:
        cate= category(c, 1)
        db_session.add(cate)


    db_session.commit()


def create_course():
    video_path = r'D:\web\5\*.mp4'
    course_name = u'Java入门教学'
    url_path = 'http://video.linyuling.com/5/'

    vs = glob.glob(video_path)

    c = course(course_name,user_id=1)
    db_session.add(c)
    for i, v in enumerate(vs):
        clip = VideoFileClip(v)
        du = int(clip.duration)
        print du
        path = url_path + v.split('\\')[-1]

        current_video = video(course_name + str(i), path, order=i+1,duration=du,course=c)
        
        db_session.add(current_video)

    db_session.commit()

def copy_course(cid, count):
    c = course.query.filter(course.status==1,course.id == cid).first()

    for i in xrange(2, count+2):
        copy_c = course(c.title, user_id=4, item_image=c.item_image)
        relation = category_to_course(course=copy_c,category_id_first=5)
        db_session.add(copy_c)
        db_session.add(relation)

    db_session.commit()

def parse(textpath):
    with open(textpath,'rb') as f:
        text = f.readlines()
        for line in text:
            if not re.match('\d.*',line):
                continue

            content = line.split('、')[1].strip()
            l = re.split('(-|——)', content)
            jitang_text = l[0].strip().strip('-').strip('——')
            author = l[-1].strip().strip('-').strip('——')
            
            print chardet.detect(jitang_text), chardet.detect(author)
            try:
                jitang_text = jitang_text.decode(chardet.detect(jitang_text)['encoding'])
                author = author.decode(chardet.detect(author)['encoding'])
            except Exception,e:
                print e
                print line
                print jitang_text
                print author
                print 'end of error'
                continue
            current = jitang(jitang_text, author)
            db_session.add(current)

    db_session.commit()
def add_category(name, pre_id=None):
    #上一级分类的在category表里的id，如果是最大分类，则pre_id=None
    pre = category.query.filter(category.id == pre_id).first()

    c = category(name, level=pre.level + 1, pre_category_id=pre_id)
    db_session.add(c)

def op_add_category():
    #文化艺术
    cs = [u'绘画',u'声乐',u'乐器',u'书法']
    #体育运动
    pes = [u'足球',u'羽毛球',u'游泳',u'田径',u'篮球',u'乒乓球']
    #生活方式
    life = [u'烹饪',u'按摩',u'绿植',u'情绪管理',]
    #职业发展
    work = [u'项目管理',u'市场营销',u'职业考试',u'时间管理',]
    #语言学习
    lang = [u'英语',u'法语',u'潮州话',u'粤语',u'手语']
    for i in cs:
        add_category(i,1)
    for i in pes:
        add_category(i,3)
    for i in life:
        add_category(i,4)
    for i in work:
        add_category(i,6)
    for i in lang:
        add_category(i,5)


#如果无数据库和表则创建数据和数据表，否则不影响现有库和表。
if __name__ == "__main__":
    #创建数据库和表
    init_db()
    user_email = "010@linyuling.com"
    user = users.query.filter(users.email == user_email).first()
    #user = users(email="admin22@linyuling.com",password=hash_string("123123"),name="admin22")
    #user = change_email.query.filter(change_email.is_available=='1').order_by(desc(change_email.id)).first()
    #current = users.query.filter(users.id==1).first()
    #current.name = 'adminaa'
    #print user
    #user.is_activated = 3
    #db_session.commit()
    #print user.query.all()
    #email = change_email(email=user_email,users_id=2)
    #db_session.add(user)
    #db_session.add(email)
    #db_session.commit()
    #print email.query.all()
    #u  = users('admin', 'adminaa@localhost')
    #print users.__table__
    #c = course(user,u"老中医按摩系列")
    #v = video(u'第二课：老中医教你做肩颈按摩','http://video.linyuling.com/game.mp4',course=c)
    
    #for i in range(100):
    #    cm = note(u"于铃同学，节日快乐{}".format(i),users=user,course_id=3,video_position="00:50")
    #    db_session.add(cm)
    for i in range(0):
        title = u"惊起却回头{}".format(i)
        cm = comment(users=user,course_id=3,comment=title)
        db_session.add(cm)

    #parse('jitang.txt')

    #text = u'我们一定要给自己提出这样的任务，第一，学习，第二，学习，第三还是学习'
    #j = jitang(text, u'列宁')
    #db_session.add(j)
    #rate = course_rate(8.5, u"不错的一门课程", 2, 8)
    #op_add_category()
    #db_session.add(rate)
    #sql_order_query = video.query.filter(video.course_id == 20)
    #print sql_order_query
    #sql_order = sql_order_query.order_by(desc(video.id)).first()
    #db_session.commit()
    #rates = course_rate.query.filter(course_rate.course_id == 8)\
    #.order_by(desc(course_rate.create_date)).slice(0, 5).all()
    #print rates
    #count = db_session.query(func.count(course.id)).first()[0]
    db_session.commit()
    #print count

    #item = u'Shell'
    #c = category(item,level=3,pre_category_id=7)
    #categorys = category.query.filter(category.level=='1').all()
    #print len(categorys)
    #print categorys
    #courses = course.query.join(category_to_course,course.id == category_to_course.course_id).\
        #filter(category_to_course.category_id_first== 2).slice(0,8).all()
    #print len(courses)
    #copy_course(8,10)
    #for i in [2,3,4,5]:
    #    relation = category_to_course(8, i)
    #    db_session.add(relation)
    #db_session.commit()
    #create_course()
    #create_category()
    #print users.query.all()
    
    #clip = VideoFileClip(r"C:\nginx-1.12.2\videos\game.mp4")
    #print(clip.duration )
    
