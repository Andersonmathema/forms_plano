import streamlit as st
from datetime import date, datetime, timedelta
from transform import *
from modelo import substituir
from gerador import gemini_ativi, gemini_estrat, gemini_rec
import io

st.title('Gerador de plano de aula')
st.caption('Preencha o formulário e edite os campos abaixo para gerar seu plano!')

# Aumentar as opções de escopo
planilha = 'Escopo.xlsx'
modelo_docx = './Plano de Aula 3o. Bimestre - Agosto.docx'

# Dados iniciais
nome = st.text_input('Seu nome')
disci = disciplinas(planilha)
disciplina = st.selectbox('Disciplina', disci)
ano = st.selectbox('Ano/série:', ['1ª', '2ª', '3ª'])
bimestre = st.selectbox('Bimestre', ['1º', '2º', '3º', '4º'])
faixa_data = st.date_input(
    "Faixa de dias do plano",
    (date(2025, 7, 21), date(2025, 12, 31)),
    min_value=date(2025, 7, 21),
    max_value=date(2025, 12, 31),
    format="DD/MM/YYYY"
)
# Garante que sempre temos início e fim sem erro
if isinstance(faixa_data, tuple) and len(faixa_data) == 2:
    data_inicio = faixa_data[0]
    data_fim = faixa_data[1]
else:
    # Enquanto o usuário ainda não selecionou a segunda data
    data_inicio = faixa_data[0] if isinstance(faixa_data, tuple) else faixa_data
    data_fim = data_inicio  # usa a mesma data como padrão

# Calcula datas automaticamente
data_s1_fim = data_inicio + timedelta(days=4)
data_s2_inicio = data_inicio + timedelta(days=7)
data_s2_fim = data_inicio + timedelta(days=11)

# Só converte para string quando for usar nos placeholders
data_inicio_str = data_inicio.strftime('%d/%m/%Y')
data_fim_str = data_fim.strftime('%d/%m/%Y')
data_s1_fim_str = data_s1_fim.strftime('%d/%m/%Y')
data_s2_inicio_str = data_s2_inicio.strftime('%d/%m/%Y')
data_s2_fim_str = data_s2_fim.strftime('%d/%m/%Y')

data_atual = datetime.now().strftime('%d/%m/%Y')

opcoes = ["Material digital do Componente",
          "Livro do Estudante 'Currículo em Ação'",
          "Livro 'São Paulo em Ação' – Orientação de Estudos",
          "Plataforma digital",
          "Outros",
          ]

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

            gerar = st.button(f"Gerar conteúdo para Aula {a}")

            if gerar:
                with st.spinner(f"⏳ Gerando conteúdo para Aula {a}..."):
                    if f"atividades_{aula_key}" not in st.session_state:
                        st.warning("Professor, REVISE o conteúdo descrito!")
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
                
                # Datas
                data_inicio=data_inicio_str,
                data_fim=data_fim_str,
                data_atual=data_atual,

                # Semana 1
                objeto_conhecimento_1=objeto_conhecimento_1,
                habilidades_1=habilidades_1,
                atividades_1=atividades_1,
                recursos=recursos_texto,
                estrategias_1=estrategias_1,
                recuperacao_1=recuperacao_1,
                semana_1=f"{data_inicio_str} à {data_s1_fim_str}" if len(aula) >= 1 else "",

                # Semana 2 (se houver)
                objeto_conhecimento_2=objeto_conhecimento_2 if len(aula) > 1 else "",
                habilidades_2=habilidades_2 if len(aula) > 1 else "",
                atividades_2=atividades_2 if len(aula) > 1 else "",
                estrategias_2=estrategias_2 if len(aula) > 1 else "",
                recuperacao_2=recuperacao_2 if len(aula) > 1 else "",
                semana_2=f"{data_s2_inicio_str} à {data_s2_fim_str}" if len(aula) > 1 else "",
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

