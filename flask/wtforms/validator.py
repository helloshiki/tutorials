"""
账号
密码
电话
UUID
日期
时间
IP
MAC
页数
URL
可选
电子邮件
字符串
数字范围
正则表达式
AnyOf
NoneOf
自定义validator
"""

from wtforms import *
from wtforms.validators import *

def test_userinfo():
    import datetime

    # 自定义验证器
    def birthday_check(form, field):
        date = datetime.datetime.strptime(field.data,'%Y-%m-%d')
        if datetime.date(1970, 1, 1) < date.date() < datetime.date(2050, 12, 31):
            return
        raise ValidationError("Invalid birthday")

    class TestForm(Form):
        username = StringField("Username", [Regexp("^(\w{4,64})$", message="Invalid Username")])
        password = StringField("Password", [Regexp("^(\w{4,64})$", message="Invalid Password")])
        sex = StringField("Sex", [AnyOf(["M", "F"], message="Invalid Sex")])
        age = IntegerField("Age", [NumberRange(0, 100, message="Invalid Age")])
        birthday = DateField("Birthday", [DataRequired(), birthday_check])
        phone = StringField("Phone", [Regexp('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}', message="Invalid Phone")])
        email = StringField("Email", [Email(message="Invalid Email")])
        headimg = StringField("HeadImg", [URL(message="Invalid HeadImg")])

    form = TestForm(**{
        "username":"hello",
        "password":"password",
        "sex":"M",
        "age":22,
        "birthday":"2010-11-09",
        "phone":"15914180656",
        "email":"329365307@qq.com",
        "headimg":"http://www.iplaypy.com/code/mobile/m5745.jpg"
    })
    assert form.validate(), form.errors
    print(form.data)


def test_ip_mac():
    class TestForm(Form):
        ip = StringField("Ip", [IPAddress(message="Invalid Ip")])
        mac = StringField("Mac", [MacAddress()])
    form = TestForm(**{
        "ip":"0.0.0.0",
        "mac":"00:e0:4c:68:20:8"
    })

    assert form.validate(), form.errors
    print(form.data)


def test_other():
    class TestForm(Form):
        uuid = StringField("UUID", [UUID()])
    form = TestForm(**{
        "uuid":'6c84fb90-12c4-11e1-840d-7b25c5ee775a',
    })
    assert form.validate(), form.errors
    print(form.data)


if __name__ == "__main__":
    # test_userinfo()
    # test_ip_mac()
    test_other()

# http://flask123.sinaapp.com/article/60/
# http://wtforms.readthedocs.io/en/latest/
# https://flask-wtf.readthedocs.io/en/stable/
