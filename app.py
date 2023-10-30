# app.py

import streamlit as st
import pandas as pd
from pydantic import ValidationError
from models import Vendas

def validar_dados(dataframe):
    """
    Validadar dados do modelo Pydantic
    """
    erros = []
    for _, row in dataframe.iterrows():  # Iterando através das linhas do DataFrame
        try:
            # Convertendo a linha do DataFrame para um dicionário e validando
            Vendas(**row.to_dict())
        except ValidationError as e:
            erros.append(e.json())

    if erros:
        return False, erros
    
    return True, "Todos os registros são válidos!"  # Retornando mensagem de sucesso

    uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=['xlsx'])

    if uploded_file:
        try:
            # Ler o arquivo Excel com o Pandas
            df = pd.read_excel(uploaded_file, engine='openpyxl',index_col=none)

            # Validação dos dados com o esquema Pydantic
            sucesso, mensagem = validar_dados(df) # passando o DataFrame para a função validar_dados

            if sucesso:
                st.success(mensagem)
            else:
                st.error('Erro de validaçao	encontrado!')
                for erro in mensagem: # Iterando sobre cada erro e imprimindo na tela
                    st.json(erro) # Imprimindo o erro em formato JSON


        except:
            st.error(f"Ocorreu um erro:{e}")