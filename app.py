import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Procer - Gestão Full", layout="wide")

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Lê a planilha sem forçar o nome da aba primeiro para testar
    df = conn.read(ttl=0)
    
    st.image("procertecnologia_logo.jpeg", width=250)
    st.subheader("📋 Inventário PROCER")
    st.dataframe(df, hide_index=True, use_container_width=True)

    st.write("---")
    
    # Formulário de Atualização
    with st.form("baixa"):
        st.subheader("🔄 Atualizar Estoque")
        # Usamos a primeira coluna independente do nome
        item = st.selectbox("Selecione o Material:", df.iloc[:, 0].tolist())
        nova_q = st.number_input("Nova Quantidade:", min_value=0, step=1)
        if st.form_submit_button("Salvar na Nuvem"):
            # Acha a linha e atualiza a segunda coluna (qtd)
            idx = df[df.iloc[:, 0] == item].index[0]
            df.iat[idx, 1] = nova_q
            conn.update(data=df)
            st.success("✅ Sincronizado com sucesso!")
            st.rerun()
            
except Exception as e:
    st.error("🚨 Erro de Sincronização")
    st.code(str(e))