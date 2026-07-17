#!/usr/bin/env python3
"""Banco de questões — Física (2º EM)."""

def q(text, opts, correct, expl, level="medio"):
    return [text, opts, correct, expl, level]

def pack(materia, code, title, desc, subs, minutes=75):
    total = sum(len(v) for v in subs.values())
    assert total == 50, f"{materia}: {total} questões"
    return {
        "materia": materia, "code": code, "title": title,
        "description": desc, "timeMinutes": minutes, "submaterias": subs
    }

FIS = pack("Física", "EM2-FIS", "Simulado — Física (2º EM)",
    "50 questões de múltipla escolha organizadas por sub-matéria.", {
    "Cinemática": [
        q("A velocidade média é calculada por:", ["Δs/Δt", "m·a", "F·d", "P/V"], 0, "v = variação de espaço / variação de tempo."),
        q("A aceleração mede a variação de:", ["Massa", "Velocidade no tempo", "Temperatura", "Volume"], 1, "a = Δv/Δt."),
        q("Movimento uniforme (MU) tem aceleração:", ["Zero", "Constante e diferente de zero", "Variável", "Infinita"], 0, "Velocidade constante → aceleração nula."),
        q("Um carro percorre 120 km em 2 h. Sua velocidade média é:", ["60 km/h", "120 km/h", "240 km/h", "30 km/h"], 0, "120/2 = 60 km/h."),
        q("Queda livre próxima à Terra tem aceleração aproximada de:", ["1 m/s²", "9,8 m/s²", "98 m/s²", "0 m/s²"], 1, "Aceleração da gravidade g ≈ 9,8 m/s²."),
        q("No gráfico s × t de MU, a inclinação representa:", ["Aceleração", "Velocidade", "Força", "Energia"], 1, "Inclinação = Δs/Δt = v."),
        q("MRUV significa movimento retilíneo com:", ["Velocidade uniforme", "Veloceração uniforme", "Trajetória circular", "Repouso"], 1, "Aceleração constante em linha reta."),
        q("A equação horária do espaço no MRUV é:", ["s = s₀ + vt", "s = s₀ + v₀t + at²/2", "F = ma", "E = mc²"], 1, "Inclui termo acelerado."),
        q("Lançamento vertical: no ponto mais alto, a velocidade vertical é:", ["Máxima", "Zero", "Igual à inicial", "Negativa infinita"], 1, "Instantaneamente v = 0 antes de descer."),
        q("Referencial inercial é aquele em que:", ["Vale a 1ª lei de Newton", "Há aceleração fictícia sempre", "Não se mede tempo", "A gravidade é zero"], 0, "Corpo livre de força resultante mantém v constante."),
    ],
    "Dinâmica": [
        q("A 2ª lei de Newton estabelece:", ["F = m·a", "E = mc²", "V = R·i", "P = m·g"], 0, "Força resultante = massa × aceleração."),
        q("A unidade de força no SI é:", ["Joule", "Newton", "Watt", "Pascal"], 1, "1 N = 1 kg·m/s²."),
        q("Peso de um corpo de 10 kg (g = 10 m/s²) é:", ["1 N", "10 N", "100 N", "1000 N"], 2, "P = m·g = 10 × 10 = 100 N."),
        q("A 3ª lei de Newton diz que:", ["Ação e reação têm mesma intensidade e sentidos opostos", "F = ma", "Energia se conserva sempre", "Velocidade é constante"], 0, "Forças em pares atuam em corpos diferentes."),
        q("Atrito cinético tende a:", ["Aumentar movimento", "Opor-se ao deslizamento", "Anular gravidade", "Criar energia"], 1, "Força contrária ao movimento relativo."),
        q("Plano inclinado: componente da força peso paralela ao plano é:", ["m·g·senθ", "m·g·cosθ", "m·a", "Zero sempre"], 0, "Decomposição do peso na direção da rampa."),
        q("Força centrípeta é responsável por:", ["Manter movimento circular", "Aumentar massa", "Gerar calor apenas", "Anular inércia totalmente"], 0, "Muda direção da velocidade."),
        q("A 1ª lei de Newton também é chamada lei da:", ["Gravitação", "Inércia", "Termodinâmica", "Conservação de carga"], 1, "Corpo tende a manter estado de movimento."),
        q("Empuxo de Arquimedes atua:", ["Para cima, igual ao peso do fluido deslocado", "Para baixo", "Horizontalmente", "Só em vácuo"], 0, "Corpo imerso recebe empuxo vertical para cima."),
        q("Diagrama de corpo livre serve para:", ["Representar forças que atuam no corpo", "Medir temperatura", "Calcular volume", "Desenhar circuitos"], 0, "Isola o corpo e indica vetores de força."),
    ],
    "Energia": [
        q("A energia cinética é dada por:", ["Ec = mv²/2", "Ep = mgh", "P = Fv", "Q = mcΔT"], 0, "Depende da massa e do quadrado da velocidade."),
        q("Energia potencial gravitacional próxima à Terra:", ["Ep = mgh", "Ec = mv²/2", "F = ma", "V = Ri"], 0, "Depende de altura h."),
        q("Princípio da conservação de energia mecânica (sem atrito):", ["Em = Ec + Ep = constante", "Energia desaparece", "Só Ep se conserva", "Ec sempre zero"], 0, "Transformação entre cinética e potencial."),
        q("Trabalho de uma força constante paralela ao deslocamento:", ["τ = F·d", "P = E/t", "F = ma", "E = Q"], 0, "τ = força × deslocamento (cos θ se não paralelo)."),
        q("Potência mede:", ["Rapidez de transferência de energia", "Massa", "Força", "Volume"], 0, "P = trabalho/tempo ou P = F·v."),
        q("1 joule equivale a:", ["1 N·m", "1 kg/m²", "1 W/s", "1 V/A"], 0, "Unidade de energia e trabalho no SI."),
        q("Rendimento de uma máquina é:", ["Energia útil / energia total × 100%", "Sempre 100%", "Massa/volume", "Força × tempo"], 0, "Parte da energia sempre se dissipa em calor."),
        q("Atrito transforma energia mecânica em:", ["Energia nuclear", "Calor", "Luz apenas", "Massa"], 1, "Dissipação térmica."),
        q("Um corpo de 2 kg a 3 m/s tem Ec de:", ["3 J", "6 J", "9 J", "18 J"], 2, "Ec = 2×9/2 = 9 J."),
        q("Máquinas simples como alavanca podem:", ["Multiplicar força (com trade-off de deslocamento)", "Criar energia do nada", "Violar conservação", "Eliminar atrito totalmente"], 0, "Facilitam trabalho, não criam energia."),
    ],
    "Ondas": [
        q("Em ondas mecânicas, a propagação requer:", ["Meio material", "Apenas vácuo", "Campo magnético", "Fótons"], 0, "Som e ondas na água precisam de meio."),
        q("A frequência mede:", ["Número de oscilações por segundo (Hz)", "Comprimento da onda", "Velocidade do som", "Amplitude"], 0, "f em hertz (1/s)."),
        q("Relação entre velocidade, frequência e comprimento de onda:", ["v = λ·f", "v = f/λ", "v = λ + f", "v = λ²"], 0, "Equação fundamental das ondas."),
        q("Som mais agudo corresponde a:", ["Maior frequência", "Menor frequência", "Maior amplitude", "Menor velocidade no ar"], 0, "Agudo = alta frequência."),
        q("Reflexão de ondas ocorre quando:", ["Onda encontra obstáculo e retorna", "Onda desaparece", "Onda muda de meio sem retorno", "Onda não se propaga"], 0, "Eco é reflexão do som."),
        q("Difracao é a:", ["Curvatura de ondas ao contornar obstáculos", "Reflexão total", "Absorção completa", "Polarização"], 0, "Ondas 'contornam' aberturas e bordas."),
        q("Ondas eletromagnéticas no vácuo propagam-se a:", ["3×10⁸ m/s", "340 m/s", "9,8 m/s", "Dependem da massa"], 0, "Velocidade da luz c."),
        q("Interferência construtiva ocorre quando:", ["Ondas somam amplitudes", "Ondas se cancelam", "Ondas param", "Ondas mudam de meio"], 0, "Cristas coincidem, amplitude aumenta."),
        q("Efeito Doppler: sirene aproximando-se parece:", ["Mais grave", "Mais aguda", "Silenciosa", "Sem alteração"], 1, "Frequência aparente aumenta na aproximação."),
        q("Ultrassom usa frequências:", ["Abaixo de 20 Hz", "Acima do audível humano (>20 kHz)", "Iguais à voz", "Zero"], 1, "Aplicações médicas e de detecção."),
    ],
    "Eletricidade": [
        q("A lei de Ohm estabelece:", ["U = R·i", "P = Fv", "F = ma", "E = mc²"], 0, "Tensão = resistência × corrente."),
        q("Corrente elétrica é fluxo de:", ["Cargas elétricas", "Massa", "Calor", "Luz apenas"], 0, "Elétrons em condutores."),
        q("Unidade de resistência elétrica:", ["Ohm (Ω)", "Volt", "Ampère", "Watt"], 0, "R mede oposição à corrente."),
        q("Potência elétrica calcula-se por:", ["P = U·i", "P = m·g", "P = λ·f", "P = F·d"], 0, "Tensão × corrente."),
        q("Circuito em série tem corrente:", ["Igual em todos os elementos", "Diferente em cada ramo", "Zero sempre", "Infinita"], 0, "Mesmo caminho → mesma corrente."),
        q("Circuito em paralelo: a tensão entre ramos é:", ["A mesma", "Sempre zero", "Diferente em cada ramo", "Infinita"], 0, "Mesmo potencial entre pontos comuns."),
        q("Resistores em série: resistência equivalente:", ["Soma das resistências", "Média", "Menor que a menor", "Sempre 1 Ω"], 0, "Req = R1 + R2 + ..."),
        q("Choque elétrico perigoso ocorre principalmente quando:", ["Corrente atravessa o corpo", "Há apenas tensão sem corrente", "Há isolante perfeito", "Não há contato"], 0, "Corrente > ~10 mA pode ser fatal."),
        q("Gerador converte energia:", ["Mecânica em elétrica", "Elétrica em mecânica", "Nuclear em química", "Térmica em gravitacional"], 0, "Indução eletromagnética."),
        q("Fusível protege circuito porque:", ["Interrompe corrente excessiva", "Aumenta tensão", "Armazena carga", "Gera energia"], 0, "Derrete quando corrente ultrapassa limite."),
    ],
})

print("FIS OK", len([x for s in FIS["submaterias"].values() for x in s]))
