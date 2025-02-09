

def ocupar_vagas(df_filter):
    primeira_ocupacao_todas(df_filter)
    remanejar_vagas(df_filter)
    return df_filter


def primeira_ocupacao_todas(df_filter, fluxo):
    for cota in fluxo:
        # sort_order = [False] * (len(cols_sorted) - 1) + [True]
        # df_filter.sort_values(by=cols_sorted, ascending=sort_order,  inplace=True)
        primeira_ocupacao(cota, df_filter)


def primeira_ocupacao(grupo_vagas_inscrito, df_filter, vagas, filtros, vagas_ocupadas): 
    num_vagas = vagas[grupo_vagas_inscrito]
    cotas_no_filtro = filtros[grupo_vagas_inscrito]
    linhas_filtradas = df_filter[(df_filter["Grupo de vagas inscrito"].isin(cotas_no_filtro)) &\
                                (df_filter["Grupo_vagas_chamado_"] == "")]\
                                .head(num_vagas)
    
    vagas_ocupadas[grupo_vagas_inscrito] = num_vagas - linhas_filtradas.shape[0]
    print(grupo_vagas_inscrito,f"num_vagas: [{num_vagas}]", "->",vagas_ocupadas[grupo_vagas_inscrito])
    
    # Atribui valores às colunas `Grupo_vagas_inicial_` e `Grupo_vagas_chamado_`
    df_filter.loc[linhas_filtradas.index, "Grupo_vagas_inicial_"] = grupo_vagas_inscrito.replace("_","-")
    df_filter.loc[linhas_filtradas.index, "Grupo_vagas_chamado_"] = grupo_vagas_inscrito.replace("_","-")


def remanejar_vagas(df_filter, vagas_ocupadas, regras_remanejamento, filtros):
    for cota in vagas_ocupadas:
        n_vagas_restantes = vagas_ocupadas[cota]
        if n_vagas_restantes > 0:
            for proxima_cota in regras_remanejamento[cota]:
                grupo_vagas_inscrito = cota
                cotas_no_filtro = filtros[ proxima_cota ]
                print(cota," => ", proxima_cota,": ", cotas_no_filtro, end='>>' )
    
                linhas_filtradas = df_filter[(df_filter["Grupo de vagas inscrito"].isin(cotas_no_filtro)) &\
                                                    (df_filter["Grupo_vagas_chamado_"] == "")]\
                                                    .head(n_vagas_restantes)
                
                # Atribui valores às colunas `Grupo_vagas_inicial_` e `Grupo_vagas_chamado_`
                df_filter.loc[linhas_filtradas.index, "Grupo_vagas_inicial_"] = grupo_vagas_inscrito.replace("_","-")
                df_filter.loc[linhas_filtradas.index, "Grupo_vagas_chamado_"] = proxima_cota.replace("_","-")
    
                vagas_ocupadas[grupo_vagas_inscrito] = n_vagas_restantes - linhas_filtradas.shape[0]
                print(" |=>> ",vagas_ocupadas[grupo_vagas_inscrito])
    
                if vagas_ocupadas[grupo_vagas_inscrito] <= 0: break