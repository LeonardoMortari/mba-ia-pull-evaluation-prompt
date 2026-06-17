"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path
# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"

def load_prompts(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

class TestPrompts:

    @pytest.fixture
    def prompt_data(self):
        return load_prompts(PROMPT_FILE)

    def test_prompt_has_system_prompt(self, prompt_data):
        assert "system_prompt" in prompt_data
        assert prompt_data["system_prompt"].strip() != ""

    def test_prompt_has_role_definition(self, prompt_data):
        system_prompt = prompt_data["system_prompt"].lower()

        role_keywords = [
            "você é",
            "especialista",
            "product manager",
            "engenharia de requisitos",
            "analista"
        ]

        assert any(keyword in system_prompt for keyword in role_keywords)

    def test_prompt_mentions_format(self, prompt_data):
        content = (
            prompt_data.get("system_prompt", "")
            + prompt_data.get("user_prompt", "")
        ).lower()

        expected_terms = [
            "user story",
            "critérios de aceitação",
            "como",
            "eu quero",
            "para que"
        ]

        assert any(term in content for term in expected_terms)

    def test_prompt_has_few_shot_examples(self, prompt_data):
        system_prompt = prompt_data["system_prompt"].lower()

        indicators = [
            "exemplo 1",
            "exemplo 2",
            "entrada:",
            "saída:"
        ]

        found = sum(indicator in system_prompt for indicator in indicators)

        assert found >= 2

    def test_prompt_no_todos(self, prompt_data):
        content = str(prompt_data).lower()

        for term in ["todo", "[todo]", "fixme", "[fixme]"]:
            assert term not in content

    def test_minimum_techniques(self, prompt_data):
        techniques = prompt_data.get("techniques_applied", [])

        assert isinstance(techniques, list)
        assert len(techniques) >= 2

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
