from graphs import Node

class MemoryUtil(Node):
    image_dir = "resources"
    image_name = "rack.png"
    fontcolor = "#ffffff"
    def __init__(self,memory_used):
        label = str(memory_used)+" GB"
        self.memory_utilize= memory_used
        super().__init__(label)
        