import stromx.runtime

class View(object):
    def __init__(self, stream):
        self.__stream = stream
        self.name = ''
        self.__observers = []
        
    @property
    def observers(self):
        return self.__observers
        
    def addConnectorObserver(self, op, connectorType, index):
        observer = ConnectorObserver(self.__stream, op, connectorType, index)
        self.__observers.append(observer)
        return observer
        
    def addParameterObserver(self, op, index):
        observer = ParameterObserver(self.__stream, op, index)
        self.__observers.append(observer)
        return observer
        
    def deserialize(self, data):
        properties = data['View']
        self.name = properties['name']
        for data in properties['observers']:
            for key in data:
                if key == 'ParameterObserver':
                    observer = ParameterObserver(self.__stream)
                elif key == 'ConnectorObserver':
                    observer = ConnectorObserver(self.__stream)
                else:
                    assert(False)
                    
                observer.deserialize(data[key])
                self.__observers.append(observer)
    
    def serialize(self):
        observers = [observer.serialize() for observer in self.observers]
        data = {
            'View': {
                'name': self.name,
                'observers': observers
            }
        }
        return data
    
class Observer(object):
    def __init__(self, stream, op):
        self.color = stromx.runtime.Color(0, 0, 0)
        self.zvalue = 0
        self.active = True
        self.visualization = 'default'
        self.__stream = stream
        self.__op = op
    
    def serialize(self):
        colorStr = '#{0:02x}{1:02x}{2:02x}'.format(self.color.r(),
                                                   self.color.g(),
                                                   self.color.b())
        data = {
           'Observer': {
                'color': colorStr,
                'op': self.__opId,
                'zvalue': self.zvalue,
                'active': self.active,
                'visualization': self.visualization
           }
        }
        
        return data
    
    def deserialize(self, properties):
        red = int(properties['color'][1:3], 16)
        green = int(properties['color'][3:5], 16)
        blue = int(properties['color'][5:], 16)
        
        self.zvalue = properties['zvalue']
        self.active = properties['active']
        self.visualization = properties['visualization']
        self.color = stromx.runtime.Color(red, green, blue)
        self.__op = self.__stream.operators()[properties['op']]
        
    @property
    def __opId(self):
        for index, op in enumerate(self.__stream.operators()):
            if op == self.__op:
                return index
            
        return -1
        
class ParameterObserver(Observer):
    def __init__(self, stream, op = None, index = None):
        super(ParameterObserver, self).__init__(stream, op)
        self.__op = op
        self.__index = index
    
    def serialize(self):
        parentData = super(ParameterObserver, self).serialize()
        data = {
            'parameter': self.__index
        }
        data.update(parentData['Observer'])
        
        return {
           'ParameterObserver': data
        }
        
    def deserialize(self, properties):
        super(ParameterObserver, self).deserialize(properties)
        self.__index = properties['parameter']
        
class ConnectorObserver(Observer):
    def __init__(self, stream, op = None, connectorType = None, index = None):
        super(ConnectorObserver, self).__init__(stream, op)
        self.__connectorType = connectorType
        self.__index = index
    
    def serialize(self):
        parentData = super(ConnectorObserver, self).serialize()
        data = {
            'type': int(self.__connectorType),
            'connector': self.__index}
        data.update(parentData['Observer'])
        
        return {
           'ConnectorObserver': data
        }
        
    def deserialize(self, properties):
        super(ConnectorObserver, self).deserialize(properties)
        self.__index = properties['connector']
        self.__connectorType = properties['type']
    