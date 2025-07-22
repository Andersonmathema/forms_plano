import streamlit as st
from transform import *
from modelo import substituir
from gerador import gemini_ativi, gemini_estrat, gemini_rec, gemini_flex, gemini_autoaval
import io

st.title('Gerador de Plano de Aula (3 Semanas)')
st.caption('Preencha os campos abaixo e edite os textos antes de gerar o documento final.')

planilha = 'Escopo.xlsx'
modelo_docx = './Plano de Aula 3o. Bimestre - Agosto.docx'

# Dados iniciais
nome = st.text_input('Professor(a)')
disciplina = st.selectbox('Disciplina', disciplinas(planilha))
ano = st.selectbox('Ano/série', ['1ª', '2ª', '3ª'])
turma = st.text_input('Turma (ex: A, B, C)')

opcoes = [
    "Material digital do Componente",
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

# Seleção de até 3 semanas (cada semana corresponde a uma aula/conjunto)
df = data_frame(planilha, disciplina)
qt_aula = qtde_aulas(df, ano, '3º')  # sempre bimestre 3 neste modelo
aulas = list(range(1, qt_aula + 1))

semanas = st.multiselect(
    'Selecione até 3 semanas (aulas) para gerar',
    aulas,
    max_selections=3
)

# Inicializa campos para cada semana
dados = {
    1: {"atividades": "", "estrategias": "", "flexibilizacao": "", "autoavaliacao": "", "recuperacao": "",
        "habilidades": "", "objeto": ""},
    2: {"atividades": "", "estrategias": "", "flexibilizacao": "", "autoavaliacao": "", "recuperacao": "",
        "habilidades": "", "objeto": ""},
    3: {"atividades": "", "estrategias": "", "flexibilizacao": "", "autoavaliacao": "", "recuperacao": "",
        "habilidades": "", "objeto": ""}
}

for idx, semana in enumerate(semanas, start=1):
    dataf = filtro(df, ano, '3º', [semana])
    key = f"semana_{semana}"

    st.subheader(f"Semana {idx} (Aula {semana})")
    st.dataframe(dataf)

    gerar = st.button(f"Gerar textos (Gemini) - Semana {idx}")
    if gerar:
        with st.spinner(f"⏳ Gerando conteúdos para Semana {idx}..."):
            st.session_state[f"atividades_{key}"] = gemini_ativi(" ".join(dataf['CONTEÚDO'].dropna()))
            st.session_state[f"estrategias_{key}"] = gemini_estrat(" ".join(dataf['OBJETIVOS'].dropna()))
            st.session_state[f"flex_{key}"] = gemini_flex(" ".join(dataf['OBJETIVOS'].dropna()))
            st.session_state[f"auto_{key}"] = gemini_autoaval(" ".join(dataf['OBJETIVOS'].dropna()))
            st.session_state[f"recuperacao_{key}"] = gemini_rec(" ".join(dataf['OBJETIVOS'].dropna()))

    # Campos editáveis
    dados[idx]["atividades"] = st.text_area(
        f"📝 Atividades - Semana {idx}",
        st.session_state.get(f"atividades_{key}", ""),
        height=150
    )
    dados[idx]["estrategias"] = st.text_area(
        f"📚 Estratégias - Semana {idx}",
        st.session_state.get(f"estrategias_{key}", ""),
        height=150
    )
    dados[idx]["flexibilizacao"] = st.text_area(
        f"♿ Flexibilização Curricular (DUA, AEE) - Semana {idx}",
        st.session_state.get(f"flex_{key}", ""),
        height=100
    )
    dados[idx]["autoavaliacao"] = st.text_area(
        f"🧐 Autoavaliação Docente - Semana {idx}",
        st.session_state.get(f"auto_{key}", ""),
        height=100
    )
    dados[idx]["recuperacao"] = st.text_area(
        f"🔁 Avaliação e Recuperação - Semana {idx}",
        st.session_state.get(f"recuperacao_{key}", ""),
        height=100
    )
    dados[idx]["habilidades"] = "; ".join(dataf['HABILIDADE'].dropna().unique())
    dados[idx]["objeto"] = "; ".join(dataf['OBJETOS DO CONHECIMENTO'].dropna().unique())

# Botão final para gerar o Word
if st.button("📄 Gerar Plano de Aula (Word)"):
    doc = substituir(
        modelo_path=modelo_docx,
        nome=nome,
        disciplina=disciplina,
        serie=ano,
        turma=turma,

        # Semana 1
        habilidades_1=dados[1]["habilidades"],
        objeto_conhecimento_1=dados[1]["objeto"],
        atividades_1=dados[1]["atividades"],
        estrategias_1=dados[1]["estrategias"],
        flexibilizacao_1=dados[1]["flexibilizacao"],
        autoavaliacao_1=dados[1]["autoavaliacao"],
        recuperacao_1=dados[1]["recuperacao"],

        # Semana 2
        habilidades_2=dados[2]["habilidades"],
        objeto_conhecimento_2=dados[2]["objeto"],
        atividades_2=dados[2]["atividades"],
        estrategias_2=dados[2]["estrategias"],
        flexibilizacao_2=dados[2]["flexibilizacao"],
        autoavaliacao_2=dados[2]["autoavaliacao"],
        recuperacao_2=dados[2]["recuperacao"],

        # Semana 3
        habilidades_3=dados[3]["habilidades"],
        objeto_conhecimento_3=dados[3]["objeto"],
        atividades_3=dados[3]["atividades"],
        estrategias_3=dados[3]["estrategias"],
        flexibilizacao_3=dados[3]["flexibilizacao"],
        autoavaliacao_3=dados[3]["autoavaliacao"],
        recuperacao_3=dados[3]["recuperacao"],

        # Recursos
        recursos=recursos_texto
    )

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="📥 Baixar Plano de Aula",
        data=buffer,
        file_name=f"Plano_{nome}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    st.success("✅ Plano de Aula gerado com sucesso!")


