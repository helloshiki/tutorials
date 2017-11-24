# 基本用法，必须弄懂

import functools


def original():
    session = None

    def get_status():
        return {"status": "status"}

    def get_status_with_login():
        if session["login"]:            # 登陆检查
            return get_status()
        return {"error": "offline"}

    def set_password(password):
        return {"status": "ok"}

    def set_password_with_login(password):
        if session["login"]:            # 登陆检查
            return set_password(password)
        return {"error": "offline"}

    session = {"login": True}
    r = get_status_with_login(); print(r)    # {'status': 'status'}

    session = {"login": False}
    r = get_status_with_login(); print(r)    # {'error': 'offline'}

    session = {"login": True}
    r = set_password_with_login("password"); print(r)    # {'status': 'ok'}

    session = {"login": False}
    r = set_password_with_login("password"); print(r)    # {'error': 'offline'}


def simple_decorator():
    session = None

    def login_required(f):
        # *args表示所有的非关键字参数， **kwargs表示所有的关键字参数
        def decorator(*args, **kwargs):
            if session["login"]:
                return f(*args, **kwargs)   # 真正的函数
            return {"error": "offline"}
        return decorator

    @login_required
    def get_status():
        return {"status": "status"}

    @login_required
    def set_password(password):
        return {"status": "ok"}

    session = {"login": True}
    r = get_status(); print(r)    # {'status': 'status'}

    session = {"login": False}
    r = get_status(); print(r)    # {'error': 'offline'}

    session = {"login": True}
    r = set_password("password"); print(r)    # {'status': 'ok'}

    session = {"login": False}
    r = set_password("password"); print(r)    # {'error': 'offline'}

    # 等价表示
    def get_status2():
        return {"status": "status"}

    def set_password2(password):
        return {"status": "ok"}

    # 相当于前面的
    # @login_required
    # def get_status
    get_status2 = login_required(get_status2)

    session = {"login": True}
    r = get_status2(); print(r)       # {'status': 'status'}

    session = {"login": False}
    r = get_status2(); print(r)       # {'error': 'offline'}


def simple_decorator_with_wraps():
    def without_wraps():
        def login_required(f):
            def decorator(*args, **kwargs):
                pass
            return decorator

        @login_required
        def get_status(session):
            pass

        print(get_status.__name__)      # decorator

    def with_wraps():
        def login_required(f):
            @functools.wraps(f)  # 隐藏装饰器 *********
            def decorator(*args, **kwargs):
                pass
            return decorator

        @login_required
        def get_status(session):
            pass

        print(get_status.__name__)      # get_status

    without_wraps()
    with_wraps()


if __name__ == "__main__":
    # original()
    # simple_decorator()
    simple_decorator_with_wraps()
