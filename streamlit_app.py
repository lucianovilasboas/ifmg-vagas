import streamlit as st
import pandas as pd
import io
from config import ordem_form, fluxo, filtros, regras_remanejamento, filter_situacao_geral
from config import fluxo_vagas_nao_ocupadas
from util import gerar_carga_de_dados, highlight_cota, to_text, total_vagas, inicializa_dataframe, zerar_vagas

st.set_page_config(page_title="Ocupação de Vagas - IFMG", page_icon="🎯", layout="wide")


# Verifica se os arquivos já estão salvos no session_state
if "output_xlsx" not in st.session_state:
    st.session_state["output_xlsx"] = None

if "output_csv" not in st.session_state:
    st.session_state["output_csv"] = None


vagas = {}
vagas_nao_ocupadas = {}
valores = []


# Interface do Streamlit
st.title("🎯 Ocupação de Vagas - IFMG 🏛️")

st.error(""" #### 📂🚨 ATENÇÃO:
- **Este é um aplicativo experimental** para auxiliar na ocupação de vagas. Favor sempre conferir os resultados antes de utilizá-los;
- **Ao formato do arquivo (📈 Excel) de entrada**. O 📈 arquivo precisa estar 🔢 ordenado por nota final (Total ou Média) de forma descendente e seguindo os critérios de desempate;
- **À realização das próxmimas chamadas**. Atualize o arquivo de entrada removendo os classificados da chamada anterior (deixe apenas os excedentes) e conferindo a ordenação conforme os critérios do Edital. 
- **Lembre-se de que se alguma matrícula for indeferida por não comprovação de cota**, o candidato deve voltar para planilha com sua opção de vaga alterada para AC e deve-se aplicar a ordenação das notas conforme os critéiros do Edital.
"""
)

st.info("""
💬 **Qualquer dúvida, sugestão ou algum problema**, reportar para o 👨‍🏫 **Prof. Luciano** pelo 📧 e-mail: 📨 luciano.espiridiao@ifmg.edu.br""")

uploaded_file = st.file_uploader("Carregar arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, sheet_name=0)

    inicializa_dataframe(df)

    # print("df.dtypes:\n", df.dtypes) 

    
    cursos_disponiveis = df["Curso"].unique().tolist()
    cursos_disponiveis = [c for c in cursos_disponiveis if isinstance(c, str)]

    campus = df["Campus"].unique().tolist()
    campus = [c.strip() for c in campus if isinstance(c, str) and "Campus" in c]
    curso_selecionado = st.selectbox("Selecione o curso", cursos_disponiveis)
    
    if curso_selecionado:
        st.subheader(f"Vagas para {curso_selecionado}")

        st.info("""📝O arquivo deve conter 9 números separados por espaço ou virgula.
                  Devem ser informadas as vagas para cotas na ordem dos campos do formulário abaixo.
                  Exemplo: 10 5 5 5 5 5 5 5 5.""")
        # Opção de upload de arquivo
        uploaded_file = st.file_uploader("""Envie um arquivo '.txt' contendo as vagas ou informe 
                                         direto nos campos do formulario.
                                         """, type=["txt"])
        

        if uploaded_file is not None:
            content = uploaded_file.read().decode("utf-8").strip()
            content = content.replace(",", " ")  # Substituir vírgulas por espaços se necessário
            valores = list(map(int, content.split()))  # Separar por espaço e converter para int
            
            if len(valores) == len(ordem_form):
                for idx, cota in enumerate(ordem_form):
                    vagas[cota[0]] = valores[idx]
            else:
                st.error("O arquivo não contém a quantidade correta de valores. Insira exatamente 9 números.")        
                
        with st.form("form_vagas"):
            cols = st.columns(len(ordem_form))
            for idx, cota in enumerate(ordem_form):
                with cols[idx]:
                    label = f"{cota[1]} {cota[0]}"
                    vagas[cota[0]] = int(st.number_input(label, min_value=0, value=valores[idx] if len(valores)>0 else 0))

            submitted = st.form_submit_button("Processar Ocupação")
        vagas_nao_ocupadas = vagas.copy()

        if submitted:
    
            # --- Funções para ocupação de vagas ---

            def ocupar_vagas(df_filter):
                """ 
                    Função principal para ocupação de vagas. 
                """
                print("Iniciando processo de ocupação de vagas...")
                ocupacao_inicial_todas(df_filter)
                
                print("---------------------\n")
                print("Processamento de remanejamento de vagas...")
                if total_vagas(vagas_nao_ocupadas) > 0:
                    remanejar_vagas(df_filter)
                
                print("Processamento de ocupação de vagas encerrado.\n")
                

            def ocupacao_inicial_todas(df_filter):
                """
                    Ocupa as vagas iniciais de acordo com o fluxo de ocupação.
                    Caso não haja vagas suficientes, a cota será preenchida parcialmente.
                """
                if df_filter.shape[0] <= total_vagas(vagas) : 
                    # se o número de inscritos for menor ou igual ao total de vagas 
                    # ocupar todas as vagas iniciais na cota AC
                    df_filter.loc[df_filter.index, "Grupo_vagas_inicial_"] = "AC"
                    df_filter.loc[df_filter.index, "Grupo_vagas_chamado_"] = "AC"
                    df_filter.loc[df_filter.index, "Classificacao_geral_"] = list(range(1, df_filter.shape[0] + 1))
                    df_filter.loc[df_filter.index, "Situacao_geral_"] = "Classificado(a)"                    
                    df_filter.loc[df_filter.index, "Log"] = "Ocupação inicial"

                    zerar_vagas(vagas_nao_ocupadas)
                    vagas_nao_ocupadas["AC"] = total_vagas(vagas) - df_filter.shape[0]

                else:
                    for grupo_vagas_inicial in fluxo:
                        # ordenar o dataframe de acordo com as colunas especificadas e critérios de ordenação (desempate)                                      
                        ocupacao_inicial(grupo_vagas_inicial, df_filter)

                print("Processamento de ocupação inicial encerrado.\n")

            
            def ocupacao_inicial(grupo_vagas_inicial, df_filter): 
                """
                    Ocupa as vagas iniciais para uma cota específica.
                    Caso não haja vagas suficientes, a cota será preenchida parcialmente.
                """
                # df_filter.sort_values(by=cols_sorted, ascending=ascending_cols_sorted,  inplace=True)
                num_vagas = vagas.get(grupo_vagas_inicial, 0)
                cotas_no_filtro = filtros[grupo_vagas_inicial]

                linhas_filtradas = df_filter[(df_filter["Grupo de vagas inscrito"].isin(cotas_no_filtro)) &\
                                            (df_filter["Situacao_geral_"] == "")]\
                                            .head(num_vagas)
                
                n_linhas_selecionadas = linhas_filtradas.shape[0]

                vagas_nao_ocupadas[grupo_vagas_inicial] = num_vagas - n_linhas_selecionadas

                print(f"{grupo_vagas_inicial}: {num_vagas} => {vagas_nao_ocupadas[grupo_vagas_inicial]} não ocupadas.") 
                
                if n_linhas_selecionadas > 0:
                    # Atribui valores às colunas `Grupo_vagas_inicial_` e `Grupo_vagas_chamado_`
                    df_filter.loc[linhas_filtradas.index, "Grupo_vagas_inicial_"] = grupo_vagas_inicial.replace("_","-")
                    df_filter.loc[linhas_filtradas.index, "Grupo_vagas_chamado_"] = grupo_vagas_inicial.replace("_","-")
                    df_filter.loc[linhas_filtradas.index, "Log"] = "Ocupação inicial"
                    df_filter.loc[linhas_filtradas.index, "Classificacao_geral_"] = list(range(1, n_linhas_selecionadas + 1))
                    df_filter.loc[linhas_filtradas.index, "Situacao_geral_"] = "Classificado(a)"

            

            def remanejar_vagas(df_filter):
                """
                    Remaneja vagas não preenchidas para outras cotas de acordo com as regras de remanejamento
                    caso existam vagas não preenchidas.
                """
                for cota in fluxo_vagas_nao_ocupadas: # segue o fluxo de vagas não ocupadas
                    text = []
                    if vagas_nao_ocupadas[cota] > 0: print(f"{vagas_nao_ocupadas[cota]} vagas {cota} não ocupadas:")
                    # if n_vagas_restantes > 0: # se houver vagas não ocupadas
                    for proxima_cota in regras_remanejamento.get(cota, []): # segue as regras de remanejamento
                        n_vagas_restantes = vagas_nao_ocupadas.get(cota, 0) # para cada cota, verifica se há vagas não ocupadas
                        if n_vagas_restantes > 0: 
                            # print(f" :: Vagas não ocupadas para a cota {cota}: {n_vagas_restantes}")

                            cotas_no_filtro = filtros.get(proxima_cota, []) # monta o filtro da cota 
                            
                            linhas_filtradas = df_filter[(df_filter["Grupo de vagas inscrito"].isin(cotas_no_filtro)) &\
                                                                (df_filter["Situacao_geral_"] == "")]\
                                                                .head(n_vagas_restantes)
                            
                            n_linhas_selecionadas = linhas_filtradas.shape[0]
                            
                            if n_linhas_selecionadas > 0:
                                df_filter.loc[linhas_filtradas.index, "Grupo_vagas_inicial_"] = cota.replace("_","-")
                                df_filter.loc[linhas_filtradas.index, "Grupo_vagas_chamado_"] = proxima_cota.replace("_","-")
                                df_filter.loc[linhas_filtradas.index, "Log"] = "Vaga remanejada"
                                df_filter.loc[linhas_filtradas.index, "Classificacao_geral_"] = list(range(1, n_linhas_selecionadas + 1))
                                df_filter.loc[linhas_filtradas.index, "Situacao_geral_"] = "Classificado(a)"

                                text += [(proxima_cota, n_linhas_selecionadas)]
                
                            vagas_nao_ocupadas[cota] = n_vagas_restantes - n_linhas_selecionadas
                                
                            if vagas_nao_ocupadas[cota] <= 0: 
                                print(f"... foram transformadas em {to_text(text)}.\n")
                                break


                print("Fim do processo de remanejamento")
                if total_vagas(vagas_nao_ocupadas) > 0:
                    print("Vagas não ocupadas: ", vagas_nao_ocupadas)
                else:
                    print("Todas as vagas foram ocupadas.")
                print("\n---------------------\n")
            
            # --- Fim das funções de ocupação de vagas ---

            # iniciar a ocupação de vagas
            # Selecionar as colunas necessárias para a ocupação

            df_filter = df[(df["Curso"] == curso_selecionado) & (df["Situação Geral"].isin(filter_situacao_geral)) ]

            ocupar_vagas(df_filter)
            

            st.subheader("Resultado da Ocupação")

            df_filter.loc[:, "Confere_1"]  = df_filter["Grupo de vagas inicial"] ==  df_filter["Grupo_vagas_inicial_"]
            df_filter.loc[:, "Confere_2"]  = df_filter["Grupo de vagas chamado"] ==  df_filter["Grupo_vagas_chamado_"] 

            # df_filter["Confere_1"] = df_filter["Grupo de vagas inicial"] ==  df_filter["Grupo_vagas_inicial_"]
            # df_filter["Confere_2"] = df_filter["Grupo de vagas chamado"] ==  df_filter["Grupo_vagas_chamado_"] 

            # styled_df = df_filter.style.applymap(highlight_grades, subset=['Total'])
            # styled_df = df_filter.style.apply(highlight_mismatch, axis=1)
            styled_df = df_filter.style.apply(highlight_cota, axis=1)

            st.dataframe(styled_df)

            # print("campus:", campus)

            campus_ = str(campus[0]).replace(" ", "_")
            curso_selecionado_ = curso_selecionado.replace(" ", "_")
            
            output_xlsx = io.BytesIO()
            with pd.ExcelWriter(output_xlsx, engine="xlsxwriter") as writer:
                df_filter.to_excel(writer, index=False, sheet_name="Resultado")
            output_xlsx.seek(0)



            st.subheader("Carga de Dados para Matrícula")
            df_carga = gerar_carga_de_dados(df_filter)
            st.dataframe(df_carga)

            # Criando o arquivo CSV em memória
            csv_buffer = io.StringIO()
            df_carga.to_csv(csv_buffer, header=False, index=False)
            csv_data = csv_buffer.getvalue()  # Obtém os dados em string

            
            # Armazena os arquivos no session_state para evitar que sejam recriados a cada reload
            st.session_state["output_xlsx"] = output_xlsx
            st.session_state["output_csv"] = csv_data



        # Se os arquivos já foram gerados, exibe os botões de download
        if st.session_state["output_xlsx"] is not None and st.session_state["output_csv"] is not None:
            
            if total_vagas(vagas_nao_ocupadas) > 0:
                st.warning(f"Ainda *existem {total_vagas(vagas_nao_ocupadas)}* vagas não ocupadas. Verifique o resultado da ocupação")
            else:
                st.success("Todas as vagas foram ocupadas com sucesso!")
            
            st.success(f"Processamento concluído para {curso_selecionado}! Baixe os arquivos abaixo.")

            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    "Baixar resultado em .xlsx",
                    st.session_state["output_xlsx"].getvalue(),
                    file_name=f"Resultado_Ocupacao_{curso_selecionado}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            with col2:
                st.download_button(
                    "Baixar Carga de Dados para Matrícula",
                    st.session_state["output_csv"],
                    file_name=f"Carga_{curso_selecionado}.csv",
                    mime="text/csv"
                )


            # st.download_button("Baixar resultado em .xlsx", output, file_name=f"Resultado_Ocupacao_{curso_selecionado_}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            # st.download_button("Baixar Carga de Dados para Matrícula", f"Carga_{curso_selecionado_}.csv", "Carga de Dados", "csv")


st.markdown("""
---
📧 **E-mail:** [luciano.espiridiao@ifmg.edu.br](luciano.espiridiao:seuemail@ifmg.edu.br)  
🔗 **LinkedIn:** [linkedin.com/in/luciano-espiridiao](https://www.linkedin.com/in/luciano-espiridiao/)  
📸 **Instagram:** [instagram.com/luciano.ifmg](https://instagram.com/luciano.ifmg)  
""")