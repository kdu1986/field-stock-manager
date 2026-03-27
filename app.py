import streamlit as st
import json

# Configuração de Interface SOC/Procer
st.set_page_config(page_title="Procer - Estoque de Campo", layout="wide")

def carregar_estoque():
    try:
        with open('estoque.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

# Título do Sistema
st.title("📦 Gerenciador de Estoque de Campo")
st.write("---")

estoque = carregar_estoque()

if not estoque:
    st.error("❌ Arquivo 'estoque.json' não encontrado no servidor.")
else:
    # 1. Dashboard de Alertas
    itens_criticos = [i for i in estoque if i['qtd'] <= 2]
    if itens_criticos:
        st.warning(f"🚨 Existem {len(itens_criticos)} itens com estoque crítico!")

    # 2. Área de Baixa de Material
    with st.expander("⬇️ Dar baixa em material (Uso em campo)"):
        item_selecionado = st.selectbox("Selecione o item:", [i['descricao'] for i in estoque])
        quantidade_usada = st.number_input("Quantidade utilizada:", min_value=1, value=1)
        
        if st.button("Confirmar Baixa"):
            st.success(f"Baixa de {quantidade_usada} un. de '{item_selecionado}' registrada com sucesso!")

    # 3. Tabela de Inventário
    st.subheader("📋 Inventário do Veículo")
    st.dataframe(estoque, use_container_width=True)