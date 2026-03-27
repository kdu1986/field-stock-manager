import streamlit as st
import json

# Configuração da página - Identidade Visual Procer
st.set_page_config(page_title="Procer - Estoque de Campo", layout="wide")

def carregar_estoque():
    try:
        with open('estoque.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Interface Visual do Sistema
st.title("📦 Gerenciador de Estoque de Campo - PROCER")
st.write("---")

estoque = carregar_estoque()

if not estoque:
    st.warning("⚠️ Arquivo estoque.json não encontrado ou vazio no servidor.")
else:
    # Painel de Indicadores (Dashboard)
    col1, col2 = st.columns(2)
    itens_criticos = [i for i in estoque if i['qtd'] <= 2]
    
    with col1:
        st.metric("Total de Itens", len(estoque))
    with col2:
        st.metric("Itens com Estoque Baixo", len(itens_criticos))

    st.subheader("📋 Inventário Atual")
    # Exibe a tabela de forma amigável
    st.dataframe(estoque, use_container_width=True)

    if itens_criticos:
        st.error("🚨 **ATENÇÃO: REPOSIÇÃO NECESSÁRIA**")
        for item in itens_criticos:
            st.write(f"- {item['descricao']} (Quantidade atual: {item['qtd']})")
    else:
        st.success("✅ Todos os componentes de automação estão em níveis seguros no veículo.")