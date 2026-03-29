import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Procer Field - Gestão de Estoque", layout="wide", page_icon="🛠️")

# --- ESTILIZAÇÃO CSS PARA IDENTIFICAÇÃO ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stSidebar { background-color: #1e293b !important; color: white; }
    .identificacao-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #0e1117;
        border: 1px solid #3b82f6;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE IDENTIFICAÇÃO (GLOBAL) ---
def exibir_identificacao_unidade():
    st.sidebar.markdown('<div class="identificacao-card">', unsafe_allow_html=True)
    st.sidebar.markdown(f"### 📍 Unidade Operacional")
    st.sidebar.write(f"**👤 Técnico:** Carlos Eduardo")
    st.sidebar.write(f"**🚛 Veículo:** SYG9H50")
    st.sidebar.write(f"**🕒 Registro:** {datetime.now().strftime('%d/%m/%Y')}")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# --- BASE DE DADOS SIMULADA (MANTENDO TERMOS CORRETOS) ---
if 'estoque' not in st.session_state:
    data = {
        'Código': ['ANT-RF-01', 'CERES-P12', 'CONT-24V', 'FONTE-5A', 'DISJ-16A'],
        'Categoria': ['Termometria', 'Termometria', 'Elétrica', 'Elétrica', 'Elétrica'],
        'Item': [
            'Antena RF 900MHz 5dBi (Base Magnética)',
            'Módulo CERES-PAR12',
            'Contatora de Potência 24V',
            'Fonte Chaveada 24V 5A',
            'Disjuntor Motor 10-16A'
        ],
        'Saldo': [5, 2, 8, 3, 4]
    }
    st.session_state.estoque = pd.DataFrame(data)

# --- LÓGICA DO APLICATIVO ---
exibir_identificacao_unidade()

st.title("🚀 Sistema de Gestão de Inventário de Campo")
st.write("Controle de ativos e materiais para unidades móveis da **Procer Automação**.")

# --- DASHBOARD DE RESUMO ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Técnico Responsável", "Carlos Eduardo")
with col2:
    st.metric("Veículo Vinculado", "SYG9H50")
with col3:
    total_itens = st.session_state.estoque['Saldo'].sum()
    st.metric("Total de Itens no Carro", total_itens)

st.divider()

# --- ABA DE OPERAÇÕES ---
tab1, tab2 = st.tabs(["📋 Consultar Estoque", "🔄 Baixa de Material (Campo)"])

with tab1:
    st.subheader("Itens Disponíveis no Veículo SYG9H50")
    # Filtro por Categoria
    categoria_filtro = st.multiselect("Filtrar por Categoria", 
                                     options=st.session_state.estoque['Categoria'].unique(),
                                     default=st.session_state.estoque['Categoria'].unique())
    
    df_filtrado = st.session_state.estoque[st.session_state.estoque['Categoria'].isin(categoria_filtro)]
    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Registrar Uso em Cliente")
    with st.form("form_baixa"):
        col_a, col_b = st.columns(2)
        with col_a:
            cliente = st.selectbox("Selecione o Cliente", ["Agrofertil", "Agroxisto", "Outro"])
            item_nome = st.selectbox("Item Utilizado", st.session_state.estoque['Item'])
        with col_b:
            qtd_usada = st.number_input("Quantidade", min_value=1, step=1)
            os_numero = st.text_input("Nº da Ordem de Serviço (O.S.)")
            
        botao_confirmar = st.form_submit_button("Confirmar Saída de Material")
        
        if botao_confirmar:
            # Lógica simples para atualizar o saldo no estado da sessão
            idx = st.session_state.estoque.index[st.session_state.estoque['Item'] == item_nome][0]
            if st.session_state.estoque.at[idx, 'Saldo'] >= qtd_usada:
                st.session_state.estoque.at[idx, 'Saldo'] -= qtd_usada
                st.success(f"✅ Sucesso! {qtd_usada} un. de {item_nome} baixadas para o veículo SYG9H50.")
                st.info(f"**Log de Segurança:** Registrado por Carlos Eduardo em {datetime.now().strftime('%H:%M:%S')}")
            else:
                st.error("❌ Saldo insuficiente no estoque do veículo!")

# --- RODAPÉ TÉCNICO ---
st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido por Carlos Eduardo - Graduando em Cibersegurança")
st.sidebar.caption("Foco: Integridade e Rastreabilidade de Ativos")