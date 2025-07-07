import pandas as pd


def disciplinas(df):
    xls = pd.ExcelFile(df)
    abas = xls.sheet_names
    del abas[0]
    return abas


def data_frame(file_path, sheet_name):
    # Carregar os dados do arquivo Excel
    df = pd.read_excel(file_path, sheet_name)
    # Padronizando valores da coluna 'ANO/SÉRIE'
    df['ANO/SÉRIE'] = df['ANO/SÉRIE'].replace({
        "1ª série": "1ª",
        "2ª série": "2ª",
        "3ª série": "3ª"
    })

    # Padronizando símbolo de grau na coluna 'BIMESTRE'
    df['BIMESTRE'] = df['BIMESTRE'].str.replace('°', 'º')

    return df


def qtde_aulas(df, ano_serie, bimestre):
    df_contado = df[(df['ANO/SÉRIE'] == ano_serie) & (df['BIMESTRE'] == bimestre)].shape[0]
    return df_contado



def filtro(df, ano_serie, bimestre, aula):
    df_filtrado = df[(df['ANO/SÉRIE'] == ano_serie) & (df['BIMESTRE'] == bimestre) & (df['AULA'] == aula)]
    return df_filtrado




# if __name__ == '__main__':
#     data = 'Escopo.xlsx'
#     df = data_frame(data, 'Matemática')
#     ano = input("O Ano-série: ")
#     bimestre = input('O bimestre: ')
#     df_filtrado = df[(df['ANO/SÉRIE'] == ano) & (df['BIMESTRE'] == bimestre)].shape[0]
#     print(df_filtrado)
#     aula = int(input('A aula: '))
#     disciplina = disciplinas(df=data)
#     print(disciplina)
#     df_escolhido = filtro(df=df, bimestre=bimestre, ano_serie=ano, aula = aula)
#     print(df_escolhido)

#     #print(df)
