# Dicionário de cores para cada tipo de cota
color_map = {
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

fluxo_vagas_nao_ocupadas = [ "LB_PPI", "LB_Q", "LB_PCD", "LB_EP", "LI_PPI", "LI_Q", "LI_PCD", "LI_EP"]

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
    "LB_PPI": ["LB_Q",   "LB_PCD", "LB_EP",  "LI_PPI", "LI_Q",   "LI_PCD", "LI_EP",  "AC"],
    "LB_Q":   ["LB_PPI", "LB_PCD", "LB_EP",  "LI_PPI", "LI_Q",   "LI_PCD", "LI_EP",  "AC"],
    "LB_PCD": ["LB_PPI", "LB_Q",   "LB_EP",  "LI_PPI", "LI_Q",   "LI_PCD", "LI_EP",  "AC"],
    "LB_EP":  ["LB_PPI", "LB_Q",   "LB_PCD", "LI_PPI", "LI_Q",   "LI_PCD", "LI_EP",  "AC"],
    "LI_PPI": ["LB_PPI", "LB_Q",   "LB_PCD", "LB_EP",  "LI_Q",   "LI_PCD", "LI_EP",  "AC"],
    "LI_Q":   ["LB_PPI", "LB_Q",   "LB_PCD", "LB_EP",  "LI_PPI", "LI_PCD", "LI_EP",  "AC"],
    "LI_PCD": ["LB_PPI", "LB_Q",   "LB_PCD", "LB_EP",  "LI_PPI", "LI_Q",   "LI_EP",  "AC"],
    "LI_EP":  ["LB_PPI", "LB_Q",   "LB_PCD", "LB_EP",  "LI_PPI", "LI_Q",   "LI_PCD", "AC"]
}

# Dicionário de IDs de cotas
cota_id = {
    "AC": 11,
    "LB-PPI": 12,
    "LB-Q": 13,
    "LB-PCD": 14,
    "LB-EP": 15,
    "LI-PPI": 16,
    "LI-Q": 17,
    "LI-PCD": 18,
    "LI-EP": 19
}

# Dicionário de IDs de campus
campus_id = {
  "Bambuí": 1,
  "Formiga": 2,
  "Ouro Preto": 3,
  "Governador Valadares": 4,
  "Arcos": 5,
  "Betim": 6,
  "Congonhas": 7,
  "Conselheiro Lafaiete": 8,
  "Itabirito": 9,
  "Ipatinga": 10,
  "Ouro Branco": 11,
  "Piumhi": 12,
  "Ponte Nova": 13,
  "Ribeirão das Neves": 14,
  "Sabará": 15,
  "Santa Luzia": 16,
  "São João Evangelista": 17,
  "Reitoria": 18,
  "Ibirité": 19
}

# Dicionário de códigos de cursos por campus
campus_curso_id = {
    "Arcos": {
        "Bacharelado em Engenharia Mecânica": "ARBEMEC",
        "Pós-Graduação em Docência": "AREDOCN",
        "Pós-Graduação em Docência na Educação Profissional e Tecnológica": "AREEPT",
        "Pós-Graduação em Engenharia de Segurança do Trabalho": "ARESENS",
        "Pós-Graduação em Segurança do Trabalho": "ARESETR",
        "Técnico Integrado em Administração": "ARIADMI",
        "Técnico Integrado em Mecânica": "ARIMECA"
    },
    "Bambuí": {
        "Bacharelado em Administração": "BIBADMI",
        "Bacharelado em Agronomia": "BIBAGRO",
        "Bacharelado em Engenharia de Alimentos": "BIBENGA",
        "Bacharelado em Engenharia de Computação": "BIBENGC",
        "Bacharelado em Engenharia de Produção": "BIBENGP",
        "Bacharelado em Medicina Veterinária": "BIBMVET",
        "Bacharelado em Zootecnia": "BIBZOOT",
        "Licenciatura em Ciências Biológicas": "BILCBIO",
        "Licenciatura em Educação Física": "BILEDFI",
        "Licenciatura em Física": "BILFISI",
        "Mestrado em Sustentabilidade e Tecnologia Ambiental": "BiPgMPS",
        "Técnico Integrado em Administração": "BIIADMI",
        "Técnico Integrado em Agropecuária": "BIIAGRO",
        "Técnico Integrado em Biotecnologia": "BIIBIOT",
        "Técnico Integrado em Eletromecânica": "BIIELET",
        "Técnico Integrado em Informática": "BIIINFO",
        "Técnico Integrado em Manutenção Automotiva": "BIIMAUT",
        "Técnico Integrado em Meio Ambiente": "BIIMAMB",
        "Técnico Subsequente em Agropecuária": "BISAGRO",
        "Técnico Subsequente em Manutenção Automotiva": "BISMAUT"
    },
    "Betim": {
        "Bacharelado em Engenharia de Controle e Automação": "BTBEAUT",
        "Bacharelado em Engenharia Mecânica": "BTBEMEC",
        "Técnico Integrado em Automação Industrial": "BTIAUTM",
        "Técnico Integrado em Mecânica": "BTIMECC",
        "Técnico Integrado em Química": "BTIQUIM"
    },
    "Congonhas": {
        "Bacharelado em Engenharia de Produção": "COGEPRO",
        "Bacharelado em Engenharia Mecânica": "COBEMEC",
        "Licenciatura em Física": "COGFISI",
        "Licenciatura em Letras": "COLLETR",
        "Pós-Graduação em Gestão de Projetos e Operações": "COEGPOP",
        "Técnico Concomitante em Edificações": "COCEDIF",
        "Técnico Concomitante em Mineração": "COCMINE",
        "Técnico Integrado em Edificações": "COIEDIF",
        "Técnico Integrado em Mecânica": "COIMECA",
        "Técnico Integrado em Mineração": "COIMINE",
        "Técnico Subsequente em Edificações": "COSEDIF",
        "Técnico Subsequente em Mecânica": "COSMECA",
        "Técnico Subsequente em Mineração": "COSMINE"
    },
    "Conselheiro Lafaiete": {
        "Técnico Integrado em Eletrotécnica": "CLIELET",
        "Técnico Integrado em Mecânica": "CLIMECA",
        "Técnico Subsequente em Eletrotécnica": "CLSELET",
        "Técnico Subsequente em Mecânica": "CLSMECA"
    },
    "Formiga": {
        "Bacharelado em Administração": "FGGADMI",
        "Bacharelado em Ciência da Computação": "FGGCOMP",
        "Bacharelado em Engenharia Elétrica": "FGGELET",
        "Licenciatura em Matemática": "FGGMATE",
        "Mestrado Profissional em Administração": "FGMADMI",
        "Técnico Integrado em Administração": "FGIADMI",
        "Técnico Integrado em Eletrotécnica": "FGIETRO",
        "Técnico Integrado em Informática": "FGIINFO",
        "Tecnólogo em Gestão Financeira": "FGGGFIN"
    },
    "Governador Valadares": {
        "Bacharelado em Engenharia Ambiental e Sanitária": "GVBENGAS",
        "Bacharelado em Engenharia Civil": "GVBENGC",
        "Bacharelado em Engenharia de Produção": "GVBENGP",
        "Pós-Graduação em Engenharia de Segurança do Trabalho": "GVEENST",
        "Técnico Integrado em Edificações": "GVITEDI",
        "Técnico Integrado em Meio Ambiente": "GVITMAI",
        "Técnico Integrado em Segurança do Trabalho": "GVITSTI",
        "Técnico Subsequente em Segurança do Trabalho": "GVSTSTS",
        "Técnico Subsequente em Serviços Jurídicos": "GVSTSJS",
        "Tecnólogo em Gestão Ambiental": "GVTTGAT"
    },
    "Ibirité": {
        "Bacharelado em Ciência da Computação": "IBBCCOMP",
        "Bacharelado em Engenharia de Controle e Automação": "IBBECAI",
        "Técnico Concomitante em Automação Industrial": "IBCAUTO",
        "Técnico Concomitante em Eletrotécnica": "IBCELTE",
        "Técnico Concomitante em Mecatrônica": "IBCMECT",
        "Técnico Concomitante em Sistemas de Energia Renovável": "IBCSERV",
        "Técnico Integrado em Automação Industrial": "IBIAUTO",
        "Técnico Integrado em Mecatrônica": "IBIMECT",
        "Técnico Integrado em Sistemas de Energia Renovável": "IBISERV",
        "Técnico Subsequente em Automação Industrial": "IBSAUTO",
        "Técnico Subsequente em Eletrotécnica": "IBSELTE",
        "Técnico Subsequente em Mecatrônica": "IBSMECT"
    },
    "Ipatinga": {
        "Bacharelado em Engenharia Elétrica": "IPBELET",
        "Técnico Integrado em Automação Industrial": "IPIAUTO",
        "Técnico Integrado em Eletrotécnica": "IPIELET",
        "Técnico Subsequente em Eletrotécnica": "IPSELET",
        "Técnico Subsequente em Mecânica": "IPSMECA",
        "Técnico Subsequente em Segurança do Trabalho": "IPSSEGU"
    },
    "Itabirito": {
        "Bacharelado em Engenharia Elétrica": "ITBELET",
        "Técnico Integrado em Automação Industrial": "ITIAUTO",
        "Técnico Integrado em Informática": "ITIINFO",
        "Técnico Integrado em Mecânica": "ITIMECA",
        "Técnico Subsequente em Eletroeletrônica": "ITSETRO"
    },
    "Ouro Branco": {
        "Bacharelado em Administração": "OBBGADM",
        "Bacharelado em Engenharia Metalúrgica": "OBBGEMT",
        "Bacharelado em Sistemas de Informação": "OBBGSIN",
        "Licenciatura em Computação": "OBLCOMP",
        "Licenciatura em Pedagogia": "OBLPEDA",
        "Pós-Graduação em Educação Profissional e Tecnológica": "OBMPEPT",
        "Técnico Integrado em Administração": "OBITADM",
        "Técnico Integrado em Informática": "OBITINF",
        "Técnico Integrado em Metalurgia": "OBITMET",
        "Técnico Subsequente em Metalurgia": "OBSTMET"
    },
    "Ouro Preto": {
        "Licenciatura em Física": "OPLFISI",
        "Licenciatura em Geografia": "OPLGEOG",
        "Pós-Graduação em Gestão e Conservação do Patrimônio Cultural": "OPEGCPC",
        "Técnico Integrado em Administração": "OPIADMI",
        "Técnico Integrado em Automação Industrial": "OPIAUTO",
        "Técnico Integrado em Edificações": "OPIEDIF",
        "Técnico Integrado em Metalurgia": "OPIMETA",
        "Técnico Integrado em Mineração": "OPIMINE",
        "Técnico Subsequente em Edificações": "OPSEDIF",
        "Técnico Subsequente em Joalheria": "OPSJOAL",
        "Técnico Subsequente em Meio Ambiente": "OPSAMBI",
        "Técnico Subsequente em Metalurgia": "OPSMETA",
        "Técnico Subsequente em Mineração": "OPSMINE",
        "Técnico Subsequente em Segurança do Trabalho": "OPSSEGU",
        "Tecnologia em Análise e Desenvolvimento de Sistemas": "OPTADES",
        "Tecnólogo em Conservação e Restauro": "OPTCRES",
        "Tecnólogo em Gastronomia": "OPTGAST",
        "Tecnólogo em Gestão da Qualidade": "OPTGQUA"
    },
    "Piumhi": {
        "Bacharelado em Engenharia Civil": "PIBENGC",
        "Técnico Integrado em Edificações": "PIIEDIF",
        "Técnico Subsequente em Edificações": "PISEDIF"
    },
    "Ponte Nova": {
        "Técnico Integrado em Administração": "PNIADMI",
        "Técnico Integrado em Informática": "PNIINFO",
        "Técnico Subsequente em Administração": "PNSADMI",
        "Técnico Subsequente em Informática": "PNSINFO",
        "Tecnólogo em Processos Gerenciais": "PNTGER",
        "Processos Gerenciais":  "PNTGER",
    },
    "Ribeirão das Neves": {
        "Bacharelado em Administração": "RIBADMI",
        "Pós-Graduação em Gestão Pública e Desenvolvimento Regional": "RIEGPUDR",
        "Técnico Integrado em Administração": "RIIADMI",
        "Técnico Integrado em Eletroeletrônica": "RIIELET",
        "Técnico Integrado em Informática": "RIIINFO",
        "Técnico Subsequente em Administração": "RISADMI",
        "Técnico Subsequente em Logística": "RISLOGI",
        "Tecnólogo em Processos Gerenciais": "RITPROG"
    },
    "Sabará": {
        "Bacharelado em Administração": "SABADMI",
        "Bacharelado em Engenharia de Controle e Automação": "SABENCA",
        "Bacharelado em Sistemas de Informação": "SABSINF",
        "Pós-Graduação em Educação Matemática": "SAEEMAT",
        "Técnico Integrado em Administração": "SAIADMI",
        "Técnico Integrado em Eletrônica": "SAIELET",
        "Técnico Integrado em Informática": "SAIINFO",
        "Técnico Subsequente em Eletrônica": "SASELET",
        "Tecnólogo em Logística": "SATLOGI",
        "Tecnólogo em Processos Gerenciais": "SATPGER"
    },
    "Santa Luzia": {
        "Bacharelado em Arquitetura e Urbanismo": "SLBARQU",
        "Bacharelado em Engenharia Civil": "SLBECIV",
        "Pós-Graduação em Proteção e Defesa Civil": "SLEPDCI",
        "Técnico Integrado em Edificações": "SLIEDIF",
        "Técnico Integrado em Segurança do Trabalho": "SLISEGTRA",
        "Técnico Subsequente em Paisagismo": "SLSPAIG",
        "Técnico Subsequente em Segurança do Trabalho": "SLSSEGTRA",
        "Tecnólogo em Design de Interiores": "SLTDESI"
    },
    "São João Evangelista": {
        "Bacharelado em Administração": "SJBADMI",
        "Bacharelado em Agronomia": "SJBAGRN",
        "Bacharelado em Engenharia Florestal": "SJBENGF",
        "Bacharelado em Sistemas de Informação": "SJBSINF",
        "Licenciatura em Ciências Biológicas": "SJLCBIO",
        "Licenciatura em Matemática": "SJLMATE",
        "Pós-Graduação em Agrimensura": "SJEAGM",
        "Pós-Graduação em Educação Matemática": "SJEEDM",
        "Pós-Graduação em Ensino e Tecnologias Educacionais": "SJEETED",
        "Pós-Graduação em Gestão": "SJEGEST",
        "Pós-Graduação em Meio Ambiente": "SJEMAMB2",
        "Técnico Integrado em Agrimensura": "SJITAGM",
        "Técnico Integrado em Agropecuária": "SJITAGR",
        "Técnico Integrado em Informática": "SJITINF",
        "Técnico Integrado em Manutenção e Suporte em Informática": "SJITMSI",
        "Técnico Integrado em Nutrição e Dietética": "SJITNDI",
        "Técnico Subsequente em Agrimensura": "SJSTAGR",
        "Tecnólogo em Silvicultura": "SJTSILV"
    }
}
