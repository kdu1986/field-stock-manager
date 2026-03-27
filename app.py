import streamlit as st
import json

# Configuração da página
st.set_page_config(page_title="Procer - Estoque de Campo", layout="wide")

def carregar_estoque():
    try:
        with open('estoque.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Interface Visual
st.title("📦 Gerenciador de Estoque de Campo")
st.write("---")

estoque = carregar_estoque()

if not estoque:
    st.warning("⚠️ Arquivo estoque.json não encontrado ou vazio.")
else:
    # Métricas rápidas
    col1, col2 = st.columns(2)
    itens_criticos = [i for i in estoque if i['qtd'] <= 2]
    
    with col1:
        st.metric("Total de Itens", len(estoque))
    with col2:
        st.metric("Itens Críticos", len(itens_criticos), delta_color="inverse")

    st.subheader("📋 Inventário Atual")
    st.table(estoque)

    if itens_criticos:
        st.error("🚨 **ALERTA DE REPOSIÇÃO NECESSÁRIA:**")
        for item in itens_criticos:
            st.write(f"- {item['descricao']} (Restam apenas {item['qtd']})")
    else:
        st.success("✅ Tudo em dia no carro!")