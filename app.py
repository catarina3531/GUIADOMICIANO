import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Configuração da Página
st.set_page_config(
    page_title="Portal de Vendas & CRM",
    page_icon="💼",
    layout="wide"
)

# Criando a conexão com o Google Sheets usando a URL fornecida
conn = st.connection("gsheets", type=GSheetsConnection)

# Menu Lateral
st.sidebar.title("Menu de Navegação")
menu = st.sidebar.radio("Escolha uma opção:", ["Dashboard", "Clientes & CRM", "Vendas e Comissões", "Gerador de Propostas"])

if menu == "Dashboard":
    st.title("📊 Visão Geral")
    st.metric(label="Comissões do Mês", value="R$ 4.500,00", delta="+12%")
    st.metric(label="Clientes para Contatar Hoje", value="3")
    
    # Exemplo de leitura rápida dos dados da planilha na visão geral
    try:
        df_clientes = conn.read(worksheet="Clientes", ttl=5)
        st.subheader("Clientes Cadastrados Recentemente")
        st.dataframe(df_clientes.tail(5), use_container_width=True)
    except Exception as e:
        st.info("Cadastre o primeiro cliente na aba 'Clientes & CRM' para começar a visualizar os dados aqui!")

elif menu == "Clientes & CRM":
    st.title("👥 Gestão de Clientes e Prospecção")
    
    with st.form("form_cliente", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            empresa = st.text_input("Nome da Empresa")
            comprador = st.text_input("Nome do Comprador")
            contato = st.text_input("Contato (Telefone / E-mail)")
        with col2:
            categoria = st.selectbox("Categoria do Contato", ["Indústria", "Transformação", "Distribuidor"])
            proximo_contato = st.date_input("Data para Próximo Contato")
        
        observacao = st.text_area("Retorno dos contatos / Anotações")
        
        submitted = st.form_submit_button("Salvar Cliente")
        
        if submitted:
            if empresa:
                try:
                    # Prepara a nova linha de dados
                    novo_cliente = pd.DataFrame([{
                        "Empresa": empresa,
                        "Comprador": comprador,
                        "Contato": contato,
                        "Categoria": categoria,
                        "Proximo Contato": str(proximo_contato),
                        "Observacao": observacao
                    }])

                    # Lê os dados atuais, concatena o novo e atualiza a planilha
                    existing_data = conn.read(worksheet="Clientes", ttl=0)
                    updated_df = pd.concat([existing_data, novo_cliente], ignore_index=True)
                    conn.update(worksheet="Clientes", data=updated_df)
                    
                    st.success(f"Cliente {empresa} cadastrado com sucesso na planilha!")
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")
            else:
                st.warning("Por favor, preencha pelo menos o Nome da Empresa.")

    # Exibindo a base de clientes atualizada abaixo do formulário
    st.divider()
    st.subheader("Base de Clientes")
    try:
        df_clientes = conn.read(worksheet="Clientes", ttl=5)
        st.dataframe(df_clientes, use_container_width=True)
    except Exception as e:
        st.info("A aba 'Clientes' na sua planilha precisa ter os cabeçalhos configurados (Empresa, Comprador, Contato, Categoria, Proximo Contato, Observacao).")

elif menu == "Vendas e Comissões":
    st.title("💰 Vendas e Comissões")
    st.write("Acompanhamento de faturamento e comissões a receber.")

elif menu == "Gerador de Propostas":
    st.title("📄 Gerador de Propostas Comerciais")
    st.write("Preencha os dados para gerar a proposta em formato limpo.")
