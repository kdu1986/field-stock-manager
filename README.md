# 📡 Sistema de Gestão de Insumos - Unidade de Campo (Procer)

Este projeto foi desenvolvido para otimizar o controle de estoque em veículos de assistência técnica em campo, permitindo o registro de baixas por cliente e alertas de reposição.

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.13
* **Interface:** Streamlit (Framework Web)
* **Manipulação de Dados:** Pandas & JSON
* **Contexto Acadêmico:** Projeto desenvolvido para o curso de Cybersecurity (Anhanguera / Unicesumar)

## 🚀 Funcionalidades
- **Autenticação de Segurança:** Acesso restrito para o modo administrador (Técnico Carlos Eduardo).
- **Gestão por Cliente:** Registro de material utilizado com campo para observação técnica e nome do cliente (Ex: Agrofertil, Agroxisto).
- **Histórico:** Log de movimentações para auditoria e controle de custos.
- **Alertas Críticos:** Notificação automática de itens com estoque baixo (Termometria, Módulos Ceres, etc).

## 📁 Estrutura do Projeto
- `interface.py`: Código principal da aplicação.
- `estoque.json`: Banco de dados em formato JSON para portabilidade.
- `historico.json`: Registro de todas as baixas realizadas.