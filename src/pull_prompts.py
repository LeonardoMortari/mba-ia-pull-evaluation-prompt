"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

def pull_prompts_from_langsmith():
    prompt_name = "leonanluppi/bug_to_user_story_v1"

    try:
        print_section_header("Pull do Prompt")

        prompt = hub.pull(prompt_name)

        prompt_data = {
            "name": prompt_name,
            "version": "v1",
            "description": "Prompt original obtido do LangSmith Hub",
            "system_prompt": str(prompt),
        }

        output_file = "prompts/bug_to_user_story_v1.yml"

        if save_yaml(prompt_data, output_file):
            print(f"✅ Prompt salvo em {output_file}")
            return True

        return False

    except Exception as e:
        print(f"❌ Erro ao fazer pull do prompt: {e}")
        return False


def main():
    print_section_header("LangSmith Prompt Pull")

    required_vars = [
        "LANGSMITH_API_KEY"
    ]

    if not check_env_vars(required_vars):
        return 1

    success = pull_prompts_from_langsmith()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
