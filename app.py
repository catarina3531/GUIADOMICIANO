import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Configuração da Página
st.set_page_config(
    page_title="Portal de Vendas & CRM",
    page_icon="💼",
    layout="wide"
)

# Função para conectar ao Google Sheets de forma segura via Secrets
@st.cache_resource
def conectar_gsheets():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = dict(st.secrets["connections"]["gsheets"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    
    url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    return client.open_by_url(url)

try:
    spreadsheet = conectar_gsheets()
except Exception as e:
    st.error(f"Erro ao conectar com o Google Sheets: {e}")

# Menu Lateral
st.sidebar.title("Menu de Navegação")
menu = st.sidebar.radio("Escolha uma opção:", ["Dashboard", "Clientes & CRM", "Vendas e Comissões", "Gerador de Propostas"])

if menu == "Dashboard":
    st.title("📊 Visão Geral")
    st.metric(label="Comissões do Mês", value="R$ 4.500,00", delta="+12%")
    st.metric(label="Clientes para Contatar Hoje", value="3")
    
    try:
        sheet_clientes = spreadsheet.worksheet("Clientes")
        dados = sheet_clientes.get_all_records()
        if dados:
            df_clientes = pd.DataFrame(dados)
            st.subheader("Clientes Cadastrados Recentemente")
            st.dataframe(df_clientes.tail(5), use_container_width=True)
        else:
            st.info("A planilha 'Clientes' está vazia.")
    except Exception:
        st.info("Cadastre o primeiro cliente na aba 'Clientes & CRM' para começar!")

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
                    sheet_clientes = spreadsheet.worksheet("Clientes")
                    nova_linha = [empresa, comprador, contato, categoria, str(proximo_contato), observacao]
                    sheet_clientes.append_row(nova_linha)
                    st.success(f"Cliente {empresa} cadastrado com sucesso na planilha!")
                except Exception as e:
                    st.error(f"Erro ao salvar na planilha: {e}")
            else:
                st.warning("Por favor, preencha pelo menos o Nome da Empresa.")

    st.divider()
    st.subheader("Base de Clientes")
    try:
        sheet_clientes = spreadsheet.worksheet("Clientes")
        dados = sheet_clientes.get_all_records()
        if dados:
            df_clientes = pd.DataFrame(dados)
            st.dataframe(df_clientes, use_container_width=True)
        else:
            st.info("Nenhum cliente cadastrado ainda.")
    except Exception as e:
        st.warning("Certifique-se de que a aba 'Clientes' existe na planilha e possui os cabeçalhos corretos.")

elif menu == "Vendas e Comissões":
    st.title("💰 Vendas e Comissões")
    st.write("Acompanhamento de faturamento e comissões a receber.")

elif menu == "Gerador de Propostas":
    st.title("📄 Gerador de Propostas Comerciais")
    st.write("Preencha os dados para gerar a proposta em formato limpo.")
