from docx import Document

def substituir_texto(paragrafo, mapa):
    for run in paragrafo.runs:
        for chave, valor in mapa.items():
            if chave in run.text:
                run.text = run.text.replace(chave, valor)

def substituir(modelo_path, nome, disciplina, serie,
               objeto_conhecimento, habilidades, atividades,
               recursos, estrategias, recuperacao):

    documento = Document(modelo_path)

    placeholders = {
        "{Nome}": nome,
        "{Disciplina}": disciplina,
        "{Ano_turma}": serie,
        "{Objeto_conhecimento}": objeto_conhecimento,
        "{Habilidades}": habilidades,
        "{Atividades}": atividades,
        "{Recursos}": recursos,
        "{Estratégias}": estrategias,
        "{Recuperação}": recuperacao
    }

    for paragrafo in documento.paragraphs:
        substituir_texto(paragrafo, placeholders)

    for tabela in documento.tables:
        for linha in tabela.rows:
            for celula in linha.cells:
                for paragrafo in celula.paragraphs:
                    substituir_texto(paragrafo, placeholders)

    caminho = f'./Plano_{nome}.docx'
    documento.save(caminho)
            
    
if __name__ == '__main__':
    substituir('C://Users//ander//OneDrive//Documentos//forms_plano//Modelo Plano de AULA.docx','Anderson','Matemática', '3ª', 'Objeto', 'Skills', 'activity', 'resources','strategy','Rec')


