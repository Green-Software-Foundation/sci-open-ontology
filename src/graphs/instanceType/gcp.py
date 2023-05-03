from . import InstanceType

class GcpInstanceType(InstanceType):
    image_dir="resources/instanceType/gcpInstanceType"

class E2Standard2(GcpInstanceType):
    image_name="e2-standard2.png"
    vcpu=2
    max_vcpus = 32
    memory=8
    embodied_emission=1.2303

class E2Standard4(GcpInstanceType):
    image_name="e2-standard4.png"
    vcpu=4
    max_vcpus = 32
    memory=16
    embodied_emission=1.2303