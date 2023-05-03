from . import CloudRegion

class GcpRegion(CloudRegion):
    image_dir="resources/cloudRegion/gcpRegion"

class USWest1(GcpRegion):
    image_name="us-west1.png"
    carbon_intensity = 7.8E-06

class USWest2(GcpRegion):
    image_name="us-west2.png"
    carbon_intensity = 0.00011638