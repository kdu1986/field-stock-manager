import streamlit as st
import json
import pandas as pd
import os
from datetime import datetime

# 1. Configurações Iniciais do Streamlit
st.set_page_config(page_title="Procer Campo - Logística", page_icon="📡", layout="wide")

# Caminhos Simplificados (Considerando que tudo está na mesma pasta raiz)
ARQUIVO_JSON = 'estoque.json'
ARQUIVO_HISTORICO = 'historico.json'
# Use o nome do arquivo da logo que está na sua pasta raiz
LOGO_PATH = "procertecnologia_logo.jpeg" 

# 2. Funções de Persistência
def carregar_dados(arquivo, padrao=[]):
    try:
        if not os.path.exists(arquivo): return padrao
        with open(arquivo, 'r', encoding='utf-8-sig') as f:
            dados = json.load(f)
            for d in dados:
                if d.get('categoria') == 'Telemetria':
                    d['categoria'] = 'Termometria'
            return dados
    except: return padrao

def salvar_dados(arquivo, dados):
    # Salva diretamente no arquivo (sem referenciar pasta pai)
    with open(arquivo, 'w', encoding='utf-8-sig') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# 3. Sidebar e Controle de Acesso
try:
    st.sidebar.image(LOGO_PATH, width=120)
except:
    st.sidebar.write("📡")

st.sidebar.title("🔐 Acesso Restrito")
perfil = st.sidebar.radio("Perfil de Usuário:", ["Visualização", "Administrador (Carlos)"])
auth = False

if perfil == "Administrador (Carlos)":
    senha = st.sidebar.text_input("Senha de Acesso:", type="password")
    if senha == "admin":
        auth = True
        st.sidebar.success("Autenticado")

# 4. Cabeçalho Corporativo
col_logo, col_titulo, col_id = st.columns([1.2, 5, 2.5])
with col_logo:
    try:
        st.image(LOGO_PATH, = "procertecnologia_logo.jpeg")
    except:
        st.write("📡")

with col_titulo:
    st.markdown("<h1 style='margin: 0; padding-top: 10px;'>Gestão de Insumos Procer</h1>", unsafe_allow_html=True)

with col_id:
    st.markdown(f"<div style='text-align: right; color: #00FFCC; padding-top: 20px;'><p style='margin: 0; font-weight: bold;'>Técnico: Carlos Eduardo</p><p style='margin: 0;'>Veículo: Unidade de Campo</p></div>", unsafe_allow_html=True)

st.markdown("---")

# 5. Lógica de Negócio
dados = carregar_dados(ARQUIVO_JSON)
historico = carregar_dados(ARQUIVO_HISTORICO)

if auth:
    aba_baixa, aba_entrada, aba_hist = st.tabs(["📉 Dar Baixa", "📈 Reposição", "📜 Histórico"])
    
    with aba_baixa:
        itens = [d['descricao'] for d in dados if d['qtd'] > 0]
        if itens:
            with st.form("baixa_material", clear_on_submit=True):
                sel_item = st.selectbox("Selecione o Item:", itens)
                qtd_sai = st.number_input("Quantidade utilizada:", min_value=1, step=1)
                cliente = st.text_input("Cliente atendido:")
                obs_tecnica = st.text_area("Observação:")
                if st.form_submit_button("Confirmar Retirada"):
                    for d in dados:
                        if d['descricao'] == sel_item:
                            d['qtd'] -= qtd_sai
                            historico.append({
                                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                                "Item": sel_item, "Qtd": qtd_sai, "Cliente": cliente, "Observação": obs_tecnica
                            })
                            break
                    salvar_dados(ARQUIVO_JSON, dados)
                    salvar_dados(ARQUIVO_HISTORICO, historico)
                    st.success("Baixa realizada!")
                    st.rerun()
        else:
            st.warning("Estoque zerado.")

    with aba_entrada:
        with st.form("entrada_estoque"):
            n_desc = st.text_input("Descrição:").upper()
            n_qtd = st.number_input("Quantidade:", min_value=1)
            n_cat = st.selectbox("Categoria:", ["Termometria", "Módulos Ceres", "Elétrica", "RF", "Infraestrutura"])
            if st.form_submit_button("Adicionar"):
                dados.append({"descricao": n_desc, "qtd": n_qtd, "categoria": n_cat})
                salvar_dados(ARQUIVO_JSON, dados)
                st.rerun()

    with aba_hist:
        if historico:
            st.dataframe(pd.DataFrame(historico)[::-1], use_container_width=True)

# 6. Exibição da Tabela Geral
st.markdown("### 📋 Inventário Atual")
if dados:
    df_view = pd.DataFrame(dados)
    st.dataframe(df_view, use_container_width=True, hide_index=True)
    
    # Alertas Críticos
    if 'qtd' in df_view.columns:
        alertas = df_view[df_view['qtd'] <= 2]
        if not alertas.empty:
            with st.expander("⚠️ ESTOQUE BAIXO", expanded=True):
                for _, r in alertas.iterrows():
                    st.write(f"- **{r['descricao']}**: {r['qtd']} unidades.")
else:
    st.info("O inventário está vazio.")
    if st.button("Inicializar com Item de Exemplo"):
        salvar_dados(ARQUIVO_JSON, [{"descricao": "EQUIPAMENTO TESTE", "qtd": 5, "categoria": "Infraestrutura"}])
        st.rerun()