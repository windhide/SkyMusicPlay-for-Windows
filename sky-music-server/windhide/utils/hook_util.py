import builtins
import platform

from windhide._global import global_variable
from windhide._global.global_variable import isProd


# 重定向 print 到空函数

def sout_null():
    if isProd:
        builtins.print = lambda *args, **kwargs: None
    cpu_check()
    return None

def cpu_check():
    cpu_info = platform.processor()
    if "Intel" in cpu_info:
        global_variable.cpu_type = 'Intel'
    elif "AMD" in cpu_info:
        global_variable.cpu_type = 'AMD'