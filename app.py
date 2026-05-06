import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da Página
st.set_page_config(page_title="Dashboard de Monitoramento de PC", layout="wide")

# Título
st.title("Dashboard de Monitoramento de PC")
st.markdown("Monitoramento baseado nos dados do arquivo `Big_data_dataset.csv`.")

# Função para carregar os dados (com cache para não recarregar toda hora)
@st.cache_data
def load_data():
    # O arquivo tem as seguintes colunas de interesse:
    # cpu_utilization, memory_usage, disk_io, network_latency, process_count, 
    # thread_count, context_switches, cache_miss_rate, temperature, power_consumption, uptime, status
    df = pd.read_csv('Big_data_dataset.csv')
    return df

try:
    df = load_data()
    
    # Criar 3 colunas para KPIs
    col1, col2, col3 = st.columns(3)
    
    # KPIs: Média de uso da CPU, Memória, Temperatura
    avg_cpu = df['cpu_utilization'].mean()
    avg_mem = df['memory_usage'].mean()
    avg_temp = df['temperature'].mean()
    
    with col1:
        st.metric(label="Média de Uso de CPU", value=f"{avg_cpu:.2f}%")
    with col2:
        st.metric(label="Média de Uso de Memória", value=f"{avg_mem:.2f}%")
    with col3:
        st.metric(label="Temperatura Média", value=f"{avg_temp:.2f} °C")
        
    st.markdown("---")
    
    # Vamos gerar gráficos usando matplotlib conforme solicitado
    st.subheader("Análise Gráfica")
    
    colA, colB = st.columns(2)
    
    with colA:
        st.markdown("**Gráfico de Linha: Uso de CPU vs Memória (Amostra de 100 registros)**")
        # Pegar as primeiras 100 linhas (ou uma amostra) para não ficar um gráfico poluído
        sample_df = df.head(100)
        
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(sample_df.index, sample_df['cpu_utilization'], label='CPU (%)', color='blue', alpha=0.7)
        ax.plot(sample_df.index, sample_df['memory_usage'], label='Memória (%)', color='orange', alpha=0.7)
        ax.set_title("Evolução do Uso de CPU vs Memória")
        ax.set_xlabel("Índice (Tempo / Observação)")
        ax.set_ylabel("Uso (%)")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig)
        
    with colB:
        st.markdown("**Histograma: Distribuição de Temperaturas**")
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.hist(df['temperature'].dropna(), bins=30, color='red', edgecolor='black', alpha=0.7)
        ax2.set_title("Distribuição da Temperatura do PC")
        ax2.set_xlabel("Temperatura (°C)")
        ax2.set_ylabel("Frequência")
        ax2.grid(axis='y', linestyle='--', alpha=0.5)
        st.pyplot(fig2)
        
    st.markdown("---")
    
    # Mostrar Tabela Completa Expandível
    with st.expander("Visualizar Dados Brutos (Dataset)"):
        st.dataframe(df)

except Exception as e:
    st.error(f"Erro ao carregar os dados. Verifique se o arquivo 'Big_data_dataset.csv' está presente. Detalhes: {e}")
