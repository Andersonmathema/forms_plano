from docx import Document

modelo = 'Modelo Plano de AULA.docx'

arquivoWord = Document(modelo)

def substituir(nome,
               disciplina,
               serie,
               objeto_conhecimento,
               habilidades,
               atividades,
               recursos,
               estrategias,
               recuperação
    ):

    for paragrafo in arquivoWord.paragraphs:
        if "{Nome}" in paragrafo.text:
            paragrafo.text = paragrafo.text.replace("{Nome}", nome)
        if "{Disciplina}" in paragrafo.text:
            paragrafo.text = paragrafo.text.replace('{Disciplina}', disciplina)
    
            
    caminho = './Plano_' + nome + '.docx'

    arquivoWord.save(caminho)
            
