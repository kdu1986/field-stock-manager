import streamlit as st
import json

# 🛡️ Configuração de Interface SOC/Procer
st.set_page_config(page_title="Procer - Estoque de Campo", layout="centered")

def carregar_estoque():
    try:
        # Abre com utf-8-sig para ignorar caracteres invisíveis do Windows
        with open('estoque.json', 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except Exception as e:
        return []

# --- CABEÇALHO ---
# Tenta carregar a logo da Procer se o arquivo existir no seu GitHub
try:
    st.image("procertecnologia_logo.jpeg", width=250)
except:
    st.title("📦 Gerenciador de Estoque - PROCER")

st.write("---")

estoque = carregar_estoque()

if not estoque:
    st.error("❌ Erro de Integridade: Arquivo 'estoque.json' não encontrado ou corrompido.")
else:
    # --- ALERTAS DE CAMPO ---
    itens_criticos = [i for i in estoque if i['qtd'] <= 1]
    if itens_criticos:
        st.warning(f"🚨 Atenção: {len(itens_criticos)} itens com estoque crítico!")

    # --- TABELA DE INVENTÁRIO (LAYOUT AJUSTADO) ---
    st.subheader("📋 Inventário do Veículo")
    
    col_config = {
        "descricao": st.column_config.TextColumn("Descrição", width="large"),
        "qtd": st.column_config.NumberColumn("Qtd", width="small"),
        "categoria": st.column_config.TextColumn("Categoria", width="medium"),
    }

    st.dataframe(
        estoque, 
        column_config=col_config, 
        hide_index=True, 
        use_container_width=True
    )

    # --- ÁREA DE BAIXA (INTERATIVO) ---
    st.write("---")
    with st.expander("⬇️ Registrar Uso de Material em Cliente"):
        item_selecionado = st.selectbox("Selecione o material utilizado:", [i['descricao'] for i in estoque])
        if st.button("Confirmar Baixa no Sistema"):
            st.success(f"Baixa de '{item_selecionado}' registrada com sucesso!")
            st.info("Sincronize com o servidor para persistir a alteração.")