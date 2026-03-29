import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 🛡️ Configuração de Interface SOC/Procer
st.set_page_config(page_title="Procer - Gestão de Estoque", layout="wide")

# --- CONEXÃO COM GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    # ttl=0 para garantir que o gestor veja a mudança no exato segundo que ela ocorre
    return conn.read(worksheet="estoque", ttl=0)

# --- CABEÇALHO ---
try:
    st.image("procertecnologia_logo.jpeg", width=250)
except:
    st.title("📦 Sistema de Gestão de Campo - PROCER")

st.write("---")

# Carregamento dos dados
try:
    df = carregar_dados()
    
    # --- VISUALIZAÇÃO PRINCIPAL ---
    st.subheader("📋 Inventário do Veículo")
    st.dataframe(df, hide_index=True, use_container_width=True)

    st.write("---")
    
    # --- PAINEL DE CONTROLE (EDITAR TUDO) ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⬇️ Dar Baixa ou Repor")
        with st.form("form_atualizar"):
            item_sel = st.selectbox("Selecione o Material:", df['descricao'].tolist())
            nova_qtd = st.number_input("Nova Quantidade Total:", min_value=0, step=1)
            btn_atualizar = st.form_submit_button("Salvar Alteração de Quantidade")

            if btn_atualizar:
                idx = df.index[df['descricao'] == item_sel].tolist()[0]
                df.at[idx, 'qtd'] = nova_qtd
                conn.update(worksheet="estoque", data=df)
                st.success(f"✅ {item_sel} atualizado para {nova_qtd} unidades!")
                st.rerun()

    with col2:
        st.subheader("➕ Adicionar Novo Item")
        with st.form("form_novo_item"):
            nova_desc = st.text_input("Nome do Material:")
            nova_cat = st.selectbox("Categoria:", ["Automação", "Termometria", "Elétrica", "Outros"])
            qtd_inicial = st.number_input("Quantidade Inicial:", min_value=1, step=1)
            btn_novo = st.form_submit_button("Cadastrar no Sistema")

            if btn_novo and nova_desc:
                # Cria uma nova linha e adiciona ao DataFrame
                novo_dado = pd.DataFrame([{"descricao": nova_desc, "qtd": qtd_inicial, "categoria": nova_cat}])
                df = pd.concat([df, novo_dado], ignore_index=True)
                conn.update(worksheet="estoque", data=df)
                st.success(f"🚀 {nova_desc} cadastrado com sucesso!")
                st.rerun()

except Exception as e:
    st.error("🚨 Erro de Sincronização. Verifique os Secrets e a Planilha.")
    st.code(str(e))