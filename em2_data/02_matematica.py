#!/usr/bin/env python3
"""Banco de questões — Matemática (2º EM)."""

def q(text, opts, correct, expl, level="medio"):
    return [text, opts, correct, expl, level]

def pack(materia, code, title, desc, subs, minutes=75):
    total = sum(len(v) for v in subs.values())
    assert total == 50, f"{materia}: {total} questões"
    return {
        "materia": materia, "code": code, "title": title,
        "description": desc, "timeMinutes": minutes, "submaterias": subs
    }

MAT = pack("Matemática", "EM2-MAT", "Simulado — Matemática (2º EM)",
    "50 questões de múltipla escolha organizadas por sub-matéria.", {
    "Funções": [
        q("O domínio da função f(x) = 1/(x - 2) é:", ["ℝ", "ℝ \\ {2}", "ℝ⁺", "[2, +∞)"], 1, "O denominador não pode ser zero; x ≠ 2."),
        q("A função f(x) = 2x + 3 é do tipo:", ["Quadrática", "Afim", "Exponencial", "Logarítmica"], 1, "Forma ax + b caracteriza função afim."),
        q("A raiz da função f(x) = 3x - 9 é:", ["x = 0", "x = 3", "x = -3", "x = 9"], 1, "3x - 9 = 0 → x = 3."),
        q("O gráfico de f(x) = x² é uma:", ["Reta", "Parábola", "Hipérbole", "Circunferência"], 1, "Função quadrática tem gráfico parabólico."),
        q("Se f(x) = x + 1 e g(x) = 2x, então (f ∘ g)(2) vale:", ["3", "4", "5", "6"], 2, "g(2)=4; f(4)=5."),
        q("Uma função crescente satisfaz:", ["f(a) > f(b) se a > b", "f(a) < f(b) se a > b", "f(a) = f(b) sempre", "Não tem imagem"], 0, "Crescente: valores maiores de x geram maiores f(x)."),
        q("O vértice da parábola y = (x - 1)² + 4 está em:", ["(1, 4)", "(-1, 4)", "(1, -4)", "(4, 1)"], 0, "Forma canônica y = a(x-h)² + k → vértice (h, k)."),
        q("A função f(x) = |x| é:", ["Sempre negativa", "Par", "Ímpar", "Injetora em ℝ"], 1, "f(-x) = f(x), logo é par."),
        q("O conjunto imagem de f(x) = x² + 1 é:", ["[1, +∞)", "(-∞, 1]", "ℝ", "[0, +∞)"], 0, "x² ≥ 0, então x² + 1 ≥ 1."),
        q("A taxa de variação de f(x) = 5x - 2 é:", ["-2", "2", "5", "7"], 2, "Coeficiente angular da função afim é 5."),
    ],
    "Geometria": [
        q("A soma dos ângulos internos de um triângulo é:", ["90°", "180°", "270°", "360°"], 1, "Propriedade fundamental dos triângulos euclidianos."),
        q("A área de um retângulo de base 8 cm e altura 5 cm é:", ["13 cm²", "26 cm²", "40 cm²", "80 cm²"], 2, "A = b × h = 8 × 5 = 40 cm²."),
        q("No teorema de Pitágoras, a² + b² = c², c representa:", ["Cateto menor", "Cateto maior", "Hipotenusa", "Altura"], 2, "c é o lado oposto ao ângulo reto."),
        q("Dois triângulos são semelhantes quando:", ["Têm a mesma área", "Têm ângulos correspondentes iguais", "Têm o mesmo perímetro", "São congruentes"], 1, "Semelhança exige ângulos iguais e lados proporcionais."),
        q("O volume de um cubo de aresta 3 cm é:", ["9 cm³", "18 cm³", "27 cm³", "36 cm³"], 2, "V = a³ = 3³ = 27 cm³."),
        q("Um polígono regular de 6 lados tem cada ângulo interno de:", ["60°", "90°", "120°", "135°"], 2, "Ângulo interno = (n-2)×180°/n = 120°."),
        q("A distância entre os pontos A(1, 2) e B(4, 6) é:", ["3", "4", "5", "7"], 2, "d = √[(4-1)² + (6-2)²] = √25 = 5."),
        q("A equação x² + y² = 25 representa uma:", ["Reta", "Parábola", "Circunferência", "Elipse"], 2, "Forma padrão de circunferência centrada na origem."),
        q("O seno de 30° vale:", ["1/2", "√2/2", "√3/2", "1"], 0, "Valores notáveis: sen 30° = 1/2."),
        q("Dois retas paralelas cortadas por uma transversal formam ângulos:", ["Sempre retos", "Alternos internos congruentes", "Sempre suplementares", "Sempre iguais a 90°"], 1, "Alternos internos entre paralelas são congruentes."),
    ],
    "Álgebra": [
        q("A solução de 2x + 5 = 13 é:", ["x = 3", "x = 4", "x = 5", "x = 9"], 1, "2x = 8 → x = 4."),
        q("O produto (x + 3)(x - 3) é igual a:", ["x² - 9", "x² + 9", "x² - 6", "x² + 6x - 9"], 0, "Produto da diferença de dois quadrados."),
        q("Fatorando x² - 5x + 6 obtemos:", ["(x - 2)(x - 3)", "(x + 2)(x + 3)", "(x - 1)(x - 6)", "(x + 1)(x + 6)"], 0, "Dois números que somam -5 e multiplicam 6: -2 e -3."),
        q("A equação x² = -4 no conjunto dos reais:", ["Tem duas soluções", "Tem uma solução", "Não tem solução real", "Tem infinitas soluções"], 2, "Quadrado de real nunca é negativo."),
        q("O discriminante Δ = b² - 4ac de x² - 4x + 4 = 0 vale:", ["0", "4", "8", "16"], 0, "Δ = 16 - 16 = 0 → raiz dupla."),
        q("Simplificando √72 obtemos:", ["6√2", "8√2", "3√8", "12√6"], 0, "√72 = √(36×2) = 6√2."),
        q("A expressão 3x - 2y = 12 representa:", ["Uma reta", "Uma parábola", "Um ponto", "Um círculo"], 0, "Equação do 1º grau em duas variáveis."),
        q("Resolvendo o sistema x + y = 5 e x - y = 1, temos x =", ["2", "3", "4", "5"], 1, "Somando as equações: 2x = 6 → x = 3."),
        q("O inverso multiplicativo de 4 é:", ["-4", "1/4", "4", "0,25 e 1/4 são ambos corretos, mas 1/4"], 1, "a · a⁻¹ = 1 → a⁻¹ = 1/4."),
        q("A potência (-2)³ vale:", ["6", "-6", "8", "-8"], 3, "(-2)³ = -8; expoente ímpar mantém o sinal."),
    ],
    "Estatística": [
        q("A média aritmética de 4, 6 e 8 é:", ["5", "6", "7", "18"], 1, "(4+6+8)/3 = 18/3 = 6."),
        q("A mediana do conjunto {2, 5, 7, 9, 12} é:", ["5", "7", "9", "6"], 1, "Valor central quando ordenado."),
        q("A moda de {3, 5, 5, 7, 9, 5} é:", ["3", "5", "7", "9"], 1, "5 é o valor mais frequente."),
        q("Em um gráfico de barras, a altura de cada barra indica:", ["A cor da categoria", "A frequência ou valor", "O tempo", "A temperatura"], 1, "Barras representam quantidades por categoria."),
        q("A amplitude de {10, 15, 20, 25} é:", ["5", "10", "15", "25"], 2, "Amplitude = máximo - mínimo = 25 - 10 = 15."),
        q("Um gráfico de setores (pizza) é adequado para:", ["Mostrar evolução no tempo", "Comparar partes de um todo", "Medir temperatura", "Representar funções"], 1, "Setores mostram proporções percentuais."),
        q("Em uma pesquisa amostral, a população é:", ["O grupo sorteado", "O conjunto total de interesse", "Apenas os entrevistados", "O questionário"], 1, "População = universo que se deseja estudar."),
        q("A probabilidade de sair cara ao lançar uma moeda honesta é:", ["0", "1/4", "1/2", "1"], 2, "Dois resultados equiprováveis: cara ou coroa."),
        q("Um histograma difere de gráfico de barras porque:", ["Usa dados contínuos em intervalos", "Não usa eixos", "Só mostra percentuais", "Não tem barras"], 0, "Histograma agrupa dados contínuos em classes."),
        q("O desvio padrão mede:", ["A média", "A dispersão dos dados", "A moda", "A mediana"], 1, "Indica o quanto os dados se afastam da média."),
    ],
    "Razão e Proporção": [
        q("A razão entre 12 e 8 na forma simplificada é:", ["3:2", "2:3", "4:3", "6:4"], 0, "12/8 = 3/2 → razão 3:2."),
        q("Se 3 operários fazem um trabalho em 12 dias, 6 operários (mesmo ritmo) levam:", ["6 dias", "12 dias", "24 dias", "4 dias"], 0, "Grandeza inversamente proporcional: dobra operários, metade do tempo."),
        q("Em uma receita, farinha e açúcar estão na razão 5:2. Para 10 xícaras de farinha, o açúcar é:", ["2 xícaras", "4 xícaras", "5 xícaras", "8 xícaras"], 1, "5:2 = 10:4 → 4 xícaras de açúcar."),
        q("Porcentagem equivalente a 0,25 é:", ["2,5%", "25%", "250%", "0,25%"], 1, "0,25 = 25/100 = 25%."),
        q("Um produto de R$ 200 com 15% de desconto custa:", ["R$ 30", "R$ 170", "R$ 185", "R$ 215"], 1, "Desconto = 30; preço final = 200 - 30 = 170."),
        q("A escala 1:50000 significa que 1 cm no mapa representa:", ["500 cm na realidade", "500 m na realidade", "500 km na realidade", "50 km na realidade"], 1, "1 cm → 50000 cm = 500 m."),
        q("Se x/4 = 15/12, então x vale:", ["3", "5", "15", "20"], 1, "Proporção: x = 4×15/12 = 5."),
        q("Aumento de 20% sobre R$ 150 resulta em:", ["R$ 170", "R$ 180", "R$ 30", "R$ 120"], 1, "150 + 20% de 150 = 150 + 30 = 180."),
        q("Três números estão em proporção contínua se:", ["São iguais", "a/b = b/c", "Somam zero", "São primos"], 1, "Proporção contínua: meio termo é média proporcional."),
        q("Em uma mistura de suco, água e concentrado estão na razão 4:1. A fração de concentrado é:", ["1/4", "1/5", "4/5", "1/3"], 1, "Total 5 partes; concentrado = 1/5."),
    ],
})

print("MAT OK", len([x for s in MAT["submaterias"].values() for x in s]))
