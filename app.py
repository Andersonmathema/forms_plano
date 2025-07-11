import streamlit as st
from datetime import date, datetime
from transform import *
from modelo import substituir
from gerador import gemini_ativi, gemini_estrat, gemini_rec
import io

st.title('Gerador de plano de aula')
st.caption('Preencha o formulário e edite os campos abaixo para gerar seu plano!')

planilha = 'Escopo.xlsx'
modelo_docx = './Modelo Plano de AULA.docx'

# Dados iniciais
nome = st.text_input('Seu nome')
disci = disciplinas(planilha)
disciplina = st.selectbox('Disciplina', disci)
ano = st.selectbox('Ano/série:', ['1ª', '2ª', '3ª'])
bimestre = st.selectbox('Bimestre', ['1º', '2º', '3º', '4º'])
faixa_data = st.date_input(
    "Faixa de dias do plano",
    (date(2025, 1, 1), date(2025, 1, 31)),
    min_value=date(2025, 1, 1),
    max_value=date(2025, 12, 31),
    format="DD/MM/YYYY"
)
opcoes = ["Material digital", "Plataformas", "Livro do aluno", "Outros"]

recursos = []
for opcao in opcoes:
    if st.checkbox(opcao):
        recursos.append(opcao)

aulas = []
buffer = None  # Inicializa fora do bloco

if disciplina:
    df = data_frame(planilha, disciplina)
    qt_aula = qtde_aulas(df, ano, bimestre)
    for a in range(1, qt_aula + 1):
        aulas.append(a)

    aula = st.multiselect('Selecione as aulas desejadas', aulas)

    if aula:
        aula_key = "_".join(map(str, aula))
        dataf = filtro(df, ano, bimestre, aula)
        data_atual = datetime.now().strftime('%d/%m/%Y')

        st.markdown("### Visualize os dados filtrados:")
        st.dataframe(dataf)

        # Textos editáveis gerados pelo Gemini
        with st.spinner("⏳ Gerando conteúdo do plano de aula... isso pode levar alguns segundos..."):
            if f"atividades_{aula_key}" not in st.session_state:
                st.session_state[f"atividades_{aula_key}"] = gemini_ativi(dataf['CONTEÚDO'].unique()[0])
                st.session_state[f"estrategias_{aula_key}"] = gemini_estrat(dataf['OBJETIVOS'].unique()[0])
                st.session_state[f"recuperacao_{aula_key}"] = gemini_rec(dataf['OBJETIVOS'].unique()[0])

        
        texto_atividades = st.text_area(
            "📝 Atividades sugeridas",
            st.session_state[f"atividades_{aula_key}"],
            height=150
            )
        texto_estrategias = st.text_area(
            "📚 Estratégias de ensino",
            st.session_state[f"estrategias_{aula_key}"],
            height=250
            )
        texto_recuperacao = st.text_area(
            "🔁 Recuperação/Avaliação",
            st.session_state[f"recuperacao_{aula_key}"],
            height=150
            )

        # Geração do documento
        doc = substituir(
            modelo_path=modelo_docx,
            nome=nome,
            disciplina=disciplina,
            serie=ano,
            bimestre=bimestre,
            objeto_conhecimento=dataf['OBJETOS DO CONHECIMENTO'].unique()[0],
            habilidades=dataf['HABILIDADE'].unique()[0],
            atividades=texto_atividades,
            recursos= recursos,
            estrategias=texto_estrategias,
            recuperacao=texto_recuperacao,
            semana_1='Polígonos e Classificação',
            semana_2='Perímetros de figuras planas',
            semana_3='Cálculo de áreas',
            semana_4='Volume de sólidos geométricos',
            data_inicio=faixa_data[0].strftime('%d/%m/%Y'),
            data_fim=faixa_data[1].strftime('%d/%m/%Y'),
            data_atual=data_atual
        )

        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)        

        button = st.download_button(
            label="📥 Baixar plano de aula",
            data=buffer,
            file_name=f"Plano_{nome}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        if button:
            st.success("✅ Plano de aula gerado com sucesso!")