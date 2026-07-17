#!/usr/bin/env python3
"""Banco de questões — Geografia (2º EM)."""

def q(text, opts, correct, expl, level="medio"):
    return [text, opts, correct, expl, level]

def pack(materia, code, title, desc, subs, minutes=75):
    total = sum(len(v) for v in subs.values())
    assert total == 50, f"{materia}: {total} questões"
    return {
        "materia": materia, "code": code, "title": title,
        "description": desc, "timeMinutes": minutes, "submaterias": subs
    }

GEO = pack("Geografia", "EM2-GEO", "Simulado — Geografia (2º EM)",
    "50 questões de múltipla escolha organizadas por sub-matéria.", {
    "Climatologia": [
        q("O clima tropical úmido (equatorial) caracteriza-se por:", ["Baixas temperaturas o ano todo", "Altas temperaturas e chuvas abundantes", "Estação seca prolongada", "Neve frequente"], 1, "Próximo à linha do Equador, calor e umidade."),
        q("A chuva orográfica ocorre quando:", ["Massas de ar sobem encostas de montanhas", "O mar esquenta", "Há poluição urbana", "O vento para totalmente"], 0, "Ar úmido ascende, resfria e condensa."),
        q("El Niño provoca no Brasil, em geral:", ["Seca no Norte e chuvas no Sul", "Seca em todo o país", "Neve na Amazônia", "Fim das estações"], 0, "Altera padrões de precipitação e temperatura."),
        q("O efeito estufa natural é responsável por:", ["Resfriar a Terra", "Manter temperatura adequada à vida", "Eliminar a atmosfera", "Criar ozônio"], 1, "Gases retêm calor; sem ele a Terra seria gelada."),
        q("Clima mediterrâneo apresenta verões:", ["Muito chuvosos", "Quentes e secos", "Gelados", "Sem variação"], 1, "Típico do Mediterrâneo: verão seco, inverno chuvoso."),
        q("A amplitude térmica anual é maior em:", ["Regiões litorâneas equatoriais", "Interiores continentais temperados", "Ilhas oceânicas tropicais", "Florestas tropicais"], 1, "Continentalidade amplia diferença entre verão e inverno."),
        q("Massa de ar polar atlântica (mPa) traz ao Brasil:", ["Calor seco", "Frentes frias e instabilidade no Sul/Sudeste", "Desertos", "Ciclones tropicais constantes"], 1, "Origem polar; avança sobre regiões do Sul/Sudeste."),
        q("A camada de ozônio concentra-se na:", ["Troposfera", "Estratosfera", "Hidrosfera", "Litosfera"], 1, "Protege contra radiação UV nociva."),
        q("Bioma com maior biodiversidade e clima quente-úmido:", ["Caatinga", "Amazônia", "Pampa", "Campos de altitude"], 1, "Floresta tropical úmida amazônica."),
        q("Mudanças climáticas antropogênicas relacionam-se principalmente à:", ["Emissão de gases de efeito estufa", "Rotação da Terra", "Marés oceânicas", "Atividade vulcânica natural apenas"], 0, "CO₂ e outros gases intensificam aquecimento global."),
    ],
    "Urbanização": [
        q("Urbanização é o processo de:", ["Aumento da população rural", "Crescimento das cidades e população urbana", "Desmatamento", "Industrialização agrícola apenas"], 1, "Êxodo rural e expansão urbana."),
        q("Metropolização refere-se à formação de:", ["Aldeias isoladas", "Grandes aglomerados urbanos integrados", "Desertos", "Reservas indígenas"], 1, "Conurbação entre cidades e regiões metropolitanas."),
        q("Gentrificação ocorre quando:", ["Bairros populares são valorizados e expulsam moradores originais", "Cidades perdem população", "Indústrias fecham", "Há total igualdade habitacional"], 0, "Valorização imobiliária desloca população de baixa renda."),
        q("Favelização está associada a:", ["Habitação irregular e infraestrutura precária", "Planejamento urbano perfeito", "Baixa densidade demográfica", "Zonas rurais"], 0, "Ocupação não planejada em áreas urbanas."),
        q("O SUS e saneamento básico são desafios urbanos porque:", ["Cidades concentram demanda por serviços", "Não existem doenças urbanas", "Só afetam o campo", "Eliminam desigualdade"], 0, "Metrópoles exigem infraestrutura complexa."),
        q("Zona de transição (Chicago School) situa-se:", ["No centro financeiro", "Entre centro e periferia", "Apenas na periferia rural", "No subsolo"], 1, "Área de deterioração e reconversão."),
        q("Megacidade é aquela com população superior a:", ["100 mil", "500 mil", "10 milhões", "1 milhão apenas"], 2, "Critério comum: mais de 10 milhões de habitantes."),
        q("Mobilidade urbana sustentável inclui:", ["Priorizar transporte individual a combustão", "Transporte público e não motorizado", "Eliminar calçadas", "Apenas estacionamentos"], 1, "Ônibus, metrô, ciclovias reduzem congestionamento."),
        q("No Brasil, a urbanização acelerou-se especialmente a partir de:", ["1500", "Década de 1950", "1990 apenas", "2020"], 1, "Industrialização e êxodo rural pós-guerra."),
        q("Periferia urbana frequentemente apresenta:", ["Melhor acesso a empregos formais que o centro", "Distância de serviços e empregos centrais", "Baixa densidade sempre", "Ausência de população"], 1, "Exclusão socioespacial nas grandes cidades."),
    ],
    "Globalização": [
        q("Globalização caracteriza-se por:", ["Isolamento de nações", "Integração econômica, cultural e tecnológica", "Fim do comércio", "Autarcia"], 1, "Fluxos globais de bens, capitais e informações."),
        q("Multinacionais são empresas que:", ["Operam apenas em um país", "Atuam em vários países", "São sempre estatais", "Não exportam"], 1, "Produção e mercados em escala global."),
        q("A divisão internacional do trabalho implica:", ["Todos os países produzem tudo", "Especialização produtiva entre países", "Fim das exportações", "Igualdade total de renda"], 1, "Centros e periferias com funções distintas."),
        q("Blocos econômicos como Mercosul visam:", ["Guerra comercial", "Integração regional e livre-comércio", "Isolamento", "Proibição de investimentos"], 1, "Facilitar comércio entre membros."),
        q("Cadeias produtivas globais significam:", ["Produção inteira em um só país", "Etapas da produção distribuídas mundialmente", "Fim da logística", "Produção artesanal"], 0, "Ex.: iPhone com componentes de vários países."),
        q("Homogeneização cultural na globalização manifesta-se em:", ["Difusão de marcas, mídia e hábitos globais", "Desaparecimento total de culturas locais sempre", "Fim da internet", "Proibição de turismo"], 0, "Cultura de massa e consumo global."),
        q("Deslocalização industrial ocorre quando:", ["Fábricas migram para reduzir custos", "Indústria desaparece", "Tudo é produzido localmente", "Não há comércio"], 0, "Busca mão de obra barata e incentivos fiscais."),
        q("Organização Mundial do Comércio (OMC) regula:", ["Clima", "Comércio internacional", "Educação", "Espaço sideral"], 1, "Regras e negociações comerciais globais."),
        q("Globalização financeira implica:", ["Capitais circulam rapidamente pelo mundo", "Moedas não existem", "Bancos são locais apenas", "Fim dos investimentos"], 0, "Mercados financeiros interconectados 24h."),
        q("Críticas à globalização incluem:", ["Aumento de desigualdades e precarização", "Eliminação de toda pobreza", "Fim do neocolonialismo", "Autossuficiência universal"], 0, "Benefícios nem sempre distribuídos equitativamente."),
    ],
    "População": [
        q("Densidade demográfica calcula-se por:", ["População ÷ área", "Nascimentos ÷ óbitos", "Área ÷ população", "PIB ÷ população"], 0, "Habitantes por km²."),
        q("Transição demográfica: queda da mortalidade inicialmente provoca:", ["Queda imediata da natalidade", "Crescimento acelerado da população", "Envelhecimento instantâneo", "Estagnação zero"], 1, "Natalidade alta + mortalidade baixa = boom populacional."),
        q("Envelhecimento populacional ocorre quando:", ["Há muitos jovens", "A proporção de idosos aumenta", "A natalidade explode", "Emigração é zero"], 1, "Queda de natalidade e maior expectativa de vida."),
        q("Êxodo rural é a migração do campo para:", ["Outro campo", "A cidade", "Outro planeta", "Zonas desérticas"], 1, "Busca de emprego e serviços urbanos."),
        q("Taxa de fecundidade mede:", ["Número médio de filhos por mulher", "Mortes por mil", "Migrantes por ano", "Idade média"], 0, "Indicador de reprodução populacional."),
        q("População economicamente ativa (PEA) inclui:", ["Apenas aposentados", "Empregados e desempregados em idade de trabalhar", "Somente crianças", "Turistas"], 1, "Força de trabalho disponível ou ocupada."),
        q("No Brasil, a região com maior concentração populacional é:", ["Norte", "Sudeste", "Centro-Oeste", "Amapá isolado"], 1, "SP, RJ, MG concentram milhões."),
        q("Migração internacional de refugiados decorre frequentemente de:", ["Guerras, perseguições e crises humanitárias", "Turismo", "Férias", "Estudos de curta duração"], 0, "Busca de proteção internacional."),
        q("Pirâmide etária com base estreita indica:", ["Alta natalidade", "Baixa natalidade e envelhecimento", "Guerra", "Alta imigração de jovens"], 1, "Topo largo = muitos idosos."),
        q("Crescimento zero populacional ocorre quando:", ["Natalidade equilibra mortalidade e migração", "Não há nascimentos", "Todos emigram", "A população dobra"], 0, "Taxa de crescimento próxima de zero."),
    ],
    "Geopolítica": [
        q("Geopolítica estuda:", ["Relação entre poder político e espaço geográfico", "Apenas clima", "Somente rochas", "Receitas culinárias"], 0, "Território, recursos e estratégias estatais."),
        q("O conceito de Estado-nação envolve:", ["Território, população, governo e soberania", "Apenas fronteiras naturais", "Somente bandeira", "Empresa privada"], 0, "Elementos clássicos do Estado moderno."),
        q("Guerra Fria foi um conflito entre:", ["EUA e URSS por influência global", "Brasil e Argentina", "França e Inglaterra medieval", "China e Japão feudal"], 0, "Bipolaridade capitalista vs. socialista."),
        q("Organização das Nações Unidas (ONU) foi criada em:", ["1914", "1945", "1989", "2001"], 1, "Pós-Segunda Guerra Mundial."),
        q("Unipolaridade pós-1991 referia-se à hegemonia de:", ["URSS", "EUA", "Alemanha", "Brasil"], 1, "Fim da URSS deixou EUA como superpotência."),
        q("Soft power (Nye) baseia-se em:", ["Força militar exclusiva", "Influência cultural, diplomática e econômica", "Apenas sanções", "Guerra nuclear"], 1, "Persuasão sem coerção militar direta."),
        q("Recursos estratégicos como petróleo geram:", ["Indiferença geopolítica", "Disputas e alianças internacionais", "Fim do comércio", "Paz automática"], 1, "Energia e minerais movem interesses globais."),
        q("Fronteiras artificiais impostas por colonizadores podem:", ["Ignorar etnias e gerar conflitos", "Sempre unir povos", "Eliminar guerras", "Ser sempre naturais"], 0, "África e Oriente Médio: exemplos de divisões coloniais."),
        q("O BRICS agrupa países com objetivo de:", ["Cooperação econômica e maior influência global", "Guerra contra a ONU", "Isolamento total", "União política como um só país"], 0, "Brasil, Rússia, Índia, China, África do Sul."),
        q("Terrorismo transnacional desafia Estados porque:", ["Atua além de fronteiras com redes globais", "Respeita sempre tratados", "Não usa tecnologia", "Só ocorre em um bairro"], 0, "Segurança exige cooperação internacional."),
    ],
})

print("GEO OK", len([x for s in GEO["submaterias"].values() for x in s]))
