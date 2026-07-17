#!/usr/bin/env python3
"""Generate data/dpo-global-bank.js — ludic bilingual DPO certification bank."""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "data" / "dpo-global-bank.js"


def q(stem_en, stem_pt, opts_en, opts_pt, correct, expl_en, expl_pt, domain, level="medio"):
    assert len(opts_en) == len(opts_pt) == 4
    return {
        "type": "single",
        "stemEn": stem_en,
        "stemPt": stem_pt,
        "optionsEn": [{"text": t, "correct": i == correct} for i, t in enumerate(opts_en)],
        "optionsPt": [{"text": t, "correct": i == correct} for i, t in enumerate(opts_pt)],
        "explanationEn": expl_en,
        "explanationPt": expl_pt,
        "submateria": domain,
        "level": level,
    }


TRACKS = [
    {"id": "global", "name": "Global", "region": "global", "desc": "Certificações internacionais (IAPP, EXIN, PECB, ISACA, ISO)"},
    {"id": "brazil", "name": "Brasil", "region": "brazil", "desc": "LGPD e certificações com foco no Brasil"},
    {"id": "europe", "name": "Europa", "region": "europe", "desc": "GDPR e certificações por país europeu"},
    {"id": "americas", "name": "Américas", "region": "americas", "desc": "Privacidade nos EUA e América"},
    {"id": "asia", "name": "Ásia", "region": "asia", "desc": "Privacidade na Ásia-Pacífico"},
]

# --- Certification question banks (ludic everyday scenarios) ---

ISFS = {
    "Conceitos de SI": [
        q(
            "Your mother shared your phone number in the family WhatsApp group without asking. In information security terms, what principle did she violate?",
            "Sua mãe compartilhou seu número de telefone no grupo de WhatsApp da família sem perguntar. Em termos de segurança da informação, qual princípio ela violou?",
            ["Confidentiality — only authorized people should access your data", "Availability — systems must always be online", "Integrity — data must never change", "Authentication — you need a password"],
            ["Confidencialidade — só quem está autorizado deve acessar seus dados", "Disponibilidade — sistemas devem estar sempre online", "Integridade — dados nunca podem mudar", "Autenticação — você precisa de senha"],
            0,
            "Confidentiality limits access to authorized parties — sharing personal data in a group without consent breaks it.",
            "Confidencialidade limita o acesso a partes autorizadas — compartilhar dados pessoais em grupo sem consentimento viola esse princípio.",
            "Conceitos de SI",
        ),
        q(
            "The gym app tracks your location 24/7 even when you're not exercising. Which CIA triad element is MOST at risk if hackers steal that history?",
            "O app da academia rastreia sua localização 24h mesmo quando você não está treinando. Qual elemento do triângulo CIA está MAIS em risco se hackers roubarem esse histórico?",
            ["Confidentiality of sensitive movement patterns", "Availability of the gym website", "Integrity of your membership fee", "Authentication of the front desk"],
            ["Confidencialidade dos padrões sensíveis de movimento", "Disponibilidade do site da academia", "Integridade da mensalidade", "Autenticação da recepção"],
            0,
            "Location history is sensitive personal data — unauthorized disclosure is a confidentiality breach.",
            "Histórico de localização é dado pessoal sensível — divulgação não autorizada é violação de confidencialidade.",
            "Conceitos de SI",
        ),
        q(
            "Your cousin changed the due date on a shared spreadsheet 'as a joke.' Which security principle was compromised?",
            "Seu primo alterou a data de vencimento numa planilha compartilhada 'de brincadeira'. Qual princípio de segurança foi comprometido?",
            ["Integrity — data was altered without authorization", "Confidentiality — data was made public", "Availability — the file was deleted", "Non-repudiation — nobody signed"],
            ["Integridade — dado foi alterado sem autorização", "Confidencialidade — dado foi tornado público", "Disponibilidade — arquivo foi apagado", "Não repúdio — ninguém assinou"],
            0,
            "Unauthorized modification of data violates integrity regardless of intent.",
            "Alteração não autorizada de dados viola integridade independentemente da intenção.",
            "Conceitos de SI",
        ),
        q(
            "During Black Friday, your favorite shop's website crashes for 6 hours. Customers cannot buy. Which CIA element failed?",
            "Na Black Friday, o site da sua loja favorita cai por 6 horas. Clientes não conseguem comprar. Qual elemento CIA falhou?",
            ["Availability", "Confidentiality", "Integrity", "Accountability"],
            ["Disponibilidade", "Confidencialidade", "Integridade", "Responsabilização"],
            0,
            "Availability ensures systems and data are accessible when needed.",
            "Disponibilidade garante que sistemas e dados estejam acessíveis quando necessário.",
            "Conceitos de SI",
        ),
        q(
            "At a café, you use 'password123' for Wi-Fi, email, and banking. Your friend says that's risky. What is the BEST advice?",
            "Num café, você usa 'senha123' no Wi-Fi, e-mail e banco. Seu amigo diz que é arriscado. Qual é o MELHOR conselho?",
            ["Use unique strong passwords and enable MFA where possible", "Write passwords on a sticky note for safety", "Share one family password for convenience", "Change password only once a year"],
            ["Use senhas fortes e únicas e ative MFA quando possível", "Anote senhas em post-it por segurança", "Compartilhe uma senha familiar por conveniência", "Troque a senha só uma vez por ano"],
            0,
            "Credential reuse and weak passwords are top attack vectors — MFA adds a critical layer.",
            "Reuso e senhas fracas são vetores comuns — MFA adiciona camada crítica.",
            "Conceitos de SI",
        ),
    ],
    "ISO/IEC 27001": [
        q(
            "Your startup wants ISO 27001. The consultant asks for a document listing which Annex A controls apply and why. What document is this?",
            "Sua startup quer ISO 27001. A consultora pede documento listando controles do Anexo A aplicáveis e por quê. Qual documento é esse?",
            ["Statement of Applicability (SoA)", "Privacy policy for customers", "Marketing plan", "Employee birthday list"],
            ["Declaração de Aplicabilidade (SoA)", "Política de privacidade para clientes", "Plano de marketing", "Lista de aniversários"],
            0,
            "The SoA documents selected controls and justification — core ISO 27001 requirement.",
            "A SoA documenta controles selecionados e justificativa — requisito central da ISO 27001.",
            "ISO/IEC 27001",
        ),
        q(
            "After a phishing email fooled three employees, management wants a repeatable improve-fix-check cycle. Which framework concept applies?",
            "Depois que um e-mail de phishing enganou três funcionários, a direção quer ciclo repetível de melhorar-corrigir-verificar. Qual conceito de framework se aplica?",
            ["PDCA (Plan-Do-Check-Act)", "GDPR Article 17", "LGPD consent only", "DNS caching"],
            ["PDCA (Plan-Do-Check-Act)", "Artigo 17 do GDPR", "Apenas consentimento LGPD", "Cache DNS"],
            0,
            "PDCA drives continuous improvement in an ISMS.",
            "PDCA impulsiona melhoria contínua no SGSI.",
            "ISO/IEC 27001",
        ),
        q(
            "You hire a cloud provider to store customer files. ISO 27001 expects you to evaluate them for what?",
            "Você contrata um provedor cloud para armazenar arquivos de clientes. A ISO 27001 espera que você avalie o quê?",
            ["Information security risks in the supply chain", "Office paint color", "Coffee brand in the cafeteria", "Social media follower count"],
            ["Riscos de segurança da informação na cadeia de suprimentos", "Cor da tinta do escritório", "Marca de café da cantina", "Número de seguidores"],
            0,
            "Supplier security assessment is required — third parties are common risk vectors.",
            "Avaliação de segurança de fornecedores é exigida — terceiros são vetores comuns de risco.",
            "ISO/IEC 27001",
        ),
    ],
    "Ameaças e vulnerabilidades": [
        q(
            "A message says 'Your package is waiting — click here.' The link looks like your carrier but the domain is odd. What attack is this?",
            "Uma mensagem diz 'Sua encomenda aguarda — clique aqui.' O link parece da transportadora mas o domínio é estranho. Que ataque é esse?",
            ["Phishing / social engineering", "Backup failure", "Encryption at rest", "Load balancing"],
            ["Phishing / engenharia social", "Falha de backup", "Criptografia em repouso", "Balanceamento de carga"],
            0,
            "Phishing tricks users into clicking malicious links — classic social engineering.",
            "Phishing engana usuários a clicar links maliciosos — engenharia social clássica.",
            "Ameaças e vulnerabilidades",
        ),
        q(
            "Your laptop was stolen from a car. Full-disk encryption was enabled. What protection does encryption primarily provide here?",
            "Seu notebook foi roubado do carro. Criptografia de disco estava ativa. Que proteção a criptografia oferece aqui?",
            ["Confidentiality if the thief cannot decrypt", "Guaranteed recovery of the laptop", "Automatic police tracking", "Elimination of all malware"],
            ["Confidencialidade se o ladrão não conseguir descriptografar", "Recuperação garantida do notebook", "Rastreamento policial automático", "Eliminação de todo malware"],
            0,
            "Encryption at rest protects confidentiality when physical access is lost.",
            "Criptografia em repouso protege confidencialidade quando o acesso físico se perde.",
            "Ameaças e vulnerabilidades",
        ),
        q(
            "The IT team patches servers every Tuesday. Why is patch management important for your personal banking app experience?",
            "A TI aplica patches toda terça. Por que gestão de patches importa para seu app bancário?",
            ["It closes known vulnerabilities attackers exploit", "It makes logos prettier", "It removes your login history legally", "It disables two-factor authentication"],
            ["Fecha vulnerabilidades conhecidas que atacantes exploram", "Deixa logos mais bonitos", "Remove histórico de login legalmente", "Desativa autenticação de dois fatores"],
            0,
            "Patches fix known flaws — delaying them increases breach risk.",
            "Patches corrigem falhas conhecidas — atrasar aumenta risco de incidente.",
            "Ameaças e vulnerabilidades",
        ),
    ],
    "Controles organizacionais": [
        q(
            "New hires get a 10-minute video saying 'don't share passwords.' What ISO control category does this support?",
            "Novos funcionários veem vídeo de 10 min dizendo 'não compartilhe senhas'. Que categoria de controle ISO isso apoia?",
            ["Security awareness and training", "Physical access only", "Financial audit", "Product design"],
            ["Conscientização e treinamento em SI", "Apenas acesso físico", "Auditoria financeira", "Design de produto"],
            0,
            "Human error is a major threat — awareness training is an organizational control.",
            "Erro humano é ameaça major — treinamento de conscientização é controle organizacional.",
            "Controles organizacionais",
        ),
        q(
            "Your company labels documents 'Public', 'Internal', 'Confidential.' Why?",
            "Sua empresa rotula documentos 'Público', 'Interno', 'Confidencial'. Por quê?",
            ["To apply appropriate handling based on sensitivity", "To increase printing costs", "To replace encryption entirely", "To avoid backups"],
            ["Aplicar tratamento adequado conforme sensibilidade", "Aumentar custo de impressão", "Substituir criptografia totalmente", "Evitar backups"],
            0,
            "Information classification drives proportional security measures.",
            "Classificação da informação orienta medidas de segurança proporcionais.",
            "Controles organizacionais",
        ),
    ],
    "Governança e conformidade": [
        q(
            "Before buying a smaller competitor, legal asks about their data breaches and security certs. This diligence relates to:",
            "Antes de comprar uma concorrente menor, jurídico pergunta sobre vazamentos e certificações de segurança. Essa diligência relaciona-se a:",
            ["M&A security and privacy due diligence", "Office furniture inventory", "Holiday calendar", "Logo redesign"],
            ["Due diligence de SI e privacidade em M&A", "Inventário de móveis", "Calendário de feriados", "Redesign de logo"],
            0,
            "Acquisitions can inherit data liabilities — due diligence identifies risks.",
            "Aquisições podem herdar passivos de dados — due diligence identifica riscos.",
            "Governança e conformidade",
        ),
        q(
            "Two colleagues: one approves access, the other grants it — never the same person. Which principle is this?",
            "Dois colegas: um aprova acesso, outro concede — nunca a mesma pessoa. Qual princípio é esse?",
            ["Segregation of duties (SoD)", "Privacy by default", "Data minimization", "Right to erasure"],
            ["Segregação de funções (SoD)", "Privacidade por padrão", "Minimização de dados", "Direito ao apagamento"],
            0,
            "SoD prevents fraud and excessive privilege concentration.",
            "SoD previne fraude e concentração excessiva de privilégios.",
            "Governança e conformidade",
        ),
    ],
}

PDPF = {
    "Fundamentos de privacidade": [
        q(
            "A fitness app asks for your weight, mood, and full contact list 'to personalize ads.' Which privacy principle is MOST violated?",
            "Um app de fitness pede peso, humor e lista completa de contatos 'para personalizar anúncios'. Qual princípio de privacidade está MAIS violado?",
            ["Data minimization / necessity", "Availability", "Network speed", "Hardware warranty"],
            ["Minimização / necessidade de dados", "Disponibilidade", "Velocidade de rede", "Garantia de hardware"],
            0,
            "Collect only what is adequate and necessary for the stated purpose.",
            "Colete apenas o adequado e necessário para a finalidade informada.",
            "Fundamentos de privacidade",
        ),
        q(
            "Your neighbor photographs kids at a birthday party and posts on Instagram without asking parents. Under privacy law concepts, this mainly concerns:",
            "Seu vizinho fotografa crianças numa festa e posta no Instagram sem perguntar aos pais. Sob conceitos de privacidade, isso diz respeito principalmente a:",
            ["Personal data of identifiable children and consent/legal basis", "Copyright of the cake design only", "Wi-Fi password strength", "ISO 9001 quality"],
            ["Dados pessoais de crianças identificáveis e base legal/consentimento", "Apenas direitos autorais do bolo", "Força da senha Wi-Fi", "Qualidade ISO 9001"],
            0,
            "Children's images are personal data — special protection and legal bases apply.",
            "Imagens de crianças são dados pessoais — proteção especial e bases legais se aplicam.",
            "Fundamentos de privacidade",
        ),
        q(
            "When signing up for a newsletter, the box 'I agree to everything' is pre-checked. Valid consent generally requires:",
            "Ao assinar newsletter, a caixa 'Concordo com tudo' já vem marcada. Consentimento válido geralmente exige:",
            ["Freely given, specific, informed, and unambiguous opt-in", "Silence equals consent", "Pre-checked boxes by default", "Consent from a third cousin"],
            ["Opt-in livre, específico, informado e inequívoco", "Silêncio vale como consentimento", "Caixas pré-marcadas por padrão", "Consentimento de um primo distante"],
            0,
            "Valid consent must be active and informed — not bundled or pre-ticked.",
            "Consentimento válido deve ser ativo e informado — não agrupado ou pré-marcado.",
            "Fundamentos de privacidade",
        ),
        q(
            "A smart speaker listens by default until you opt out in settings. 'Privacy by default' means:",
            "Uma caixa inteligente escuta por padrão até você desativar. 'Privacidade por padrão' significa:",
            ["Most protective settings should be the factory default", "Maximum data collection is default", "No privacy notice is needed", "Users must hack settings"],
            ["Configurações mais protetivas devem ser o padrão de fábrica", "Coleta máxima é o padrão", "Aviso de privacidade não é necessário", "Usuários devem hackear configurações"],
            0,
            "Privacy by default requires protective settings out of the box.",
            "Privacidade por padrão exige configurações protetivas desde a origem.",
            "Fundamentos de privacidade",
        ),
    ],
    "LGPD — bases e direitos": [
        q(
            "You request a copy of all data a store has about you. Under LGPD, this is exercising your right to:",
            "Você pede cópia de todos os dados que uma loja tem sobre você. Pela LGPD, isso é exercer o direito de:",
            ["Access (confirmação e acesso)", "Portability only to competitors", "Free products forever", "Delete all legal invoices"],
            ["Acesso (confirmação e acesso)", "Portabilidade só para concorrentes", "Produtos grátis para sempre", "Apagar todas as notas fiscais legais"],
            0,
            "LGPD Art. 18 includes confirmation of processing and access to data.",
            "Art. 18 da LGPD inclui confirmação de tratamento e acesso aos dados.",
            "LGPD — bases e direitos",
        ),
        q(
            "A clinic keeps your medical records 20 years after last visit 'just because.' Which LGPD principle is questioned?",
            "Uma clínica guarda prontuários 20 anos após última consulta 'porque sim'. Qual princípio LGPD é questionado?",
            ["Storage limitation / need for retention", "Purpose limitation only for marketing", "Publicity by default", "No controller duties"],
            ["Limitação de conservação / necessidade de retenção", "Limitação de finalidade só para marketing", "Publicidade por padrão", "Ausência de deveres do controlador"],
            0,
            "Data should not be kept longer than necessary for the purpose or legal obligation.",
            "Dados não devem ser mantidos além do necessário para finalidade ou obrigação legal.",
            "LGPD — bases e direitos",
        ),
        q(
            "Who is the 'controller' when you buy shoes online and the store decides why and how your data is used?",
            "Quem é o 'controlador' quando você compra sapatos online e a loja decide por quê e como seus dados são usados?",
            ["The online store (controlador)", "The delivery driver only (operador)", "Your browser (subprocessor)", "The payment card brand always"],
            ["A loja online (controlador)", "Apenas o entregador (operador)", "Seu navegador (suboperador)", "Sempre a bandeira do cartão"],
            0,
            "The controller determines purposes and means of processing.",
            "O controlador determina finalidades e meios de tratamento.",
            "LGPD — bases e direitos",
        ),
    ],
    "GDPR — visão geral": [
        q(
            "A Brazilian e-commerce ships to Germany. Must it consider GDPR for German customers?",
            "Um e-commerce brasileiro envia para a Alemanha. Deve considerar GDPR para clientes alemães?",
            ["Yes — GDPR applies when offering goods/services to people in the EU/EEA", "No — GDPR only applies inside Brazil", "Only if the CEO speaks German", "Never for online sales"],
            ["Sim — GDPR aplica quando oferece bens/serviços a pessoas na UE/EEE", "Não — GDPR só vale no Brasil", "Só se o CEO falar alemão", "Nunca para vendas online"],
            0,
            "GDPR has extraterritorial scope for targeting/data subjects in the EU.",
            "GDPR tem extraterritorialidade para titulares na UE.",
            "GDPR — visão geral",
        ),
        q(
            "After discovering a breach Friday night, when must you generally notify the supervisory authority under GDPR?",
            "Após descobrir violação na sexta à noite, quando notificar a autoridade supervisora pelo GDPR?",
            ["Within 72 hours where feasible", "Within 5 years", "Only if customers complain first", "Never if encrypted"],
            ["Em até 72 horas quando viável", "Em até 5 anos", "Só se clientes reclamarem primeiro", "Nunca se criptografado"],
            0,
            "Article 33 sets the 72-hour notification benchmark to authorities.",
            "Art. 33 estabelece prazo de 72 horas para notificação à autoridade.",
            "GDPR — visão geral",
        ),
    ],
    "Tratamento e segurança": [
        q(
            "Your HR spreadsheet lists employees with real names replaced by codes, but IT can re-link them. This is:",
            "Planilha de RH lista funcionários com nomes substituídos por códigos, mas TI pode reassociar. Isso é:",
            ["Pseudonymization — still personal data if re-identification is possible", "Irreversible anonymization", "Public domain data", "Non-personal metadata always"],
            ["Pseudonimização — ainda é dado pessoal se reidentificação for possível", "Anonimização irreversível", "Dado de domínio público", "Metadado não pessoal sempre"],
            0,
            "Pseudonymization reduces risk but data may remain personal data.",
            "Pseudonimização reduz risco mas o dado pode continuar sendo pessoal.",
            "Tratamento e segurança",
        ),
        q(
            "A vendor processes payroll for your company under contract instructions. In GDPR terms they are typically a:",
            "Um fornecedor processa folha sob instruções contratuais. Nos termos do GDPR, ele é tipicamente:",
            ["Processor (operador)", "Controller of your business strategy", "Supervisory authority", "Data subject"],
            ["Operador (processor)", "Controlador da sua estratégia", "Autoridade supervisora", "Titular dos dados"],
            0,
            "Processors act on controller instructions — Art. 28 requires a contract.",
            "Operadores agem conforme instruções do controlador — Art. 28 exige contrato.",
            "Tratamento e segurança",
        ),
    ],
    "Papéis e responsabilidades": [
        q(
            "The company appoints Maria as DPO but she also approves all marketing campaigns using customer data. What risk exists?",
            "A empresa nomeia Maria como DPO mas ela também aprova campanhas de marketing com dados de clientes. Que risco existe?",
            ["Conflict of interest — DPO must be independent", "No risk if she is friendly", "DPO must always be external lawyer only", "GDPR prohibits any DPO"],
            ["Conflito de interesses — DPO deve ser independente", "Sem risco se for simpática", "DPO deve ser sempre advogado externo", "GDPR proíbe qualquer DPO"],
            0,
            "DPO independence avoids monitoring one's own decisions.",
            "Independência do DPO evita monitorar as próprias decisões.",
            "Papéis e responsabilidades",
        ),
        q(
            "Before launching face recognition at office doors, the DPO asks for a formal risk assessment. This is:",
            "Antes de lançar reconhecimento facial nas portas, o DPO pede avaliação formal de risco. Isso é:",
            ["DPIA / privacy impact assessment for high-risk processing", "Optional marketing survey", "Pen test of coffee machine", "ISO 14001 audit"],
            ["DPIA / avaliação de impacto para tratamento de alto risco", "Pesquisa de marketing opcional", "Pen test da cafeteira", "Auditoria ISO 14001"],
            0,
            "DPIA is required when processing likely results in high risk to rights.",
            "DPIA é exigida quando tratamento provavelmente gera alto risco aos direitos.",
            "Papéis e responsabilidades",
        ),
    ],
}

PDPP = {
    "DPIA e gestão de riscos": [
        q(
            "Your city deploys AI cameras in parks 'for safety.' Residents worry about profiling. As DPO, your FIRST step is:",
            "Sua cidade instala câmeras com IA nos parques 'por segurança.' Moradores temem perfilamento. Como DPO, seu PRIMEIRO passo é:",
            ["Conduct or commission a DPIA before scaling deployment", "Post photos on social media", "Ignore complaints until fined", "Sell footage to advertisers"],
            ["Conduzir ou encomendar DPIA antes de escalar", "Postar fotos nas redes", "Ignorar reclamações até multa", "Vender imagens a anunciantes"],
            0,
            "Systematic monitoring with new tech typically triggers high-risk assessment.",
            "Monitoramento sistemático com nova tecnologia tipicamente exige avaliação de alto risco.",
            "DPIA e gestão de riscos",
        ),
        q(
            "After controls, some risk remains but leadership accepts it with documentation. This leftover is:",
            "Após controles, algum risco permanece mas a direção aceita com documentação. Esse restante é:",
            ["Residual risk", "Zero risk guarantee", "Marketing KPI", "Backup checksum"],
            ["Risco residual", "Garantia de risco zero", "KPI de marketing", "Checksum de backup"],
            0,
            "Residual risk must be documented and accepted by accountable roles.",
            "Risco residual deve ser documentado e aceito por papéis responsáveis.",
            "DPIA e gestão de riscos",
        ),
    ],
    "Operação do DPO": [
        q(
            "A customer emails: 'Delete my account data.' Legal says invoices must stay 5 years. Best DPO guidance?",
            "Cliente e-mail: 'Apague dados da minha conta.' Jurídico diz que notas devem ficar 5 anos. Melhor orientação do DPO?",
            ["Delete what is not legally required; retain minimum for legal obligation with justification", "Delete everything including tax records", "Ignore the request", "Publish the request online"],
            ["Apague o que não for legalmente exigido; retenha mínimo por obrigação legal com justificativa", "Apague tudo inclusive fiscais", "Ignore o pedido", "Publique o pedido online"],
            0,
            "Erasure rights have exceptions — legal retention must be limited and documented.",
            "Direito ao apagamento tem exceções — retenção legal deve ser limitada e documentada.",
            "Operação do DPO",
        ),
        q(
            "Your ROPA (record of processing) hasn't been updated since a new analytics tool launched. Why is this a problem?",
            "Seu registro de tratamentos (ROPA) não é atualizado desde novo tool de analytics. Por que isso é problema?",
            ["Accountability — you must demonstrate actual processing activities", "ROPA is optional decoration", "Only ISO needs records", "Analytics tools are exempt"],
            ["Responsabilização — deve demonstrar tratamentos reais", "ROPA é decoração opcional", "Só ISO precisa de registros", "Ferramentas analytics são isentas"],
            0,
            "ROPA must reflect reality for compliance demonstration.",
            "ROPA deve refletir a realidade para demonstração de conformidade.",
            "Operação do DPO",
        ),
    ],
    "Casos práticos LGPD/GDPR": [
        q(
            "An employee accidentally emails a spreadsheet with 500 customer emails to the wrong vendor. First priority?",
            "Funcionário envia planilha com 500 e-mails de clientes ao fornecedor errado. Primeira prioridade?",
            ["Contain incident, assess impact, notify per legal thresholds", "Delete your own inbox only", "Wait one year", "Post apology on Twitter only"],
            ["Conter incidente, avaliar impacto, notificar conforme limiares legais", "Apagar só sua caixa de entrada", "Esperar um ano", "Postar desculpas só no Twitter"],
            0,
            "Incident response: contain, assess, notify authorities/data subjects as required.",
            "Resposta a incidente: conter, avaliar, notificar autoridades/titulares conforme exigido.",
            "Casos práticos LGPD/GDPR",
        ),
        q(
            "Marketing wants to buy an email list from a conference sponsor without opt-in proof. PDPP-aligned advice?",
            "Marketing quer comprar lista de e-mails de patrocinador sem prova de opt-in. Conselho alinhado ao PDPP?",
            ["Reject — need valid legal basis and proof of consent/legitimate interest assessment", "Buy immediately for growth", "Use list until someone complains", "Share list publicly"],
            ["Recusar — é necessária base legal válida e prova de consentimento/LIA", "Comprar imediatamente por crescimento", "Usar até alguém reclamar", "Compartilhar lista publicamente"],
            0,
            "Acquired lists without lawful basis create regulatory and reputational risk.",
            "Listas adquiridas sem base legal criam risco regulatório e reputacional.",
            "Casos práticos LGPD/GDPR",
        ),
    ],
    "Contratos e terceiros": [
        q(
            "Your cloud vendor subcontracts storage in another country without telling you. Contractually this likely breaches:",
            "Seu vendor cloud subcontrata armazenamento em outro país sem avisar. Contratualmente isso provavelmente viola:",
            ["Authorization and transparency on subprocessors", "Logo usage guidelines", "Office hours clause", "Coffee budget cap"],
            ["Autorização e transparência sobre suboperadores", "Diretrizes de uso de logo", "Cláusula de horário", "Teto de budget de café"],
            0,
            "Controllers must authorize subprocessors with equivalent protections.",
            "Controladores devem autorizar suboperadores com proteções equivalentes.",
            "Contratos e terceiros",
        ),
    ],
    "Monitoramento e melhoria": [
        q(
            "After a breach, the team documents root cause and updates training. This closes the loop of:",
            "Após violação, equipe documenta causa raiz e atualiza treinamento. Isso fecha o ciclo de:",
            ["Continuous improvement (lessons learned)", "Eliminating all future risk forever", "Removing the DPO role", "Stopping all digital services"],
            ["Melhoria contínua (lições aprendidas)", "Eliminar todo risco futuro para sempre", "Remover papel do DPO", "Parar todos serviços digitais"],
            0,
            "Post-incident review drives program maturity.",
            "Revisão pós-incidente impulsiona maturidade do programa.",
            "Monitoramento e melhoria",
        ),
    ],
}

# Helper to pad certifications to minimum count with generic ludic templates
def pad_cert(domains, min_q=15, cert_name="privacy"):
    flat = []
    for domain, items in domains.items():
        for item in items:
            flat.append((domain, item))
    templates = [
        q(
            f"Your friend asks what '{cert_name}' certification helps with at work. Best answer:",
            f"Seu amigo pergunta para que serve certificação '{cert_name}' no trabalho. Melhor resposta:",
            ["Demonstrates structured knowledge for privacy/security roles", "Replaces all laws automatically", "Guarantees zero incidents", "Eliminates need for DPO"],
            ["Demonstra conhecimento estruturado para papéis de privacidade/segurança", "Substitui todas as leis automaticamente", "Garante zero incidentes", "Elimina necessidade de DPO"],
            0,
            "Certifications validate competence — they complement but don't replace legal compliance.",
            "Certificações validam competência — complementam mas não substituem conformidade legal.",
            "Revisão geral",
        ),
    ]
    idx = 0
    while len(flat) < min_q:
        domain = list(domains.keys())[idx % len(domains)]
        t = templates[idx % len(templates)].copy()
        t["submateria"] = domain
        flat.append((domain, t))
        idx += 1
    out = {}
    for domain, item in flat[:max(min_q, len(flat))]:
        out.setdefault(domain, []).append(item)
    return out


def lgpd_brazil_extra():
    return {
        "LGPD no dia a dia": [
            q(
                "A condominium WhatsApp group shares resident CPF photos to 'verify deliveries.' Under LGPD, this is:",
                "Grupo de WhatsApp do condomínio compartilha fotos de CPF de moradores para 'verificar entregas'. Pela LGPD, isso é:",
                ["Likely unlawful disclosure — need legal basis and minimization", "Always allowed in groups", "Exempt because it's WhatsApp", "Only ANPD can use CPF"],
                ["Provável divulgação ilícita — exige base legal e minimização", "Sempre permitido em grupos", "Isento por ser WhatsApp", "Só ANPD pode usar CPF"],
                0,
                "CPF is personal data — sharing in groups rarely has valid legal basis.",
                "CPF é dado pessoal — compartilhar em grupos raramente tem base legal válida.",
                "LGPD no dia a dia",
            ),
            q(
                "Your employer uses biometric fingerprint for time clock without offering an alternative. LGPD concerns include:",
                "Empregador usa biometria de digital no ponto sem alternativa. Preocupações LGPD incluem:",
                ["Sensitive data, transparency, necessity, and less intrusive alternatives", "No rules for employees", "Biometrics are never personal data", "Only GDPR applies"],
                ["Dado sensível, transparência, necessidade e alternativas menos invasivas", "Sem regras para empregados", "Biometria nunca é dado pessoal", "Só GDPR se aplica"],
                0,
                "Art. 11 LGPD — sensitive data needs specific bases and safeguards.",
                "Art. 11 LGPD — dado sensível exige bases específicas e salvaguardas.",
                "LGPD no dia a dia",
            ),
            q(
                "You want to know if a telemarketing company has your data. You may file a request with the company as:",
                "Você quer saber se telemarketing tem seus dados. Pode fazer pedido à empresa como:",
                ["Data subject (titular) exercising access rights", "Anonymous hacker", "Competitor spy only", "Police without warrant always"],
                ["Titular exercendo direito de acesso", "Hacker anônimo", "Apenas espião concorrente", "Polícia sem mandado sempre"],
                0,
                "Titular rights include confirmation and access under Art. 18 LGPD.",
                "Direitos do titular incluem confirmação e acesso pelo Art. 18 LGPD.",
                "LGPD no dia a dia",
            ),
        ],
        "ANPD e sanções": [
            q(
                "A startup ignores repeated ANPD guidance after a warning. Possible administrative sanctions include:",
                "Startup ignora orientações repetidas da ANPD após advertência. Sanções administrativas possíveis incluem:",
                ["Fine, publicity of violation, partial suspension of database", "Free marketing from ANPD", "Automatic ISO certificate", "Tax exemption"],
                ["Multa, publicidade da infração, bloqueio parcial de banco de dados", "Marketing grátis da ANPD", "Certificado ISO automático", "Isenção fiscal"],
                0,
                "Art. 52 LGPD lists sanctions including fines and blocking.",
                "Art. 52 LGPD lista sanções incluindo multas e bloqueio.",
                "ANPD e sanções",
            ),
        ],
        "Encarregado (DPO) BR": [
            q(
                "Under LGPD, the DPO (Encarregado) channel helps citizens:",
                "Pela LGPD, o canal do Encarregado (DPO) ajuda cidadãos a:",
                ["Communicate with the controller and facilitate rights exercise", "Approve all HR salaries", "Replace the board of directors", "Sell personal data"],
                ["Comunicar-se com controlador e facilitar exercício de direitos", "Aprovar todos salários de RH", "Substituir conselho", "Vender dados pessoais"],
                0,
                "DPO is interface between controller, data subjects, and ANPD.",
                "DPO é interface entre controlador, titulares e ANPD.",
                "Encarregado (DPO) BR",
            ),
        ],
    }


def cipp_e_domains():
    return pad_cert({
        "Domain I — Privacy laws": [
            q(
                "A US company hires you in France to process EU employee data. Which frame is MOST relevant for employee privacy?",
                "Empresa americana contrata você na França para dados de funcionários UE. Qual marco é MAIS relevante?",
                ["GDPR as lex specialis for EU personal data", "Only US HIPAA for all data", "Brazilian LGPD only", "No law applies to HR"],
                ["GDPR como lex specialis para dados pessoais na UE", "Apenas HIPAA EUA para tudo", "Só LGPD brasileira", "Nenhuma lei aplica a RH"],
                0,
                "CIPP/E covers EU regulatory frameworks including GDPR and ePrivacy.",
                "CIPP/E cobre frameworks regulatórios UE incluindo GDPR e ePrivacy.",
                "Domain I — Privacy laws",
            ),
        ],
        "Domain II — Data lifecycle": [
            q(
                "You delete old CRM contacts but backups still hold them for 90 days per policy. This illustrates:",
                "Você apaga contatos antigos do CRM mas backups ainda os guardam 90 dias por política. Isso ilustra:",
                ["Retention and erasure must cover live systems AND backup cycles", "Backups are never personal data", "Deletion is impossible legally", "Only marketing cares"],
                ["Retenção e apagamento devem cobrir sistemas E ciclos de backup", "Backups nunca são dados pessoais", "Apagamento é impossível legalmente", "Só marketing se importa"],
                0,
                "Lifecycle management includes backup and archive policies.",
                "Gestão do ciclo de vida inclui políticas de backup e arquivo.",
                "Domain II — Data lifecycle",
            ),
        ],
        "Domain III — International transfers": [
            q(
                "Your team in Lisbon sends customer data to a US analytics SaaS. Post-Schrems II, you should:",
                "Equipe em Lisboa envia dados a SaaS de analytics nos EUA. Pós-Schrems II, você deve:",
                ["Assess SCCs plus supplementary measures and transfer impact", "Transfer freely without review", "Only use fax machines", "Ignore EU law for SaaS"],
                ["Avaliar SCCs mais medidas suplementares e impacto de transferência", "Transferir livremente sem revisão", "Usar só fax", "Ignorar lei UE para SaaS"],
                0,
                "CIPP/E requires understanding transfer tools and TIA.",
                "CIPP/E exige entender mecanismos de transferência e TIA.",
                "Domain III — International transfers",
            ),
        ],
    }, min_q=15, cert_name="CIPP/E")


def generic_iapp(cert_name, focus):
    base = {
        f"{cert_name} — Governança": [
            q(
                f"Your manager says '{cert_name} is just checkbox compliance.' Best professional response:",
                f"Seu gestor diz '{cert_name} é só compliance de checkbox.' Melhor resposta profissional:",
                ["Privacy programs reduce risk, build trust, and enable lawful innovation", "Ignore privacy until fined", "Collect all data preemptively", "Hide policies from users"],
                ["Programas de privacidade reduzem risco, constroem confiança e permitem inovação lícita", "Ignore privacidade até multa", "Colete todos os dados preventivamente", "Oculte políticas dos usuários"],
                0,
                f"{cert_name} emphasizes operational privacy governance.",
                f"{cert_name} enfatiza governança operacional de privacidade.",
                f"{cert_name} — Governança",
            ),
        ],
        f"{cert_name} — Operacional": [
            q(
                f"A {focus} project launches tomorrow without privacy review. You should:",
                f"Projeto de {focus} lança amanhã sem revisão de privacidade. Você deve:",
                ["Escalate for privacy review — accountability requires documented assessment", "Stay silent to meet deadline", "Delete all logs", "Publish datasets openly"],
                ["Escalar para revisão de privacidade — responsabilização exige avaliação documentada", "Ficar em silêncio por prazo", "Apagar todos logs", "Publicar datasets abertamente"],
                0,
                "Program management includes privacy gates before launch.",
                "Gestão de programas inclui gates de privacidade antes do lançamento.",
                f"{cert_name} — Operacional",
            ),
        ],
    }
    return pad_cert(base, min_q=15, cert_name=cert_name)


CERTS = [
    {"code": "EXIN-ISFS", "materia": "ISFS", "org": "EXIN", "trackId": "global", "region": "global",
     "title": "Information Security Foundation (ISFS)", "timeMinutes": 60,
     "description": "Fundamentos de SI alinhados à ISO/IEC 27001 — cenários do dia a dia.",
     "domains": pad_cert(ISFS, 18)},
    {"code": "EXIN-PDPF", "materia": "PDPF", "org": "EXIN", "trackId": "global", "region": "global",
     "title": "Privacy and Data Protection Foundation (PDPF)", "timeMinutes": 60,
     "description": "Fundamentos de privacidade, LGPD e GDPR com situações cotidianas.",
     "domains": pad_cert(PDPF, 18)},
    {"code": "EXIN-PDPP", "materia": "PDPP", "org": "EXIN", "trackId": "global", "region": "global",
     "title": "Privacy and Data Protection Practitioner (PDPP)", "timeMinutes": 90,
     "description": "Prática de DPO — casos reais, riscos, contratos e incidentes.",
     "domains": pad_cert(PDPP, 18)},
    {"code": "EXIN-CDPO", "materia": "CDPO", "org": "EXIN", "trackId": "global", "region": "global",
     "title": "Certified Data Protection Officer (EXIN CDPO)", "timeMinutes": 90,
     "description": "Programa integrado EXIN para Encarregado de Dados.",
     "domains": pad_cert({**ISFS, **{"Programa CDPO": PDPF["Fundamentos de privacidade"][:2]}}, 16, "EXIN CDPO")},
    {"code": "IAPP-CIPP-E", "materia": "CIPP/E", "org": "IAPP", "trackId": "global", "region": "global",
     "title": "Certified Information Privacy Professional — Europe (CIPP/E)", "timeMinutes": 150,
     "description": "Profissional de privacidade focado em GDPR e regulamentação europeia.",
     "domains": cipp_e_domains()},
    {"code": "IAPP-CIPM", "materia": "CIPM", "org": "IAPP", "trackId": "global", "region": "global",
     "title": "Certified Information Privacy Manager (CIPM)", "timeMinutes": 150,
     "description": "Gestão de programas de privacidade — métricas, auditoria, cultura.",
     "domains": generic_iapp("CIPM", "programa de privacidade")},
    {"code": "IAPP-CIPT", "materia": "CIPT", "org": "IAPP", "trackId": "global", "region": "global",
     "title": "Certified Information Privacy Technologist (CIPT)", "timeMinutes": 150,
     "description": "Privacidade em engenharia — PETs, segurança, arquitetura.",
     "domains": generic_iapp("CIPT", "engenharia de privacidade")},
    {"code": "IAPP-AIGP", "materia": "AIGP", "org": "IAPP", "trackId": "global", "region": "global",
     "title": "Artificial Intelligence Governance Professional (AIGP)", "timeMinutes": 120,
     "description": "Governança de IA — riscos, transparência, conformidade (expansão futura).",
     "domains": generic_iapp("AIGP", "IA generativa"), "stub": True},
    {"code": "IAPP-FIP", "materia": "FIP", "org": "IAPP", "trackId": "global", "region": "global",
     "title": "FIP — Fellow of Information Privacy (path)", "timeMinutes": 120,
     "description": "Trilha fellow IAPP — visão integrada CIPP/CIPM/CIPT (stub).",
     "domains": generic_iapp("FIP", "programa fellow"), "stub": True},
    {"code": "PECB-CDPO", "materia": "CDPO", "org": "PECB", "trackId": "global", "region": "global",
     "title": "PECB Certified Data Protection Officer", "timeMinutes": 120,
     "description": "CDPO PECB — ISO 17024, alinhado a GDPR/LGPD.",
     "domains": generic_iapp("PECB CDPO", "conformidade PECB")},
    {"code": "ISACA-CDPSE", "materia": "CDPSE", "org": "ISACA", "trackId": "global", "region": "global",
     "title": "Certified Data Privacy Solutions Engineer (CDPSE)", "timeMinutes": 120,
     "description": "Privacidade + engenharia — controles técnicos e arquitetura.",
     "domains": generic_iapp("CDPSE", "soluções técnicas")},
    {"code": "ISO-27701", "materia": "ISO 27701", "org": "ISO", "trackId": "global", "region": "global",
     "title": "ISO/IEC 27701 — Privacy Information Management", "timeMinutes": 90,
     "description": "Extensão de privacidade para SGSI ISO 27001.",
     "domains": pad_cert({"PIMS": PDPF["Fundamentos de privacidade"][:3], "Controles": ISFS["ISO/IEC 27001"][:3]}, 16, "ISO 27701")},
    {"code": "IAPP-CDPO-BR", "materia": "CDPO/BR", "org": "IAPP", "trackId": "brazil", "region": "brazil",
     "title": "Certified Data Protection Officer — Brazil (CDPO/BR)", "timeMinutes": 120,
     "description": "Encarregado de Dados com foco LGPD e contexto brasileiro.",
     "domains": pad_cert(lgpd_brazil_extra(), 18, "CDPO/BR")},
    {"code": "EXIN-LGPD", "materia": "LGPD", "org": "EXIN", "trackId": "brazil", "region": "brazil",
     "title": "EXIN Trilha LGPD", "timeMinutes": 90,
     "description": "Trilha EXIN focada na Lei Geral de Proteção de Dados.",
     "domains": pad_cert(lgpd_brazil_extra(), 16, "EXIN LGPD")},
    {"code": "IAPP-CDPO-FR", "materia": "CDPO/FR", "org": "IAPP", "trackId": "europe", "region": "europe",
     "title": "Certified Data Protection Officer — France (CDPO/FR)", "timeMinutes": 120,
     "description": "DPO na França — Loi Informatique et Libertés e GDPR.",
     "domains": generic_iapp("CDPO/FR", "contexto francês")},
    {"code": "CNIL-DPO", "materia": "CNIL", "org": "CNIL", "trackId": "europe", "region": "europe",
     "title": "CNIL-recognized Data Protection Officer", "timeMinutes": 90,
     "description": "Referencial CNIL para DPO na França.",
     "domains": generic_iapp("CNIL DPO", "referencial CNIL")},
    {"code": "TUV-DPO-DE", "materia": "TÜV DPO", "org": "TÜV", "trackId": "europe", "region": "europe",
     "title": "TÜV Certified Data Protection Officer (Germany)", "timeMinutes": 90,
     "description": "DPO certificado TÜV — BDSG e GDPR na Alemanha.",
     "domains": generic_iapp("TÜV DPO", "BDSG alemão")},
    {"code": "UK-GDPR", "materia": "UK GDPR", "org": "ICO", "trackId": "europe", "region": "europe",
     "title": "UK GDPR & Data Protection Act", "timeMinutes": 90,
     "description": "Privacidade pós-Brexit — UK GDPR e ICO guidance.",
     "domains": generic_iapp("UK GDPR", "Reino Unido")},
    {"code": "IAPP-CIPP-US", "materia": "CIPP/US", "org": "IAPP", "trackId": "americas", "region": "americas",
     "title": "CIPP/US — US Privacy Laws", "timeMinutes": 150,
     "description": "CCPA/CPRA, COPPA, HIPAA context — privacidade nos EUA.",
     "domains": generic_iapp("CIPP/US", "privacidade EUA")},
    {"code": "IAPP-CIPP-A", "materia": "CIPP/A", "org": "IAPP", "trackId": "asia", "region": "asia",
     "title": "CIPP/A — Asia Privacy (stub)", "timeMinutes": 120,
     "description": "PDPA, PIPL, APPI — expansão futura Ásia-Pacífico.",
     "domains": generic_iapp("CIPP/A", "Ásia-Pacífico"), "stub": True},
]


def main():
    bank = {"version": "2.0", "tracks": TRACKS, "certifications": CERTS}
    total_q = sum(
        len(items)
        for c in CERTS
        for items in c["domains"].values()
    )
    js = "/* Velora DPO Global Bank — original ludic scenarios, exam-outline aligned */\n"
    js += "/* Generated by generate_dpo_global_bank.py — do not edit by hand */\n"
    js += "const DPO_GLOBAL_BANK = "
    js += json.dumps(bank, ensure_ascii=False, indent=2)
    js += ";\n"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(js, encoding="utf-8")
    print(f"Wrote {OUT} — {len(CERTS)} certs, {total_q} questions")


if __name__ == "__main__":
    main()
