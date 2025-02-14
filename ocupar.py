
import argparse
import yaml
from config import ordem_form, fluxo, filtros, regras_remanejamento, filter_situacao_geral
from funcoes import OcupacaoVagas
import os
import pandas as pd

def ler_excel(file_name):
    """
        Ler excel de candidatos
    """
    df = pd.read_excel(file_name, sheet_name=0)
    df["Grupo_vagas_inicial_"] = ""
    df["Grupo_vagas_chamado_"] = ""
    df["Log"] = ""

    return df


def ler_vagas(vagas_file):
    """ Carregar dados do YAML se existir """
    if os.path.exists(vagas_file):
        with open(vagas_file, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    return {}


def ocupar_vagas_por_curso(xlsx_file_name, vagas, curso, campus):
    """
        Função principal para ocupação de vagas. 
    """
    df = ler_excel(xlsx_file_name)

    df_filter = df[(df["Curso"] == curso) & (df["Situação Geral"].isin(filter_situacao_geral)) ]

    ov = OcupacaoVagas(df_filter, fluxo, vagas, filtros, regras_remanejamento)
    ov.ocupar_vagas(df_filter)


    # Criar um objeto ExcelWriter
    caminho_arquivo = f"__Resultado_{campus}_.xlsx"

    # Criar um ExcelWriter no modo correto
    if os.path.exists(caminho_arquivo):
        # Carregar o arquivo existente
        with pd.ExcelWriter(caminho_arquivo, engine="openpyxl", mode="a") as writer:
            df_filter.to_excel(writer, sheet_name=curso, index=False)
    else:
        # Criar novo arquivo
        with pd.ExcelWriter(caminho_arquivo, engine="openpyxl", mode="w") as writer:
            df_filter.to_excel(writer, sheet_name=curso, index=False)  


def ocupar_vagas(xlsx_file_name, vagas_file_name, campus):
    """
        Ocupar vagas de candidatos
    """
    vagas_por_campus = ler_vagas(vagas_file_name).get(campus, {})

    for curso in vagas_por_campus:
        ocupar_vagas_por_curso(xlsx_file_name,vagas_por_campus.get(curso, {}), curso, campus)


def distribuir_vagas(xlsx_file_name):
    """
        Distribuir vagas de candidatos conforme regras de cotas
    """
    pass



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Aplicação para processamento de vagas e cursos")
    subparsers = parser.add_subparsers(dest="comando", required=True)

    parser_tudo = subparsers.add_parser("ocupar_vagas", help="Processa todas as vagas de um campus")
    parser_tudo.add_argument("-i", "--input", required=True, help="Arquivo Excel de entrada")
    parser_tudo.add_argument("-v", "--vagas", required=True, help="Arquivo YAML com as vagas")
    parser_tudo.add_argument("-c", "--campus", required=True, help="Campus a ser processado")
    parser_tudo.set_defaults(func=lambda args: ocupar_vagas(args.input, args.vagas, args.campus))    

    args = parser.parse_args()
    args.func(args)

