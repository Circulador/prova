#!/usr/bin/env python3
"""Gera em2_bank_data.json com 50 questões por matéria (2º EM)."""
import json, pathlib

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "em2_bank_data.json"

def q(text, opts, correct, expl, level="medio"):
    return [text, opts, correct, expl, level]

def pack(materia, code, title, desc, subs, minutes=75):
    total = sum(len(v) for v in subs.values())
    assert total == 50, f"{materia}: {total} questões"
    return {
        "materia": materia, "code": code, "title": title,
        "description": desc, "timeMinutes": minutes, "submaterias": subs
    }

# --- LÍNGUA PORTUGUESA ---
PORT = pack("Língua Portuguesa", "EM2-PORT", "Simulado — Língua Portuguesa (2º EM)",
    "50 questões de múltipla escolha organizadas por sub-matéria.", {
    "Gramática": [
        q("O sujeito da oração 'Os alunos estudaram para a prova' é:", ["Simples", "Composto", "Oculto", "Indeterminado"], 0, "Há um único núcleo: alunos."),
        q("Em 'Choveu muito ontem', o sujeito é:", ["Simples", "Composto", "Desinencial", "Indeterminado"], 3, "Verbos impessoais como 'chover' têm sujeito indeterminado."),
        q("A palavra 'rapidamente' classifica-se como:", ["Substantivo", "Adjetivo", "Advérbio", "Preposição"], 2, "Modifica o verbo, indicando modo."),
        q("Qual alternativa apresenta apenas palavras prosódicas?", ["casa, mesa, livro", "e, mas, porém", "correr, pular, nadar", "belo, feio, grande"], 1, "Conjunções coordenativas são prosódicas."),
        q("O plural de 'cidadão' é:", ["cidadãos", "cidadões", "cidadães", "cidadãoes"], 1, "Formação irregular: cidadão → cidadões."),
        q("'Menos pior' é considerado:", ["Correto", "Pleonasmo vicioso", "Figura de linguagem", "Neologismo"], 1, "Comparativo de inferioridade com 'pior' é vício de linguagem."),
        q("Em 'Comprei um carro novo', 'novo' é:", ["Substantivo", "Adjetivo", "Advérbio", "Artigo"], 1, "Caracteriza o substantivo carro."),
        q("A oração 'Quando cheguei, todos já tinham saído' tem:", ["Oração subordinada adverbial temporal", "Oração coordenada adversativa", "Oração subordinada substantiva", "Oração coordenada conclusiva"], 0, "'Quando cheguei' indica tempo."),
        q("O pronome 'que' em 'O livro que li é bom' exerce função de:", ["Sujeito", "Objeto direto", "Predicativo", "Adjunto adverbial"], 1, "Retoma 'livro' como OD de 'li'."),
        q("Colocação pronominal correta:", ["Me disseram a verdade.", "Disseram-me a verdade.", "Disseram me a verdade.", "Me disseram a verdade ontem."], 1, "Ênclise após verbo no início é preferível; próclise com advérbio 'ontem' seria 'Me disseram ontem'."),
    ],
    "Interpretação de Texto": [
        q("O gênero textual 'notícia' caracteriza-se por:", ["Subjetividade do autor", "Informar fatos de interesse público", "Narrar ficção", "Convencer o leitor"], 1, "Notícia prioriza informação objetiva."),
        q("A inferência textual consiste em:", ["Copiar trechos do texto", "Concluir informações não explícitas", "Ignorar o contexto", "Resumir o título"], 1, "Inferir vai além do literal."),
        q("Ironia ocorre quando:", ["Autor repete ideias", "Há contraste entre o dito e o pretendido", "Texto é neutro", "Não há interlocutor"], 1, "Ironia usa sentido oposto ao literal."),
        q("Paráfrase significa:", ["Reescrever com outras palavras mantendo sentido", "Criticar o autor", "Ampliar o texto", "Traduzir para outro idioma"], 0, "Parafrasear é reformular."),
        q("Intertextualidade é:", ["Ausência de referências", "Diálogo entre textos", "Erro de ortografia", "Tipo de pontuação"], 1, "Textos dialogam com outros textos."),
        q("Tese de um artigo de opinião é:", ["A conclusão do leitor", "Posição central defendida", "A bibliografia", "O título apenas"], 1, "Tese é a ideia principal defendida."),
        q("Coesão textual garante:", ["Beleza estética", "Encadeamento lógico entre partes", "Originalidade", "Tamanho do texto"], 1, "Coesão liga elementos do texto."),
        q("Denotação refere-se a:", ["Sentido figurado", "Sentido literal da palavra", "Opinião do autor", "Rima"], 1, "Denotação = sentido dicionarizado."),
        q("Conotação refere-se a:", ["Sentido literal", "Sentido figurado ou subjetivo", "Ortografia", "Sílaba tônica"], 1, "Conotação carrega valor afetivo/cultural."),
        q("Em uma charge, o humor geralmente apoia-se em:", ["Descrição técnica", "Crítica social por imagem e texto", "Receita culinária", "Lista de dados"], 1, "Charge combina imagem e crítica."),
    ],
    "Literatura": [
        q("O Romantismo valorizou principalmente:", ["Razão e ciência", "Emoção, subjetividade e natureza", "Objetividade jornalística", "Regras clássicas rígidas"], 1, "Romantismo exalta sentimento e individualidade."),
        q("Machado de Assis é autor de:", ["Os Sertões", "Dom Casmurro", "O Cortiço", "Iracema"], 1, "Dom Casmurro é romance machadiano."),
        q("A rima ABAB indica:", ["Rimas alternadas", "Rimas emparelhadas", "Rima rica", "Ausência de rima"], 0, "Versos 1-3 e 2-4 rimam alternadamente."),
        q("O Modernismo brasileiro iniciou-se em:", ["1889", "1922", "1945", "1964"], 1, "Semana de Arte Moderna de 1922."),
        q("Soneto possui tradicionalmente:", ["8 versos", "10 versos", "14 versos", "20 versos"], 2, "Soneto clássico = 14 versos."),
        q("Realismo literário busca:", ["Idealização heroica", "Análise crítica da sociedade", "Fuga da realidade", "Mito fundador"], 1, "Realismo observa e critica a sociedade."),
        q("Narrador onisciente:", ["Sabe tudo sobre personagens", "Participa da história", "É criança", "Não existe"], 0, "Onisciente domina informações."),
        q("Metáfora consiste em:", ["Repetição de sons", "Comparação implícita", "Exagero", "Inversão"], 1, "Metáfora = comparação sem conectivo."),
        q("Clímax de uma narrativa é:", ["Apresentação do cenário", "Momento de maior tensão", "Descrição do autor", "Nota de rodapé"], 1, "Clímax = ponto alto da ação."),
        q("Quinhentismo relaciona-se à:", ["Produção literária da colonização", "Poesia concretista", "Literatura contemporânea", "Teatro grego"], 0, "Século XVI, cartas e crônicas coloniais."),
    ],
    "Ortografia e Semântica": [
        q("Emprego correto de 'mas':", ["Mais eu fui.", "Queria ir, mas choveu.", "Mas pessoas vieram.", "Fui mas casa."], 1, "'Mas' = conjunção adversativa."),
        q("'Há' em 'Há dois anos' indica:", ["Ação no futuro", "Tempo passado / existência", "Modo imperativo", "Lugar"], 1, "Verbo haver no sentido de tempo decorrido."),
        q("Palavra com hiato:", ["saída", "chuva", "porta", "livro"], 0, "Sa-í-da: vogais em sílabas separadas."),
        q("Sinônimo de 'rápido':", ["Lento", "Veloz", "Pesado", "Frio"], 1, "Veloz = rápido."),
        q("Antônimo de 'claro':", ["Luminoso", "Escuro", "Brilhante", "Transparente"], 1, "Escuro opõe-se a claro."),
        q("Acento diferencial: pôde/pode distingue:", ["Número", "Tempo verbal", "Gênero", "Grau"], 1, "Pôde (pretérito) x pode (presente)."),
        q("'Porque' explicativo separa-se:", ["Sempre", "Quando equivale a 'pois'", "Nunca se escreve", "Só no início"], 1, "Explicativo pode ser 'porque' junto."),
        q("Parônimo de 'sessão':", ["Cessão", "Seção", "Ambas anteriores", "Nenhuma"], 2, "Sessão, cessão e seção são parônimos."),
        q("Polissemia ocorre quando:", ["Palavra tem um sentido", "Palavra tem vários sentidos", "Palavra não existe", "Palavra é estrangeira"], 1, "Ex.: 'manga' (fruta/roupa)."),
        q("Homônimo perfeito:", ["manga/manga (sentidos diferentes)", "caro/caro (mesmo som e sentido)", "mais/mas", "saída/saida"], 1, "Homônimo perfeito: mesma forma e som."),
    ],
    "Variação Linguística": [
        q("Variação diatópica relaciona-se a:", ["Tempo", "Região geográfica", "Situação formal", "Idade"], 1, "Diatópica = regional."),
        q("Linguagem formal usa:", ["Gírias e abreviações", "Norma culta e registro elevado", "Apenas oralidade", "Erros propositais"], 1, "Formal = norma padrão."),
        q("Preconceito linguístico é:", ["Valorizar todas as variantes", "Julgar inferior quem fala diferente", "Estudar dialetos", "Traduzir textos"], 1, "Preconceito estigmatiza variantes."),
        q("Neologismo é:", ["Palavra arcaica", "Palavra nova ou recente", "Erro de digitação", "Sigla antiga"], 1, "Ex.: 'selfie', 'podcast'."),
        q("Linguagem coloquial caracteriza-se por:", ["Rigidez e distanciamento", "Espontaneidade e proximidade", "Apenas escrita", "Termos técnicos"], 1, "Coloquial = conversa cotidiana."),
        q("Variação diacrônica estuda:", ["Regiões", "Mudanças ao longo do tempo", "Níveis de formalidade", "Gêneros textuais"], 1, "Diacrônica = histórica."),
        q("Registro técnico usa:", ["Vocabulário especializado", "Somente gírias", "Apenas emojis", "Linguagem infantil"], 0, "Termos da área específica."),
        q("A norma-padrão:", ["Substitui todas as variantes", "Convencionou-se para comunicação formal", "Não existe no Brasil", "É igual ao dialeto caipira"], 1, "Norma-padrão para contextos oficiais."),
        q("Estrangeirismo é:", ["Palavra de origem estrangeira usada no idioma", "Erro gramatical", "Tipo de verso", "Pontuação"], 0, "Ex.: 'software', 'marketing'."),
        q("Variação diastrática relaciona-se a:", ["Grupo social", "Região", "Tempo histórico", "Canal de comunicação"], 0, "Diastrática = condição social."),
    ],
})

print("PORT OK", len([x for s in PORT["submaterias"].values() for x in s]))
