import os
import psutil
import schedule
import time

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def startIfNotProcessRunning():
    if checkIfProcessRunning('practice-bscscan-worker-1'):
        print('practice-bscscan-worker-1 was running')
    else:
        os.startfile("D:\教程\youtube视频资料\Solidity教程\codes\python\practice\dist\practice-bscscan-worker-1.exe")

    if checkIfProcessRunning('practice-bscscan-worker-2'):
        print('practice-bscscan-worker-2 was running')
    else:
        os.startfile("D:\教程\youtube视频资料\Solidity教程\codes\python\practice\dist\practice-bscscan-worker-2.exe")


schedule.every(20).seconds.do(startIfNotProcessRunning)


while True:
    schedule.run_pending()
    time.sleep(1)

 