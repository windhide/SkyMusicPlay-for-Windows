# 打包放行
import builtins

from windhide._global.global_variable import isProd


# 重定向 print 到空函数

def sout_null():
    if isProd:
        builtins.print = lambda *args, **kwargs: None
    return None
