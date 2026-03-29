import streamlit as st
import json

# Configuração da Página para Web
st.set_page_config(page_title="Procer - Estoque de Campo", layout="wide")

def carregar_estoque():
    try:
        # Garante a leitura correta do JSON
        with open('estoque.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Interface Visual do Streamlit
st.title("📦 Gerenciador de Estoque - PROCER")
st.write("---")

estoque = carregar_estoque()

if not estoque:
    st.error("❌ Arquivo 'estoque.json' não encontrado ou vazio no servidor.")
else:
    # Painel de Alertas
    itens_faltantes = [i for i in estoque if i['qtd'] == 0]
    
    if itens_faltantes:
        st.warning(f"🚨 Atenção: {len(itens_faltantes)} itens precisam de reposição!")
    
    # Exibição da Tabela na Web
    st.subheader("📋 Inventário do Veículo")
    st.dataframe(estoque, use_container_width=True)

    # Funcionalidade de Baixa (Interativo)
    with st.expander("⬇️ Registrar Uso de Material"):
        item_sel = st.selectbox("Selecione o item:", [i['descricao'] for i in estoque])
        if st.button("Confirmar Baixa"):
            st.success(f"Uso de '{item_sel}' registrado com sucesso!")