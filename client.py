import requests
import neighborhood
import logging


class Node:
    def __init__(self, info: dict):
        self.Architecture = ''
        self.BogoMIPS = ''
        self.ByteOrder = ''
        self.CPUMHz = 0
        self.CPUfamily = ''
        self.CPUmaxMHz = 0
        self.CPUminMHz = 0
        self.CPUopmodes = ''
        self.CPUs = 0
        self.Corespersocket = 0
        self.GPUcount = 0
        self.GPUtype = []
        self.L1dcache = ''
        self.L1icache = ''
        self.L2cache = ''
        self.L3cache = ''
        self.Model = ''
        self.Modelname = ''
        self.NUMAnode0CPUs = 0
        self.NUMAnodes = 0
        self.OnlineCPUslist = 0
        self.Sockets = 0
        self.Stepping = 0
        self.Threadspercore = 0
        self.VendorID = ''
        self.Virtualization = ''
        self.System = ''
        self.ip = ''
        self.number = 0
        self.working = False
        self.__dict__.update(info)
        self.ComputePowerMHz = self.CPUmaxMHz * self.CPUs

    def is_working(self):
        self.working = bool(requests.get('http://' + self.ip + ':5432/is_working').text)
        return self.working


class Cluster:
    def __init__(self):
        self.nodes = {}  # index by IP
        self.working_nodes = []
        self.free_nodes = []
        self.total_nodes = 0
        self.total_compute_power_MHz = 0
        self.total_cores = 0
        self.total_threads = 0

    def generate_nodes(self, node_ips: list):
        self.nodes = []
        # get node info, create node class instances
        for i, ip in enumerate(node_ips):
            node_info = requests.get('http://' + ip + ':5432/info').json()
            node_info['ip'] = ip
            node_info['number'] = i
            self.nodes[ip] = Node(node_info)

    def find_nodes(self, ips=None):
        searched = False
        if ips is None:
            ips = neighborhood.neighborhood()
            searched = True
        node_ips = []
        for ip in ips:
            try:
                if bool(requests.get('http://' + ip + ':5432/is_node', timeout=0.1).text):
                    node_ips.append(ip)
            except:
                if not searched:
                    logging.warning(ip, 'is not responsive, removing from Cluster')
                pass
        self.generate_nodes(node_ips)

    def who_is_working(self):
        for ip, node in self.nodes.items():
            self.working_nodes = []
            self.free_nodes = []
            working = node.is_working()
            if working:
                self.working_nodes.append(ip)
            else:
                self.free_nodes.append(ip)

    def cluster_stats(self):
        self.total_nodes = len(self.nodes)
        self.total_cores = 0
        self.total_compute_power_MHz = 0
        self.total_threads = 0

        for node in self.nodes:
            self.total_cores += node.CPUs
            self.total_threads += node.Threadspercore * node.CPUs
            self.total_compute_power_MHz += node.ComputePowerMHz
        return {
            'total_nodes': self.total_nodes,
            'total_cores': self.total_cores,
            'total_threads': self.total_threads,
            'total_total_compute_power_MHz': self.total_compute_power_MHz
        }
