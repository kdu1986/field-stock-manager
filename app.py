import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Procer Field - Gestão de Estoque", layout="wide", page_icon="🛠️")
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_estoque():
    return conn.read(worksheet="estoque", ttl=0)

# --- ESTILIZAÇÃO E IDENTIFICAÇÃO (SEU LAYOUT) ---
st.sidebar.markdown(f"### 📍 Unidade Operacional\n**👤 Técnico:** Carlos Eduardo\n**🚛 Veículo:** SYG9H50")

st.title("🚀 Sistema de Gestão de Inventário")

try:
    df_estoque = carregar_estoque()

    tab1, tab2 = st.tabs(["📋 Consultar Estoque", "🔄 Baixa de Material (Campo)"])

    with tab1:
        st.dataframe(df_estoque, use_container_width=True, hide_index=True)

    with tab2:
        with st.form("form_baixa"):
            col_a, col_b = st.columns(2)
            with col_a:
                cliente = st.selectbox("Selecione o Cliente", ["Agrofertil", "Agroxisto", "Outro"])
                item_nome = st.selectbox("Item Utilizado", df_estoque.iloc[:, 0].tolist())
            with col_b:
                qtd_usada = st.number_input("Quantidade", min_value=1, step=1)
                os_numero = st.text_input("Nº da Ordem de Serviço (O.S.)")
            
            botao_confirmar = st.form_submit_button("Confirmar Saída de Material")
            
            if botao_confirmar:
                # 1. Lógica de Subtração (Aba estoque)
                idx = df_estoque[df_estoque.iloc[:, 0] == item_nome].index[0]
                
                if df_estoque.iat[idx, 1] >= qtd_usada:
                    df_estoque.iat[idx, 1] -= qtd_usada
                    
                    # 2. Criar registro para o Histórico (Aba historico)
                    novo_log = pd.DataFrame([{
                        "data": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                        "tecnico": "Carlos Eduardo",
                        "veiculo": "SYG9H50",
                        "cliente": cliente,
                        "os": os_numero,
                        "item": item_nome,
                        "qtd_retirada": qtd_usada
                    }])

                    # Tenta ler o histórico atual para anexar o novo
                    try:
                        df_hist = conn.read(worksheet="historico", ttl=0)
                        df_hist = pd.concat([df_hist, novo_log], ignore_index=True)
                    except:
                        df_hist = novo_log # Se a aba estiver vazia, cria do zero

                    # --- SALVAMENTO DUPLO ---
                    conn.update(worksheet="estoque", data=df_estoque)
                    conn.update(worksheet="historico", data=df_hist)
                    
                    st.success(f"✅ Baixa registrada e Log gerado na aba 'historico'!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Saldo insuficiente!")

except Exception as e:
    st.error("🚨 Erro de Sincronização")
    st.code(str(e))