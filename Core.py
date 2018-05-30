#! /usr/local/bin/python3
#This is the top level file which will execute all the things!

from Manager import Manager
from RPC import RPC
from Config import Config
import subprocess, time
from SysLog import Log

if __name__ == "__main__":
    Log = Log("Core")

    print("Starting System Logger...")
    API = subprocess.Popen(["python3","-OO","/usr/src/app/SysLog.py"]) #Bring up SysLogger in child process (-OO for full optimization)
    time.sleep(0.5) #Wait for logger process to be up
    Log.Log("Started Logger!")

    print("Starting System Manager...")
    Core = Manager() #Bring up System Core

    Log.Log("Loading Config")
    print("Loading Configuration...")
    Config = Config("/usr/src/app/config/config.json") #Load Config File

    Log.Log("Stating DBWriter")
    print("Starting DBWriter...")
    API = subprocess.Popen(["python3", "-OO", "/usr/src/app/DBWriter.py"]) #Bring up DBWriter in child process (-OO for full optimization)

    Log.Log("Setting Config")
    print("Setting Configuration...")
    Config.Set(Core) #Set configuration of Server. After this is called, All configured source drivers and tags should be running.

    Log.Log("Starting API")
    print("Starting API Server...")
    API = subprocess.Popen(["/usr/src/app/runAPI.sh"]) #Bring up restAPI in child process

    Log.Log("Starting RPC Loop")
    print("Starting RPC event loop...")
    RPC = RPC(Core, Config) #Instantiate RPC
    RPC.Run() #Start RPC event loop
