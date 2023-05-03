from graphs import Node

class CpuUtil(Node):
    image_dir = "resources"
    image_name = "cpu_utilization.png"
    fontcolor = "#ffffff"
    def __init__(self,cpu_percent):
        label = str(cpu_percent)+" %"
        self.cpu_utilize= cpu_percent
        super().__init__(label)