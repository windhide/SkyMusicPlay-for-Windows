
from windhide.auto.auto_thread import HeartFireThread
from windhide.auto.candles_run import ControlThread
from windhide.static.global_variable import GlobalVariable


def auto_click_fire():
    if GlobalVariable.auto_thread is not None:
        GlobalVariable.auto_thread.stop()
    GlobalVariable.auto_thread = HeartFireThread()
    GlobalVariable.auto_thread.daemon = True
    GlobalVariable.auto_thread.start()

async def auto_candles_run(mapSelect, json):
    if GlobalVariable.auto_thread is not None:
        GlobalVariable.auto_thread.stop()
    GlobalVariable.auto_thread = ControlThread(mapSelect=mapSelect, json=json)
    GlobalVariable.auto_thread.start()

def shutdown():
    GlobalVariable.auto_thread.stop()