import re
import yaml
import os
from config import campus_id, campus_curso_id, cota_id
import pandas as pd

# Dicionário de cores para cada tipo de cota
cota_color_map = {
    "AC": "#D4E157",  # Verde claro
    "LI-PPI": "#FF7043",  # Laranja
    "LI-Q": "#FFCC80",  # Amarelo claro
    "LI-PCD": "#B3E5FC",  # Azul claro
    "LI-EP": "#80CBC4",  # Verde água
    "LB-PPI": "#F06292",  # Rosa
    "LB-Q": "#FFD54F",  # Amarelo mais forte
    "LB-PCD": "#81D4FA",  # Azul médio
    "LB-EP": "#A1887F",  # Marrom claro
}



# Função para colorir as células com base na nota
def highlight_grades(val):
    color = 'green' if val >= 25 else 'red'
    return f'background-color: {color}; color: white;'

def highlight_mismatch(row):
    if row['Confere_1'] == row['Confere_2']:
        return ['background-color: red; color: white'] * len(row)
    return [''] * len(row)

# Função para aplicar a cor de fundo com base na cota
def highlight_cota(row):
    cota = row['Grupo_vagas_chamado_']
    color = cota_color_map.get(cota, "white")  # Branco se não encontrar
    return [f'background-color: {color}; color: black;'] * len(row)




def aplicar_mascara_cpf(cpf):
    """Aplica a máscara de CPF (XXX.XXX.XXX-XX) somente se ainda não estiver formatado."""
    cpf = str(cpf).strip()
    # Expressão regular para identificar se a máscara já está aplicada
    mascara_cpf = re.compile(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")
    if mascara_cpf.match(cpf):  # Se já estiver formatado, retorna como está
        return cpf
    cpf = re.sub(r"\D", "", cpf)  # Remove quaisquer caracteres não numéricos
    if len(cpf) == 10:  # Se tiver 10 dígitos, adiciona um zero à esquerda
        cpf = "0" + cpf
    if len(cpf) == 11:  # Aplica a máscara apenas se tiver 11 dígitos
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf  # Retorna o original se não for um CPF válido



def gerar_carga_de_dados(df: pd.DataFrame):
    """
        Gera a carga de dados para sitema de matrícula.
        ```csv
            CPF (no formato xxx.xxx.xxx-xx),ID do Campus,ID do curso,ID do edital,ID da cota inscrito,ID da cota chamada,Nº de inscrição,Classificação;

        ```
    """
    # selecionar as colunas necessárias para a carga de dados
    cols = ["CPF do candidato", "Campus", "Curso", "Grupo de vagas inscrito", "Grupo_vagas_chamado_", "Inscrição", "Classificação Geral"]

    df_filter = df[df["Grupo_vagas_chamado_"] != ""][cols].copy()
    campus = df_filter["Campus"].iloc[0].replace("Campus ", "").strip()

    # print("Campus ->"    , f"'{campus}'")

    df_filter["ID_Campus"] = campus_id.get(campus, 0)
    df_filter["ID_Curso"] = df_filter["Curso"].apply(lambda c: campus_curso_id.get(campus, {}).get(c.split(" - ")[0], ""))    
    df_filter["ID_Edital"] = "<preenchido pelo campus>"
    df_filter["Grupo de vagas inscrito"] = df_filter["Grupo de vagas inscrito"].apply(lambda c: cota_id.get(c, 0))
    df_filter["Grupo_vagas_chamado_"] = df_filter["Grupo_vagas_chamado_"].apply(lambda c: cota_id.get(c, 0))
    df_filter["Classificação Geral"] = df_filter["Classificação Geral"].apply(lambda i: f"{i};")

    df_filter["CPF do candidato"] = df_filter["CPF do candidato"].apply(aplicar_mascara_cpf)

    order_cols = ["CPF do candidato", "ID_Campus", "ID_Curso", "ID_Edital", "Grupo de vagas inscrito", "Grupo_vagas_chamado_", "Inscrição", "Classificação Geral"]

    return df_filter[order_cols]


def total_vagas(vagas):
    """
        Retorna o total de vagas disponíveis.
    """
    return sum(vagas.values())


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
