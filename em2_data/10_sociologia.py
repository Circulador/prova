#!/usr/bin/env python3
"""Banco de questões — Sociologia (2º EM)."""

def q(text, opts, correct, expl, level="medio"):
    return [text, opts, correct, expl, level]

def pack(materia, code, title, desc, subs, minutes=75):
    total = sum(len(v) for v in subs.values())
    assert total == 50, f"{materia}: {total} questões"
    return {
        "materia": materia, "code": code, "title": title,
        "description": desc, "timeMinutes": minutes, "submaterias": subs
    }

SOC = pack("Sociologia", "EM2-SOC", "Simulado — Sociologia (2º EM)",
    "50 questões de múltipla escolha organizadas por sub-matéria.", {
    "Cultura": [
        q("Cultura, em sentido sociológico, compreende:", ["Apenas obras de arte eruditas", "Conjunto de valores, símbolos e práticas compartilhadas", "Herança genética", "Clima e relevo"], 1, "Cultura = modo de vida e significados sociais."),
        q("Etnocentrismo consiste em:", ["Valorizar a própria cultura como superior", "Estudar todas as culturas igualmente", "Negar qualquer identidade", "Isolar-se totalmente"], 0, "Julgar outras culturas pelo padrão próprio."),
        q("Relativismo cultural defende:", ["Compreender práticas no contexto de cada cultura", "Impor uma cultura universal", "Eliminar tradições", "Proibir diferenças"], 0, "Evita julgamentos absolutos sem contexto."),
        q("Cultura material inclui:", ["Objetos, tecnologias e bens produzidos", "Apenas crenças", "Valores invisíveis", "Emoções individuais"], 0, "Ex.: ferramentas, roupas, arquitetura."),
        q("Cultura imaterial inclui:", ["Normas, língua e religião", "Carros e prédios", "Minérios", "Animais domésticos"], 0, "Símbolos e significados não físicos."),
        q("Indústria cultural (Adorno/Horkheimer) critica:", ["Produção massificada de bens culturais", "Arte popular autêntica", "Tradições orais", "Rituais indígenas"], 0, "Cultura como mercadoria padronizada."),
        q("Globalização cultural pode gerar:", ["Hibridismo e circulação de símbolos", "Isolamento total", "Fim de todas as línguas", "Ausência de mídia"], 0, "Mistura e troca entre culturas."),
        q("Patrimônio cultural imaterial protege:", ["Práticas e saberes transmitidos", "Apenas edifícios antigos", "Só obras em museus", "Recursos minerais"], 0, "Ex.: capoeira, culinária, festas."),
        q("Identidade cultural relaciona-se a:", ["Sentimento de pertencimento e reconhecimento", "Apenas documentos legais", "Clima tropical", "Idade biológica"], 0, "Quem somos enquanto grupo."),
        q("Contracultura caracteriza-se por:", ["Oposição ou desafio a valores dominantes", "Reproduzir normas sem questionar", "Isolamento biológico", "Ausência de conflito"], 0, "Ex.: movimentos hippie, punk."),
    ],
    "Trabalho": [
        q("Divisão social do trabalho significa:", ["Especialização de funções na sociedade", "Todos fazem a mesma tarefa", "Ausência de profissões", "Trabalho apenas infantil"], 0, "Durkheim: interdependência por especialização."),
        q("Proletariado, para Marx, é:", ["Classe que vende força de trabalho", "Grupo de grandes proprietários", "Clero feudal", "Servidores públicos apenas"], 0, "Trabalhadores assalariados sem meios de produção."),
        q("Burguesia industrial detém:", ["Meios de produção e capital", "Apenas ferramentas manuais", "Terras comunais", "Nenhum recurso"], 0, "Classe dominante capitalista."),
        q("Alienação do trabalho, segundo Marx, implica:", ["Perda de controle sobre produto e processo", "Maior criatividade", "Propriedade plena", "Autogestão"], 0, "Trabalhador separado do fruto e sentido do trabalho."),
        q("Taylorismo enfatiza:", ["Organização científica e padronização do trabalho", "Autonomia total do operário", "Trabalho artesanal", "Greves gerais"], 0, "Eficiência e controle do tempo."),
        q("Fordismo associa-se a:", ["Produção em massa e linha de montagem", "Economia feudal", "Trocas de subsistência", "Trabalho doméstico isolado"], 0, "Modelo industrial do século XX."),
        q("Trabalho informal caracteriza-se por:", ["Ausência de registro e direitos formais", "Carteira assinada e benefícios plenos", "Apenas setor público", "Salários sempre altos"], 0, "Precariedade e invisibilidade estatística."),
        q("Desemprego estrutural decorre de:", ["Mudanças profundas na economia e tecnologia", "Férias coletivas", "Aposentadoria voluntária", "Excesso de vagas"], 0, "Desajuste entre oferta de emprego e qualificação."),
        q("Teletrabalho intensificado na pandemia alterou:", ["Fronteiras entre casa e trabalho", "Apenas o transporte público", "O clima", "A língua oficial"], 0, "Novas formas de organização e controle."),
        q("Sindicatos buscam principalmente:", ["Defesa de direitos e condições de trabalho", "Eliminar salários", "Proibir negociação", "Fechar empresas"], 0, "Organização coletiva dos trabalhadores."),
    ],
    "Movimentos Sociais": [
        q("Movimento social é:", ["Ação coletiva organizada por mudanças sociais", "Ato individual isolado", "Evento esportivo", "Campanha publicitária"], 0, "Grupos mobilizados por causas comuns."),
        q("Movimentos feministas lutam por:", ["Igualdade de gênero e direitos das mulheres", "Manutenção do patriarcado", "Exclusão política", "Proibição de voto"], 0, "Reivindicações históricas por equidade."),
        q("Movimento negro no Brasil combate:", ["Racismo estrutural e desigualdades", "Direitos civis", "Educação", "Cultura afro"], 0, "Luta contra discriminação e violência."),
        q("Movimentos ambientalistas defendem:", ["Sustentabilidade e preservação", "Poluição irrestrita", "Desmatamento total", "Uso ilimitado de combustíveis fósseis"], 0, "Meio ambiente e futuro das gerações."),
        q("Reforma agrária como pauta relaciona-se a:", ["Redistribuição de terras e justiça no campo", "Expulsão de camponeses", "Latifúndio eterno", "Urbanização forçada"], 0, "MST e movimentos camponeses."),
        q("Redes sociais nos movimentos atuais:", ["Amplificam mobilização e visibilidade", "Impedem qualquer protesto", "Substituem totalmente organização", "Eliminam reivindicações"], 0, "Hashtags e organização digital."),
        q("Movimento estudantil histórico (1968) exigiu:", ["Democracia, reformas e participação", "Restauração autoritária", "Fim da educação", "Monarquia"], 0, "Contexto de contestação global."),
        q("Identidade coletiva em movimentos fortalece:", ["Senso de pertencimento e ação conjunta", "Isolamento individual", "Apatia", "Conflito interno permanente"], 0, "Unidade simbólica e política."),
        q("Repressão estatal a movimentos pode incluir:", ["Violência policial e criminalização", "Diálogo institucional sempre", "Financiamento automático", "Voto obrigatório"], 0, "Depende do contexto político."),
        q("Conquistas de movimentos sociais podem resultar em:", ["Novas leis e políticas públicas", "Ausência de mudanças", "Retrocessos permanentes", "Fim da sociedade"], 0, "Ex.: direitos civis, ambientais."),
    ],
    "Desigualdade": [
        q("Desigualdade social refere-se a:", ["Diferenças de acesso a recursos e oportunidades", "Igualdade biológica", "Uniformidade de renda", "Ausência de classes"], 0, "Distribuição desigual de riqueza, educação, saúde."),
        q("O Índice de Gini mede:", ["Desigualdade de renda", "Temperatura média", "PIB absoluto", "População total"], 0, "0 = igualdade perfeita; 1 = concentração máxima."),
        q("Estratificação social organiza sociedade em:", ["Camadas ou classes hierárquicas", "Grupos idênticos", "Apenas indivíduos isolados", "Categorias biológicas fixas"], 0, "Classes, status e prestígio."),
        q("Mobilidade social vertical ascendente ocorre quando:", ["Indivíduo melhora posição socioeconômica", "Há queda de status", "Nada muda", "Todos ocupam mesmo lugar"], 0, "Ex.: filho de operário vira médico."),
        q("Pobreza extrema implica:", ["Dificuldade de suprir necessidades básicas", "Renda alta", "Acesso pleno a serviços", "Excesso de consumo"], 0, "Fome, moradia precária, exclusão."),
        q("Racismo estrutural manifesta-se em:", ["Práticas institucionais que reproduzem desigualdade racial", "Apenas insultos individuais", "Ausência de preconceito", "Igualdade plena"], 0, "Discriminação incorporada em estruturas."),
        q("Gênero e desigualdade: mulheres historicamente:", ["Receberam menos oportunidades e salários", "Sempre tiveram paridade total", "Não participaram do mercado", "Ocuparam todos os cargos de poder"], 0, "Patriarcado e divisão sexual do trabalho."),
        q("Elite econômica concentra:", ["Riqueza e influência política", "Pobreza extrema", "Trabalho manual apenas", "Nenhum recurso"], 0, "Pequeno grupo detém grande parte do patrimônio."),
        q("Políticas de ação afirmativa visam:", ["Reduzir desigualdades históricas", "Aumentar exclusão", "Eliminar cotas sempre", "Ignorar discriminação"], 0, "Cotas, bolsas, prioridades."),
        q("Interseccionalidade (Crenshaw) analisa:", ["Cruzamento de opressões (raça, gênero, classe)", "Apenas classe social", "Somente renda", "Clima e geografia"], 0, "Experiências múltiplas de discriminação."),
    ],
    "Cidadania": [
        q("Cidadania inclui direitos:", ["Civis, políticos e sociais", "Apenas militares", "Somente econômicos privados", "Nenhum"], 0, "Marshall: tripla dimensão da cidadania."),
        q("Direitos civis garantem:", ["Liberdades individuais e igualdade perante a lei", "Voto apenas", "Salário mínimo", "Férias pagas"], 0, "Ex.: liberdade de expressão, habeas corpus."),
        q("Direitos políticos incluem:", ["Votar, ser votado e participar do governo", "Apenas consumir", "Trabalhar sem descanso", "Propriedade privada exclusiva"], 0, "Participação na vida pública."),
        q("Direitos sociais referem-se a:", ["Educação, saúde e previdência", "Apenas liberdade de imprensa", "Serviço militar", "Propriedade de terras"], 0, "Bem-estar e dignidade material."),
        q("Participação cidadã pode ocorrer via:", ["Voto, associações, conselhos e protestos", "Apenas isolamento", "Desinteresse total", "Violência exclusiva"], 0, "Democracia exige engajamento."),
        q("Constituição de 1988 ampliou:", ["Direitos sociais e democracia no Brasil", "Censura", "Tortura institucional", "Exclusão de minorias"], 0, "Cidadania democrática pós-ditadura."),
        q("Apatia política caracteriza-se por:", ["Desinteresse e afastamento da vida pública", "Mobilização intensa", "Participação constante", "Voluntariado massivo"], 0, "Abstenção e descrença."),
        q("Tolerância democrática implica:", ["Respeitar diferenças dentro da lei", "Impor uma única opinião", "Proibir dissidência", "Violência contra opositores"], 0, "Pluralismo e convivência."),
        q("Cidadania digital envolve:", ["Uso responsável e crítico da internet", "Apenas consumo passivo", "Fake news sem verificação", "Anonimato para ataques"], 0, "Ética, privacidade, informação."),
        q("Controle social cidadão inclui:", ["Fiscalizar poder público e políticas", "Aceitar tudo sem questionar", "Eliminar transparência", "Corruptela tolerada"], 0, "Accountability e participação."),
    ],
})
