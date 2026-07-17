#!/usr/bin/env python3
"""Generate EXIN DPO track question bank (ISFS, PDPF, PDPP — 50 each)."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "exin_dpo_bank_data.json"

TRILHA = "Trilha DPO — EXIN"
TRILHA_ID = "EXIN-DPO"

CERTS = [
    {
        "code": "EXIN-ISFS",
        "materia": "ISFS",
        "title": "Information Security Foundation (ISFS)",
        "description": "Fundamentos de segurança da informação com base na ISO/IEC 27001.",
        "timeMinutes": 60,
        "submaterias": {
            "Conceitos de SI": [
                ("O que significa a sigla CIA na segurança da informação?", ["Confidencialidade, Integridade e Disponibilidade", "Controle, Identificação e Auditoria", "Criptografia, Internet e Acesso", "Compliance, Investigação e Análise"], 0, "CIA é o triângulo clássico da segurança da informação."),
                ("Qual é o objetivo principal da disponibilidade?", ["Garantir acesso autorizado quando necessário", "Impedir qualquer cópia de dados", "Eliminar todos os riscos", "Criptografar todos os sistemas"], 0, "Disponibilidade assegura que ativos estejam acessíveis quando requeridos."),
                ("Integridade da informação garante que:", ["Dados não sejam alterados indevidamente", "Dados sejam sempre públicos", "Backups nunca falhem", "Senhas sejam compartilhadas"], 0, "Integridade protege contra alteração não autorizada."),
                ("Confidencialidade relaciona-se a:", ["Restringir acesso a quem está autorizado", "Publicar dados abertamente", "Aumentar velocidade de rede", "Desligar servidores"], 0, "Somente pessoas autorizadas devem acessar informações sensíveis."),
                ("Um ativo de informação pode ser:", ["Dado, sistema, pessoa ou processo", "Apenas hardware", "Somente papel", "Exclusivamente software livre"], 0, "Ativos incluem tangíveis e intangíveis relevantes para a organização."),
                ("Avaliação de risco envolve:", ["Identificar ameaças, vulnerabilidades e impacto", "Ignorar controles existentes", "Copiar políticas de outra empresa", "Eliminar auditorias"], 0, "Risco combina probabilidade e impacto de eventos."),
                ("Controle de segurança é:", ["Medida para tratar riscos", "Sinônimo de ameaça", "Tipo de vírus", "Backup automático apenas"], 0, "Controles reduzem, transferem ou aceitam riscos."),
                ("Autenticação verifica:", ["Identidade de quem acessa", "Horário de expediente", "Tamanho do arquivo", "Velocidade da rede"], 0, "Autenticação responde 'quem é você?'."),
                ("Autorização define:", ["O que o usuário autenticado pode fazer", "A senha mínima", "O fabricante do firewall", "A cor do datacenter"], 0, "Autorização responde 'o que pode acessar?'."),
                ("Segurança da informação é responsabilidade:", ["De toda a organização", "Somente da TI", "Apenas do CEO", "Exclusiva de auditores externos"], 0, "Cultura de segurança envolve todos os níveis."),
            ],
            "ISO/IEC 27001": [
                ("A ISO/IEC 27001 especifica requisitos para:", ["Sistema de Gestão de Segurança da Informação (SGSI)", "Contabilidade financeira", "Marketing digital", "Gestão ambiental"], 0, "27001 é a norma certificável de SGSI."),
                ("O ciclo PDCA aplicado ao SGSI significa:", ["Plan-Do-Check-Act", "Protect-Detect-Correct-Audit", "Policy-Data-Control-Access", "Plan-Deploy-Copy-Archive"], 0, "PDCA promove melhoria contínua."),
                ("A Declaração de Aplicabilidade (SoA) documenta:", ["Controles selecionados e justificativas", "Salários da equipe", "Lista de clientes", "Contratos de marketing"], 0, "SoA mostra quais controles do Anexo A se aplicam."),
                ("O Anexo A da ISO 27001 contém:", ["Controles de segurança recomendados", "Requisitos legais da LGPD", "Tabelas de preços", "Normas contábeis"], 0, "Anexo A lista controles organizacionais e técnicos."),
                ("Auditoria interna do SGSI tem objetivo de:", ["Verificar conformidade e eficácia", "Substituir certificação externa", "Eliminar documentação", "Publicar dados pessoais"], 0, "Auditorias internas precedem e complementam certificação."),
                ("Escopo do SGSI deve considerar:", ["Limites organizacionais e requisitos", "Apenas um servidor", "Somente e-mail", "Exclusivamente nuvem pública"], 0, "Escopo define onde o SGSI se aplica."),
                ("Melhoria contínua no SGSI é apoiada por:", ["Análise crítica pela direção e ações corretivas", "Ignorar não conformidades", "Eliminar registros", "Desativar logs"], 0, "Top management review e CAPA são essenciais."),
                ("Controle de acesso lógico inclui:", ["Gestão de identidades e privilégios", "Cor das paredes", "Tipo de café", "Marca de notebooks"], 0, "IAM e least privilege são práticas centrais."),
                ("Gestão de incidentes de segurança exige:", ["Procedimentos de detecção, resposta e lições aprendidas", "Ocultar todos os incidentes", "Desligar logs permanentemente", "Compartilhar senhas"], 0, "Resposta estruturada reduz impacto."),
                ("Fornecedores devem ser avaliados quanto a:", ["Riscos de segurança da informação", "Cor da logomarca", "Número de funcionários apenas", "Localização geográfica exclusiva"], 0, "Cadeia de suprimentos é vetor comum de risco."),
            ],
            "Ameaças e vulnerabilidades": [
                ("Phishing é um tipo de:", ["Engenharia social", "Backup", "Criptografia assimétrica", "Política de senhas"], 0, "Phishing engana usuários para revelar credenciais."),
                ("Malware inclui:", ["Vírus, worms, ransomware e trojans", "Apenas antivírus", "Firewalls", "Certificados SSL"], 0, "Software malicioso compromete confidencialidade e integridade."),
                ("Vulnerabilidade zero-day é:", ["Falha desconhecida sem patch disponível", "Senha fraca conhecida", "Backup diário", "Política de mesa limpa"], 0, "Zero-day não tem correção pública imediata."),
                ("Ataque de negação de serviço (DoS) visa:", ["Indisponibilizar serviço ou recurso", "Criptografar dados", "Aumentar integridade", "Melhorar performance"], 0, "DoS afeta disponibilidade."),
                ("Engenharia social explora:", ["Comportamento humano", "Apenas falhas de hardware", "Leis tributárias", "Normas ISO de qualidade"], 0, "Manipulação psicológica contorna controles técnicos."),
                ("Senha forte deve incluir:", ["Complexidade, comprimento e unicidade", "Nome da empresa repetido", "Data de nascimento", "Mesma senha em todos os sistemas"], 0, "Boas práticas reduzem risco de comprometimento."),
                ("MFA (autenticação multifator) adiciona:", ["Camadas extras além da senha", "Apenas biometria obrigatória", "Eliminação de logs", "Acesso root universal"], 0, "MFA combina fatores como senha + token."),
                ("Patch management trata de:", ["Aplicar atualizações de segurança", "Criar vírus", "Desativar antivírus", "Publicar dados"], 0, "Correções fecham vulnerabilidades conhecidas."),
                ("Insider threat refere-se a:", ["Risco originado por pessoas internas", "Ataques apenas externos", "Falhas de energia", "Enchentes"], 0, "Colaboradores mal-intencionados ou descuidados são ameaça."),
                ("Segmentação de rede ajuda a:", ["Limitar propagação de ataques", "Aumentar superfície de ataque", "Eliminar firewalls", "Compartilhar credenciais"], 0, "Zonas isoladas contêm incidentes."),
            ],
            "Controles organizacionais": [
                ("Política de segurança da informação deve ser:", ["Aprovada pela alta direção e comunicada", "Secreta e oral apenas", "Opcional para TI", "Substituída por e-mails informais"], 0, "Comprometimento da liderança é requisito do SGSI."),
                ("Classificação da informação permite:", ["Tratar dados conforme sensibilidade", "Publicar tudo igualmente", "Eliminar backups", "Ignorar rótulos"], 0, "Níveis como público, interno, confidencial."),
                ("Treinamento de conscientização em SI visa:", ["Reduzir erros humanos e phishing", "Substituir controles técnicos", "Eliminar políticas", "Desativar MFA"], 0, "Usuários são linha de defesa."),
                ("Controle de acesso físico protege:", ["Instalações e equipamentos", "Apenas dados na nuvem", "Redes sociais", "E-mails marketing"], 0, "Badges, catracas e CCTV são exemplos."),
                ("Gestão de mudanças em TI reduz:", ["Riscos de alterações não autorizadas", "Necessidade de testes", "Documentação", "Aprovações"], 0, "Mudanças controladas evitam indisponibilidade."),
                ("Backup e restore garantem:", ["Recuperação após perda ou ransomware", "Eliminação de logs", "Acesso público", "Cópia única sem teste"], 0, "Testes de restauração validam backups."),
                ("Criptografia em repouso protege:", ["Dados armazenados em discos ou mídia", "Apenas tráfego HTTP", "Senhas em texto claro", "Políticas impressas"], 0, "Dados cifrados resistem a acesso físico indevido."),
                ("Logs e monitoramento servem para:", ["Detectar atividades anômalas", "Aumentar anonimato de atacantes", "Eliminar auditoria", "Ocultar incidentes"], 0, "SIEM correlaciona eventos."),
                ("Acordo de confidencialidade (NDA) protege:", ["Informações trocadas com terceiros", "Dados já públicos", "Opiniões pessoais", "Notícias abertas"], 0, "NDA reforça confidencialidade contratual."),
                ("Continuidade de negócios (BC) foca em:", ["Manter operações críticas após incidentes", "Aumentar riscos", "Eliminar planos de crise", "Ignorar RTO/RPO"], 0, "BC e DR complementam disponibilidade."),
            ],
            "Governança e conformidade": [
                ("Governança de TI alinha:", ["Tecnologia aos objetivos e riscos do negócio", "Apenas compras de software", "Marketing e vendas", "Folha de pagamento"], 0, "Governança define direção e controle."),
                ("Due diligence em M&A inclui avaliar:", ["Riscos de segurança e privacidade do alvo", "Apenas cor da marca", "Cardápio da cantina", "Estacionamento"], 0, "Aquisições podem trazer passivos de dados."),
                ("Conformidade regulatória significa:", ["Atender leis e normas aplicáveis", "Ignorar legislação", "Copiar dados sem base legal", "Eliminar registros legais"], 0, "Compliance reduz sanções e danos reputacionais."),
                ("Registro de tratamento de dados apoia:", ["Accountability e transparência", "Ocultação total", "Venda de dados", "Eliminação de titulares"], 0, "Documentação demonstra conformidade."),
                ("Pen test (teste de intrusão) simula:", ["Atacante para identificar falhas", "Backup diário", "Treinamento de RH", "Auditoria financeira"], 0, "Testes éticos validam defesas."),
                ("Segregação de funções (SoD) evita:", ["Concentração de privilégios incompatíveis", "Trabalho em equipe", "Auditoria externa", "Documentação"], 0, "Quem aprova não deve executar sem controle."),
                ("Indicadores de segurança (KPI/KRI) medem:", ["Eficácia do programa de SI", "Apenas lucro", "Número de funcionários", "Cor do logo"], 0, "Métricas orientam decisões."),
                ("Gestão de vulnerabilidades inclui:", ["Identificar, priorizar e corrigir falhas", "Ignorar scans", "Publicar exploits", "Desativar patches"], 0, "Ciclo contínuo reduz exposição."),
                ("Certificação ISO 27001 é obtida após:", ["Auditoria de certificação bem-sucedida", "Compra de software", "E-mail interno", "Reunião única"], 0, "Organismo certificador valida conformidade."),
                ("Cultura de segurança madura apresenta:", ["Comportamento proativo e reporte de incidentes", "Medo de punição silenciosa", "Ocultação de erros", "Senhas compartilhadas"], 0, "Confiança para reportar acelera resposta."),
            ],
        },
    },
    {
        "code": "EXIN-PDPF",
        "materia": "PDPF",
        "title": "Privacy and Data Protection Foundation (PDPF)",
        "description": "Conceitos essenciais de privacidade, LGPD e GDPR.",
        "timeMinutes": 60,
        "submaterias": {
            "Fundamentos de privacidade": [
                ("Privacidade de dados relaciona-se principalmente a:", ["Direitos dos titulares sobre informações pessoais", "Velocidade de internet", "Hardware de servidores", "Marketing de produtos"], 0, "Privacidade protege autodeterminação informativa."),
                ("Dado pessoal na LGPD é:", ["Informação relacionada a pessoa natural identificada ou identificável", "Apenas CPF impresso", "Somente dado anonimizado", "Qualquer dado agregado estatístico"], 0, "Art. 5º LGPD define dado pessoal."),
                ("Dado anonimizado:", ["Não identifica titular, considerando meios técnicos", "Sempre é dado pessoal", "Exige consentimento renovado diário", "Proíbe qualquer uso"], 0, "Anonimização irreversível sai do escopo."),
                ("Encarregado de Dados (DPO) atua como:", ["Canal de comunicação entre controlador, titulares e ANPD", "Substituto do CEO", "Auditor financeiro", "Gerente de vendas"], 0, "DPO facilita conformidade e diálogo."),
                ("Princípio da finalidade exige:", ["Tratar dados para propósitos legítimos informados", "Usar dados para qualquer fim", "Alterar finalidade sem aviso", "Vender bases livremente"], 0, "Finalidade limita e orienta tratamento."),
                ("Princípio da necessidade significa:", ["Coletar apenas o mínimo adequado", "Coletar todos os dados possíveis", "Armazenar indefinidamente", "Ignorar retenção"], 0, "Proporcionalidade na coleta."),
                ("Consentimento válido deve ser:", ["Livre, informado e inequívoco", "Tácito e genérico", "Obtido por coação", "Silencioso por padrão"], 0, "Consentimento é base legal específica."),
                ("Interesse legítimo exige:", ["Balanceamento com direitos do titular", "Ignorar titulares", "Proibir LIA", "Eliminar opt-out"], 0, "Legitimate interest assessment é boa prática."),
                ("Privacy by design implica:", ["Integrar privacidade desde a concepção", "Adicionar privacidade só após lançamento", "Ignorar DPIA", "Coletar tudo primeiro"], 0, "Proativo, não reativo."),
                ("Privacy by default exige:", ["Configurações mais protetivas por padrão", "Máxima coleta por padrão", "Compartilhamento amplo inicial", "Retenção infinita"], 0, "Minimização desde o default."),
            ],
            "LGPD — bases e direitos": [
                ("A LGPD (Lei 13.709/2018) regula:", ["Tratamento de dados pessoais", "Apenas dados públicos", "Somente setor financeiro", "Exclusivamente saúde"], 0, "Marco legal brasileiro de proteção de dados."),
                ("Titular de dados tem direito de:", ["Acesso, correção, eliminação e portabilidade", "Ignorar políticas", "Acessar dados de terceiros livremente", "Eliminar logs de auditoria"], 0, "Capítulo III LGPD lista direitos."),
                ("ANPD é:", ["Autoridade Nacional de Proteção de Dados", "Agência de aviação", "Banco central", "Instituto de metrologia"], 0, "Fiscaliza e orienta a LGPD no Brasil."),
                ("Controlador de dados:", ["Define finalidades e meios do tratamento", "Apenas armazena por ordem", "Nunca decide bases legais", "Sempre é o DPO"], 0, "Controlador determina o 'porquê' e 'como'."),
                ("Operador de dados:", ["Trata em nome do controlador", "Sempre define finalidade", "Substitui ANPD", "Ignora contratos"], 0, "Operador segue instruções do controlador."),
                ("Base legal 'execução de contrato' permite:", ["Tratar dados necessários ao contrato", "Qualquer marketing", "Venda de bases", "Dados de terceiros sem aviso"], 0, "Dados indispensáveis à relação contratual."),
                ("Eliminação de dados deve ocorrer quando:", ["Não mais necessários ou titular solicita", "Sempre após 1 dia", "Nunca", "Apenas por marketing"], 0, "Retenção limitada e direito ao apagamento."),
                ("Portabilidade permite ao titular:", ["Receber dados em formato estruturado", "Copiar dados de outros titulares", "Eliminar backups legais", "Ignorar segurança"], 0, "Facilita mudança de fornecedor."),
                ("Oposição ao tratamento pode ser exercida quando:", ["Base legal não torna oposição inviável", "Sempre proibida", "Apenas por empresas públicas", "Somente via judicial"], 0, "Titular pode se opor em certas bases."),
                ("Sanções da LGPD podem incluir:", ["Multa, publicização e bloqueio de dados", "Apenas advertência verbal", "Promoção de produtos", "Isenção total"], 0, "Art. 52 prevê sanções administrativas."),
            ],
            "GDPR — visão geral": [
                ("O GDPR aplica-se a:", ["Tratamento de dados de pessoas na UE", "Apenas empresas americanas", "Somente governo brasileiro", "Exclusivamente e-commerce BR"], 0, "Regulamento europeu extra-territorial em casos definidos."),
                ("Multa máxima GDPR pode chegar a:", ["€20 milhões ou 4% do faturamento global", "€100 fixos", "Sem multas", "Apenas advertência"], 0, "Sanções proporcionais e dissuasórias."),
                ("DPO no GDPR é obrigatório quando:", ["Há monitoramento sistemático em larga escala ou dados sensíveis em larga escala", "Qualquer microempresa", "Nunca", "Apenas setor público BR"], 0, "Art. 37 define obrigatoriedade."),
                ("Privacy Impact Assessment (PIA/DPIA) é exigida quando:", ["Tratamento provavelmente alto risco", "Sempre para e-mail", "Nunca", "Apenas marketing B2B"], 0, "Avalia impacto antes do tratamento."),
                ("Transferência internacional GDPR exige:", ["Garantias adequadas ou mecanismos válidos", "Envio livre sem análise", "Ignorar titulares", "Apenas e-mail criptografado"], 0, "Capítulo V regula transferências."),
                ("Cláusulas contratuais padrão (SCCs) servem para:", ["Legitimar transferências internacionais", "Eliminar DPO", "Publicar dados", "Ignorar LGPD"], 0, "Mecanismo reconhecido pela UE."),
                ("Direito ao esquecimento relaciona-se a:", ["Apagamento de dados pessoais", "Esquecer senhas", "Eliminar empresas", "Apagar logs de segurança obrigatórios"], 0, "Art. 17 GDPR — erasure."),
                ("Accountability no GDPR significa:", ["Demonstrar conformidade", "Ocultar tratamentos", "Eliminar registros", "Ignorar auditorias"], 0, "Responsabilização proativa."),
                ("Representante na UE é necessário quando:", ["Controlador fora da UE oferece serviços na UE", "Empresa só atua no Brasil", "Sempre", "Nunca para startups"], 0, "Ponto de contato para autoridades."),
                ("Notificação de violação GDPR em geral deve ocorrer em:", ["72 horas à autoridade", "1 ano", "Nunca", "Apenas se solicitado por cliente"], 0, "Prazo salvo exceções documentadas."),
            ],
            "Tratamento e segurança": [
                ("Minimização de dados exige:", ["Coletar só o necessário", "Coletar o máximo possível", "Retenção infinita", "Compartilhar com parceiros"], 0, "Princípio GDPR e LGPD."),
                ("Pseudonimização:", ["Substitui identificadores por pseudônimos", "Anonimiza irreversivelmente sempre", "Elimina criptografia", "Publica dados abertos"], 0, "Reduz risco mantendo utilidade."),
                ("Registro de operações de tratamento documenta:", ["Finalidades, categorias, bases e retenção", "Apenas senhas", "Salários", "Receitas"], 0, "ROPA / registro de tratamentos."),
                ("Contrato com operador deve incluir:", ["Instruções, confidencialidade e segurança", "Marketing conjunto", "Venda de leads", "Acesso root compartilhado"], 0, "Art. 39 LGPD e Art. 28 GDPR."),
                ("Incidente com dados pessoais envolve:", ["Acesso, vazamento ou perda não autorizada", "Backup bem-sucedido", "Patch aplicado", "Treinamento interno"], 0, "Personal data breach."),
                ("Comunicação a titulares após incidente deve ser:", ["Clara, em prazo adequado, com medidas tomadas", "Oculta", "Apenas interna", "Opcional sempre"], 0, "Transparência reduz danos."),
                ("Criptografia como medida de segurança ajuda:", ["Confidencialidade e integridade", "Marketing", "SEO", "Eliminar DPO"], 0, "Controle técnico recomendado."),
                ("Retenção de dados deve seguir:", ["Política definida e prazos legais", "Armazenamento eterno", "Exclusão aleatória", "Ignorar contratos"], 0, "Storage limitation."),
                ("Treinamento de privacidade para equipes reduz:", ["Erros e violações acidentais", "Necessidade de políticas", "Papel do DPO", "Logs"], 0, "Humanos são vetor comum."),
                ("Privacy notice / aviso de privacidade informa:", ["Finalidades, bases, direitos e contato DPO", "Apenas slogan", "Senhas", "Código fonte"], 0, "Transparência ao titular."),
            ],
            "Papéis e responsabilidades": [
                ("Joint controllers (co-controladores) devem:", ["Definir responsabilidades por contrato", "Ignorar titulares", "Compartilhar sem base", "Eliminar registros"], 0, "Art. 41 LGPD / Art. 26 GDPR."),
                ("Suboperador exige:", ["Autorização do controlador e garantias", "Livre contratação sem aviso", "Acesso total a dados", "Eliminação de cláusulas"], 0, "Cadeia de processamento."),
                ("DPO deve reportar-se a:", ["Alta administração", "Apenas marketing", "Titulares diretamente", "Fornecedores"], 0, "Independência funcional."),
                ("Conflito de interesses do DPO ocorre se:", ["DPO também aprova tratamentos que monitora", "DPO treina equipe", "DPO responde titulares", "DPO mantém ROPA"], 0, "Independência é requisito."),
                ("Comitê de privacidade apoia:", ["Governança e decisões transversais", "Substituir ANPD", "Eliminar DPIA", "Venda de dados"], 0, "Fórum multidisciplinar."),
                ("Data Protection Impact Assessment avalia:", ["Riscos à privacidade de titulares", "Apenas custos financeiros", "Cor do site", "Velocidade do app"], 0, "DPIA/RIPD documenta mitigação."),
                ("Legitimate Interest Assessment documenta:", ["Teste de balanceamento", "Consentimento tácito", "Eliminação de direitos", "Marketing spam"], 0, "LIA suporta base de interesse legítimo."),
                ("Privacy governance inclui:", ["Políticas, papéis, métricas e cultura", "Apenas antivírus", "Somente firewall", "Exclusivamente jurídico"], 0, "Programa holístico."),
                ("Due diligence de privacidade em terceiros verifica:", ["Conformidade e riscos do fornecedor", "Apenas preço", "Logo", "Estacionamento"], 0, "Vendor risk management."),
                ("Accountability demonstra-se com:", ["Registros, políticas, treinamentos e auditorias", "Ocultação", "Eliminação de logs legais", "Boca fechada"], 0, "Evidências de conformidade."),
            ],
        },
    },
    {
        "code": "EXIN-PDPP",
        "materia": "PDPP",
        "title": "Privacy and Data Protection Practitioner (PDPP)",
        "description": "Aplicação prática da LGPD/GDPR, casos reais, riscos e avaliações.",
        "timeMinutes": 90,
        "submaterias": {
            "DPIA e gestão de riscos": [
                ("DPIA deve ser revisada quando:", ["Mudam finalidade, escopo ou tecnologia", "Nunca", "Apenas anualmente fixo", "Somente após multa"], 0, "Reavaliação contínua de riscos."),
                ("RIPD (Relatório de Impacto) na LGPD é exigido quando:", ["Tratamento pode gerar alto risco", "Sempre para cookies", "Nunca", "Apenas B2B"], 0, "Art. 38 LGPD."),
                ("Consulta prévia à ANPD ocorre quando:", ["RIPD indica risco residual alto", "Qualquer cookie", "Backup diário", "Treinamento interno"], 0, "Autoridade pode orientar mitigação."),
                ("Mitigação de risco inclui:", ["Controles técnicos e organizacionais", "Ignorar titulares", "Publicar dados", "Eliminar DPO"], 0, "Reduzir probabilidade ou impacto."),
                ("Risco residual é:", ["Risco que permanece após controles", "Risco zero garantido", "Apenas risco financeiro", "Risco ignorado"], 0, "Aceitação documentada pode ser necessária."),
                ("Matriz de risco combina:", ["Probabilidade e impacto", "Cor e tamanho", "Marketing e vendas", "Hardware e software apenas"], 0, "Priorização de tratamentos."),
                ("Tratamento de dados sensíveis exige:", ["Cuidado reforçado e bases específicas", "Mesmas regras de dados comuns sempre", "Proibição absoluta", "Ignorar consentimento"], 0, "Art. 11 LGPD / Art. 9 GDPR."),
                ("Dados de crianças requerem:", ["Consentimento do responsável e melhor interesse", "Coleta livre", "Venda permitida", "Ignorar idade"], 0, "Proteção reforçada."),
                ("Decisões automatizadas com efeito legal exigem:", ["Direito de revisão humana e informação", "Proibição total sempre", "Ocultar lógica", "Eliminar oposição"], 0, "Transparência algorítmica."),
                ("Privacy risk register centraliza:", ["Riscos, owners e planos de ação", "Apenas senhas", "Receitas", "Logos"], 0, "Governança operacional."),
            ],
            "Operação do DPO": [
                ("DPO deve facilitar:", ["Exercício de direitos dos titulares", "Ocultação de tratamentos", "Venda de bases", "Eliminação de registros legais"], 0, "Canal de confiança."),
                ("Registro de tratamentos (ROPA) deve ser:", ["Atualizado e refletir realidade", "Estático por 10 anos", "Secreto para ANPD", "Opcional"], 0, "Accountability."),
                ("Resposta a solicitação de titular deve ser:", ["Dentro de prazos legais", "Ignorada", "Apenas verbal", "Sem identificação"], 0, "LGPD: 15 dias prorrogáveis; GDPR: 1 mês."),
                ("DPO não é responsável por:", ["Decisões finais de negócio do controlador", "Orientar conformidade", "Treinar equipes", "Interface com ANPD"], 0, "DPO assessora; controlador responde."),
                ("Conflito entre marketing e privacidade resolve-se com:", ["Base legal, LIA e opt-in quando aplicável", "Coleta máxima", "Ignorar opt-out", "Compra de listas"], 0, "Balanceamento documentado."),
                ("Auditoria de privacidade verifica:", ["Conformidade prática vs políticas", "Apenas cor do site", "Lucro trimestral", "Número de funcionários"], 0, "Gap analysis."),
                ("Plano de resposta a incidentes inclui:", ["Detecção, contenção, notificação e lições", "Ocultação", "Eliminação de logs", "Silêncio total"], 0, "Playbook testado."),
                ("Treinamento role-based para privacidade significa:", ["Conteúdo adaptado à função", "Mesmo treino para todos sem foco", "Apenas e-mail anual", "Nenhum registro"], 0, "RH vs TI vs marketing."),
                ("KPIs de privacidade podem incluir:", ["Prazo médio DSAR, incidentes, treinamentos", "Apenas faturamento", "Cor da UI", "Número de likes"], 0, "Medir programa."),
                ("Relatório à direção sobre privacidade deve:", ["Resumir riscos, incidentes e investimentos", "Ocultar problemas", "Substituir DPO", "Eliminar DPIA"], 0, "Governança executiva."),
            ],
            "Casos práticos LGPD/GDPR": [
                ("Vazamento por e-mail errado exige:", ["Avaliar notificação ANPD/titulares", "Ignorar", "Publicar lista", "Eliminar backups legais"], 0, "Incident response."),
                ("Marketing sem opt-in válido viola:", ["Princípios de finalidade e consentimento", "Apenas ISO 27001", "Normas contábeis", "Direito penal sempre"], 0, "Comunicações precisam de base legal."),
                ("Funcionário acessa dados sem necessidade:", ["Incidente de acesso não autorizado", "Prática normal", "Direito do titular", "Backup"], 0, "Need-to-know e logs."),
                ("Transferência para EUA pós-Schrems II exige:", ["Avaliar SCCs e medidas suplementares", "Transferência livre", "Ignorar GDPR", "Apenas criptografia sem análise"], 0, "Jurisprudência europeia."),
                ("App coleta localização contínua deve:", ["Informar, base legal clara e minimização", "Ocultar na política", "Retenção infinita", "Vender dados"], 0, "Dados sensíveis de comportamento."),
                ("Eliminação solicitada com obrigação legal de retenção:", ["Retenção limitada ao exigido por lei", "Apagar tudo imediatamente", "Ignorar titular", "Publicar dados"], 0, "Conflito de obrigações."),
                ("Cookies não essenciais requerem:", ["Consentimento prévio informado", "Carregamento automático", "Ocultar banner", "Retenção eterna"], 0, "ePrivacy / boas práticas GDPR."),
                ("Fornecedor subcontrata sem aviso:", ["Violação contratual e risco", "Prática aceita", "Benefício automático", "Elimina DPO"], 0, "Cadeia de responsabilidade."),
                ("Biometria para ponto exige:", ["Base legal, segurança reforçada e alternativa", "Coleta livre", "Compartilhamento público", "Retenção infinita"], 0, "Dado sensível."),
                ("Pesquisa com dados pseudonimizados ainda requer:", ["Avaliar riscos e bases legais", "Nenhuma regra", "Publicação aberta", "Eliminação de ética"], 0, "Pseudonimização ≠ anonimização."),
            ],
            "Contratos e terceiros": [
                ("DPA (Data Processing Agreement) deve definir:", ["Objeto, duração, instruções e subcontratação", "Apenas preço", "Marketing", "Logo"], 0, "Art. 39 LGPD."),
                ("Auditoria de fornecedor cloud inclui:", ["Certificações, localização e subprocessadores", "Apenas uptime", "Cor do dashboard", "Número de VMs"], 0, "Due diligence técnica."),
                ("Suboperador só pode ser contratado com:", ["Autorização e garantias equivalentes", "Livre escolha sem aviso", "Acesso root ao controlador", "Eliminação de logs"], 0, "Responsabilidade em cadeia."),
                ("Exit plan de fornecedor prevê:", ["Devolução ou eliminação segura de dados", "Retenção eterna pelo vendor", "Venda de base", "Ignorar titulares"], 0, "Continuidade e portabilidade."),
                ("Cláusula de confidencialidade protege:", ["Dados pessoais e segredos de negócio", "Apenas marketing", "Opiniões públicas", "Notícias"], 0, "NDA reforça contrato."),
                ("Transferência internacional via BCRs exige:", ["Regras vinculantes aprovadas", "E-mail informal", "Ignorar ANPD", "Apenas HTTPS"], 0, "Binding Corporate Rules."),
                ("SLA de privacidade pode incluir:", ["Prazos DSAR, notificação de incidentes", "Apenas latência", "Cor do app", "Número de likes"], 0, "Métricas contratuais."),
                ("Due diligence reduz:", ["Riscos de terceiros não conformes", "Necessidade de contratos", "Papel do DPO", "Treinamentos"], 0, "Vendor management."),
                ("Indenização em contrato de processamento:", ["Aloca riscos financeiros", "Elimina LGPD", "Substitui DPIA", "Remove DPO"], 0, "Cláusula de liability."),
                ("Revisão anual de contratos verifica:", ["Mudanças regulatórias e operacionais", "Apenas inflação", "Logo", "Estacionamento"], 0, "Contratos vivos."),
            ],
            "Monitoramento e melhoria": [
                ("Programa de privacidade maduro inclui:", ["Políticas, DPIA, treinamento, auditoria e métricas", "Apenas banner de cookies", "Somente antivírus", "Nenhum registro"], 0, "Ciclo PDCA de privacidade."),
                ("Revisão pós-incidente documenta:", ["Causa raiz e ações preventivas", "Culpa individual apenas", "Ocultação", "Eliminação de logs"], 0, "Lessons learned."),
                ("Privacy maturity model avalia:", ["Nível de capacidade organizacional", "Apenas faturamento", "Número de servidores", "Cor do site"], 0, "Roadmap de evolução."),
                ("Integração LGPD + ISO 27001 beneficia:", ["Segurança e privacidade alinhadas", "Elimina DPO", "Remove DPIA", "Ignora titulares"], 0, "Controles complementares."),
                ("Automated compliance tools auxiliam:", ["ROPA, DSAR e monitoramento", "Substituir DPO totalmente", "Eliminar políticas", "Vender dados"], 0, "GRC tech."),
                ("Comunicação transparente após incidente inclui:", ["Natureza, dados afetados e medidas", "Ocultação total", "Apenas interno", "Dados de terceiros"], 0, "Confiança do titular."),
                ("Benchmarking de privacidade compara:", ["Práticas com mercado e reguladores", "Apenas concorrentes ilegais", "Preços", "Logos"], 0, "Melhoria contínua."),
                ("Certificação EXIN PDPP valida:", ["Competência prática do profissional", "ISO 27001 da empresa", "LGPD automática", "Eliminação de riscos"], 0, "Certificação individual."),
                ("Trilha DPO EXIN completa reúne:", ["ISFS + PDPF + PDPP", "Apenas ISFS", "Somente GDPR", "Nenhum exame"], 0, "Três exames independentes."),
                ("Encarregado deve equilibrar:", ["Negócio, compliance e direitos dos titulares", "Apenas marketing", "Somente TI", "Ignorar ANPD"], 0, "Papel estratégico do DPO."),
            ],
        },
    },
]


def build():
    track = {"trilha": TRILHA, "trilhaId": TRILHA_ID, "certifications": []}
    for cert in CERTS:
        entry = {
            "code": cert["code"],
            "materia": cert["materia"],
            "title": cert["title"],
            "description": cert["description"],
            "timeMinutes": cert["timeMinutes"],
            "submaterias": {},
        }
        total = 0
        for sub, items in cert["submaterias"].items():
            qs = []
            for text, opts, correct, expl in items:
                qs.append({
                    "type": "single",
                    "text": text,
                    "options": [{"text": o, "correct": i == correct} for i, o in enumerate(opts)],
                    "explanation": expl,
                    "submateria": sub,
                    "level": "medio",
                })
            entry["submaterias"][sub] = qs
            total += len(qs)
            assert len(items) == 10, f"{cert['code']}/{sub} must have 10 questions"
        assert total == 50, f"{cert['code']} must have 50 questions, got {total}"
        track["certifications"].append(entry)
    OUT.write_text(json.dumps(track, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} — {len(track['certifications'])} certs, 150 questions")


if __name__ == "__main__":
    build()
