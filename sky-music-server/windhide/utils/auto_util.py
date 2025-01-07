
from windhide._global import global_variable
from windhide.auto.auto_thread import HeartFireThread
from windhide.auto.candles_run import ControlThread

def auto_click_fire():
    if global_variable.auto_thread != None:
        global_variable.auto_thread.stop()
    global_variable.auto_thread = HeartFireThread()
    global_variable.auto_thread.daemon = True
    global_variable.auto_thread.start()

async def auto_candles_run(mapSelect, json):
    if global_variable.auto_thread != None:
        global_variable.auto_thread.stop()
    global_variable.auto_thread = ControlThread(mapSelect=mapSelect, json=json)
    global_variable.auto_thread.start()

def shutdown():
    global_variable.auto_thread.stop()