#!/usr/bin/env python3
"""Banco de questões — Química (2º EM)."""

def q(text, opts, correct, expl, level="medio"):
    return [text, opts, correct, expl, level]

def pack(materia, code, title, desc, subs, minutes=75):
    total = sum(len(v) for v in subs.values())
    assert total == 50, f"{materia}: {total} questões"
    return {
        "materia": materia, "code": code, "title": title,
        "description": desc, "timeMinutes": minutes, "submaterias": subs
    }

QUI = pack("Química", "EM2-QUI", "Simulado — Química (2º EM)",
    "50 questões de múltipla escolha organizadas por sub-matéria.", {
    "Tabela Periódica": [
        q("Os elementos de um mesmo grupo (coluna) possuem:", ["Mesmo número de camadas", "Mesmo número de elétrons de valência", "Mesma massa atômica", "Mesmo número de nêutrons"], 1, "Grupos têm propriedades químicas semelhantes."),
        q("O número atômico (Z) indica:", ["Prótons no núcleo", "Massa do átomo", "Número de moléculas", "Carga do íon"], 0, "Z = prótons = elétrons no átomo neutro."),
        q("Metais alcalinos (grupo 1) são:", ["Muito reativos e formam bases fortes", "Gases nobres", "Halogenios", "Metais de transição inertes"], 0, "Li, Na, K — reatividade elevada com água."),
        q("Gases nobres (grupo 18) caracterizam-se por:", ["Alta reatividade química", "Baixa reatividade (octeto estável)", "Serem metais", "Formarem sais facilmente"], 1, "Camada de valência completa."),
        q("Períodos (linhas) da tabela correspondem a:", ["Número de camadas eletrônicas", "Número de prótons apenas", "Massa atómica", "Tipo de ligação"], 0, "Cada período = uma camada adicional."),
        q("O elemento com Z = 6 é:", ["Oxigênio", "Carbono", "Nitrogênio", "Boro"], 1, "Carbono: 6 prótons."),
        q("Eletronegatividade aumenta na tabela:", ["Do canto inferior esquerdo ao superior direito", "Do superior direito ao inferior esquerdo", "Apenas para metais", "Não varia"], 0, "Tendência periódica: F é o mais eletronegativo."),
        q("Isótopos são átomos do mesmo elemento com:", ["Mesmo Z, diferente número de nêutrons", "Diferente Z", "Mesma massa sempre", "Diferente número de elétrons no átomo neutro"], 0, "Ex.: carbono-12 e carbono-14."),
        q("Metais de transição localizam-se no:", ["Centro da tabela (bloco d)", "Grupo 18", "Grupo 1 apenas", "Topo da tabela"], 0, "Fe, Cu, Zn são metais de transição."),
        q("Halogênios (grupo 17) formam frequentemente:", ["Íons -1 (anions)", "Íons +2", "Gases nobres", "Ligações metálicas"], 0, "F, Cl, Br, I — ganham 1 elétron."),
    ],
    "Ligações Químicas": [
        q("Ligação iônica ocorre entre:", ["Átomos com grande diferença de eletronegatividade (metal + ametal)", "Somente não metais iguais", "Gases nobres", "Metais iguais"], 0, "Transferência de elétrons: NaCl."),
        q("Ligação covalente envolve:", ["Compartilhamento de elétrons", "Mar de elétrons", "Transferência total", "Atração iônica"], 0, "Comum entre não metais: H₂O, O₂."),
        q("Ligação metálica caracteriza-se por:", ["Mar de elétrons deslocalizados", "Compartilhamento em pares", "Íons fixos apenas", "Moléculas isoladas"], 0, "Condutividade e maleabilidade dos metais."),
        q("Fórmula do cloreto de sódio:", ["NaCl", "NaCl₂", "Na₂Cl", "NaO"], 0, "Na⁺ e Cl⁻ → NaCl."),
        q("Ligação covalente polar ocorre quando:", ["Há diferença de eletronegatividade entre átomos ligados", "Átomos idênticos se ligam", "Não há elétrons compartilhados", "Só metais participam"], 0, "Ex.: HCl, H₂O."),
        q("Dupla ligação aparece em moléculas como:", ["O₂ e CO₂", "NaCl", "Fe", "Ne"], 0, "Compartilhamento de 4 elétrons."),
        q("Geometria da molécula de água (VSEPR):", ["Angular", "Linear", "Tetraédrica", "Trigonal plana"], 0, "Dois pares ligantes + dois livres → angular."),
        q("Forças intermoleculares de hidrogênio são:", ["Fortes entre H ligado a F, O ou N", "Ligações covalentes", "Ligações iônicas", "Inexistentes na água"], 0, "Explicam alto ponto de ebulição da água."),
        q("Hibridização sp³ ocorre em:", ["Metano (CH₄)", "Etileno", "Acetileno", "Berílio"], 0, "Geometria tetraédrica."),
        q("Ligações pi envolvem:", ["Sobreposição lateral de orbitais p", "Sobreposição frontal (sigma) apenas", "Transferência iônica", "Mar de elétrons metálico"], 0, "Presentes em duplas e triplas ligações."),
    ],
    "Reações": [
        q("Reação de combustão completa do metano produz:", ["CO₂ e H₂O", "CO e C", "Apenas H₂", "NaCl"], 0, "CH₄ + 2O₂ → CO₂ + 2H₂O."),
        q("Balancear equação significa:", ["Igualar número de átomos de cada elemento", "Igualar coeficientes aleatoriamente", "Mudar fórmulas", "Ignorar oxigênio"], 0, "Conservação da massa (Lavoisier)."),
        q("Reação endotérmica:", ["Absorve calor do ambiente", "Libera calor", "Não envolve energia", "Só ocorre com metais"], 0, "Produtos têm mais energia que reagentes."),
        q("Catalisador:", ["Acelera reação sem ser consumido", "É consumido totalmente", "Para a reação", "Aumenta energia de ativação"], 0, "Oferece caminho alternativo de menor Ea."),
        q("Reação de neutralização ácido-base produz:", ["Sal e água", "Apenas gás", "Metal puro", "Álcool"], 0, "HCl + NaOH → NaCl + H₂O."),
        q("Oxidação envolve:", ["Perda de elétrons", "Ganho de elétrons", "Ganho de prótons", "Perda de nêutrons"], 0, "Agente oxidante ganha elétrons."),
        q("Redução envolve:", ["Ganho de elétrons", "Perda de elétrons", "Perda de massa", "Evaporação"], 0, "Agente redutor perde elétrons."),
        q("Velocidade de reação aumenta com:", ["Maior temperatura e concentração", "Menor superfície de contato", "Ausência de colisões", "Temperatura zero absoluto"], 0, "Mais colisões efetivas por unidade de tempo."),
        q("Reação reversível:", ["Pode ocorrer nos dois sentidos", "Só vai para frente", "Não atinge equilíbrio", "Destrói massa"], 0, "Equilíbrio químico: taxas iguais."),
        q("Lei da conservação das massas (Lavoisier):", ["Massa total dos reagentes = massa dos produtos", "Massa desaparece", "Massa dobra", "Só vale para gases"], 0, "Átomos são rearranjados, não criados/destruídos."),
    ],
    "Substâncias": [
        q("Substância pura:", ["Composição definida e constante", "Mistura de vários componentes", "Sempre impureza", "Só existe no estado gasoso"], 0, "Elementos e compostos são substâncias puras."),
        q("Mistura homogênea exemplo:", ["Água com sal dissolvido", "Água com óleo", "Areia e ferro", "Salada"], 0, "Fase única visível: solução salina."),
        q("Mistura heterogênea exemplo:", ["Água e areia", "Ar", "Álcool e água", "Liga de ouro"], 0, "Fases distintas visíveis."),
        q("Ponto de fusão de substância pura é:", ["Constante e característico", "Variável sempre", "Inexistente", "Igual para todas"], 0, "Propriedade intensiva de identificação."),
        q("Solubilidade depende de:", ["Temperatura, natureza do soluto e solvente", "Cor do recipiente", "Formato do copo", "Pressão atmosférica apenas"], 0, "Ex.: mais sal dissolve em água quente."),
        q("Filtração separa:", ["Sólido insolúvel de líquido", "Líquidos imiscíveis", "Gases", "Íons dissolvidos"], 0, "Retém partículas sólidas no filtro."),
        q("Destilação separa líquidos por:", ["Diferença de pontos de ebulição", "Densidade apenas", "Cor", "Magnetismo"], 0, "Evapora e condensa componentes."),
        q("Densidade d = m/V. Um corpo com d > da água:", ["Afunda na água", "Flutua", "Evapora", "Dissolve"], 0, "Corpos mais densos que o fluido afundam."),
        q("Ácido clorídrico (HCl) em solução aquosa é:", ["Ácido forte", "Base forte", "Sal neutro", "Gás nobre"], 0, "Ioniza completamente: H⁺ + Cl⁻."),
        q("pH = 7 indica solução:", ["Neutra", "Ácida", "Básica", "Concentrada em ácido"], 0, "pH 7 à 25°C: [H⁺] = [OH⁻]."),
    ],
    "Química Orgânica": [
        q("Carbono forma cadeias longas porque:", ["Pode fazer 4 ligações covalentes", "É metal", "Tem 1 elétron de valência", "Não reage"], 0, "Tetravalência do carbono."),
        q("Hidrocarboneto saturado exemplo:", ["Metano (CH₄)", "Etileno", "Etanol", "Ácido acético"], 0, "Apenas C e H, ligações simples."),
        q("Grupo funcional álcool contém:", ["Grupo -OH", "Grupo -COOH", "Grupo -NH₂", "Grupo -CHO"], 0, "Hidroxila caracteriza álcoois."),
        q("Isomeria plana: mesma fórmula molecular, diferente:", ["Fórmula", "Estrutura ou arranjo espacial", "Número de átomos", "Massa atômica"], 1, "Ex.: butano e isobutano."),
        q("Polímero é formado por:", ["Monômeros unidos em cadeia", "Um único átomo", "Íons apenas", "Metais"], 0, "Plásticos, borracha, DNA."),
        q("Combustão de hidrocarbonetos produz principalmente:", ["CO₂ e H₂O", "O₂ puro", "Metais", "Aminoácidos"], 0, "Reação com oxigênio."),
        q("Grupo carboxila (-COOH) caracteriza:", ["Ácidos carboxílicos", "Éteres", "Cetonas", "Aminas primárias"], 0, "Ex.: ácido acético."),
        q("Nome IUPAC do eteno é:", ["Eteno (etileno)", "Etano", "Etanol", "Eter"], 0, "Alceno de 2 carbonos: dupla ligação."),
        q("Plástico PET pertence à classe de:", ["Poliésteres", "Hidrocarbonetos gasosos", "Metais", "Sais iônicos"], 0, "Polímero sintético reciclável."),
        q("Química orgânica estuda principalmente compostos de:", ["Carbono", "Ferro", "Hélio", "Sódio apenas"], 0, "Compostos carbono-carbono e carbono-hidrogênio."),
    ],
})

print("QUI OK", len([x for s in QUI["submaterias"].values() for x in s]))
