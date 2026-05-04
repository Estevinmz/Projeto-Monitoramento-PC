from apscheduler.schedulers.background import BackgroundScheduler
import system_monitor
import database
import logging

log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.WARNING)  # Reduz spam no console

def monitor_job():
    # Obtém métricas atuais
    metrics = system_monitor.get_system_metrics()
    
    # Salva no banco de dados SQLite
    database.insert_metric(
        cpu=metrics['cpu_percent'],
        ram=metrics['ram_percent'],
        disk=metrics['disk_percent'],
        net_download=metrics['net_download_mbs'],
        net_upload=metrics['net_upload_mbs']
    )
    
    # Checa limites (Alertas)
    if metrics['cpu_percent'] > 80.0:
        msg = f"Uso de CPU elevado ({metrics['cpu_percent']}%)"
        database.insert_alert('CPU_HIGH', msg)
        
    if metrics['ram_percent'] > 90.0:
        msg = f"Memória RAM quase cheia ({metrics['ram_percent']}%)"
        database.insert_alert('RAM_HIGH', msg)

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Executa a checagem e gravação a cada 5 segundos
    scheduler.add_job(monitor_job, 'interval', seconds=5)
    scheduler.start()
