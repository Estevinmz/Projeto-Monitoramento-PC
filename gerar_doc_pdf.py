from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus.tableofcontents import TableOfContents
import os

class MyDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                self.notify('TOCEntry', (0, text, self.page))
            elif style == 'Heading2':
                self.notify('TOCEntry', (1, text, self.page))
            elif style == 'Heading3':
                self.notify('TOCEntry', (2, text, self.page))

filepath = "Documentacao_Monitoramento_PC.pdf"
doc = MyDocTemplate(filepath, pagesize=A4, rightMargin=2*cm, leftMargin=3*cm, topMargin=3*cm, bottomMargin=2*cm)

styles = getSampleStyleSheet()

# ABNT basic styles
styles.add(ParagraphStyle(name='ABNT_Normal', fontName='Helvetica', fontSize=12, alignment=TA_JUSTIFY, leading=18, spaceAfter=12)) # 1.5 line spacing (~18pt leading)
styles.add(ParagraphStyle(name='ABNT_Center', fontName='Helvetica-Bold', fontSize=12, alignment=TA_CENTER, spaceAfter=12))
styles.add(ParagraphStyle(name='ABNT_Heading1', fontName='Helvetica-Bold', fontSize=12, spaceAfter=12, spaceBefore=12))
styles.add(ParagraphStyle(name='ABNT_Heading2', fontName='Helvetica-Bold', fontSize=12, spaceAfter=12, spaceBefore=12))
styles.add(ParagraphStyle(name='ABNT_List', fontName='Helvetica', fontSize=12, alignment=TA_JUSTIFY, leading=18, leftIndent=20))

# Redefining Heading styles for TOC interception
styles['Heading1'].fontName = 'Helvetica-Bold'
styles['Heading1'].fontSize = 12
styles['Heading1'].spaceBefore = 12
styles['Heading1'].spaceAfter = 12

styles['Heading2'].fontName = 'Helvetica-Bold'
styles['Heading2'].fontSize = 12
styles['Heading2'].spaceBefore = 12
styles['Heading2'].spaceAfter = 12

styles['Heading3'].fontName = 'Helvetica-Bold'
styles['Heading3'].fontSize = 12
styles['Heading3'].spaceBefore = 12
styles['Heading3'].spaceAfter = 12

story = []

story.append(Paragraph("DOCUMENTAÇÃO DO PROTÓTIPO: MONITORAMENTO DE PC", styles['ABNT_Center']))
story.append(Spacer(1, 24))

toc = TableOfContents()
toc.levelStyles = [
    ParagraphStyle(fontName='Helvetica-Bold', fontSize=12, name='TOCHeading1', leftIndent=20, firstLineIndent=-20, spaceBefore=5, leading=16),
    ParagraphStyle(fontName='Helvetica', fontSize=12, name='TOCHeading2', leftIndent=40, firstLineIndent=-20, spaceBefore=0, leading=16),
    ParagraphStyle(fontName='Helvetica', fontSize=12, name='TOCHeading3', leftIndent=60, firstLineIndent=-20, spaceBefore=0, leading=16),
]
story.append(Paragraph("SUMÁRIO", styles['ABNT_Center']))
story.append(Spacer(1, 12))
story.append(toc)
story.append(PageBreak())

story.append(Paragraph("1 PROBLEMA", styles['Heading1']))
story.append(Paragraph("Atualmente, muitos usuários não possuem ferramentas simples e acessíveis para acompanhar o desempenho do computador. Isso dificulta a identificação de problemas como uso excessivo de CPU, consumo elevado de memória RAM e sobrecarga do sistema, podendo causar lentidão, travamentos e perda de produtividade.", styles['ABNT_Normal']))

story.append(Paragraph("2 OBJETIVO", styles['Heading1']))
story.append(Paragraph("Desenvolver uma aplicação capaz de monitorar os principais recursos do computador, como CPU, memória RAM e disco, apresentando informações claras ao usuário e gerando alertas em situações críticas.", styles['ABNT_Normal']))

story.append(Paragraph("3 JUSTIFICATIVA", styles['Heading1']))
story.append(Paragraph("A criação deste sistema é importante para auxiliar na manutenção preventiva e na otimização do desempenho dos computadores. Além disso, o projeto contribui para o desenvolvimento de habilidades práticas em programação, análise de dados e sistemas computacionais.", styles['ABNT_Normal']))

story.append(Paragraph("4 DESCRIÇÃO DO PROJETO", styles['Heading1']))
story.append(Paragraph("O sistema será desenvolvido em Python, utilizando bibliotecas especializadas em monitoramento, como psutil. A aplicação poderá apresentar uma interface simples, exibindo dados atualizados em tempo real, como porcentagem de uso da CPU, memória e armazenamento.", styles['ABNT_Normal']))

story.append(Paragraph("5 FUNCIONALIDADES", styles['Heading1']))
story.append(Paragraph("• Monitoramento de CPU em tempo real", styles['ABNT_List']))
story.append(Paragraph("• Monitoramento de memória RAM", styles['ABNT_List']))
story.append(Paragraph("• Monitoramento de disco", styles['ABNT_List']))
story.append(Paragraph("• Exibição de informações atualizadas continuamente", styles['ABNT_List']))
story.append(Paragraph("• Geração de alertas em caso de uso elevado", styles['ABNT_List']))
story.append(Spacer(1, 12))

story.append(Paragraph("6 RESULTADOS ESPERADOS", styles['Heading1']))
story.append(Paragraph("Espera-se que o sistema seja leve, eficiente e de fácil utilização, permitindo ao usuário identificar problemas rapidamente e melhorar o desempenho do computador.", styles['ABNT_Normal']))

story.append(Paragraph("7 VISÃO GERAL", styles['Heading1']))
story.append(Paragraph("Este prototipo eh uma aplicacao web baseada em Flask projetada para monitorar em tempo real os recursos do sistema operacional. Ele coleta metricas de hardware, lista processos ativos (permitindo o encerramento deles), registra o historico em um banco de dados e possibilita a exportacao de relatorios em PDF.", styles['ABNT_Normal']))

story.append(Paragraph("8 ARQUITETURA E MÓDULOS PRINCIPAIS", styles['Heading1']))

story.append(Paragraph("8.1 Aplicação Web e API (app.py)", styles['Heading2']))
story.append(Paragraph("O arquivo principal gerencia o servidor Flask, as rotas da API e integra os modulos de banco de dados e agendamento de tarefas.", styles['ABNT_Normal']))
story.append(Paragraph("<b>Principais Rotas:</b>", styles['ABNT_Normal']))
story.append(Paragraph("• <b>/</b>: Rota raiz, carrega a interface de usuario (index.html).", styles['ABNT_List']))
story.append(Paragraph("• <b>/api/metrics</b>: Fornece o estado atual do sistema (CPU, RAM, Disco, Rede, Temperatura) e os ultimos alertas gerados.", styles['ABNT_List']))
story.append(Paragraph("• <b>/api/processes</b>: Retorna uma lista dos 15 processos com maior consumo de memoria RAM.", styles['ABNT_List']))
story.append(Paragraph("• <b>/api/kill/&lt;pid&gt;</b>: Rota (metodo POST) para encerrar um processo em execucao usando o seu identificador (PID).", styles['ABNT_List']))
story.append(Paragraph("• <b>/api/history</b>: Retorna o historico de metricas armazenadas nos ultimos 5 minutos, ideal para plotagem de graficos na interface.", styles['ABNT_List']))
story.append(Paragraph("• <b>/export/pdf</b>: Gera e envia para download um relatorio PDF com o retrato instantaneo das metricas atuais usando ReportLab.", styles['ABNT_List']))
story.append(Spacer(1, 12))

story.append(Paragraph("8.2 Coleta de Dados do Sistema (system_monitor.py)", styles['Heading2']))
story.append(Paragraph("Este modulo utiliza a biblioteca <b>psutil</b> para interagir diretamente com o sistema operacional e hardware.", styles['ABNT_Normal']))
story.append(Paragraph("<b>Funcionalidades de Destaque:</b>", styles['ABNT_Normal']))
story.append(Paragraph("• <b>Metricas de Hardware</b>: Mede o uso percentual e absoluto de CPU e RAM, espaco no Disco raiz e temperatura dos sensores da placa.", styles['ABNT_List']))
story.append(Paragraph("• <b>Metricas de Rede</b>: Calcula a taxa de trafego de rede (Download e Upload em MB/s) verificando a diferenca de bytes transferidos em curtos intervalos de tempo. Tambem captura o IP local e numero de conexoes ativas.", styles['ABNT_List']))
story.append(Paragraph("• <b>Gestao de Processos</b>: A funcao <i>get_top_processes</i> varre os processos em execucao, tratando excecoes para processos encerrados, e retorna os que mais consomem memoria. A funcao <i>kill_process</i> atua para encerrar tarefas indesejadas pelo PID.", styles['ABNT_List']))

doc.multiBuild(story)
print(f"PDF gerado com sucesso em: {os.path.abspath(filepath)}")
