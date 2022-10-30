from flask import Blueprint, render_template, request
import platform
import psutil


info = Blueprint('info', __name__)


def bytes_to_gb(bytes):
    gb = bytes/(1024*1024*1024)
    gb = round(gb, 2)
    return gb



@info.route('/', methods=['GET', 'POST'])
def index():
    with open("/proc/cpuinfo", "r")  as cpu_file:
        cpu_file_info = cpu_file.readlines()

    with open("/proc/meminfo", "r") as memory_file:
        memory_file_info = memory_file.readlines()

    with open("/proc/uptime", "r") as uptime_file:
        uptime_file_info = int(float(uptime_file.read().split(" ")[0].strip()))

    with open("/proc/loadavg", "r") as loadavg_file:
        loadavg_file_info = loadavg_file.read().strip()

    partition_device = []

    for partition in psutil.disk_partitions():
        partition_device.append({
            "partition device": partition.device,
            "file system":      partition.fstype,
            "mount point":      partition.mountpoint,
            "total disk space": f"{bytes_to_gb(psutil.disk_usage(partition.mountpoint).total)} GB",
            "free disk space":  f"{bytes_to_gb(psutil.disk_usage(partition.mountpoint).total)} GB",
            "disk space used":  f"{bytes_to_gb(psutil.disk_usage(partition.mountpoint).percent)} GB"
        })

    network_device = []

    for interface_name, interface_addresses in psutil.net_if_addrs().items():
        for address in interface_addresses:
            network_device.append({
                "interface name":   interface_name,
                "ip address":       address.address,
                "netmask":          address.netmask,
                "broadcast ip":     address.broadcast
            })

    info_dict = {
        "general info": {
            "architecture": platform.architecture()[0],
            "system":       platform.system(),
            "node":         platform.node(),
            "platform":     platform.platform(),
            "machine":      platform.machine(),
            "os release":   platform.release(),
            "os version":   platform.version(),
            "uptime":       f"{uptime_file_info // 3600}:{(uptime_file_info % 3600) // 60} hr",
            "load average": loadavg_file_info
            # "battery info": {
            #     False if not psutil.sensors_battery() else
            #     "battery percentage":   f"{round(psutil.sensors_battery().percent, 1)}%",
            #     "battery time left":    f"{round(psutil.sensors_battery().secsleft/3600, 2)} hr",
            #     "power plugged":        psutil.sensors_battery().power_plugged
            # }
        },
        "processor info": {
            "processors":           [x.strip().split(":")[1] for x in cpu_file_info if "model name" in x],
            "physical cores":       psutil.cpu_count(logical=False),
            "total cores":          psutil.cpu_count(logical=True),
            "max frequency":        f"{psutil.cpu_freq().max:.2f} Mhz",
            "min frequency":        f"{psutil.cpu_freq().min:.2f} Mhz",
            "current frequency":    f"{psutil.cpu_freq().current:.2f} Mhz",
            "cpu usage per core":   [f"core {i}: {usage}%" for i, usage in enumerate(psutil.cpu_percent(percpu=True, interval=1))],
            "total cpu usage":      f"{psutil.cpu_percent()}%"
        },
        "memory info": {
            "total memory":         memory_file_info[0].strip(),
            "free memory":          memory_file_info[1].strip(),
            "memory used":          f"{psutil.virtual_memory().percent}%",
            "total swap memory":    bytes_to_gb(psutil.swap_memory().total),
            "free swap memory":     bytes_to_gb(psutil.swap_memory().free),
            "swap memory used":     f"{bytes_to_gb(psutil.swap_memory().percent)}%"
        },
        "disk info": {
            "partition device": partition_device
        },
        "network info": {
            "network device": network_device
        }
    }
    return info_dict