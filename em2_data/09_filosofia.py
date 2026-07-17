#!/usr/bin/env python3
"""Banco de questões — Filosofia (2º EM)."""

def q(text, opts, correct, expl, level="medio"):
    return [text, opts, correct, expl, level]

def pack(materia, code, title, desc, subs, minutes=75):
    total = sum(len(v) for v in subs.values())
    assert total == 50, f"{materia}: {total} questões"
    return {
        "materia": materia, "code": code, "title": title,
        "description": desc, "timeMinutes": minutes, "submaterias": subs
    }

FIL = pack("Filosofia", "EM2-FIL", "Simulado — Filosofia (2º EM)",
    "50 questões de múltipla escolha organizadas por sub-matéria.", {
    "Iluminismo": [
        q("O Iluminismo valorizou principalmente:", ["Autoridade religiosa absoluta", "Razão, ciência e crítica ao dogmatismo", "Misticismo medieval", "Tradição feudal"], 1, "Século XVIII: luz da razão."),
        q("Voltaire defendia:", ["Tolerância e liberdade de pensamento", "Absolutismo sem crítica", "Escravidão", "Censura total"], 0, "Crítica à intolerância e fanatismo."),
        q("Montesquieu propôs a separação dos poderes em:", ["Executivo, legislativo e judiciário", "Clero, nobreza e povo", "Rei, exército e igreja", "Economia, cultura e esporte"], 0, "O Espírito das Leis."),
        q("Rousseau, no contrato social, enfatizou:", ["Vontade geral e soberania popular", "Direito divino dos reis", "Anarquia total", "Isolamento individual"], 0, "Legitimidade pelo acordo coletivo."),
        q("Kant sintetizou o Iluminismo com:", ["'Ousa saber' (Sapere aude)", "Fé cega", "Guerra permanente", "Tradição oral"], 0, "Coragem de usar a própria razão."),
        q("Enciclopedistas como Diderot buscavam:", ["Compilar e difundir conhecimento racional", "Proibir ciência", "Restaurar feudalismo", "Eliminar artes"], 0, "Encyclopédie como obra emblemática."),
        q("Despotismo esclarecido pretendia:", ["Reformas racionais conduzidas pelo monarca", "República imediata", "Teocracia", "Retorno ao feudalismo"], 0, "Monarca aplica ideias iluministas."),
        q("Locke influenciou o Iluminismo com ideias sobre:", ["Direitos naturais e governo limitado", "Determinismo biológico", "Escolástica", "Alquimia"], 0, "Vida, liberdade e propriedade."),
        q("Crítica iluminista ao Antigo Regime focava:", ["Privilégios estamentais e absolutismo", "Excesso de democracia", "Ciência moderna", "Comércio internacional"], 0, "Questionamento do poder absoluto."),
        q("A frase 'homem nasce livre e everywhere está em cadeias' é de:", ["Rousseau", "Platão", "Nietzsche", "Marx"], 0, "Do Contrato Social."),
    ],
    "Contratualismo": [
        q("Contratualismo explica a sociedade política por:", ["Contrato entre indivíduos", "Decreto divino apenas", "Instinto animal", "Sorte"], 0, "Acordo racional funda o Estado."),
        q("Para Hobbes, no estado de natureza a vida é:", ["Solitária, pobre, nasty, brutish and short", "Pacífica e cooperativa", "Igualitária utópica", "Sem conflitos"], 0, "Guerra de todos contra todos."),
        q("Hobbes defende um soberano:", ["Absoluto para garantir paz", "Eleito a cada mês", "Inexistente", "Apenas simbólico"], 0, "Leviatã com poder coercitivo."),
        q("Locke distingue-se de Hobbes ao enfatizar:", ["Direitos inalienáveis e governo limitado", "Tiranía necessária", "Anulação da propriedade", "Guerra permanente"], 0, "Direito de resistir ao tirano."),
        q("Rousseau critica a desigualdade originada na:", ["Propriedade privada e civilização", "Razão pura", "Democracia direta", "Educação pública"], 0, "Discurso sobre a Origem da Desigualdade."),
        q("Contrato social para Rousseau preserva:", ["Liberdade mediante vontade geral", "Escravidão voluntária", "Monarquia absoluta", "Isolamento"], 0, "Obediência à lei que se dá a si mesmo."),
        q("Estado de natureza no contratualismo é:", ["Situação hipotética pré-política", "Período histórico documentado", "Era industrial", "Idade média"], 0, "Construção teórica, não história empírica."),
        q("Legitimidade do poder no contrato vem de:", ["Consentimento dos governados", "Força bruta apenas", "Herança divina", "Acaso"], 0, "Autoridade derivada do acordo."),
        q("Rawls (contrato moderno) usa o véu da ignorância para:", ["Garantir imparcialidade na escolha de princíios de justiça", "Ocultar crimes", "Negar direitos", "Defender utilitarismo extremo"], 0, "Teoria da justiça como equidade."),
        q("Crítica comum ao contratualismo:", ["Individualismo e abstração do sujeito", "Excesso de coletivismo", "Negar razão", "Defender teocracia"], 0, "Ignora desigualdades históricas reais."),
    ],
    "Ética": [
        q("Ética de Aristóteles centra-se em:", ["Virtude e eudaimonia (felicidade)", "Utilidade máxima", "Dever categórico", "Vontade de poder"], 0, "Ética das virtudes."),
        q("Utilitarismo (Bentham/Mill) julga ações pelo:", ["Maior felicidade para o maior número", "Dever absoluto", "Tradição", "Beleza estética"], 0, "Consequencialismo hedonista."),
        q("Dever categórico é conceito de:", ["Kant", "Nietzsche", "Epicuro", "Maquiavel"], 0, "Agir conforme máxima universalizável."),
        q("Ética do cuidado enfatiza:", ["Relações, empatia e responsabilidade", "Cálculo frio apenas", "Egoísmo", "Guerra"], 0, "Gilligan e críticas ao universalismo masculino."),
        q("Dilema do bonde (trolley problem) explora:", ["Conflitos entre consequências e deveres", "Física newtoniana", "Estética", "Lógica matemática"], 0, "Ética aplicada e escolhas morais."),
        q("Relativismo moral sustenta que:", ["Valores morais variam conforme cultura/contexto", "Existe uma única moral absoluta universal", "Ética não existe", "Só importa a lei"], 0, "Críticas: pode tolerar injustiças."),
        q("Ética profissional inclui:", ["Códigos de conduta e responsabilidade", "Lucro a qualquer custo", "Ocultação de erros", "Corrupção"], 0, "Medicina, direito, jornalismo têm códigos."),
        q("Autonomia moral (Kant) significa:", ["Agir pela razão e lei moral autoimposta", "Seguir ordens sem pensar", "Obediência cega", "Hedonismo"], 0, "Dignidade da pessoa racional."),
        q("Ética ambiental questiona:", ["Antropocentrismo e destruição da natureza", "Apenas moda", "Esportes", "Matemática"], 0, "Responsabilidade intergeracional."),
        q("Solidariedade, em ética política, implica:", ["Reconhecimento mútuo e cooperação", "Competição extrema", "Isolamento", "Violência"], 0, "Valor democrático e social."),
    ],
    "Marx": [
        q("Materialismo histórico de Marx analisa:", ["Modos de produção e lutas de classes", "Ideias desconectadas da economia", "Destino divino", "Psicanálise"], 0, "Infraestrutura econômica condiciona superestrutura."),
        q("Mais-valia é:", ["Lucro do capitalista sobre trabalho não pago", "Salário justo", "Imposto estatal", "Doação"], 0, "Exploração da força de trabalho."),
        q("Luta de classes opõe, no capitalismo:", ["Proletariado e burguesia", "Rei e nobreza feudal", "Deuses e homens", "Professores e alunos"], 0, "Classes sociais capitalistas."),
        q("Alienação do trabalhador significa:", ["Separação do produto, processo e potencial humano", "Felicidade plena", "Propriedade dos meios de produção", "Lazer"], 0, "Trabalho estranhado ao trabalhador."),
        q("Comunismo, para Marx, seria:", ["Sociedade sem classes e propriedade privada dos meios de produção", "Estado absolutista", "Feudalismo", "Anarquia mercantil"], 0, "Estágio pós-capitalista teórico."),
        q("Ideologia, no marxismo, é:", ["Conjunto de ideias que legitima dominação", "Verdade pura", "Ciência exata", "Arte neutra"], 0, "Falsa consciência que naturaliza ordem."),
        q("Manifesto Comunista foi escrito por:", ["Marx e Engels", "Lenin solo", "Rousseau", "Hobbes"], 0, "1848: 'Proletários de todos os países...'"),
        q("Crítica marxista ao capitalismo inclui:", ["Concentração de riqueza e crises cíclicas", "Igualdade plena", "Fim do trabalho", "Ausência de tecnologia"], 0, "Contradições internas do modo capitalista."),
        q("Superestrutura compreende:", ["Cultura, política, ideologia", "Apenas fábricas", "Solo agrícola", "Clima"], 0, "Instituições e ideias sobre base econômica."),
        q("Socialismo científico opõe-se ao utópico por:", ["Análise histórica das condições materiais", "Sonhos sem método", "Teologia", "Misticismo"], 0, "Marx critica socialistas utópicos."),
    ],
    "Existencialismo": [
        q("Existencialismo enfatiza:", ["Existência precede essência", "Essência divina fixa", "Determinismo biológico total", "Utilidade"], 0, "Sartre: o homem se faz por escolhas."),
        q("Sartre afirmou que o homem é:", ["Condemnado to be free", "Totalmente determinado", "Sem responsabilidade", "Apenas corpo"], 0, "Liberdade implica responsabilidade."),
        q("Angústia existencial relaciona-se a:", ["Consciência da liberdade e escolha", "Falta de comida", "Soma matemática", "Clima"], 0, "Peso das decisões."),
        q("Camus tratou do absurdo em:", ["O Mito de Sísifo", "A República", "Leviatã", "Utopia"], 0, "Conflito entre busca de sentido e mundo silencioso."),
        q("Bad faith (má-fé) para Sartre é:", ["Autoengano para negar liberdade", "Honestidade radical", "Fé religiosa autêntica", "Altruísmo"], 0, "Pretender ser coisa, não sujeito."),
        q("Kierkegaard é precursor existencialista por focar:", ["Individualidade, escolha e angústia", "Sistema hegeliano fechado", "Utilitarismo", "Materialismo"], 0, "Existência concreta vs. abstração."),
        q("Nietzsche declarou 'Deus está morto' para criticar:", ["Valores nihilistas e moral tradicional sem fundamento", "Ateísmo militante", "Ciência", "Arte"], 0, "Crise de sentido na modernidade."),
        q("Autenticidade existencial exige:", ["Assumir escolhas próprias", "Viver conforme os outros sempre", "Negar liberdade", "Isolamento total"], 0, "Viver de acordo com decisões reconhecidas."),
        q("Heidegger analisou o ser pelo conceito de:", ["Dasein (ser-aí)", "Átomo", "Utilidade", "Tabula rasa"], 0, "Existência humana como questão do ser."),
        q("Existencialismo pós-guerra reflete:", ["Trauma, crise de sentido e responsabilidade individual", "Otimismo ilimitado", "Feudalismo", "Colonialismo antigo"], 0, "Contexto de guerras e totalitarismos."),
    ],
})

print("FIL OK", len([x for s in FIL["submaterias"].values() for x in s]))
