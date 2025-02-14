

import pandas as pd


class OcupacaoVagas:

    def __init__(self, df_filter, fluxo, vagas, filtros, regras_remanejamento, campus_curso_id, cota_id, campus_id):

        self.df_filter = df_filter
        self.fluxo = fluxo
        self.vagas = vagas
        self.filtros = filtros
        self.regras_remanejamento = regras_remanejamento
        self.campus_curso_id = campus_curso_id
        self.cota_id = cota_id
        self.campus_id = campus_id
        self.vagas_nao_ocupadas = vagas.copy()



    def ocupar_vagas(self,df_filter):
        """ 
            Função principal para ocupação de vagas. 
        """
        self.ocupacao_inicial_todas(df_filter)
        self.remanejar_vagas(df_filter)
        

    def ocupacao_inicial_todas(self, df_filter):
        """
            Ocupa as vagas iniciais de acordo com o fluxo de ocupação.
            Caso não haja vagas suficientes, a cota será preenchida parcialmente.
        
        """
        # global fluxo

        for cota in self.fluxo:
            # sort_order = [False] * (len(cols_sorted) - 1) + [True]
            # df_filter.sort_values(by=cols_sorted, ascending=sort_order,  inplace=True)
            self.ocupacao_inicial(cota, df_filter)


    def ocupacao_inicial(self,grupo_vagas_inscrito, df_filter): 
        """
            Ocupa as vagas iniciais para uma cota específica.
            Caso não haja vagas suficientes, a cota será preenchida parcialmente.
        
        """
        # global vagas, filtros, vagas_nao_ocupadas

        num_vagas = self.vagas.get(grupo_vagas_inscrito, 0)
        cotas_no_filtro = self.filtros[grupo_vagas_inscrito]

        linhas_filtradas = df_filter[(df_filter["Grupo de vagas inscrito"].isin(cotas_no_filtro)) &\
                                    (df_filter["Grupo_vagas_chamado_"] == "")]\
                                    .head(num_vagas)
        
        self.vagas_nao_ocupadas[grupo_vagas_inscrito] = num_vagas - linhas_filtradas.shape[0]
        print(grupo_vagas_inscrito,f"num_vagas: [{num_vagas}]", "->",self.vagas_nao_ocupadas[grupo_vagas_inscrito])
        
        if linhas_filtradas.shape[0] > 0:
            # Atribui valores às colunas `Grupo_vagas_inicial_` e `Grupo_vagas_chamado_`
            df_filter.loc[linhas_filtradas.index, "Grupo_vagas_inicial_"] = grupo_vagas_inscrito.replace("_","-")
            df_filter.loc[linhas_filtradas.index, "Grupo_vagas_chamado_"] = grupo_vagas_inscrito.replace("_","-")
            df_filter.loc[linhas_filtradas.index, "Log"] = "Ocupação inicial"


    def remanejar_vagas(self,df_filter):
        """
            Remaneja vagas não preenchidas para outras cotas de acordo com as regras de remanejamento
            caso existam vagas não preenchidas.
        
        """

        # global vagas_nao_ocupadas, regras_remanejamento, filtros

        for cota in self.vagas_nao_ocupadas:
            n_vagas_restantes = self.vagas_nao_ocupadas.get(cota, 0)
            if n_vagas_restantes > 0:
                for proxima_cota in self.regras_remanejamento.get(cota, []):
                    cotas_no_filtro = self.filtros.get(proxima_cota, [])
                    # print(cota," => ", proxima_cota,": ", cotas_no_filtro, end='>>' )
        
                    linhas_filtradas = df_filter[(df_filter["Grupo de vagas inscrito"].isin(cotas_no_filtro)) &\
                                                        (df_filter["Grupo_vagas_chamado_"] == "")]\
                                                        .head(n_vagas_restantes)
                    
                    if linhas_filtradas.shape[0] > 0:
                        # Atribui valores às colunas `Grupo_vagas_inicial_` e `Grupo_vagas_chamado_`
                        df_filter.loc[linhas_filtradas.index, "Grupo_vagas_inicial_"] = cota.replace("_","-")
                        df_filter.loc[linhas_filtradas.index, "Grupo_vagas_chamado_"] = proxima_cota.replace("_","-")
                        df_filter.loc[linhas_filtradas.index, "Log"] = "Vaga remanejada"
        
                        self.vagas_nao_ocupadas[cota] = n_vagas_restantes - linhas_filtradas.shape[0]
                        print(" |=>> ",self.vagas_nao_ocupadas[cota])
        
                    if self.vagas_nao_ocupadas[cota] <= 0: 
                        print(f"Encerrou a ocupação da vaga para a cota {cota}")
                        break



    def gerar_carga_de_dados(self, df: pd.DataFrame):
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

        df_filter["ID_Campus"] = self.campus_id.get(campus, 0)
        df_filter["ID_Curso"] = df_filter["Curso"].apply(lambda c: self.campus_curso_id.get(campus, {}).get(c.split(" - ")[0], ""))    
        df_filter["ID_Edital"] = "<preenchido pelo campus>"
        df_filter["Grupo de vagas inscrito"] = df_filter["Grupo de vagas inscrito"].apply(lambda c: self.cota_id.get(c, 0))
        df_filter["Grupo_vagas_chamado_"] = df_filter["Grupo_vagas_chamado_"].apply(lambda c: self.cota_id.get(c, 0))
        df_filter["Classificação Geral"] = df_filter["Classificação Geral"].apply(lambda i: f"{i};")

        order_cols = ["CPF do candidato", "ID_Campus", "ID_Curso", "ID_Edital", "Grupo de vagas inscrito", "Grupo_vagas_chamado_", "Inscrição", "Classificação Geral"]

        return df_filter[order_cols]
    
    