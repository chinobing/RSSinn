import psutil
import time
import signal
import os
from datetime import datetime


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
    return False;
def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
    listOfProcessObjects = []
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
    return listOfProcessObjects;


async def kill_child_processes(parent_pid, sig=signal.SIGTERM):
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        return
    children = parent.children(recursive=True)
    # print(children)
    for process in children:
        process.send_signal(sig)

        process.kill() #test needed
    parent.kill() #test needed

# def zombies_process_killer():
    # procObjList = [procObj for procObj in psutil.process_iter() if 'chrome' in procObj.name().lower()]
    # for elem in procObjList:
    #    print (elem)
    # kill_child_processes(os.getpid())
    # Find PIDs od all the running instances of process that contains 'chrome' in it's name
    # procObjList = [procObj for procObj in psutil.process_iter() if 'chrome' in procObj.name().lower() ]
    # for elem in procObjList:
    #    print (elem)

async def zombies_process_killer():
    print("*** Check if a process is running or not ***")
    # Check if any chrome process was running or not.
    if checkIfProcessRunning('chrome'):
        print('Yes a chrome process was running')
    else:
        print('No chrome process was running')
    # print("*** Find PIDs of a running process by Name ***")
    # Find PIDs od all the running instances of process that contains 'chrome' in it's name
    listOfProcessIds = findProcessIdByName('chrome')
    if len(listOfProcessIds) > 0:
       print('Process Exists | PID and other details are')
       for elem in listOfProcessIds:
           processID = elem['pid']
           processName = elem['name']
           processCreationTime =  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(elem['create_time']))
           create_time = datetime.strptime(processCreationTime, '%Y-%m-%d %H:%M:%S')
           now = datetime.now()
           delta = now - create_time
           if delta.seconds>=60:
               print(f'process_ID={processID}, process_Name={processName}, Created_Time {processCreationTime}, running for {delta.seconds} seconds. Process has been killed at {now}.')
               await kill_child_processes(processID)
    else :
       print('No Running Process found with given text')
    # print('** Find running process by name using List comprehension **')
    # # Find PIDs od all the running instances of process that contains 'chrome' in it's name
    # procObjList = [procObj for procObj in psutil.process_iter() if 'chrome' in procObj.name().lower() ]
    # for elem in procObjList:
    #    print (elem)
