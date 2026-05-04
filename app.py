from flask import Flask, render_template, jsonify, request, send_file
import system_monitor
import database
import scheduler
import os

app = Flask(__name__)

# Inicializa Banco de Dados e Agendador de tarefas
database.init_db()
scheduler.start_scheduler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/metrics')
def api_metrics():
    metrics = system_monitor.get_system_metrics()
    alerts = database.get_alerts(limit=3)
    return jsonify({
        "metrics": metrics,
        "alerts": alerts
    })

@app.route('/api/processes')
def api_processes():
    procs = system_monitor.get_top_processes(limit=15)
    return jsonify(procs)

@app.route('/api/kill/<int:pid>', methods=['POST'])
def api_kill(pid):
    success, msg = system_monitor.kill_process(pid)
    return jsonify({"success": success, "message": msg})

@app.route('/api/history')
def api_history():
    # Retorna as métricas dos últimos 5 minutos (5s * 60 = 300s = 5m)
    history = database.get_metrics_history(limit=60)
    return jsonify(history)

@app.route('/export/pdf')
def export_pdf():
    # Gera um PDF usando reportlab
    from reportlab.pdfgen import canvas
    
    filepath = "relatorio_monitoramento.pdf"
    c = canvas.Canvas(filepath)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "Relatório de Monitoramento do PC")
    
    c.setFont("Helvetica", 12)
    metrics = system_monitor.get_system_metrics()
    y = 750
    for k, v in metrics.items():
        c.drawString(100, y, f"{k}: {v}")
        y -= 20
        
    c.drawString(100, y - 20, "Este relatório reflete o estado atual do sistema no momento da exportação.")
    c.save()
    
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    # Inicializa o cálculo de porcentagem da CPU do psutil
    system_monitor.psutil.cpu_percent(interval=None)
    # Roda o servidor Flask
    app.run(host='0.0.0.0', port=5000, debug=False)
