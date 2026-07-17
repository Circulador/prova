#!/usr/bin/env python3
"""Banco de questões — História (2º EM)."""

def q(text, opts, correct, expl, level="medio"):
    return [text, opts, correct, expl, level]

def pack(materia, code, title, desc, subs, minutes=75):
    total = sum(len(v) for v in subs.values())
    assert total == 50, f"{materia}: {total} questões"
    return {
        "materia": materia, "code": code, "title": title,
        "description": desc, "timeMinutes": minutes, "submaterias": subs
    }

HIST = pack("História", "EM2-HIST", "Simulado — História (2º EM)",
    "50 questões de múltipla escolha organizadas por sub-matéria.", {
    "Revolução Francesa": [
        q("A Revolução Francesa teve início em:", ["1776", "1789", "1804", "1815"], 1, "Queda da Bastilha em 14 de julho de 1789."),
        q("O lema 'Liberdade, Igualdade, Fraternidade' associou-se a:", ["Antigo Regime", "Revolução Francesa", "Restauração", "Santa Aliança"], 1, "Lema simbólico da Revolução."),
        q("A Bastilha simbolizava:", ["A Igreja", "O absolutismo e o despotismo real", "A burguesia", "A aldeia camponesa"], 1, "Prisão real, símbolo do poder absolutista."),
        q("Os principais integrantes do Terceiro Estado eram:", ["Nobres e clérigos", "Burgueses, camponeses e trabalhadores urbanos", "Apenas o rei", "Generais napoleônicos"], 1, "Terceiro Estado = maioria da população sem privilégios."),
        q("A fase conhecida como Terror (1793-1794) caracterizou-se por:", ["Monarquia constitucional", "Repressão violenta liderada por Robespierre", "Paz com a Inglaterra", "Retorno dos nobres"], 1, "Comité de Salut Pública e guilhotina."),
        q("O Antigo Regime baseava-se em:", ["Democracia direta", "Sociedade estamental e absolutismo", "Socialismo", "República federativa"], 1, "Privilégios de clero e nobreza; poder real absoluto."),
        q("A Declaração dos Direitos do Homem e do Cidadão (1789) proclamou:", ["Direitos divinos do rei", "Direitos naturais e igualdade perante a lei", "Escravidão legal", "Veto absoluto real"], 1, "Documento fundador de princípios liberais."),
        q("Napoleão Bonaparte assumiu o poder após:", ["A Restauração", "O golpe de 18 Brumário (1799)", "A Queda da Bastilha", "A Revolução de 1848"], 1, "18 Brumário encerrou o Diretório."),
        q("As guerras revolucionárias francesas opuseram a França a:", ["Apenas Portugal", "Coalizões europeias monárquicas", "Os EUA", "O Império Otomano isoladamente"], 1, "Monarquias europeias temiam a expansão revolucionária."),
        q("A abolição dos privilégios feudais ocorreu na:", ["Noite do 4 de agosto de 1789", "Batalha de Waterloo", "Coroação de Napoleão", "Restauração de Luís XVIII"], 0, "Assembleia Nacional aboliu privilégios feudais."),
    ],
    "Independência do Brasil": [
        q("A Independência do Brasil foi proclamada em:", ["7 de setembro de 1822", "15 de novembro de 1889", "13 de maio de 1888", "21 de abril de 1792"], 0, "Grito do Ipiranga, Dom Pedro I."),
        q("As 'Dores de Independência' referem-se a:", ["Guerras contra Portugal e facções internas", "Abolição da escravidão", "Proclamação da República", "Revolta de Canudos"], 0, "Conflitos militares pós-1822."),
        q("A transferência da corte portuguesa para o Rio (1808) deveu-se a:", ["Invasão napoleônica a Portugal", "Revolta mineradora", "Tratado de Tordesilhas", "Guerra do Paraguai"], 0, "Família real fugiu das tropas de Napoleão."),
        q("A Constituição de 1824 estabeleceu:", ["República presidencialista", "Monarquia constitucional unitária", "Confederação de províncias", "Império absolutista"], 1, "Poder moderador e três poderes."),
        q("O 'Dia do Fico' (9 de janeiro de 1822) simbolizou:", ["Abdicação de Dom Pedro", "Decisão de Dom Pedro de ficar no Brasil", "Fim da escravidão", "Proclamação da República"], 1, "Dom Pedro recusou ordem de retorno a Portugal."),
        q("A Confederação do Equador (1824) foi:", ["Movimento separatista no Nordeste", "Aliança com a Argentina", "Tratado com a Inglaterra", "Reforma agrária"], 0, "Revolta republicana e federalista no Norte/Nordeste."),
        q("O reconhecimento da independência por Portugal ocorreu em:", ["1822", "1825", "1831", "1889"], 1, "Tratado de 1825 reconheceu a independência."),
        q("José Bonifácio foi importante na Independência como:", ["Conspirador republicano", "Conselheiro de Dom Pedro e modernizador", "Líder farroupilha", "Presidente da República"], 1, "Patriarca da Independência."),
        q("A independência brasileira diferiu da Hispano-Americana por ser:", ["Violenta e anticolonial desde o início", "Relativamente pacífica e liderada pela elite", "Liderada por camponeses", "Separada em várias repúblicas"], 1, "Elite local manteve unidade territorial."),
        q("O Ato Adicional de 1834 ampliou:", ["Escravidão", "Autonomia provincial e poder do Legislativo", "Poder moderador", "Voto universal"], 1, "Reforma liberal após abdicação de Dom Pedro I."),
    ],
    "Era Napoleônica": [
        q("Napoleão foi coroado Imperador dos Franceses em:", ["1789", "1799", "1804", "1815"], 2, "Coroação em Notre-Dame, 1804."),
        q("O Bloqueio Continental visava:", ["Isolar economicamente a Grã-Bretanha", "Unir a América Latina", "Abolir a escravidão", "Conquistar a Rússia apenas"], 0, "Proibir comércio europeu com a Inglaterra."),
        q("A Batalha de Waterloo (1815) resultou em:", ["Vitória definitiva de Napoleão", "Derrota final de Napoleão", "Independência da Grécia", "Queda da Bastilha"], 1, "Napoleão exilado em Santa Helena."),
        q("O Código Napoleônico influenciou:", ["Apenas a França", "Legislações civis de diversos países", "Somente a Rússia", "Direito canônico exclusivamente"], 1, "Código civil modelo para Europa e América."),
        q("A Campanha da Rússia (1812) foi desastrosa porque:", ["Napoleão venceu facilmente", "Exército francês foi destruído pelo inverno e retirada", "Portugal invadiu a França", "Houve revolta na Bastilha"], 1, "Grande parte do exército pereceu na retirada."),
        q("As Guerras Peninsulares ocorreram na:", ["Península Ibérica", "Península Itálica", "Balcãs", "Escandinávia"], 0, "Espanha e Portugal contra ocupação francesa."),
        q("O Congresso de Viena (1815) buscou:", ["Restaurar equilíbrio europeu pós-Napoleão", "Proclamar repúblicas", "Expandir o Império Francês", "Unificar a Alemanha"], 0, "Restauração e nova ordem conservadora."),
        q("Napoleão vendeu a Louisiana aos EUA em:", ["1789", "1803", "1815", "1822"], 1, "Duplicou território americano; financiou guerras."),
        q("A invasão napoleônica ao Egito (1798) tinha objetivo de:", ["Cortar rotas britânicas e expandir influência", "Colonizar o Brasil", "Apoiar a Revolução Industrial", "Restaurar monarquia"], 0, "Estratégia contra a Grã-Bretanha no Oriente."),
        q("O exílio de Napoleão em Elba foi seguido por:", ["Abdicação definitiva", "Retorno dos Cem Dias", "Coroação na Rússia", "Independência do Haiti"], 1, "Napoleão retornou brevemente em 1815."),
    ],
    "Industrialização": [
        q("A Revolução Industrial iniciou-se principalmente na:", ["França", "Inglaterra", "Alemanha", "Itália"], 1, "Século XVIII, setor têxtil inglês."),
        q("A máquina a vapor foi crucialmente aprimorada por:", ["Adam Smith", "James Watt", "Karl Marx", "Louis Pasteur"], 1, "Watt melhorou eficiência da máquina a vapor."),
        q("O sistema fabril substituiu gradualmente:", ["A produção doméstica (putting-out system)", "A agricultura", "O comércio marítimo", "A escrita"], 0, "Concentração de trabalho e máquinas nas fábricas."),
        q("A classe operária (proletariado) surgiu com:", ["Feudalismo", "Industrialização urbana", "Antigo Regime", "Revolução Francesa apenas"], 1, "Trabalhadores assalariados nas indústrias."),
        q("O ludismo foi um movimento de:", ["Operários que destruíam máquinas", "Nobres contra revolução", "Camponeses pela terra", "Comerciantes pelo livre-comércio"], 0, "Protesto contra desemprego tecnológico na Inglaterra."),
        q("A divisão internacional do trabalho implica:", ["Autossuficiência de cada país", "Especialização produtiva entre nações", "Fim do comércio", "Igualdade salarial global"], 1, "Países centrais e periféricos com papéis distintos."),
        q("O capitalismo industrial caracteriza-se por:", ["Produção artesanal doméstica", "Investimento em máquinas e lucro privado", "Propriedade coletiva dos meios de produção", "Escambo"], 1, "Acumulação de capital e mercado de trabalho."),
        q("As condições iniciais nas fábricas incluíam:", ["Jornada curta e salários altos", "Jornadas longas e ambientes insalubres", "Trabalho voluntário apenas", "Propriedade dos operários"], 1, "Exploração e urbanização acelerada."),
        q("A ferrovia expandiu a industrialização porque:", ["Facilitou transporte de matérias-primas e produtos", "Substituiu todas as fábricas", "Acabou com o comércio", "Eliminou cidades"], 0, "Integração de mercados regionais e nacionais."),
        q("No Brasil, a industrialização significativa intensificou-se especialmente a partir de:", ["1500", "1930", "1889 apenas", "2000"], 1, "Estratégia de substituição de importações (Vargas)."),
    ],
    "América Portuguesa": [
        q("O Tratado de Tordesilhas (1494) dividiu terras entre:", ["Inglaterra e França", "Portugal e Castela/Espanha", "Holanda e Portugal", "Portugal e Brasil"], 1, "Linha de demarcação no Atlântico."),
        q("A economia colonial brasileira baseou-se inicialmente em:", ["Indústria pesada", "Pau-brasil e plantation açucareira", "Petróleo", "Tecnologia"], 1, "Extrativismo e monocultura exportadora."),
        q("As bandeiras paulistas buscavam principalmente:", ["Ouro, escravos indígenas e expansão territorial", "Independência imediata", "Industrialização", "Comércio com a Ásia"], 0, "Entradas e bandeirantes no sertão."),
        q("A Inconfidência Mineira (1789) foi inspirada por:", ["Ideias iluministas e insatisfação com derrama", "Revolução Industrial", "Guerra do Paraguai", "Revolta Farroupilha"], 0, "Tiradentes e conspiração em Minas Gerais."),
        q("A escravidão africana intensificou-se no Brasil devido a:", ["Demanda de mão de obra nas lavouras exportadoras", "Falta de indígenas apenas", "Proibição do tráfico desde 1500", "Lei Áurea antecipada"], 0, "Plantation e tráfico atlântico."),
        q("A mineração de ouro (séc. XVIII) concentrou-se em:", ["Amazônia", "Minas Gerais", "Pampa gaúcho", "Nordeste litorâneo"], 1, "Ciclo do ouro em MG e região central."),
        q("As capitanias hereditárias foram:", ["Províncias republicanas", "Sistema inicial de administração colonial", "Estados federados", "Missões jesuíticas"], 1, "Divisão territorial da colonização portuguesa."),
        q("O ciclo do café predominou no Brasil a partir do:", ["Século XVI", "Século XIX", "Século XXI", "Período pré-cabral"], 1, "Vale do Paraíba e Oeste Paulista."),
        q("As missões jesuíticas nos Sete Povos das Missões visavam:", ["Catequese e organização de indígenas", "Mineração de ouro", "Proclamação da República", "Comércio de especiarias"], 0, "Reduções jesuíticas no Sul."),
        q("A abertura dos portos às nações amigas (1808) significou:", ["Fim do monopólio comercial português", "Isolamento do Brasil", "Proclamação da República", "Abolição imediata"], 0, "Liberalização comercial durante a corte no Rio."),
    ],
})

print("HIST OK", len([x for s in HIST["submaterias"].values() for x in s]))
