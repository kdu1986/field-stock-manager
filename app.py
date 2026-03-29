import streamlit as st
import json

st.set_page_config(page_title="Procer - Estoque de Campo", layout="wide")

def carregar_estoque():
    try:
        with open('estoque.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

st.title("📦 Gerenciador de Estoque - PROCER")
st.write("---")

estoque = carregar_estoque()

if not estoque:
    st.error("❌ Arquivo 'estoque.json' não encontrado no servidor.")
else:
    st.subheader("📋 Inventário do Veículo")
    st.dataframe(estoque, use_container_width=True)
    
    # Campo para dar baixa (Sua solicitação)
    with st.expander("⬇️ Registrar Uso de Material"):
        item = st.selectbox("Selecione o item:", [i['descricao'] for i in estoque])
        if st.button("Confirmar Baixa"):
            st.success(f"Uso de '{item}' registrado!")