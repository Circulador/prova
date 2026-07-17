#!/usr/bin/env python3
"""Banco de questões — Biologia (2º EM)."""

def q(text, opts, correct, expl, level="medio"):
    return [text, opts, correct, expl, level]

def pack(materia, code, title, desc, subs, minutes=75):
    total = sum(len(v) for v in subs.values())
    assert total == 50, f"{materia}: {total} questões"
    return {
        "materia": materia, "code": code, "title": title,
        "description": desc, "timeMinutes": minutes, "submaterias": subs
    }

BIO = pack("Biologia", "EM2-BIO", "Simulado — Biologia (2º EM)",
    "50 questões de múltipla escolha organizadas por sub-matéria.", {
    "Citologia": [
        q("A célula eucarionte possui:", ["Núcleo delimitado por membrana", "Material genético livre no citoplasma", "Ausência de organelas", "Parede de peptidoglicano"], 0, "Núcleo verdadeiro distingue eucariontes."),
        q("A mitocôndria é responsável por:", ["Fotossíntese", "Respiração celular aeróbica (ATP)", "Digestão intracelular", "Síntese de proteínas"], 1, "Centro de produção de ATP."),
        q("O retículo endoplasmático rugoso possui:", ["Ribossomos aderidos", "Cloroplastos", "Centríolos", "Vacúolo central grande"], 0, "RER: síntese e processamento de proteínas."),
        q("A membrana plasmática é formada principalmente por:", ["Fosfolipídios e proteínas", "Celulose", "Quitina", "Peptidoglicano"], 0, "Mosaico fluido de fosfolipídios."),
        q("Ribossomos são locais de:", ["Síntese proteica (tradução)", "Replicação de DNA", "Fotossíntese", "Divisão celular"], 0, "Traduzem mRNA em proteínas."),
        q("Na mitose, o resultado é:", ["Duas células filhas geneticamente idênticas", "Quatro gametas", "Crossing-over", "Redução cromossômica"], 0, "Divisão somática conserva 2n."),
        q("Cloroplastos encontram-se em:", ["Células vegetais e algas", "Células animais", "Bactérias sem fotossíntese", "Vírus"], 0, "Organela da fotossíntese."),
        q("O complexo de Golgi atua na:", ["Modificação e empacotamento de proteínas", "Respiração", "Divisão nuclear", "Síntese de DNA"], 0, "Formação de vesículas de secreção."),
        q("Lisossomos contêm:", ["Enzimas hidrolíticas", "Clorofila", "DNA circular", "Flagelos"], 0, "Digestão intracelular."),
        q("Células procariontes diferem por:", ["Ausência de núcleo delimitado", "Presença de mitocôndrias", "Núcleo duplo", "Organização em tecidos"], 0, "Bactérias: DNA no nucleoide."),
    ],
    "Genética": [
        q("A unidade hereditária básica é o:", ["Gene", "Cromossomo inteiro", "Ribossomo", "ATP"], 0, "Gene = segmento de DNA com informação."),
        q("Em humanos, o número cromossômico diploide (2n) é:", ["23", "46", "92", "12"], 1, "23 pares = 46 cromossomos."),
        q("Lei da segregação (Mendel) refere-se à:", ["Separação dos alelos na meiose", "Dominância incompleta sempre", "Ligação gênica", "Mutação"], 0, "Cada gameta recebe um alelo."),
        q("Genótipo AA representa:", ["Homozigoto dominante", "Heterozigoto", "Homozigoto recessivo", "Aneuploidia"], 0, "Dois alelos iguais dominantes."),
        q("Cromossomo sexo XX determina:", ["Sexo feminino em humanos", "Sexo masculino", "Intersexo sempre", "Ausência de cromossomos"], 0, "XX feminino; XY masculino."),
        q("DNA replica-se por mecanismo:", ["Semiconservativo", "Conservativo total", "Dispersivo aleatório", "Não se replica"], 0, "Cada fita serve de molde."),
        q("Código genético é:", ["Universal (com poucas exceções)", "Diferente em cada célula", "Baseado em RNA apenas", "Sem códon de início"], 0, "Tripletes codificam aminoácidos."),
        q("Alelo dominante manifesta-se:", ["Na presença de um ou dois alelos dominantes", "Só se homozigoto", "Nunca", "Apenas na meiose"], 0, "Mascara recessivo em heterozigoto."),
        q("Síndrome de Down (trissomia 21) é exemplo de:", ["Aberração cromossômica", "Mutação pontual", "Dominância incompleta", "Codominância"], 0, "Três cópias do cromossomo 21."),
        q("Engenharia genética pode usar:", ["Plasmídeos e enzimas de restrição", "Apenas seleção natural", "Fotossíntese", "Mitose exclusivamente"], 0, "Técnicas de recombinante."),
    ],
    "Evolução": [
        q("Teoria da seleção natural foi proposta por:", ["Darwin e Wallace", "Lamarck apenas", "Mendel", "Pasteur"], 0, "Darwin (1859) e Wallace."),
        q("Seleção natural favorece:", ["Indivíduos com vantagem adaptativa no ambiente", "Todos igualmente", "Só os maiores", "Organismos estáticos"], 0, "Maior sobrevivência e reprodução."),
        q("Especiação pode ocorrer por:", ["Isolamento reprodutivo entre populações", "Fotossíntese", "Mitose", "Digestão"], 0, "Barreiras geográficas ou ecológicas."),
        q("Fósseis são importantes porque:", ["Documentam formas de vida passadas", "Produzem oxigênio", "São sempre artificiais", "Não têm idade"], 0, "Evidência paleontológica da evolução."),
        q("Homologia de estruturas indica:", ["Origem comum evolutiva", "Convergência sem parentesco", "Criação independente", "Ausência de DNA"], 0, "Ex.: ossos homólogos em membros."),
        q("Mutações são fonte de:", ["Variação genética", "Estabilidade absoluta", "Fim da evolução", "Clonagem natural"], 0, "Materia-prima para seleção."),
        q("Lamarck postulou que:", ["Características adquiridas seriam herdadas", "Seleção natural explica tudo", "Não há mudança nas espécies", "DNA não existe"], 0, "Teoria da herança dos caracteres adquiridos."),
        q("Evidência molecular da evolução inclui:", ["Similaridade de sequências de DNA entre espécies", "Identidade total de genomas", "Ausência de genes", "DNA apenas em plantas"], 0, "Filogenia molecular."),
        q("Adaptação é:", ["Característica que aumenta fitness no ambiente", "Sempre prejudicial", "Imutável", "Exclusiva de humanos"], 0, "Resultado de seleção natural."),
        q("Evolução biológica define-se como:", ["Mudança nas frequências alélicas ao longo do tempo", "Mudança individual na vida", "Crescimento corporal", "Aprendizado cultural"], 0, "Populacional, não individual."),
    ],
    "Ecologia": [
        q("Ecossistema inclui:", ["Componentes bióticos e abióticos interagindo", "Apenas animais", "Somente clima", "Laboratório"], 0, "Seres vivos + ambiente físico."),
        q("Produtor primário em ecossistema terrestre típico:", ["Planta fotossintética", "Fungo decompositor", "Carnívoro", "Detritívoro"], 0, "Base da cadeia alimentar."),
        q("Pirâmide ecológica de energia:", ["Diminui a cada nível trófico", "Aumenta infinitamente", "É constante", "Não existe perda"], 0, "~10% de transferência entre níveis."),
        q("Cadeia alimentar: capim → gafanhoto → pássaro representa:", ["Produtor → consumidor primário → secundário", "Decomposição", "Ciclo do carbono", "Fixação de nitrogênio"], 0, "Fluxo linear de energia."),
        q("Sucessão ecológica é:", ["Substituição gradual de comunidades", "Extinção imediata", "Poluição", "Clonagem"], 0, "Ex.: capoeira → floresta madura."),
        q("Bioma Cerrado caracteriza-se por:", ["Vegetação arbustiva, clima tropical sazonal", "Floresta equatorial úmida", "Deserto polar", "Recife de coral"], 0, "Savana brasileira."),
        q("Efeito estufa aumentado intensifica:", ["Retenção de calor na atmosfera", "Resfriamento global", "Camada de ozônio estratosférica", "Fotossíntese oceânica apenas"], 0, "Gases antropogênicos retêm IR."),
        q("Biodiversidade refere-se à:", ["Variedade de espécies e genes", "Número de indivíduos de uma espécie", "Tamanho dos animais", "Velocidade de crescimento"], 0, "Diversidade biológica em múltiplos níveis."),
        q("Relação mutualística (+/+) exemplo:", ["Polinização abelha-flor", "Predação", "Parasitismo", "Competição"], 0, "Ambos se beneficiam."),
        q("Ciclo do carbono envolve:", ["Fotossíntese, respiração e combustão", "Apenas evaporação", "Somente mineração", "Digestão estomacal"], 0, "CO₂ ↔ matéria orgânica."),
    ],
    "Fisiologia Humana": [
        q("O sangue transporta principalmente:", ["O₂, nutrientes e resíduos", "Apenas água pura", "Somente hormônios", "Linfócitos apenas"], 0, "Função de transporte e homeostase."),
        q("A unidade funcional do rim é:", ["Néfron", "Alvéolo", "Neurônio", "Osteócito"], 0, "Filtração e formação da urina."),
        q("Insulina produzida no pâncreas:", ["Reduz glicemia", "Aumenta glicemia", "Para o coração", "Digestão de proteínas"], 0, "Facilita entrada de glicose nas células."),
        q("Sistema nervoso central compreende:", ["Encéfalo e medula espinhal", "Apenas nervos periféricos", "Somente músculos", "Pele"], 0, "CNS vs. SNP."),
        q("Hemoglobina localiza-se nos:", ["Glóbulos vermelhos", "Plaquetas", "Leucócitos", "Plasma apenas"], 0, "Transporte de O₂."),
        q("Digestão da amido inicia-se na:", ["Boca (saliva amilase)", "Estômago", "Intestino grosso", "Traqueia"], 0, "Enzima salivar quebra amido."),
        q("A troca gasosa pulmonar ocorre nos:", ["Alvéolos", "Brônquios principais", "Traqueia", "Laringe"], 0, "Superfície fina e vascularizada."),
        q("Anticorpos são produzidos por:", ["Linfócitos B (plasmócitos)", "Glóbulos vermelhos", "Osteoblastos", "Neurônios"], 0, "Resposta imune adaptativa."),
        q("Homeostase significa:", ["Manutenção do equilíbrio interno", "Crescimento descontrolado", "Febre permanente", "Parada cardíaca"], 0, "Temperatura, pH, glicose regulados."),
        q("Contração muscular esquelética envolve:", ["Actina e miosina deslizando", "Fotossíntese", "Mitose", "Digestão de lipídios"], 0, "Teoria do filamento deslizante."),
    ],
})

print("BIO OK", len([x for s in BIO["submaterias"].values() for x in s]))
