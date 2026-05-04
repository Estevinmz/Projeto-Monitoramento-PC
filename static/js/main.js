// Alternância de Tema
const themeToggle = document.getElementById('themeToggle');
themeToggle.addEventListener('click', () => {
    const html = document.documentElement;
    if (html.getAttribute('data-theme') === 'dark') {
        html.removeAttribute('data-theme');
    } else {
        html.setAttribute('data-theme', 'dark');
    }
});

// Configuração do Gráfico (Chart.js)
const ctx = document.getElementById('historyChart').getContext('2d');
const historyChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            { label: 'CPU (%)', data: [], borderColor: '#3498db', tension: 0.3, borderWidth: 2, pointRadius: 0 },
            { label: 'RAM (%)', data: [], borderColor: '#ff7f0e', tension: 0.3, borderWidth: 2, pointRadius: 0 }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 0 }, // desativa a animação para melhor performance em tempo real
        interaction: { mode: 'index', intersect: false },
        scales: { 
            y: { min: 0, max: 100, grid: { color: 'rgba(200,200,200,0.1)' } },
            x: { grid: { display: false } }
        },
        plugins: { legend: { labels: { color: '#888' } } }
    }
});

// Atualiza Métricas dos Cards
async function updateMetrics() {
    try {
        const res = await fetch('/api/metrics');
        const data = await res.json();
        
        document.getElementById('cpuVal').innerText = data.metrics.cpu_percent + '%';
        document.getElementById('ramVal').innerText = data.metrics.ram_percent + '%';
        document.getElementById('ramInfo').innerText = `${data.metrics.ram_used_gb} GB / ${data.metrics.ram_total_gb} GB`;
        document.getElementById('diskVal').innerText = data.metrics.disk_percent + '%';
        document.getElementById('netVal').innerText = `↓ ${data.metrics.net_download_mbs} MB/s | ↑ ${data.metrics.net_upload_mbs} MB/s`;
        document.getElementById('ipVal').innerText = data.metrics.local_ip;
        document.getElementById('connVal').innerText = data.metrics.active_connections;

        // Atualiza alertas flutuantes
        const alertsContainer = document.getElementById('alertsContainer');
        alertsContainer.innerHTML = '';
        data.alerts.forEach(alert => {
            const div = document.createElement('div');
            div.className = 'alert';
            // Exibir apenas a hora:minuto:segundo
            const time = alert.timestamp.split(' ')[1];
            div.innerText = `[${time}] ${alert.message}`;
            alertsContainer.appendChild(div);
        });

    } catch(e) { console.error("Erro ao buscar métricas:", e); }
}

// Atualiza Gráfico de Histórico
async function updateHistory() {
    try {
        const res = await fetch('/api/history');
        const history = await res.json();
        
        const labels = history.map(h => h.timestamp.split(' ')[1]);
        const cpuData = history.map(h => h.cpu_percent);
        const ramData = history.map(h => h.ram_percent);

        historyChart.data.labels = labels;
        historyChart.data.datasets[0].data = cpuData;
        historyChart.data.datasets[1].data = ramData;
        historyChart.update();
    } catch(e) { console.error("Erro ao atualizar gráfico:", e); }
}

// Atualiza Tabela de Processos
async function updateProcesses() {
    try {
        const res = await fetch('/api/processes');
        const procs = await res.json();
        
        const tbody = document.querySelector('#procTable tbody');
        tbody.innerHTML = '';
        procs.forEach(p => {
            const cpu = p.cpu_percent ? p.cpu_percent.toFixed(1) : '0.0';
            const ram = p.memory_percent ? p.memory_percent.toFixed(1) : '0.0';
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${p.pid}</td>
                <td style="font-weight: 500;">${p.name}</td>
                <td>${cpu}%</td>
                <td>${ram}%</td>
                <td><button class="btn-kill" onclick="killProcess(${p.pid}, '${p.name}')">Matar</button></td>
            `;
            tbody.appendChild(tr);
        });
    } catch(e) { console.error("Erro ao atualizar processos:", e); }
}

// Mata um Processo
async function killProcess(pid, name) {
    if(!confirm(`Tem certeza que deseja encerrar o processo "${name}" (PID: ${pid})?\nIsso pode causar instabilidade no sistema se for um processo vital.`)) return;
    try {
        const res = await fetch(`/api/kill/${pid}`, { method: 'POST' });
        const data = await res.json();
        if(data.success) {
            alert("Sucesso: " + data.message);
            updateProcesses(); // Atualiza a tabela imediatamente
        } else {
            alert("Falha ao matar processo: " + data.message);
        }
    } catch(e) { 
        alert("Erro na requisição para matar o processo."); 
    }
}

// Timers de Polling (AJAX)
setInterval(updateMetrics, 2000);   // Cada 2 segundos
setInterval(updateProcesses, 3000); // Cada 3 segundos
setInterval(updateHistory, 5000);   // Cada 5 segundos para o gráfico

// Chamadas iniciais
updateMetrics();
updateHistory();
updateProcesses();
