import streamlit as st
import pandas as pd
import io
from config import ordem_form, fluxo, filtros, regras_remanejamento, filter_situacao_geral, color_map, campus_id, campus_curso_id, cota_id

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

uploaded_file = st.file_uploader("Carregar arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, sheet_name=0)
    df["Grupo_vagas_inicial_"] = ""
    df["Grupo_vagas_chamado_"] = ""
    df["Log"] = ""



    
    cursos_disponiveis = df["Curso"].unique().tolist()
    campus = df["Campus"].unique().tolist()
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
                color = color_map.get(cota, "white")  # Branco se não encontrar
                return [f'background-color: {color}; color: black;'] * len(row)


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

                order_cols = ["CPF do candidato", "ID_Campus", "ID_Curso", "ID_Edital", "Grupo de vagas inscrito", "Grupo_vagas_chamado_", "Inscrição", "Classificação Geral"]

                return df_filter[order_cols]



            # --- Funções para ocupação de vagas ---


            def ocupar_vagas(df_filter):
                """ 
                    Função principal para ocupação de vagas. 
                """
                ocupacao_inicial_todas(df_filter)
                remanejar_vagas(df_filter)
                

            def ocupacao_inicial_todas(df_filter):
                """
                    Ocupa as vagas iniciais de acordo com o fluxo de ocupação.
                    Caso não haja vagas suficientes, a cota será preenchida parcialmente.
                
                """
                # global fluxo

                for cota in fluxo:
                    # sort_order = [False] * (len(cols_sorted) - 1) + [True]
                    # df_filter.sort_values(by=cols_sorted, ascending=sort_order,  inplace=True)
                    ocupacao_inicial(cota, df_filter)

            
            def ocupacao_inicial(grupo_vagas_inscrito, df_filter): 
                """
                    Ocupa as vagas iniciais para uma cota específica.
                    Caso não haja vagas suficientes, a cota será preenchida parcialmente.
                
                """
                # global vagas, filtros, vagas_nao_ocupadas

                num_vagas = vagas.get(grupo_vagas_inscrito, 0)
                cotas_no_filtro = filtros[grupo_vagas_inscrito]

                linhas_filtradas = df_filter[(df_filter["Grupo de vagas inscrito"].isin(cotas_no_filtro)) &\
                                            (df_filter["Grupo_vagas_chamado_"] == "")]\
                                            .head(num_vagas)
                
                vagas_nao_ocupadas[grupo_vagas_inscrito] = num_vagas - linhas_filtradas.shape[0]
                # print(grupo_vagas_inscrito,f"num_vagas: [{num_vagas}]", "->",vagas_nao_ocupadas[grupo_vagas_inscrito])
                
                if linhas_filtradas.shape[0] > 0:
                    # Atribui valores às colunas `Grupo_vagas_inicial_` e `Grupo_vagas_chamado_`
                    df_filter.loc[linhas_filtradas.index, "Grupo_vagas_inicial_"] = grupo_vagas_inscrito.replace("_","-")
                    df_filter.loc[linhas_filtradas.index, "Grupo_vagas_chamado_"] = grupo_vagas_inscrito.replace("_","-")
                    df_filter.loc[linhas_filtradas.index, "Log"] = "Ocupação inicial"
            

            def remanejar_vagas(df_filter):
                """
                    Remaneja vagas não preenchidas para outras cotas de acordo com as regras de remanejamento
                    caso existam vagas não preenchidas.
                
                """

                # global vagas_nao_ocupadas, regras_remanejamento, filtros

                for cota in vagas_nao_ocupadas:
                    n_vagas_restantes = vagas_nao_ocupadas.get(cota, 0)
                    if n_vagas_restantes > 0:
                        for proxima_cota in regras_remanejamento.get(cota, []):
                            cotas_no_filtro = filtros.get(proxima_cota, [])
                            # print(cota," => ", proxima_cota,": ", cotas_no_filtro, end='>>' )
                
                            linhas_filtradas = df_filter[(df_filter["Grupo de vagas inscrito"].isin(cotas_no_filtro)) &\
                                                                (df_filter["Grupo_vagas_chamado_"] == "")]\
                                                                .head(n_vagas_restantes)
                            
                            if linhas_filtradas.shape[0] > 0:
                                # Atribui valores às colunas `Grupo_vagas_inicial_` e `Grupo_vagas_chamado_`
                                df_filter.loc[linhas_filtradas.index, "Grupo_vagas_inicial_"] = cota.replace("_","-")
                                df_filter.loc[linhas_filtradas.index, "Grupo_vagas_chamado_"] = proxima_cota.replace("_","-")
                                df_filter.loc[linhas_filtradas.index, "Log"] = "Vaga remanejada"
                
                                vagas_nao_ocupadas[cota] = n_vagas_restantes - linhas_filtradas.shape[0]
                                # print(" |=>> ",vagas_nao_ocupadas[cota])
                
                            if vagas_nao_ocupadas[cota] <= 0: 
                                print(f"Encerrou a ocupação da vaga para a cota {cota}")
                                break

            
            # --- Fim das funções de ocupação de vagas ---

            # iniciar a ocupação de vagas
            # Selecionar as colunas necessárias para a ocupação

            # df_filter = df[(df["Curso"] == curso_selecionado) & (df["Situação Geral"].isin(filter_situacao_geral)) ][cols_all]
            df_filter = df[(df["Curso"] == curso_selecionado) & (df["Situação Geral"].isin(filter_situacao_geral)) ]

            ocupar_vagas(df_filter)
            

            st.subheader("Resultado da Ocupação")
            # df_filter["Confere_1"] = df_filter["Grupo de vagas inicial"] ==  df_filter["Grupo_vagas_inicial_"]
            # df_filter["Confere_2"] = df_filter["Grupo de vagas chamado"] ==  df_filter["Grupo_vagas_chamado_"] 

            # styled_df = df_filter.style.applymap(highlight_grades, subset=['Total'])
            # styled_df = df_filter.style.apply(highlight_mismatch, axis=1)
            styled_df = df_filter.style.apply(highlight_cota, axis=1)

            st.dataframe(styled_df)

            campus_ = campus[0].replace(" ", "_")
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

