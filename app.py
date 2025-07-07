import streamlit as st
from transform import *

st.title('Gerador de plano de aula')
st.caption('Preencha o formulário e submeta para baixar o plano!')

data = 'Escopo.xlsx'
disci = disciplinas(data)
disciplina = st.selectbox('Disciplina', disci)
ano = st.selectbox('Ano/série:', ['1ª', '2ª', '3ª'])
bimestre = st.selectbox('Bimestre', ['1º', '2º', '3º', '4º'])
aulas = []

if disciplina:
    df = data_frame(data, disciplina)
    aula = qtde_aulas(df, ano, bimestre)
    for a in range(1, aula + 1):
        aulas.append(a)
    opc = st.multiselect('Selecione',aulas)
    for option in opc:
        st.dataframe(filtro(df, ano, bimestre, option))
            



