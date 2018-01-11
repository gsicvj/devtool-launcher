import inspect
import subprocess as sub
#from tools import DevTool

class Process:

  def __init__(self, tool=None, running=False):
    self.tool = tool
    self.running = running
    self.instance = None

  def setTool(self, tool):
    if tool:
      self.tool = tool

  def getTool(self):
    return self.tool

  def setRunning(self, boolean):
    self.running = boolean

  def isRunning(self):
    return self.running

  def setInstance(self, instance):
    if instance:
      self.instance = instance

  def getInstance(self):
    return self.instance

  def kill(self):
    if self.instance:
      self.instance.kill()

  def toString(self):
    returnString = "[\n\tName => " + self.tool.name
    returnString += ",\n\tPath => " + self.tool.path
    returnString += ",\n\tRunning => " + str(self.running)
    returnString += "\n]"
    print returnString

class ProcessBox:

  def __init__(self):
    self.processes = {}
    self.size = 0

  def add(self, process):
    if process:
      key = process.getTool().getName()
      self.processes[key] = process
      self.size += 1

  def remove(self, process):
    if process:
      key = process.getTool().getName()
      del self.processes[key]
      self.size -= 1

  def get(self, name):   
      return self.processes[name]

  def size(self):
    return self.size

  def contains(self, name):
    if name:
      return name in self.processes
    return False

class ProcessWorker:
  # holds a list of processes
  # performs action upon processes
  def __init__(self, processbox=ProcessBox()):
    if processbox:
      self.processbox = processbox

  def status(self, name):
    if name:
      return self.processbox.get(name).isRunning()
    return False

  def start(self, name):
    if name:
      try: 
        process = self.processbox.get(name)
        if not process.isRunning():
          path = process.getTool().getPath()
          instance = sub.Popen(path)
          process.setInstance(instance)
          process.setRunning(True)
          return True
      except Exception as err:
        print "Failed starting a process: " + str(err)

    return False

  def stop(self, name):
    if name:
      try:
        process = self.processbox.get(name)
        if process.isRunning():
          process.kill()
          process.setInstance(None)
          process.setRunning(False)
          return True
      except Exception as err:
        print "Failed stoping a process: " + str(err)
    return False

  def create(self, tool):
    if tool:
      name = tool.getName()
      if not self.processbox.contains(name):
        process = Process(tool)
        self.processbox.add(process)
        return True

    return False
