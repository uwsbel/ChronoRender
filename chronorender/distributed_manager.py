import RndrJob

# push render jobs to job manager (ie torque) 
# or handle it locally
class DistributedManagerException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class DistributedManager():
    def __init__(self):
        self.name = ''
