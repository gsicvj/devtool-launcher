import inspect
from actions import ProcessWorker

class DevTool:

    def __init__(self, name=None, path=None):
        self.name = name
        self.path = path

    def setName(self, name):
        if name:
            self.name = name

    def getName(self):
        return self.name

    def setPath(self, path):
        if path:
            self.path = path

    def getPath(self):
        return self.path

    def toString(self):
        returnString = "[\n\tName => " + self.name
        returnString += ",\n\tPath => " + self.path
        returnString += "\n]"
        print returnString

class ToolBox:

  def __init__(self):
    self.tools = {}
    self.size = 0

  # append tool to the list
  def add(self, tool):
    if isinstance(tool, DevTool):
      if tool.getName() not in self.tools:
        self.tools[tool.getName()] = tool
        self.size += 1
      else:
        print "Toolbox: Trying to add a non unique key"
    else:
      print "Toolbox: Trying to add a non matching type"

  # remove tool by name
  def remove(self, name):
    if name:
        del self.tools[name]
        self.size -= 1

  def get(self, name):
    return self.tools[name]

  def size(self):
    return self.size

  def contains(self, name):
    if name:
      return name in self.tools
    return False

class ToolHandler:
    # holds a list of tools
    # communicates with ProcessWorker
    def __init__(self, toolbox=ToolBox()):
        if toolbox:
            self.toolbox = toolbox
        self.worker = ProcessWorker()

    def setTools(self, toolbox):
        if isinstance(toolbox, ToolBox):
            self.toolbox = toolbox

    def getTools(self):
        return self.toolbox

    def newTool(self, name, path):
        if name and path:
            tool = DevTool(name, path)
            self.toolbox.add(tool)
            self.worker.create(tool)
            return True
        return False

    def isBeingUsed(self, name):
        if name:
            return self.worker.status(name)
        return False

    def useTool(self, name):
        if name:
            return self.worker.start(name)
        return False

    def returnTool(self, name):
        if name:
            return self.worker.stop(name)
        return False