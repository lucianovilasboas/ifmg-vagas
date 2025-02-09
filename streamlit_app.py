import streamlit as st
import pandas as pd
import io
from config import ordem_form, fluxo, filtros, regras_remanejamento

st.set_page_config(page_title="Ocupação de Vagas - IFMG", page_icon="🎯", layout="wide")

vagas = {}
vagas_ocupadas = {}

# Interface do Streamlit
st.title("🎯 Ocupação de Vagas - IFMG 🏛️")

uploaded_file = st.file_uploader("Carregar arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, sheet_name=0)
    df["Grupo_vagas_inicial_"] = ""
    df["Grupo_vagas_chamado_"] = ""
    df["Log"] = ""




    
    cursos_disponiveis = df["Curso"].unique().tolist()
    curso_selecionado = st.selectbox("Selecione o curso", cursos_disponiveis)
    
    if curso_selecionado:
        st.subheader(f"Vagas para {curso_selecionado}")
                
        with st.form("form_vagas"):
            cols = st.columns(len(ordem_form))
            for idx, cota in enumerate(ordem_form):
                with cols[idx]:
                    label = f"{cota[1]} {cota[0]}"
                    vagas[cota] = int(st.number_input(label, min_value=0, value=0))

            submitted = st.form_submit_button("Processar Ocupação")
        vagas_ocupadas = vagas.copy()

        if submitted:
    
            def ocupar_vagas(df_filter):
                primeira_ocupacao_todas(df_filter)
                remanejar_vagas(df_filter)
                

            def primeira_ocupacao_todas(df_filter):
                global fluxo

                for cota in fluxo:
                    # sort_order = [False] * (len(cols_sorted) - 1) + [True]
                    # df_filter.sort_values(by=cols_sorted, ascending=sort_order,  inplace=True)
                    primeira_ocupacao(cota, df_filter)

            
            def primeira_ocupacao(grupo_vagas_inscrito, df_filter): 
                # global vagas, filtros, vagas_ocupadas

                num_vagas = vagas[grupo_vagas_inscrito]
                cotas_no_filtro = filtros[grupo_vagas_inscrito]
                linhas_filtradas = df_filter[(df_filter["Grupo de vagas inscrito"].isin(cotas_no_filtro)) &\
                                            (df_filter["Grupo_vagas_chamado_"] == "")]\
                                            .head(num_vagas)
                
                vagas_ocupadas[grupo_vagas_inscrito] = num_vagas - linhas_filtradas.shape[0]
                print(grupo_vagas_inscrito,f"num_vagas: [{num_vagas}]", "->",vagas_ocupadas[grupo_vagas_inscrito])
                
                if linhas_filtradas.shape[0] > 0:
                    # Atribui valores às colunas `Grupo_vagas_inicial_` e `Grupo_vagas_chamado_`
                    df_filter.loc[linhas_filtradas.index, "Grupo_vagas_inicial_"] = grupo_vagas_inscrito.replace("_","-")
                    df_filter.loc[linhas_filtradas.index, "Grupo_vagas_chamado_"] = grupo_vagas_inscrito.replace("_","-")
                    df_filter.loc[linhas_filtradas.index, "Log"] = "Ocupação inicial"
            

            def remanejar_vagas(df_filter):
                # global vagas_ocupadas, regras_remanejamento, filtros

                for cota in vagas_ocupadas:
                    n_vagas_restantes = vagas_ocupadas[cota]
                    if n_vagas_restantes > 0:
                        for proxima_cota in regras_remanejamento[cota]:
                            cotas_no_filtro = filtros[ proxima_cota ]
                            print(cota," => ", proxima_cota,": ", cotas_no_filtro, end='>>' )
                
                            linhas_filtradas = df_filter[(df_filter["Grupo de vagas inscrito"].isin(cotas_no_filtro)) &\
                                                                (df_filter["Grupo_vagas_chamado_"] == "")]\
                                                                .head(n_vagas_restantes)
                            
                            if linhas_filtradas.shape[0] > 0:
                                # Atribui valores às colunas `Grupo_vagas_inicial_` e `Grupo_vagas_chamado_`
                                df_filter.loc[linhas_filtradas.index, "Grupo_vagas_inicial_"] = cota.replace("_","-")
                                df_filter.loc[linhas_filtradas.index, "Grupo_vagas_chamado_"] = proxima_cota.replace("_","-")
                                df_filter.loc[linhas_filtradas.index, "Log"] = "Vaga remanejada"
                
                                vagas_ocupadas[cota] = n_vagas_restantes - linhas_filtradas.shape[0]
                                print(" |=>> ",vagas_ocupadas[cota])
                
                            if vagas_ocupadas[cota] <= 0: 
                                print(f"Encerrou a ocupação da vaga para a cota {cota}")
                                break

            
            filter_situacao_geral = ["Classificado(a)", "Excedente" ]
            # df_filter = df[(df["Curso"] == curso_selecionado) & (df["Situação Geral"].isin(filter_situacao_geral)) ][cols_all]

            df_filter = df[(df["Curso"] == curso_selecionado) & (df["Situação Geral"].isin(filter_situacao_geral)) ]

            ocupar_vagas(df_filter)
            
            st.subheader("Resultado da Ocupação")

            df_filter["Confere_1"] = df_filter["Grupo de vagas inicial"] ==  df_filter["Grupo_vagas_inicial_"]
            df_filter["Confere_2"] = df_filter["Grupo de vagas chamado"] ==  df_filter["Grupo_vagas_chamado_"] 

            # # Aplicar estilo ao DataFrame
            # styled_df = df_resultado.style.apply(highlight_differences, subset=["Grupo de vagas inicial", "Grupo_vagas_inicial_", 
            #                                                                 "Grupo de vagas chamado", "Grupo_vagas_chamado_"])

            st.dataframe(df_filter)
            
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df_filter.to_excel(writer, index=False, sheet_name="Resultado Final")
            output.seek(0)
            st.download_button("Baixar resultado em .xlsx", output, file_name="resultado_ocupacao.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
