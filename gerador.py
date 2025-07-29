import os
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI

load_dotenv()

# --- Configuração Gemini ---
genai.configure(api_key=os.getenv("API_KEY_GEMINI"))
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

# --- Configuração OpenAI ---
openai_client = OpenAI(api_key=os.getenv("API_KEY_OPENAI"))
openai_model = "gpt-4o-mini"  # pode mudar para gpt-4o ou gpt-4.1 se preferir


# --- Funções principais ---

def gemini_metodologia(contexto: str) -> str:
    prompt = f"""
    Gere um parágrafo (3 a 4 linhas) para a seção de METODOLOGIA de um plano de aula.
    Contexto: {contexto}.
    O texto deve descrever estratégias de ensino com metodologias ativas e recursos,
    com linguagem formal e direta, sem markdown ou listas.
    """
    response = gemini_model.generate_content(prompt)
    return response.text.strip()


def gemini_proposta(contexto: str) -> str:
    prompt = f"""
    Gere um parágrafo (3 a 4 linhas) para a seção de PROPOSTA PARA ALUNO ELEGÍVEL em um plano de aula.
    Contexto: {contexto}.
    O texto deve propor adaptações pedagógicas e recursos de acessibilidade (DUA/AEE),
    mantendo tom formal e objetivo. Não use markdown ou listas.
    """
    response = gemini_model.generate_content(prompt)
    return response.text.strip()


# --- Versões OpenAI (alternativa) ---

def openai_metodologia(contexto: str) -> str:
    prompt = f"""
    Gere um parágrafo (3 a 4 linhas) para a seção de METODOLOGIA de um plano de aula.
    Contexto: {contexto}.
    Descreva estratégias de ensino com metodologias ativas e uso de recursos,
    em linguagem formal e objetiva, sem listas ou markdown.
    """
    completion = openai_client.chat.completions.create(
        model=openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return completion.choices[0].message.content.strip()


def openai_proposta(contexto: str) -> str:
    prompt = f"""
    Gere um parágrafo (3 a 4 linhas) para a seção de PROPOSTA PARA ALUNO ELEGÍVEL em um plano de aula.
    Contexto: {contexto}.
    Crie sugestões de adaptações e acessibilidade (DUA/AEE) de forma formal e objetiva,
    sem listas ou markdown.
    """
    completion = openai_client.chat.completions.create(
        model=openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return completion.choices[0].message.content.strip()
