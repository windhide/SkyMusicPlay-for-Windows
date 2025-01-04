# 打包放行
import builtins
# 重定向 print 到空函数

def sout_null():
    builtins.print = lambda *args, **kwargs: None
    return None