import sqlite3
import datetime
import os

DB_PATH = 'monitor.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    # Tabela de Histórico de Métricas
    c.execute('''
        CREATE TABLE IF NOT EXISTS metrics_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            cpu_percent REAL,
            ram_percent REAL,
            disk_percent REAL,
            net_download REAL,
            net_upload REAL
        )
    ''')
    # Tabela de Alertas
    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            alert_type TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_metric(cpu, ram, disk, net_download, net_upload):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO metrics_history (cpu_percent, ram_percent, disk_percent, net_download, net_upload)
        VALUES (?, ?, ?, ?, ?)
    ''', (cpu, ram, disk, net_download, net_upload))
    conn.commit()
    conn.close()

def get_metrics_history(limit=60):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT timestamp, cpu_percent, ram_percent, disk_percent, net_download, net_upload
        FROM metrics_history
        ORDER BY id DESC LIMIT ?
    ''', (limit,))
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in reversed(rows)]

def insert_alert(alert_type, message):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO alerts_log (alert_type, message)
        VALUES (?, ?)
    ''', (alert_type, message))
    conn.commit()
    conn.close()

def get_alerts(limit=10):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM alerts_log ORDER BY id DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]
