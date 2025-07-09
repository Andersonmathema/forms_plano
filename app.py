import streamlit as st
from datetime import date
from transform import *

st.title('Gerador de plano de aula')
st.caption('Preencha o formulário e submeta para baixar o plano!')

data = 'Escopo.xlsx'
nome = st.text_input('Seu nome')
disci = disciplinas(data)
disciplina = st.selectbox('Disciplina', disci)
ano = st.selectbox('Ano/série:', ['1ª', '2ª', '3ª'])
bimestre = st.selectbox('Bimestre', ['1º', '2º', '3º', '4º'])
faixa_data = st.date_input("Faixa de dias do plano",
    (date(2025, 1, 1), date(2025, 1, 31)),
    min_value= date(2025, 1, 1),
    max_value= date(2025, 12, 31),
    format="DD.MM.YYYY",
)
aulas = []

if disciplina:
    df = data_frame(data, disciplina)
    aula = qtde_aulas(df, ano, bimestre)
    for a in range(1, aula + 1):
        aulas.append(a)
    opc = st.multiselect('Selecione',aulas)
    st.text(aulas)
            