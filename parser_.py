import argparse
import json

def converter_para_json(entrada, converte_codigo=True):

    entrada = entrada.encode('utf-8').decode('utf-8-sig')  

    # Dividir as linhas do texto
    linhas = entrada.strip().split("\n")

    # Criar um dicionário para armazenar os dados
    campus_dict = {} 

    for linha in linhas:
        partes = linha.split("\t")  # Separar por tabulação

        if len(partes) != 3:
            print(f"Linha mal formatada: {linha}")
            continue  # Ignorar linhas mal formatadas

        campus, curso, codigo = partes
        codigo = codigo.strip()  # Remover espaços em branco
        if converte_codigo:
            codigo = int(codigo)  # Converter código para inteiro

        # Adicionar ao dicionário estruturado
        if campus not in campus_dict:
            campus_dict[campus] = {}
        
        campus_dict[campus][curso] = codigo

    return json.dumps(campus_dict, ensure_ascii=False, indent=4)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Conversor de texto para JSON")
    parser.add_argument("entrada", help="Arquivo de entrada contendo os dados")
    parser.add_argument("-c","--converte", action="store_true", help="Converte o código para inteiro")

    args = parser.parse_args()
    arq = args.entrada
    converte = args.converte

    with open(arq, "r", encoding="utf-8") as f:
        entrada_texto = f.read()

    json_resultado = converter_para_json(entrada_texto, converte_codigo=converte)    


    with open(arq.replace(".txt",".json"), "w", encoding="utf-8") as f:
        f.write(json_resultado)
