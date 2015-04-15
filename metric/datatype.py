

class base:

    def type_check():
        # TBD: how to compare the datatype and data?
        return

class scalar(base):

    def __init__(self):
        return

    def type(self, datatype):
        types = ['int', 'float', 'long', 'string', 'char']
        
        if datatype in types:
            return 'scalar'

    def cast(self, data):
        if len(data) == 1:
            return data[0]
        else:
            return None



class keyvalue(base):

    def __init__(self):
        return


    def type(self, datatype):
        types = ['map',]
        
        if datatype in types:
            return 'map'

    def cast(self, data):
        try:
            result = '.'.join(data[:-1])
            result = result + '@' + str(data[-1])
            return result
        except:
           return None
        

class tree(base):

    def __init__(self):
        return

# Dynamic class name
parser = {}
parser['int'] = scalar
parser['long'] = scalar
parser['float'] = scalar
parser['string'] = scalar
parser['str'] = scalar
parser['scalar'] = scalar

parser['keyvalue'] = keyvalue

parser['tree'] = tree


if __name__ == '__main__':

    data = ['MAN','WORKER', '33', '1203']
    dtype = 'keyvalue'
    keyvalue = parser[dtype]().cast(data) 
    print data
    print keyvalue

    data = ['here',]
    dtype = 'scalar'
    scalar = parser[dtype]().cast(data)
    print data
    print scalar
    
