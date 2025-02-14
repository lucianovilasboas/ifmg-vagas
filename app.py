
import argparse

def processar_tudo(vagas, campus):
    print(f"Processando tudo com vagas: {vagas} para o campus: {campus}")


def processar(vagas, cursos):
    print(f"Processando vagas: {vagas} para os cursos: {', '.join(cursos)}")


def distribuir_vagas(xlsx_file_name, campus):
    print(f"Ocupando vagas do arquivo {xlsx_file_name} para o campus {campus}")

def main():
    parser = argparse.ArgumentParser(description="Aplicação para processamento de vagas e cursos")
    subparsers = parser.add_subparsers(dest="comando", required=True)

    # Subcomando processar_tudo
    parser_tudo = subparsers.add_parser("processar_tudo", help="Processa todas as vagas de um campus")
    parser_tudo.add_argument("--vagas", required=True, help="Arquivo YAML com as vagas")
    parser_tudo.add_argument("--campus", required=True, help="Campus a ser processado")
    parser_tudo.set_defaults(func=lambda args: processar_tudo(args.vagas, args.campus))

    # Subcomando processar
    parser_proc = subparsers.add_parser("processar", help="Processa vagas para cursos específicos")
    parser_proc.add_argument("--vagas", required=True, help="Arquivo YAML com as vagas")
    parser_proc.add_argument("--curso", required=True, nargs='+', help="Cursos a serem processados")
    parser_proc.set_defaults(func=lambda args: processar(args.vagas, args.curso))


    # Subcomando distribuir_vagas
    parser_distribuir = subparsers.add_parser("distribuir_vagas", help="Ocupa vagas de candidatos")
    parser_distribuir.add_argument("--input", required=True, help="Arquivo Excel de entrada")
    parser_distribuir.add_argument("--campus", required=True, help="Campus a ser processado")
    parser_distribuir.set_defaults(func=lambda args: distribuir_vagas(args.input, args.campus))


    # Parseando os argumentos
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
