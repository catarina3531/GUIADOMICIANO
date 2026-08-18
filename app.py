import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(
    page_title="Portal de Vendas & CRM",
    page_icon="💼",
    layout="wide"
)

# Menu Lateral
st.sidebar.title("Menu de Navegação")
menu = st.sidebar.radio("Escolha uma opção:", ["Dashboard", "Clientes & CRM", "Vendas e Comissões", "Gerador de Propostas"])

if menu == "Dashboard":
    st.title("📊 Visão Geral")
    st.metric(label="Comissões do Mês", value="R$ 4.500,00", delta="+12%")
    st.metric(label="Clientes para Contatar Hoje", value="3")
    st.info("Aqui colocaremos os gráficos de desempenho e lembretes importantes.")

elif menu == "Clientes & CRM":
    st.title("👥 Gestão de Clientes e Prospecção")
    
    with st.form("form_cliente"):
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
            st.success(f"Cliente {empresa} cadastrado com sucesso!")
            # Aqui faremos a integração para salvar no Google Sheets

elif menu == "Vendas e Comissões":
    st.title("💰 Vendas e Comissões")
    st.write("Acompanhamento de faturamento e comissões a receber.")

elif menu == "Gerador de Propostas":
    st.title("📄 Gerador de Propostas Comerciais")
    st.write("Preencha os dados para gerar a proposta em formato limpo.")
