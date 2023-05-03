from . import DataCenter

class USRegion(DataCenter):
    label='US Region'
    def __init__(self):
        super().__init__(self.label)
    