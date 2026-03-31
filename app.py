import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Procer Field - Gestão de Estoque", layout="wide", page_icon="🛠️")

# --- CONEXÃO COM GOOGLE SHEETS ---
# Certifique-se de que as credenciais estão nos 'Secrets' do Streamlit Cloud
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_estoque():
    # ttl=0 garante que ele busque dados frescos sempre que a página recarregar
    return conn.read(worksheet="estoque", ttl=0)

def carregar_historico():
    try:
        return conn.read(worksheet="historico", ttl=0)
    except:
        # Se a aba estiver vazia ou der erro, retorna um DataFrame com as colunas certas
        return pd.DataFrame(columns=["data", "tecnico", "veiculo", "cliente", "os", "item", "qtd_retirada"])

# --- SIDEBAR (IDENTIFICAÇÃO) ---
st.sidebar.markdown("### 📍 Unidade Operacional")
st.sidebar.info("**👤 Técnico:** Carlos Eduardo\n\n**🚛 Veículo:** SYG9H50")

st.title("🚀 Sistema de Gestão de Inventário")

try:
    df_estoque = carregar_estoque()

    tab1, tab2 = st.tabs(["📋 Consultar Estoque", "🔄 Baixa de Material (Campo)"])

    with tab1:
        st.subheader("Estoque Atual")
        st.dataframe(df_estoque, use_container_width=True, hide_index=True)

    with tab2:
        with st.form("form_baixa"):
            st.subheader("Registrar Saída")
            col_a, col_b = st.columns(2)
            
            with col_a:
                cliente = st.selectbox("Selecione o Cliente", ["Agrofertil", "Agroxisto", "Outro"])
                # Pega os nomes dos itens da primeira coluna da planilha
                item_nome = st.selectbox("Item Utilizado", df_estoque.iloc[:, 0].tolist())
            
            with col_b:
                qtd_usada = st.number_input("Quantidade", min_value=1, step=1)
                os_numero = st.text_input("Nº da Ordem de Serviço (O.S.)")
            
            botao_confirmar = st.form_submit_button("Confirmar Saída de Material")
            
            if botao_confirmar:
                # Localiza a linha do item (considerando que o nome está na coluna 0)
                idx = df_estoque[df_estoque.iloc[:, 0] == item_nome].index[0]
                saldo_atual = df_estoque.iat[idx, 1] # Coluna 1 deve ser a Quantidade
                
                if saldo_atual >= qtd_usada:
                    # 1. Atualiza o DataFrame de estoque localmente
                    df_estoque.iat[idx, 1] = saldo_atual - qtd_usada
                    
                    # 2. Cria o registro para o Histórico
                    novo_log = pd.DataFrame([{
                        "data": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                        "tecnico": "Carlos Eduardo",
                        "veiculo": "SYG9H50",
                        "cliente": cliente,
                        "os": os_numero,
                        "item": item_nome,
                        "qtd_retirada": qtd_usada
                    }])

                    # Carrega histórico atual e anexa o novo
                    df_hist = carregar_historico()
                    df_hist_atualizado = pd.concat([df_hist, novo_log], ignore_index=True)

                    # 3. SALVAMENTO NO GOOGLE SHEETS
                    try:
                        conn.update(worksheet="estoque", data=df_estoque)
                        conn.update(worksheet="historico", data=df_hist_atualizado)
                        
                        st.success(f"✅ Baixa de {item_nome} registrada com sucesso!")
                        st.balloons()
                        st.rerun()
                    except Exception as error:
                        st.error(f"Erro ao salvar na planilha: {error}")
                else:
                    st.error(f"❌ Saldo insuficiente! Saldo atual: {saldo_atual}")

except Exception as e:
    st.error("🚨 Erro de Sincronização ou Formatação da Planilha")
    st.info("Verifique se as abas 'estoque' e 'historico' existem e se as colunas estão corretas.")
    st.code(str(e))
