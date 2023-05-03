from . import Instances
from graphviz import Digraph

class CloudVirtualMachine(Instances):
    image_name = "vm.png"
    graph_attrs = {
            "shape": "box",
            "style": "rounded",
            "labeljust": "l",
            "pencolor": "#AEB6BE",
            "fontname": "Sans-Serif",
            "fontsize": "12",
            "rankdir":"TB",
            "bgcolor":"#E5F5FD"
        }
    def __init__(self,label,cloud_type,region,instance_type,cpu_utilization,memory_utilization,runnig_time):
        super().__init__(label)
        self.name = "cluster_"+self.label
        self.dot = Digraph(self.name)
        
        attr=self.graph_attrs.items()
        for k, v in attr:
            self.dot.graph_attr[k] = v
        self.dot.graph_attr["label"] = self.label+"_details"
        self.edge_attr={'fontcolor': '#2D3436', 'fontname': 'Sans-Serif', 'fontsize': '13', 'dir': 'none'}
        self.dot.edge(self.nodeid, cloud_type.nodeid, **self.edge_attr)
        self.dot.edge(self.nodeid, region.nodeid, **self.edge_attr)
        self.dot.edge(self.nodeid, instance_type.nodeid, **self.edge_attr)
        self.dot.edge(self.nodeid, cpu_utilization.nodeid, **self.edge_attr)
        self.dot.edge(self.nodeid, memory_utilization.nodeid, **self.edge_attr)
        self.dot.edge(self.nodeid, runnig_time.nodeid, **self.edge_attr)
        self.graph.subgraph(self.dot)  
        self.graph._carbon_emission += self.calculateSCIScore(cloud_type,region,instance_type,cpu_utilization,memory_utilization,runnig_time)
    
    def calculateSCIScore(self,cloud_type,region,instance_type,cpu_utilization,memory_utilization,runnig_time):
        min_watt = cloud_type.min_watt
        max_watt = cloud_type.max_watt
        pue = cloud_type.pue
        memory_coeff = cloud_type.memory_wtHr
        carbon_intensity = region.carbon_intensity
        vcpus = instance_type.vcpu
        max_vcpus = instance_type.max_vcpus
        embodied_carbon = instance_type.embodied_emission
        cpu_util = cpu_utilization.cpu_utilize
        memory_util=memory_utilization.memory_utilize
        instance_running_time = runnig_time.running_time

        avg_watt = min_watt + cpu_util * (max_watt-min_watt)
        operation_watt = avg_watt * vcpus * instance_running_time
        time_reserved = 24*365*4
        embodied_emission = embodied_carbon * (instance_running_time/time_reserved) * (vcpus/max_vcpus)
        memory_watt = memory_coeff * memory_util * instance_running_time
        total_watt = operation_watt + memory_watt
        operation_emission = (total_watt/1000) * pue * carbon_intensity
        total_emission =  (operation_emission + embodied_emission)*1000
        return total_emission

