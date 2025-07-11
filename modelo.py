from docx import Document


def substituir_runs(paragrafo, mapa):
    texto_original = "".join(run.text for run in paragrafo.runs)
    texto_modificado = texto_original

    for chave, valor in mapa.items():
        texto_modificado = texto_modificado.replace(str(chave), str(valor))

    if texto_original != texto_modificado:
        for _ in paragrafo.runs:
            _._element.getparent().remove(_._element)
        paragrafo.add_run(texto_modificado)


def substituir(
    modelo_path,
    nome,
    disciplina,
    serie,
    bimestre,
    objeto_conhecimento,
    habilidades,
    atividades,
    recursos,
    estrategias,
    recuperacao,
    semana_1,
    semana_2,
    semana_3,
    semana_4,
    data_inicio,
    data_fim,
    data_atual,
):


    doc = Document(modelo_path)

    placeholders = {
        "@Nome": nome,
        "@Disciplina": disciplina,
        "@Ano_turma": serie,
        "@Bimestre": bimestre,
        "@Objeto_conhecimento": objeto_conhecimento,
        "@Habilidades": habilidades,
        "@Atividades": atividades,
        "@Recursos": recursos,
        "@Estratégias": estrategias,
        "@Recuperação": recuperacao,
        "@Semana_1": semana_1,
        "@Semana_2": semana_2,
        "@Semana_3": semana_3,
        "@Semana_4": semana_4,
        "@Data_inicio": data_inicio,
        "@Data_fim": data_fim,
        "@Data_atual": data_atual

    }

    for paragrafo in doc.paragraphs:
        substituir_runs(paragrafo, placeholders)

    for tabela in doc.tables:
        for linha in tabela.rows:
            for celula in linha.cells:
                for paragrafo in celula.paragraphs:
                    substituir_runs(paragrafo, placeholders)

    return doc

            
    
# if __name__ == "__main__":
#     substituir(
#         modelo_path='./Modelo Plano de AULA.docx',
#         nome='Anderson',
#         disciplina='Matemática',
#         serie='3ª',
#         bimestre='3º',
#         objeto_conhecimento='Geometria: Áreas',
#         habilidades='EF09MA10, EF09MA12',
#         atividades='Problemas contextualizados com cálculos de área',
#         recursos='Livro didático, geoplano digital',
#         estrategias='Metodologias ativas e trabalho em grupo',
#         recuperacao='Atividades diferenciadas com uso de softwares',
#         semana_1='Polígonos e Classificação',
#         semana_2='Perímetros de figuras planas',
#         semana_3='Cálculo de áreas',
#         semana_4='Volume de sólidos geométricos',
#         data_inicio='06/01/2025',
#         data_fim='31/01/2025',
#         data_atual='11/07/2025'
#     )

