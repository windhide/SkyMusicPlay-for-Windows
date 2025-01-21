import builtins
import platform

from windhide.static.global_variable import GlobalVariable


# 重定向 print 到空函数

def sout_null():
    if GlobalVariable.isProd:
        builtins.print = lambda *args, **kwargs: None
    cpu_check()
    return None

def cpu_check():
    cpu_info = platform.processor()
    if "Intel" in cpu_info:
        GlobalVariable.cpu_type = 'Intel'
    elif "AMD" in cpu_info:
        GlobalVariable.cpu_type = 'AMD'