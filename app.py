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
recursos_texto = ", ".join(recursos)

aulas = []
buffer = None

if disciplina:
    df = data_frame(planilha, disciplina)
    qt_aula = qtde_aulas(df, ano, bimestre)
    for a in range(1, qt_aula + 1):
        aulas.append(a)

    aula = st.multiselect(
        'Selecione as aulas desejadas',
        aulas,
        max_selections=2,
        placeholder="Escolha as aulas (máximo 2 aulas)"
    )

    if aula:
        data_atual = datetime.now().strftime('%d/%m/%Y')

        # Inicializa variáveis para cada semana (caso só 1 aula seja escolhida)
        atividades_1 = estrategias_1 = recuperacao_1 = ""
        atividades_2 = estrategias_2 = recuperacao_2 = ""
        objeto_conhecimento_1 = habilidades_1 = ""
        objeto_conhecimento_2 = habilidades_2 = ""

        for idx, a in enumerate(aula, start=1):
            dataf = filtro(df, ano, bimestre, [a])
            aula_key = f"aula_{a}"

            # Pega apenas o primeiro valor de cada campo (não a lista completa)
            objeto_conhecimento = dataf['OBJETOS DO CONHECIMENTO'].dropna().unique()[0]
            habilidades = dataf['HABILIDADE'].dropna().unique()[0]

            st.markdown(f"### Aula {a}")
            st.dataframe(dataf)

            gerar = st.button(f"Gerar atividades para Aula {a}")

            if gerar:
                with st.spinner(f"⏳ Gerando conteúdo para Aula {a}..."):
                    if f"atividades_{aula_key}" not in st.session_state:
                        st.session_state[f"atividades_{aula_key}"] = gemini_ativi(
                            " ".join(dataf['CONTEÚDO'].dropna())
                        )
                        st.session_state[f"estrategias_{aula_key}"] = gemini_estrat(
                            " ".join(dataf['OBJETIVOS'].dropna())
                        )
                        st.session_state[f"recuperacao_{aula_key}"] = gemini_rec(
                            " ".join(dataf['OBJETIVOS'].dropna())
                        )

            # Campos editáveis para cada aula
            texto_atividades = st.text_area(
                f"📝 Atividades sugeridas - Aula {a}",
                st.session_state.get(f"atividades_{aula_key}", ""),
                height=150
            )
            texto_estrategias = st.text_area(
                f"📚 Estratégias de ensino - Aula {a}",
                st.session_state.get(f"estrategias_{aula_key}", ""),
                height=200
            )
            texto_recuperacao = st.text_area(
                f"🔁 Recuperação/Avaliação - Aula {a}",
                st.session_state.get(f"recuperacao_{aula_key}", ""),
                height=150
            )

            # Salva os valores de cada semana
            if idx == 1:
                atividades_1, estrategias_1, recuperacao_1 = texto_atividades, texto_estrategias, texto_recuperacao
                objeto_conhecimento_1, habilidades_1 = objeto_conhecimento, habilidades
            elif idx == 2:
                atividades_2, estrategias_2, recuperacao_2 = texto_atividades, texto_estrategias, texto_recuperacao
                objeto_conhecimento_2, habilidades_2 = objeto_conhecimento, habilidades

        # Garante que nenhum campo fique em branco
        if not atividades_1:
            atividades_1 = "Atividades não informadas"
        if not estrategias_1:
            estrategias_1 = "Estratégias não informadas"
        if not recuperacao_1:
            recuperacao_1 = "Plano de recuperação não informado"
        if not objeto_conhecimento_1:
            objeto_conhecimento_1 = "Objeto do conhecimento não informado"
        if not habilidades_1:
            habilidades_1 = "Habilidades não informadas"

        if len(aula) > 1:
            if not atividades_2:
                atividades_2 = "Atividades não informadas"
            if not estrategias_2:
                estrategias_2 = "Estratégias não informadas"
            if not recuperacao_2:
                recuperacao_2 = "Plano de recuperação não informado"
            if not objeto_conhecimento_2:
                objeto_conhecimento_2 = "Objeto do conhecimento não informado"
            if not habilidades_2:
                habilidades_2 = "Habilidades não informadas"

        # Geração final do documento
        if st.button("Gerar documento final"):
            doc = substituir(
                modelo_path=modelo_docx,
                nome=nome,
                disciplina=disciplina,
                serie=ano,
                bimestre=bimestre,

                # Semana 1
                objeto_conhecimento_1=objeto_conhecimento_1,
                habilidades_1=habilidades_1,
                atividades_1=atividades_1,
                recursos=recursos_texto,
                estrategias_1=estrategias_1,
                recuperacao_1=recuperacao_1,
                semana_1=f"Aula {aula[0]}" if len(aula) >= 1 else "",

                # Semana 2 (se houver)
                objeto_conhecimento_2=objeto_conhecimento_2 if len(aula) > 1 else "",
                habilidades_2=habilidades_2 if len(aula) > 1 else "",
                atividades_2=atividades_2 if len(aula) > 1 else "",
                estrategias_2=estrategias_2 if len(aula) > 1 else "",
                recuperacao_2=recuperacao_2 if len(aula) > 1 else "",
                semana_2=f"Aula {aula[1]}" if len(aula) > 1 else "",

                # Datas
                data_inicio=faixa_data[0].strftime('%d/%m/%Y'),
                data_fim=faixa_data[1].strftime('%d/%m/%Y'),
                data_atual=data_atual
            )

            buffer = io.BytesIO()
            doc.save(buffer)
            buffer.seek(0)

            st.success("✅ Plano de aula gerado com sucesso!")
            st.download_button(
                label="📥 Baixar plano de aula",
                data=buffer,
                file_name=f"Plano_{nome}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

