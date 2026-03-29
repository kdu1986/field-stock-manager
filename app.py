import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Procer Stock", layout="centered")

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Tenta ler sem especificar o nome da aba para testar a conexão básica
    df = conn.read(ttl=0) 
    
    st.image("procertecnologia_logo.jpeg", width=250)
    st.subheader("📋 Inventário Realtime")
    st.dataframe(df, hide_index=True, use_container_width=True)
    
except Exception as e:
    st.error("🚨 Erro Crítico de Conexão")
    st.write("Detalhe técnico para o Carlos:")
    st.code(str(e)) # Isso vai nos mostrar o erro real que o Google está devolvendo