import streamlit as st
import io
from datetime import timedelta
from transform import data_frame, filtro, qtde_aulas, disciplinas
from modelo import substituir_planilha
from gerador import gemini_metodologia, gemini_proposta

st.title("Gerador de Plano de Aula (4 Semanas)")
st.caption("Preencha os campos e gere automaticamente o plano de aula mensal.")

planilha = "./Escopo_EM_2025.xlsx"
modelo_xlsx = "./MODELO PLANO DE AULA PARCIAIS.xlsx"

# --- Dados do professor ---
nome = st.text_input("Professor(a)")
disciplina = st.selectbox("Disciplina", disciplinas(planilha))
ano = st.selectbox("Ano/série", ["1ª", "2ª", "3ª"])
turma = st.text_input("Turma (ex: A, B, C)")
aulas_semanais = st.number_input("Quantas aulas por semana?", min_value=1, max_value=6, value=4)

opcoes = [
    "Material digital do Componente",
    "Livro do Estudante 'Currículo em Ação'",
    "Livro 'São Paulo em Ação' – Orientação de Estudos",
    "Plataforma digital",
    "Outros",
]
recursos = [opcao for opcao in opcoes if st.checkbox(opcao)]
recursos_texto = "\n".join([f"- {item}" for item in recursos])

# --- Carregar DataFrame e selecionar aulas ---
df = data_frame(planilha, disciplina)
qt_aula = qtde_aulas(df, ano, "3º")  # Considerando bimestre fixo (ajustável)
aulas_disponiveis = list(range(1, qt_aula + 1))

aulas_selecionadas = st.multiselect(
    f"Selecione as aulas (máximo {aulas_semanais * 4} para 4 semanas)",
    aulas_disponiveis,
    max_selections=aulas_semanais * 4
)

# --- Função auxiliar para agrupar em 4 semanas ---
def agrupar_aulas(df, ano, aulas, aulas_semanais):
    grupos = [aulas[i:i + aulas_semanais] for i in range(0, len(aulas), aulas_semanais)]
    while len(grupos) < 4:
        grupos.append([])  # preenche semanas vazias
    semanas_info = []
    for grupo in grupos[:4]:
        if not grupo:
            semanas_info.append({
                "aulas": "",
                "objetivo": "",
                "objeto": "",
                "habilidades": "",
                "metodologia": "",
                "proposta": ""
            })
            continue
        df_filtrado = filtro(df, ano, "3º", grupo)
        habilidades = "; ".join(df_filtrado["HABILIDADE"].dropna().unique())
        objetos = "; ".join(df_filtrado["OBJETOS DO CONHECIMENTO"].dropna().unique())
        contexto = f"Habilidades: {habilidades}. Objetos: {objetos}."
        metodologia = gemini_metodologia(contexto)
        proposta = gemini_proposta(contexto)
        semanas_info.append({
            "aulas": f"Aulas {grupo[0]} a {grupo[-1]}",
            "objetivo": " ".join(df_filtrado["OBJETIVOS"].dropna().unique()),
            "objeto": objetos,
            "habilidades": habilidades,
            "metodologia": metodologia,
            "proposta": proposta
        })
    return semanas_info

# --- Botão para gerar plano ---
if st.button("📄 Gerar Plano de Aula (Excel)"):
    semanas_info = agrupar_aulas(df, ano, aulas_selecionadas, aulas_semanais)

    # Datas fictícias (ajuste conforme necessário)
    datas_semanas = []
    inicio_mes = st.date_input("Data inicial do mês")
    for i in range(4):
        inicio = inicio_mes + timedelta(days=i * 7)
        fim = inicio + timedelta(days=4)
        datas_semanas.append((inicio.strftime("%d/%m/%Y"), fim.strftime("%d/%m/%Y")))

    plano_final = substituir_planilha(
        modelo_path=modelo_xlsx,
        nome=nome,
        disciplina=disciplina,
        serie=ano,
        turma=turma,
        aulas_semanais=aulas_semanais,
        recursos=recursos_texto,
        datas_semanas=datas_semanas,
        semanas_info=semanas_info
    )

    with open(plano_final, "rb") as f:
        st.download_button(
            label="📥 Baixar Plano de Aula (Excel)",
            data=f,
            file_name=f"Plano_{nome}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    st.success("✅ Plano gerado com sucesso!")



