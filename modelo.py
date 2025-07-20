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
    data_inicio,
    data_fim,
    data_atual,
    objeto_conhecimento_1,
    objeto_conhecimento_2,
    habilidades_1,
    habilidades_2,
    atividades_1,
    atividades_2,
    recursos,
    estrategias_1,
    estrategias_2,
    recuperacao_1,
    recuperacao_2,
    semana_1,
    semana_2,
):


    doc = Document(modelo_path)

    placeholders = {
        "@Nome": nome,
        "@Disciplina": disciplina,
        "@Ano_turma": serie,
        "@Bimestre": bimestre,
        "@Data_inicio": data_inicio,
        "@Data_fim": data_fim,
        "@Data_atual": data_atual,
        "@Objeto_conhecimento_1": objeto_conhecimento_1,
        "@Objeto_conhecimento_2": objeto_conhecimento_2,
        "@Habilidades_1": habilidades_1,
        "@Habilidades_2": habilidades_2,
        "@Atividades_1": atividades_1,
        "@Atividades_2": atividades_2,
        "@Recursos_1": recursos,
        "@Recursos_2": recursos,
        "@Estrategias_1": estrategias_1,
        "@Estrategias_2": estrategias_2,
        "@Recuperacao_1": recuperacao_1,
        "@Recuperacao_2": recuperacao_2,
        "@Semana_1": semana_1,
        "@Semana_2": semana_2,
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
#     doc = substituir(
#         modelo_path='./Modelo Plano de AULA.docx',
#         nome='Anderson',
#         disciplina='Matemática',
#         serie='3ª',
#         bimestre='3º',
#         objeto_conhecimento_1='Geometria: Áreas',
#         objeto_conhecimento_2='Geometria: Áreas',
#         habilidades_1='EF09MA10, EF09MA12',
#         habilidades_2='EF09MA10, EF09MA12',
#         atividades_1='Problemas contextualizados com cálculos de área',
#         atividades_2='Problemas contextualizados com cálculos de área',
#         recursos ='Livro didático, geoplano digital',
#         estrategias_1='Metodologias ativas e trabalho em grupo',
#         estrategias_2='Metodologias ativas e trabalho em grupo',
#         recuperacao_1='Atividades diferenciadas com uso de softwares',
#         recuperacao_2='Atividades diferenciadas com uso de softwares',
#         semana_1='Polígonos e Classificação',
#         semana_2='Perímetros de figuras planas',
#         data_inicio='06/01/2025',
#         data_fim='31/01/2025',
#         data_atual='11/07/2025'
#     )

#     doc.save("./modelo2.docx")
    

