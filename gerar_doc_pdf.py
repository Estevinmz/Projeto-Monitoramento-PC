from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
import os

filepath = "Documentacao_Monitoramento_PC.pdf"
doc = SimpleDocTemplate(filepath, pagesize=letter)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

story = []

story.append(Paragraph("Documentacao do Prototipo: Monitoramento de PC", styles['Title']))
story.append(Spacer(1, 12))

story.append(Paragraph("Visao Geral", styles['Heading2']))
story.append(Paragraph("Este prototipo eh uma aplicacao web baseada em Flask projetada para monitorar em tempo real os recursos do sistema operacional. Ele coleta metricas de hardware, lista processos ativos (permitindo o encerramento deles), registra o historico em um banco de dados e possibilita a exportacao de relatorios em PDF.", styles['Normal']))
story.append(Spacer(1, 12))

story.append(Paragraph("Arquitetura e Modulos Principais", styles['Heading2']))
story.append(Spacer(1, 6))

story.append(Paragraph("1. Aplicacao Web e API (app.py)", styles['Heading3']))
story.append(Paragraph("O arquivo principal gerencia o servidor Flask, as rotas da API e integra os modulos de banco de dados e agendamento de tarefas.", styles['Normal']))
story.append(Spacer(1, 6))
story.append(Paragraph("<b>Principais Rotas:</b>", styles['Normal']))
story.append(Paragraph("• <b>/</b>: Rota raiz, carrega a interface de usuario (index.html).", styles['Normal']))
story.append(Paragraph("• <b>/api/metrics</b>: Fornece o estado atual do sistema (CPU, RAM, Disco, Rede, Temperatura) e os ultimos alertas gerados.", styles['Normal']))
story.append(Paragraph("• <b>/api/processes</b>: Retorna uma lista dos 15 processos com maior consumo de memoria RAM.", styles['Normal']))
story.append(Paragraph("• <b>/api/kill/&lt;pid&gt;</b>: Rota (metodo POST) para encerrar um processo em execucao usando o seu identificador (PID).", styles['Normal']))
story.append(Paragraph("• <b>/api/history</b>: Retorna o historico de metricas armazenadas nos ultimos 5 minutos, ideal para plotagem de graficos na interface.", styles['Normal']))
story.append(Paragraph("• <b>/export/pdf</b>: Gera e envia para download um relatorio PDF com o retrato instantaneo das metricas atuais usando ReportLab.", styles['Normal']))
story.append(Spacer(1, 12))

story.append(Paragraph("2. Coleta de Dados do Sistema (system_monitor.py)", styles['Heading3']))
story.append(Paragraph("Este modulo utiliza a biblioteca <b>psutil</b> para interagir diretamente com o sistema operacional e hardware.", styles['Normal']))
story.append(Spacer(1, 6))
story.append(Paragraph("<b>Funcionalidades de Destaque:</b>", styles['Normal']))
story.append(Paragraph("• <b>Metricas de Hardware</b>: Mede o uso percentual e absoluto de CPU e RAM, espaco no Disco raiz e temperatura dos sensores da placa.", styles['Normal']))
story.append(Paragraph("• <b>Metricas de Rede</b>: Calcula a taxa de trafego de rede (Download e Upload em MB/s) verificando a diferenca de bytes transferidos em curtos intervalos de tempo. Tambem captura o IP local e numero de conexoes ativas.", styles['Normal']))
story.append(Paragraph("• <b>Gestao de Processos</b>: A funcao <i>get_top_processes</i> varre os processos em execucao, tratando excecoes para processos encerrados, e retorna os que mais consomem memoria. A funcao <i>kill_process</i> atua para encerrar tarefas indesejadas pelo PID.", styles['Normal']))

doc.build(story)
print(f"PDF gerado com sucesso em: {os.path.abspath(filepath)}")
