import psutil
import time
import socket

# Variáveis para calcular a velocidade da rede
_last_net_io = psutil.net_io_counters()
_last_net_time = time.time()

def get_network_speed():
    global _last_net_io, _last_net_time
    current_net_io = psutil.net_io_counters()
    current_time = time.time()
    
    dt = current_time - _last_net_time
    if dt == 0: dt = 1 # previne divisão por zero
    
    bytes_recv = current_net_io.bytes_recv - _last_net_io.bytes_recv
    bytes_sent = current_net_io.bytes_sent - _last_net_io.bytes_sent
    
    download_speed = (bytes_recv / dt) / 1024 / 1024 # MB/s
    upload_speed = (bytes_sent / dt) / 1024 / 1024 # MB/s
    
    _last_net_io = current_net_io
    _last_net_time = current_time
    
    return download_speed, upload_speed

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if not temps: return "N/A"
        for name, entries in temps.items():
            for entry in entries:
                return round(entry.current, 1)
    except:
        return "N/A"
    return "N/A"

def get_system_metrics():
    dl_speed, ul_speed = get_network_speed()
    
    return {
        "cpu_percent": psutil.cpu_percent(interval=None),
        "ram_percent": psutil.virtual_memory().percent,
        "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "ram_used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
        "disk_percent": psutil.disk_usage('/').percent,
        "net_download_mbs": round(dl_speed, 2),
        "net_upload_mbs": round(ul_speed, 2),
        "local_ip": get_local_ip(),
        "active_connections": len(psutil.net_connections()),
        "temperature": get_temperature()
    }

def get_top_processes(limit=10):
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            pinfo = proc.info
            # Evita erros com processos que sumiram
            if pinfo['memory_percent'] is None:
                pinfo['memory_percent'] = 0.0
            processes.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    # Ordena pelo uso de memória (mais estável que CPU instantânea)
    processes = sorted(processes, key=lambda p: p['memory_percent'], reverse=True)
    return processes[:limit]

def kill_process(pid):
    try:
        p = psutil.Process(int(pid))
        p.terminate()
        return True, f"Processo {pid} ({p.name()}) encerrado com sucesso."
    except Exception as e:
        return False, str(e)
