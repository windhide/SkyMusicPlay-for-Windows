
from windhide.auto.auto_thread import HeartFireThread
from windhide.static.global_variable import GlobalVariable


def auto_click_fire():
    if GlobalVariable.auto_thread is not None:
        GlobalVariable.auto_thread.stop()
    GlobalVariable.auto_thread = HeartFireThread()
    GlobalVariable.auto_thread.daemon = True
    GlobalVariable.auto_thread.start()

def shutdown():
    GlobalVariable.auto_thread.stop()