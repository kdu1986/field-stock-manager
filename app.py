import json
import os

def carregar_estoque():
    # Isso garante que ele ache o arquivo mesmo se você mudar de pasta
    diretorio_atual = os.path.dirname(__file__)
    caminho_json = os.path.join(diretorio_atual, 'estoque.json')
    
    try:
        # Usamos 'utf-8-sig' para evitar erros de formatação do Windows/Excel
        with open(caminho_json, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {caminho_json}")
        return []
    except json.JSONDecodeError:
        print("Erro: O arquivo estoque.json contém erros de digitação (vírgula faltando ou aspas).")
        return []

def verificar_alertas(estoque):
    print("\n" + "="*30)
    print("RELATÓRIO DE ESTOQUE CRÍTICO")
    print("="*30)
    
    itens_faltantes = [i for i in estoque if i['qtd'] == 0]
    
    if not itens_faltantes:
        print("✅ Tudo em dia no carro!")
    else:
        for item in itens_faltantes:
            print(f"⚠️ REPOSIÇÃO: {item['descricao']}")
    print("="*30 + "\n")

if __name__ == "__main__":
    dados = carregar_estoque()
    verificar_alertas(dados)