from graphs import Graph
from graphs.softwareApp import SoftwareApp
from graphs.hardware import Hardware
from graphs.dataCenter.region import USRegion
from graphs.cpuUtil import CpuUtil
from graphs.memoryUtil import MemoryUtil
from graphs.vmRunningTime import VmRunningTime
from graphs.instances.cloudVirtualMachine import CloudVirtualMachine 
from graphs.cloudRegion.gcp import USWest1,USWest2
from graphs.cloudType.gcp import Gcp
from graphs.instanceType.gcp import E2Standard2,E2Standard4
from graphs.language import Javascript
from graphs.framework import Angular

with Graph("SCI Ontology", filename="test_graph", function_unit="Users",function_count=1000,
           start_period="01/02/2023",end_period="28/02/2023"):
    sftApp = SoftwareApp()
    datacenter = USRegion()
    hardware = Hardware()
    angular = Angular()
    javascript = Javascript()

    vm1= CloudVirtualMachine("VM1",Gcp(),USWest1(),E2Standard2(),CpuUtil(60),MemoryUtil(4),VmRunningTime(600))
    vm2= CloudVirtualMachine("VM2",Gcp(),USWest2(),E2Standard4(),CpuUtil(60),MemoryUtil(4),VmRunningTime(600))
    sftApp.forward_edge(datacenter)
    datacenter.forward_edge(hardware)
    hardware.forward_edge(vm1)
    hardware.forward_edge(vm2)
    vm1.forward_edge(angular)
    vm2.forward_edge(angular)
    angular.forward_edge(javascript)
