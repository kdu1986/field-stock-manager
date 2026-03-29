import streamlit as st
from streamlit_gsheets import GSheetsConnection

# 🛡️ Configuração de Interface
st.set_page_config(page_title="Procer - Estoque Realtime", layout="centered")

# --- CONEXÃO COM O BANCO (GOOGLE SHEETS) ---
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    # ttl=0 garante que ele sempre pegue o dado mais novo da planilha
    return conn.read(worksheet="estoque", ttl=0)

# --- CABEÇALHO ---
try:
    st.image("procertecnologia_logo.jpeg", width=250)
except:
    st.title("📦 Gerenciador de Estoque - PROCER")

st.write("---")

# Interface Principal
try:
    df = carregar_dados()

    # Tabela de Inventário
    st.subheader("📋 Inventário do Veículo (Sincronizado)")
    st.dataframe(df, hide_index=True, use_container_width=True)

    # Área de Baixa
    st.write("---")
    with st.expander("⬇️ Registrar Uso de Material"):
        with st.form("baixa_form"):
            item_sel = st.selectbox("Selecione o item:", df['descricao'].tolist())
            qtd_baixa = st.number_input("Quantidade utilizada:", min_value=1, value=1)
            btn_confirmar = st.form_submit_button("Confirmar Baixa na Planilha")

            if btn_confirmar:
                # Localiza e atualiza
                idx = df.index[df['descricao'] == item_sel].tolist()[0]
                if df.at[idx, 'qtd'] >= qtd_baixa:
                    df.at[idx, 'qtd'] -= qtd_baixa
                    
                    # SALVA DE VOLTA NO GOOGLE SHEETS
                    conn.update(worksheet="estoque", data=df)
                    
                    st.success(f"✅ Baixa de {item_sel} realizada com sucesso!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Erro: Estoque insuficiente na planilha!")

except Exception as e:
    st.error("⚠️ Erro de Conexão: Verifique se o link nos Secrets está correto.")
    st.info("Certifique-se de que a planilha está compartilhada como 'Editor'.")