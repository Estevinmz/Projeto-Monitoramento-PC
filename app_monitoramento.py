import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Monitoramento do PC", layout="wide", page_icon="🖥️")

st.title("🖥️ Sistema de Monitoramento do PC")
st.markdown("Dashboard interativo para visualização de métricas de desempenho do sistema usando dados históricos.")

# Função para carregar os dados
@st.cache_data
def load_data():
    df = pd.read_csv('Big_data_dataset.csv')
    return df

try:
    with st.spinner('Carregando dados...'):
        df = load_data()
    
    st.header("Visão Geral das Métricas")
    
    # Exibir métricas agregadas (Médias)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Uso de CPU (Média)", f"{df['cpu_utilization'].mean():.2f}%")
    col2.metric("Uso de Memória (Média)", f"{df['memory_usage'].mean():.2f}%")
    col3.metric("Temperatura (Média)", f"{df['temperature'].mean():.2f} °C")
    col4.metric("Contagem de Processos", f"{df['process_count'].mean():.0f}")

    st.markdown("---")

    st.subheader("Evolução do Uso de CPU e Memória")
    st.markdown("Visualização das últimas 200 leituras registradas no dataset.")
    
    # Selecionar os últimos 200 registros para o gráfico de linhas
    df_sample = df.tail(200).reset_index()
    
    fig1, ax1 = plt.subplots(figsize=(12, 4))
    ax1.plot(df_sample.index, df_sample['cpu_utilization'], label='CPU (%)', color='#1f77b4', linewidth=1.5)
    ax1.plot(df_sample.index, df_sample['memory_usage'], label='Memória (%)', color='#ff7f0e', linewidth=1.5)
    ax1.set_xlabel('Tempo (Últimos 200 registros)')
    ax1.set_ylabel('Utilização (%)')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig1)

    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Temperatura vs Consumo de Energia")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        # Selecionar uma amostra menor para o scatter plot ser mais rápido
        scatter_sample = df.sample(min(1000, len(df)))
        ax2.scatter(scatter_sample['temperature'], scatter_sample['power_consumption'], alpha=0.4, color='#d62728')
        ax2.set_xlabel('Temperatura (°C)')
        ax2.set_ylabel('Consumo de Energia (W)')
        ax2.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig2)
        
    with col_chart2:
        st.subheader("Uso de Disco vs Latência de Rede")
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        ax3.scatter(scatter_sample['disk_io'], scatter_sample['network_latency'], alpha=0.4, color='#2ca02c')
        ax3.set_xlabel('I/O de Disco')
        ax3.set_ylabel('Latência de Rede (ms)')
        ax3.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig3)

    st.markdown("---")
    st.subheader("Exploração de Dados Brutos")
    # Mostrar um número limitado de linhas inicialmente
    num_linhas = st.slider("Selecione o número de linhas para visualizar:", min_value=5, max_value=100, value=10)
    st.dataframe(df.head(num_linhas))

except FileNotFoundError:
    st.error("❌ Arquivo 'Big_data_dataset.csv' não encontrado. Verifique se o arquivo está localizado no mesmo diretório do script.")
except Exception as e:
    st.error(f"❌ Ocorreu um erro ao carregar o aplicativo: {e}")
