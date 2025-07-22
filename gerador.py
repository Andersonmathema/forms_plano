import os
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI

load_dotenv()

# --- Gemini ---
genai.configure(api_key=os.getenv("API_KEY_GEMINI"))
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

# --- OpenAI ---
openai_client = OpenAI(api_key=os.getenv("API_KEY_OPENAI"))
openai_model = "gpt-4o-mini"  # pode trocar para gpt-4.1 ou gpt-4o

# --- Funções com prompts mais detalhados ---

def gemini_ativi(contexto):
    prompt = f"""
    Crie um texto breve e direto (3 a 4 linhas) descrevendo atividades para um plano de aula.
    O tema é: {contexto}.
    O texto deve ser claro, objetivo e formal, adequado para documentos escolares.
    Não utilize markdown, listas ou formatação extra. Retorne somente o texto.
    """
    response = gemini_model.generate_content(prompt)
    return response.text.strip()


def gemini_estrat(contexto):
    prompt = f"""
    Crie um texto breve e direto (3 a 4 linhas) descrevendo estratégias de ensino para um plano de aula.
    O tema é: {contexto}.
    O texto deve mencionar metodologias ativas, possíveis adaptações (DUA/AEE) e alunos elegíveis,
    mantendo tom formal e objetivo. Sem markdown, apenas texto limpo.
    """
    response = gemini_model.generate_content(prompt)
    return response.text.strip()


def gemini_rec(contexto):
    prompt = f"""
    Crie um texto breve e direto (3 a 4 linhas) para a seção de recuperação de um plano de aula.
    O tema é: {contexto}.
    Descreva estratégias de adaptação/flexibilização de instrumentos de avaliação e recuperação,
    incluindo alunos elegíveis. Tom formal, sem markdown ou formatação extra.
    """
    response = gemini_model.generate_content(prompt)
    return response.text.strip()

# --- Flexibilização Curricular (Gemini) ---
def gemini_flex(contexto):
    prompt = f"""
    Crie um texto breve e direto (3 a 4 linhas) para a seção de Flexibilização Curricular (DUA, AEE) 
    em um plano de aula. O tema é: {contexto}.
    O texto deve sugerir adaptações pedagógicas e de acessibilidade para alunos com diferentes necessidades,
    mantendo tom formal e objetivo. Sem markdown, apenas texto limpo.
    """
    response = gemini_model.generate_content(prompt)
    return response.text.strip()

# --- Autoavaliação Docente (Gemini) ---
def gemini_autoaval(contexto):
    prompt = f"""
    Crie um texto breve e direto (3 a 4 linhas) para a seção de Autoavaliação Docente em um plano de aula.
    O tema é: {contexto}.
    O texto deve refletir sobre os resultados da aula, práticas pedagógicas e oportunidades de melhoria,
    com tom formal e objetivo. Sem markdown ou listas.
    """
    response = gemini_model.generate_content(prompt)
    return response.text.strip()


# --- Versões OpenAI (usando GPT) ---

def openai_ativi(contexto):
    prompt = f"""
    Crie um texto breve e direto (3 a 4 linhas) descrevendo atividades para um plano de aula.
    O tema é: {contexto}.
    O texto deve ser claro, objetivo e formal, adequado para documentos escolares.
    Não utilize markdown, listas ou formatação extra. Retorne somente o texto.
    """
    completion = openai_client.chat.completions.create(
        model=openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return completion.choices[0].message.content.strip()


def openai_estrat(contexto):
    prompt = f"""
    Crie um texto breve e direto (3 a 4 linhas) descrevendo estratégias de ensino para um plano de aula.
    O tema é: {contexto}.
    O texto deve mencionar metodologias ativas, possíveis adaptações (DUA/AEE) e alunos elegíveis,
    mantendo tom formal e objetivo. Sem markdown, apenas texto limpo.
    """
    completion = openai_client.chat.completions.create(
        model=openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return completion.choices[0].message.content.strip()


def openai_rec(contexto):
    prompt = f"""
    Crie um texto breve e direto (3 a 4 linhas) para a seção de recuperação de um plano de aula.
    O tema é: {contexto}.
    Descreva estratégias de adaptação/flexibilização de instrumentos de avaliação e recuperação,
    incluindo alunos elegíveis. Tom formal, sem markdown ou formatação extra.
    """
    completion = openai_client.chat.completions.create(
        model=openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return completion.choices[0].message.content.strip()


# --- Flexibilização Curricular (OpenAI) ---
def openai_flex(contexto):
    prompt = f"""
    Crie um texto breve e direto (3 a 4 linhas) para a seção de Flexibilização Curricular (DUA, AEE) 
    em um plano de aula. O tema é: {contexto}.
    O texto deve sugerir adaptações pedagógicas e de acessibilidade para alunos com diferentes necessidades,
    mantendo tom formal e objetivo. Sem markdown, apenas texto limpo.
    """
    completion = openai_client.chat.completions.create(
        model=openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return completion.choices[0].message.content.strip()

# --- Autoavaliação Docente (OpenAI) ---
def openai_autoaval(contexto):
    prompt = f"""
    Crie um texto breve e direto (3 a 4 linhas) para a seção de Autoavaliação Docente em um plano de aula.
    O tema é: {contexto}.
    O texto deve refletir sobre os resultados da aula, práticas pedagógicas e oportunidades de melhoria,
    com tom formal e objetivo. Sem markdown ou listas.
    """
    completion = openai_client.chat.completions.create(
        model=openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return completion.choices[0].message.content.strip()

