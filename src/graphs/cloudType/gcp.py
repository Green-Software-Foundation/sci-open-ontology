from . import _CloudType

class Gcp(_CloudType):
    image_name = "gcp.png"
    pue = 1.1
    min_watt = 0.71
    max_watt= 4.26
    memory_wtHr = 0.392