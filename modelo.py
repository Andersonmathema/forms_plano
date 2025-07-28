from openpyxl import load_workbook

def substituir_planilha(
    modelo_path,
    nome,
    disciplina,
    serie,
    turma,
    recursos,
    # Datas (início e fim de cada semana)
    data_s1_inicio, data_s1_fim,
    data_s2_inicio, data_s2_fim,
    data_s3_inicio, data_s3_fim,
    # Semana 1
    aulas_s1, habilidades_s1, metodologia_s1,
    # Semana 2
    aulas_s2, habilidades_s2, metodologia_s2,
    # Semana 3
    aulas_s3, habilidades_s3, metodologia_s3,
    output_path="PlanoGerado.xlsx"
):
    """
    Substitui os placeholders na planilha modelo, salvando como um novo arquivo.

    Placeholders suportados:
      #Nome, #Disciplina, #Ano, #Turmas, #Recursos
      #Data_S1_inicio, #Data_S1_fim, #Data_S2_inicio, #Data_S2_fim, #Data_S3_inicio, #Data_S3_fim
      #Aulas_S1, #Aulas_S2, #Aulas_S3
      #Habilidades_S1, #Habilidades_S2, #Habilidades_S3
      #Metodologia_S1, #Metodologia_S2, #Metodologia_S3
    """
    wb = load_workbook(modelo_path)
    ws = wb.active  # Considera a primeira aba

    # Mapa de placeholders com "#"
    mapa = {
        "#Nome": nome,
        "#Disciplina": disciplina,
        "#Ano": serie,
        "#Turmas": turma,
        "#Recursos": recursos,

        # Datas
        "#Data_S1_inicio": data_s1_inicio,
        "#Data_S1_fim": data_s1_fim,
        "#Data_S2_inicio": data_s2_inicio,
        "#Data_S2_fim": data_s2_fim,
        "#Data_S3_inicio": data_s3_inicio,
        "#Data_S3_fim": data_s3_fim,

        # Semana 1
        "#Aulas_S1": aulas_s1,
        "#Habilidades_S1": habilidades_s1,
        "#Metodologia_S1": metodologia_s1,

        # Semana 2
        "#Aulas_S2": aulas_s2,
        "#Habilidades_S2": habilidades_s2,
        "#Metodologia_S2": metodologia_s2,

        # Semana 3
        "#Aulas_S3": aulas_s3,
        "#Habilidades_S3": habilidades_s3,
        "#Metodologia_S3": metodologia_s3,
    }

    # Substitui placeholders em todas as células
    for row in ws.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str):
                for chave, valor in mapa.items():
                    if chave in cell.value:
                        cell.value = cell.value.replace(chave, str(valor))

    wb.save(output_path)
    return output_path


# Teste rápido para verificar substituições
if __name__ == "__main__":
    resultado = substituir_planilha(
        modelo_path="./MODELO PLANO DE AULA PARCIAIS.xlsx",
        nome="Anderson",
        disciplina="Matemática",
        serie="3º EM",
        turma="A",
        recursos="- Livro do Estudante\n- Plataforma Digital",

        # Datas (teste)
        data_s1_inicio="05/08/2025", data_s1_fim="09/08/2025",
        data_s2_inicio="12/08/2025", data_s2_fim="16/08/2025",
        data_s3_inicio="19/08/2025", data_s3_fim="23/08/2025",

        # Semana 1
        aulas_s1="Aulas 1 a 4",
        habilidades_s1="EF09MA10, EF09MA12",
        metodologia_s1="Aulas expositivas com resolução de problemas e uso de Geogebra.",

        # Semana 2
        aulas_s2="Aulas 5 a 8",
        habilidades_s2="EF09MA13, EF09MA15",
        metodologia_s2="Atividades em grupos e debates guiados para construção do conhecimento.",

        # Semana 3
        aulas_s3="Aulas 9 a 12",
        habilidades_s3="EF09MA16",
        metodologia_s3="Oficinas práticas com exercícios de aplicação e atividades avaliativas."
    )

    print(f"Plano gerado: {resultado}")


    

