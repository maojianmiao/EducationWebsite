
项目：代号010

nginx
    开启nginx：start nginx
    重载nginx服务：nginx -s reload

host配置：
    127.0.0.1   video.lyl.com

页面设计：
    主色调：#00806E
    副色调：lightseagreen
    透明度为0.2的lightseagreen颜色：#d2f0ee
    可选背景色：lightgray、 gray

运行：

    sqlite的数据库路径是绝对路劲，从git下载代码后，需要修改models/__init__.py里的database_uri变量为功能根目录education.db对应的绝对路径。
    直接运行runserver.py文件，默认端口5000

各文件夹分类：

一、common——通用接口包

    1、api——通用函数模块

二、models——网站数据模型管理包

    使用SQLAlchemy 进行数据库操作。数据库为sqlite。因为 SQLAlchemy 是一个常用的数据库抽象层和数据库关系映射包(ORM)，如果需要使用其它数据库，只需要修改配置即可。

    1、__init__.py
        初始化数据库
    2、users.py
        用户信息表模型

三、static——静态文件存放文件夹

    1、css
    2、javascript文件
    3、images——通用图片

四、templates——模板存放文件夹

    目前为每个视图模块都创建了一个文件夹存放模板。比如views下有个叫index的视图模块，则这个视图里所用到的模板都对应存放在templates/index目录下

    1、index
        对应views/index.py视图模块里所用到的模板
    2、usercontrol
        对应views/usercontrol.py视图模块里所用到的模板
五、uploads——文件上传存放文件夹

    暂未用到

六、views——视图和地址管理模块包

    使用蓝图（Blueprint）分类管理功能不同的视图。
    1、index.py
        主视图模块，内容待完善
    2、usercontrol.py
        用户控制模块

七、其它

    1、tornado_server.py
        用tornado webserver部署flask，暂时用不着
    2、test_model.py
        模型测试脚本。

八、_decorator.py
    视图装饰器，主要控制视图展示的权限
