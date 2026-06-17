"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub.
    """
    try:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt_data["system_prompt"]),
                ("human", prompt_data["user_prompt"]),
            ]
        )

        hub.push(
            prompt_name,
            prompt,
        )

        print(f"✅ Prompt publicado com sucesso: {prompt_name}")

        return True

    except Exception as e:
        print(f"❌ Erro ao publicar prompt: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica do prompt.
    """
    errors = []

    required_fields = [
        "description",
        "version",
        "system_prompt",
        "user_prompt",
        "techniques_applied",
    ]

    for field in required_fields:
        if field not in prompt_data:
            errors.append(f"Campo obrigatório faltando: {field}")

    if not prompt_data.get("system_prompt", "").strip():
        errors.append("system_prompt vazio")

    if not prompt_data.get("user_prompt", "").strip():
        errors.append("user_prompt vazio")

    techniques = prompt_data.get("techniques_applied", [])

    if len(techniques) < 2:
        errors.append(
            "É obrigatório informar pelo menos 2 técnicas."
        )

    if "TODO" in str(prompt_data):
        errors.append("Existem TODOs pendentes no prompt.")

    return (len(errors) == 0, errors)


def main():
    """
    Função principal.
    """

    print_section_header("Push de Prompt para LangSmith")

    required_vars = [
        "LANGSMITH_API_KEY",
    ]

    if not check_env_vars(required_vars):
        return 1

    prompt_file = "prompts/bug_to_user_story_v2.yml"

    prompt_data = load_yaml(prompt_file)

    if not prompt_data:
        print(f"❌ Não foi possível carregar {prompt_file}")
        return 1

    is_valid, errors = validate_prompt(prompt_data)

    if not is_valid:
        print("❌ Prompt inválido:")

        for error in errors:
            print(f"   - {error}")

        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB")

    if not username:
        print(
            "❌ Configure USERNAME_LANGSMITH_HUB no .env"
        )
        return 1

    prompt_name = f"{username}/bug_to_user_story_v2"

    success = push_prompt_to_langsmith(
        prompt_name,
        prompt_data,
    )

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
