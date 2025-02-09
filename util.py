import yaml
import os

# Carregar dados do YAML se existir
def carregar_vagas():
    if os.path.exists("vagas.yaml"):
        with open("vagas.yaml", "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    return {}


if __name__ == "__main__":

    campus = "ponte_nova"
    curso = "tec_informatica"

    vagas = carregar_vagas()

    print(f"Vagas para {curso} no campus {campus}:")
    print(vagas.get(campus, {}).get(curso, {}))
