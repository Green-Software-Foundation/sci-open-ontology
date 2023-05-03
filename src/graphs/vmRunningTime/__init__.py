from graphs import Node

class VmRunningTime(Node):
    image_dir = "resources"
    image_name = "timer.png"
    fontcolor = "#ffffff"
    def __init__(self,time_in_hr):
        label = str(time_in_hr)+" hrs"
        self.running_time= time_in_hr
        super().__init__(label)
        