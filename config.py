
filter_situacao_geral = ["Classificado(a)", "Excedente" ]

# 12.4 Havendo empate na nota final de candidatos, será levada em conta a seguinte ordem
#      de critérios para o desempate:
#   a) Maior nota na área de Linguagens, Códigos e suas Tecnologias;
#   b) Maior nota na área de Matemática e suas Tecnologias;
#   c) Maior nota na área de Ciências da Natureza e suas Tecnologias;
#   d) Maior nota na área de Ciências Humanas e suas Tecnologias;
#   e) Maior idade, levando-se em conta dia, mês e ano de nascimento.

cols_sorted = ["Total",
               "Linguagens, Códigos e suas Tecnologias",
               "Matemática e suas Tecnologias",
               "Ciências da Natureza e suas Tecnologias",
               "Ciências Humanas e suas Tecnologias",
               "Data de Nascimento"]

ascending_cols_sorted = [False, False, False, False, False, True]

other_cols = ["Inscrição",
        "Grupo de vagas inscrito",
        "Classificação Geral",
        "Situação Geral",
        "Grupo de vagas inicial",
        "Grupo de vagas chamado",
        "Grupo_vagas_inicial_",
        "Grupo_vagas_chamado_"]

cols_all = cols_sorted + other_cols

# Filtros para cotas
filtros = {
    "AC": ["AC", "LI-PPI", "LI-Q", "LI-PCD", "LI-EP", "LB-PPI", "LB-Q", "LB-PCD", "LB-EP"],
    "LI_EP": ["LI-PPI", "LI-Q", "LI-PCD", "LI-EP", "LB-PPI", "LB-Q", "LB-PCD", "LB-EP"],
    "LI_PCD": ["LI-PCD", "LB-PCD"],
    "LI_Q": ["LI-Q", "LB-Q"],
    "LI_PPI": ["LI-PPI", "LB-PPI"],
    "LB_EP": ["LB-PPI", "LB-Q", "LB-PCD", "LB-EP"],
    "LB_PCD": ["LB-PCD"],
    "LB_Q": ["LB-Q"],
    "LB_PPI": ["LB-PPI"]
}

# Fluxo de ocupação de vagas 
fluxo = [ "AC","LI_EP","LI_PCD","LI_Q","LI_PPI","LB_EP","LB_PCD","LB_Q","LB_PPI" ]

# Ordem para os inputs de vagas 
ordem_form = [("AC","🌍"), 
              ("LB_PPI","💰✊🏾🪶"), 
              ("LB_Q","💰🏡"), 
              ("LB_PCD","💰♿"), 
              ("LB_EP","💰🏫"), 
              ("LI_PPI","🎓✊🏾🪶"), 
              ("LI_Q","🎓🏡"), 
              ("LI_PCD","🎓♿"), 
              ("LI_EP","🎓🏫")] 


# Regras para remanejamento de vagas não preenchidas
regras_remanejamento = { 
    "LB_PPI": ["LB_Q", "LB_PCD", "LB_EP", "LI_PPI", "LI_Q", "LI_PCD", "LI_EP", "AC"],
    "LB_Q":   ["LB_PPI", "LB_PCD", "LB_EP", "LI_PPI", "LI_Q", "LI_PCD", "LI_EP", "AC"],
    "LB_PCD": ["LB_PPI", "LB_Q", "LB_EP", "LI_PPI", "LI_Q", "LI_PCD", "LI_EP", "AC"],
    "LB_EP":  ["LB_PPI", "LB_Q", "LB_PCD", "LI_PPI", "LI_Q", "LI_PCD", "LI_EP", "AC"],
    "LI_PPI": ["LB_PPI", "LB_Q", "LB_PCD", "LB_EP", "LI_Q", "LI_PCD", "LI_EP", "AC"],
    "LI_Q":   ["LB_PPI", "LB_Q", "LB_PCD", "LB_EP", "LI_PPI", "LI_PCD", "LI_EP", "AC"],
    "LI_PCD": ["LB_PPI", "LB_Q", "LB_PCD", "LB_EP", "LI_PPI", "LI_Q", "LI_EP", "AC"],
    "LI_EP":  ["LB_PPI", "LB_Q", "LB_PCD", "LB_EP", "LI_PPI", "LI_Q", "LI_PCD", "AC"],
    "AC":     []
}
