"""Content engine for Velora Knowledge OS bank generation."""
from __future__ import annotations

import hashlib
import json
import random
from typing import Any

SCENARIO_CONTEXTS = [
    {
        "id": "family",
        "label_pt": "família",
        "label_en": "family",
        "actor_pt": "Sua mãe",
        "actor_en": "Your mother",
        "place_pt": "grupo de WhatsApp da família",
        "place_en": "family WhatsApp group",
    },
    {
        "id": "school",
        "label_pt": "escola",
        "label_en": "school",
        "actor_pt": "A escola do seu filho",
        "actor_en": "Your child's school",
        "place_pt": "portal escolar",
        "place_en": "school portal",
    },
    {
        "id": "hospital",
        "label_pt": "hospital",
        "label_en": "hospital",
        "actor_pt": "Um hospital",
        "actor_en": "A hospital",
        "place_pt": "prontuário eletrônico",
        "place_en": "electronic health record",
    },
    {
        "id": "bank",
        "label_pt": "banco",
        "label_en": "bank",
        "actor_pt": "Seu banco",
        "actor_en": "Your bank",
        "place_pt": "aplicativo de internet banking",
        "place_en": "mobile banking app",
    },
    {
        "id": "ecommerce",
        "label_pt": "e-commerce",
        "label_en": "e-commerce",
        "actor_pt": "Uma loja online",
        "actor_en": "An online store",
        "place_pt": "checkout com recomendações personalizadas",
        "place_en": "checkout with personalized recommendations",
    },
    {
        "id": "social",
        "label_pt": "redes sociais",
        "label_en": "social media",
        "actor_pt": "Uma rede social",
        "actor_en": "A social network",
        "place_pt": "feed com anúncios direcionados",
        "place_en": "feed with targeted ads",
    },
    {
        "id": "mobile",
        "label_pt": "aplicativo móvel",
        "label_en": "mobile app",
        "actor_pt": "Um app de mobilidade",
        "actor_en": "A ride-hailing app",
        "place_pt": "permissões de localização em segundo plano",
        "place_en": "background location permissions",
    },
    {
        "id": "travel",
        "label_pt": "viagens",
        "label_en": "travel",
        "actor_pt": "Uma companhia aérea",
        "actor_en": "An airline",
        "place_pt": "check-in digital com passaporte",
        "place_en": "digital check-in with passport scan",
    },
    {
        "id": "condo",
        "label_pt": "condomínio",
        "label_en": "condominium",
        "actor_pt": "O síndico",
        "actor_en": "The building manager",
        "place_pt": "grupo de moradores",
        "place_en": "residents' group chat",
    },
    {
        "id": "company",
        "label_pt": "empresa",
        "label_en": "company",
        "actor_pt": "Seu empregador",
        "actor_en": "Your employer",
        "place_pt": "sistema de RH",
        "place_en": "HR system",
    },
    {
        "id": "support",
        "label_pt": "atendimento ao cliente",
        "label_en": "customer support",
        "actor_pt": "O call center",
        "actor_en": "The call center",
        "place_pt": "gravação de chamadas",
        "place_en": "call recording",
    },
    {
        "id": "remote",
        "label_pt": "trabalho remoto",
        "label_en": "remote work",
        "actor_pt": "Sua equipe remota",
        "actor_en": "Your remote team",
        "place_pt": "videoconferência corporativa",
        "place_en": "corporate video meeting",
    },
    {
        "id": "ai",
        "label_pt": "inteligência artificial",
        "label_en": "artificial intelligence",
        "actor_pt": "Um chatbot com IA",
        "actor_en": "An AI chatbot",
        "place_pt": "atendimento automatizado",
        "place_en": "automated customer service",
    },
    {
        "id": "iot",
        "label_pt": "dispositivos conectados",
        "label_en": "connected devices",
        "actor_pt": "Uma câmera inteligente",
        "actor_en": "A smart camera",
        "place_pt": "casa conectada",
        "place_en": "smart home",
    },
]

# Curated knowledge node specs — shared across certifications when applicable.
# Each spec produces multiple scenario-based questions via expand_node().
NODE_SPECS: list[dict[str, Any]] = [
    {
        "id": "kn_cia_triad",
        "title": "CIA Triad and Security Pillars",
        "domain": "Information Security Foundations",
        "subdomain": "Security Concepts",
        "description": "Confidentiality, integrity, availability, authenticity, and non-repudiation as foundational security properties.",
        "learning_objective": "Identify which security property is primarily at risk in a given scenario and select appropriate controls.",
        "concepts": ["Confidentiality", "Integrity", "Availability", "Authenticity", "Non-repudiation"],
        "best_practices": ["Apply defense in depth", "Map controls to the property at risk", "Avoid treating all incidents as confidentiality-only"],
        "common_errors": ["Confusing integrity with confidentiality", "Ignoring availability in cloud outages"],
        "risks": ["Unauthorized disclosure", "Unauthorized modification", "Service disruption"],
        "controls": ["Encryption", "Hashing and digital signatures", "Redundancy and backups", "MFA"],
        "official_refs": ["ISC2 CISSP Exam Outline April 2024, Domain 1.2", "ISO/IEC 27001 Annex A"],
        "laws": [],
        "frameworks": ["ISO/IEC 27001", "NIST CSF"],
        "nist": ["PR.DS-P"],
        "certs": ["ISC2-CISSP", "EXIN-ISFS", "ISACA-CISM"],
        "templates": [
            {
                "property": "Confidentiality",
                "stem_en": "{actor} shares your personal data in the {place} without asking. Which security property is MOST directly violated?",
                "stem_pt": "{actor} compartilha seus dados pessoais no {place} sem perguntar. Qual propriedade de segurança é MAIS diretamente violada?",
                "correct_en": "Confidentiality — unauthorized disclosure of information",
                "correct_pt": "Confidencialidade — divulgação não autorizada de informação",
                "distractors_en": ["Integrity — data was modified", "Availability — system is offline", "Non-repudiation — no audit trail"],
                "distractors_pt": ["Integridade — dado foi modificado", "Disponibilidade — sistema está offline", "Não repúdio — não há trilha de auditoria"],
                "expl_en": "Unauthorized sharing exposes information to parties who should not access it — a confidentiality failure.",
                "expl_pt": "Compartilhamento não autorizado expõe informação a partes que não deveriam acessá-la — falha de confidencialidade.",
            },
            {
                "property": "Integrity",
                "stem_en": "Someone alters your order total in the {place} before payment clears. Which property is compromised?",
                "stem_pt": "Alguém altera o valor do seu pedido no {place} antes do pagamento. Qual propriedade é comprometida?",
                "correct_en": "Integrity — unauthorized modification of data",
                "correct_pt": "Integridade — modificação não autorizada de dados",
                "distractors_en": ["Confidentiality only", "Availability during peak hours", "Authenticity of the brand logo"],
                "distractors_pt": ["Apenas confidencialidade", "Disponibilidade em horário de pico", "Autenticidade do logotipo"],
                "expl_en": "Changing data values without authorization is an integrity violation regardless of intent.",
                "expl_pt": "Alterar valores de dados sem autorização é violação de integridade independentemente da intenção.",
            },
            {
                "property": "Availability",
                "stem_en": "During a sale, the {place} is unreachable for hours and customers cannot complete purchases. Which CIA element failed?",
                "stem_pt": "Durante uma promoção, o {place} fica indisponível por horas e clientes não conseguem concluir compras. Qual elemento CIA falhou?",
                "correct_en": "Availability",
                "correct_pt": "Disponibilidade",
                "distractors_en": ["Confidentiality of payment tokens", "Integrity of product descriptions", "Non-repudiation of receipts"],
                "distractors_pt": ["Confidencialidade de tokens de pagamento", "Integridade de descrições de produto", "Não repúdio de recibos"],
                "expl_en": "When systems or data are inaccessible when needed, availability is the primary concern.",
                "expl_pt": "Quando sistemas ou dados ficam inacessíveis quando necessários, a disponibilidade é a preocupação principal.",
            },
        ],
    },
    {
        "id": "kn_gdpr_lawful_basis",
        "title": "GDPR Lawful Basis for Processing",
        "domain": "Privacy Law & Regulatory Frameworks",
        "subdomain": "Lawful Processing Criteria",
        "description": "Article 6 GDPR sets six lawful bases; consent under Articles 6(1)(a) and 7 must meet specific conditions.",
        "learning_objective": "Select the most appropriate lawful basis and recognize invalid consent in practical scenarios.",
        "concepts": ["Lawful basis", "Consent", "Legitimate interests", "Contract", "Legal obligation"],
        "best_practices": ["Document the chosen basis before processing", "Use consent only when no other basis applies", "Keep consent records granular and withdrawable"],
        "common_errors": ["Using consent as default", "Bundled consent in terms of service", "Confusing legitimate interests with business convenience"],
        "risks": ["Unlawful processing", "Regulatory fines", "Invalid consent chains"],
        "controls": ["ROPA", "Consent management platform", "LIA for legitimate interests"],
        "official_refs": ["GDPR Articles 6–7", "IAPP CIPP/E BoK Domain II", "EDPB Guidelines on consent"],
        "laws": ["GDPR Art. 6", "GDPR Art. 7"],
        "frameworks": ["NIST Privacy Framework Govern-P"],
        "nist": ["GV.PO-P", "CT.DM-P"],
        "certs": ["IAPP-CIPP-E", "EXIN-PDPF", "EXIN-PDPP"],
        "templates": [
            {
                "stem_en": "{actor} requires acceptance of marketing emails to create an account in the {place}. Under GDPR, this is MOST likely:",
                "stem_pt": "{actor} exige aceite de e-mails de marketing para criar conta no {place}. Pelo GDPR, isso é MAIS provavelmente:",
                "correct_en": "Invalid consent — consent must be freely given and not bundled with service access",
                "correct_pt": "Consentimento inválido — deve ser livre e não pode ser exigido para acessar o serviço",
                "distractors_en": ["Valid consent because checkbox exists", "Legitimate interest without assessment", "Legal obligation for all online accounts"],
                "distractors_pt": ["Consentimento válido porque há checkbox", "Interesse legítimo sem avaliação", "Obrigação legal para toda conta online"],
                "expl_en": "GDPR consent must be freely given; tying marketing to account creation is a classic invalid consent pattern.",
                "expl_pt": "Consentimento GDPR deve ser livre; vincular marketing à criação de conta é padrão clássico de consentimento inválido.",
            },
        ],
    },
    {
        "id": "kn_gdpr_dsr",
        "title": "GDPR Data Subject Rights",
        "domain": "Privacy Law & Regulatory Frameworks",
        "subdomain": "Data Subjects' Rights",
        "description": "Rights including access, rectification, erasure, restriction, portability, and objection under Chapter III GDPR.",
        "learning_objective": "Match a data subject request to the correct GDPR right and organizational response.",
        "concepts": ["Right of access", "Erasure", "Portability", "Objection", "Restriction"],
        "best_practices": ["Verify identity of requester", "Respond within one month", "Log requests in a dedicated process"],
        "common_errors": ["Treating erasure as absolute", "Ignoring portability format requirements"],
        "risks": ["Complaints to supervisory authority", "Reputational harm"],
        "controls": ["DSAR workflow", "Identity verification", "Legal review for exemptions"],
        "official_refs": ["GDPR Articles 12–23", "IAPP CIPP/E BoK"],
        "laws": ["GDPR Chapter III"],
        "frameworks": ["NIST Privacy Framework Communicate-P"],
        "nist": ["CM.AW-P", "CT.DM-P"],
        "certs": ["IAPP-CIPP-E", "EXIN-PDPP"],
        "templates": [
            {
                "stem_en": "A user asks {actor} for a copy of all personal data held about them in the {place}. Which right is being exercised?",
                "stem_pt": "Um usuário pede a {actor} cópia de todos os dados pessoais mantidos sobre ele no {place}. Qual direito está sendo exercido?",
                "correct_en": "Right of access (Article 15 GDPR)",
                "correct_pt": "Direito de acesso (Art. 15 GDPR)",
                "distractors_en": ["Right to erasure only", "Right to data portability without export", "Right to object to all processing automatically"],
                "distractors_pt": ["Apenas direito ao apagamento", "Portabilidade sem exportação", "Oposição automática a todo tratamento"],
                "expl_en": "A request for a copy of personal data is an access request under Article 15.",
                "expl_pt": "Pedido de cópia dos dados pessoais é solicitação de acesso pelo Art. 15.",
            },
        ],
    },
    {
        "id": "kn_gdpr_dpia",
        "title": "Data Protection Impact Assessment (DPIA)",
        "domain": "Privacy Program Management",
        "subdomain": "DPIA / Risk Assessment",
        "description": "GDPR Article 35 requires DPIA when processing is likely to result in high risk; consult DPO and supervisory authority when residual risk remains.",
        "learning_objective": "Determine when a DPIA is required and describe its role in risk mitigation.",
        "concepts": ["DPIA triggers", "High risk", "Consultation", "Mitigation measures"],
        "best_practices": ["Start DPIA early in design", "Involve DPO", "Revisit when processing changes"],
        "common_errors": ["Treating DPIA as one-time paperwork", "Skipping DPIA for systematic monitoring"],
        "risks": ["High-risk processing without mitigation", "Regulatory intervention"],
        "controls": ["DPIA template", "Risk register", "Privacy by design"],
        "official_refs": ["GDPR Article 35", "WP248 rev.01 guidelines", "EXIN PDPP syllabus 27.5%"],
        "laws": ["GDPR Art. 35"],
        "frameworks": ["NIST Privacy Framework ID.RA-P"],
        "nist": ["ID.RA-P", "GV.RM-P"],
        "certs": ["EXIN-PDPP", "IAPP-CIPP-E", "IAPP-CIPM"],
        "templates": [
            {
                "stem_en": "{actor} plans large-scale monitoring of employee activity via the {place}. What should be done FIRST under GDPR?",
                "stem_pt": "{actor} planeja monitoramento em larga escala de atividade de funcionários via {place}. O que deve ser feito PRIMEIRO pelo GDPR?",
                "correct_en": "Conduct a DPIA before deployment because systematic monitoring may create high risk",
                "correct_pt": "Realizar AIPD/DPIA antes da implantação porque monitoramento sistemático pode gerar alto risco",
                "distractors_en": ["Send marketing opt-in only", "Publish privacy policy after launch", "Rely on employee contract silence"],
                "distractors_pt": ["Enviar apenas opt-in de marketing", "Publicar política após lançamento", "Confiar no silêncio do contrato"],
                "expl_en": "Article 35 lists systematic monitoring of publicly accessible areas and similar cases as DPIA triggers.",
                "expl_pt": "Art. 35 lista monitoramento sistemático e casos similares como gatilhos de AIPD.",
            },
        ],
    },
    {
        "id": "kn_dpo_role",
        "title": "Role of the Data Protection Officer (DPO)",
        "domain": "Privacy Program Management",
        "subdomain": "DPO Role and Independence",
        "description": "GDPR Articles 37–39 define designation criteria, tasks, and independence of the DPO.",
        "learning_objective": "Recognize mandatory DPO appointment scenarios and appropriate DPO positioning.",
        "concepts": ["Mandatory designation", "Independence", "Tasks", "Contact point"],
        "best_practices": ["Ensure DPO reports to highest management", "Avoid conflicts of interest", "Provide resources"],
        "common_errors": ["DPO as IT administrator only", "DPO approving own processing"],
        "risks": ["Conflict of interest", "Ineffective oversight"],
        "controls": ["DPO charter", "Independence safeguards"],
        "official_refs": ["GDPR Articles 37–39", "EXIN PDPP syllabus 17.5%"],
        "laws": ["GDPR Art. 37-39"],
        "frameworks": ["NIST Privacy Framework Govern-P"],
        "nist": ["GV.PO-P", "GV.MT-P"],
        "certs": ["EXIN-PDPP", "EXIN-CDPO", "IAPP-CIPM"],
        "templates": [
            {
                "stem_en": "A public authority appoints its IT director as DPO while they also approve all system changes in the {place}. This is MOST problematic because:",
                "stem_pt": "Um órgão público nomeia o diretor de TI como DPO enquanto também aprova mudanças no {place}. Isso é MAIS problemático porque:",
                "correct_en": "It creates a conflict of interest undermining DPO independence",
                "correct_pt": "Cria conflito de interesses comprometendo a independência do DPO",
                "distractors_en": ["DPO must be external consultant only", "Public authorities never need a DPO", "IT directors cannot know privacy law"],
                "distractors_pt": ["DPO deve ser sempre consultor externo", "Autoridades públicas nunca precisam de DPO", "Diretor de TI não pode conhecer privacidade"],
                "expl_en": "Article 38 requires the DPO to perform tasks independently without conflict of interest.",
                "expl_pt": "Art. 38 exige que o DPO exerça funções com independência e sem conflito de interesses.",
            },
        ],
    },
    {
        "id": "kn_breach_notification",
        "title": "Personal Data Breach Notification",
        "domain": "Incident Response, BC & DR",
        "subdomain": "Breach Notification",
        "description": "GDPR Articles 33–34 require notification to supervisory authority within 72 hours and communication to data subjects when high risk.",
        "learning_objective": "Apply breach assessment, notification timelines, and communication criteria.",
        "concepts": ["72-hour notification", "High risk to rights", "Document all breaches"],
        "best_practices": ["Run breach response playbooks", "Document even non-notifiable incidents", "Coordinate with legal and communications"],
        "common_errors": ["Waiting for full forensic report before notifying", "Notifying subjects when risk is low"],
        "risks": ["Regulatory penalties", "Secondary harm to individuals"],
        "controls": ["Incident response plan", "Breach register"],
        "official_refs": ["GDPR Articles 33–34", "EXIN PDPP syllabus 12.5%"],
        "laws": ["GDPR Art. 33-34"],
        "frameworks": ["NIST Privacy Framework Protect-P"],
        "nist": ["PR.DS-P", "GV.MT-P"],
        "certs": ["EXIN-PDPP", "IAPP-CIPP-E", "ISACA-CISM"],
        "templates": [
            {
                "stem_en": "{actor} discovers unauthorized access to customer records in the {place}. Under GDPR, what is the FIRST regulatory obligation if personal data was compromised?",
                "stem_pt": "{actor} descobre acesso não autorizado a registros de clientes no {place}. Pelo GDPR, qual é a PRIMEIRA obrigação regulatória se dados pessoais foram comprometidos?",
                "correct_en": "Assess the breach and notify the supervisory authority within 72 hours if required",
                "correct_pt": "Avaliar o incidente e notificar a autoridade de supervisão em 72 horas se aplicável",
                "distractors_en": ["Notify every customer immediately regardless of risk", "Wait 30 days for internal audit", "Delete logs to reduce exposure"],
                "distractors_pt": ["Notificar todos os clientes imediatamente independente do risco", "Esperar 30 dias por auditoria", "Apagar logs para reduzir exposição"],
                "expl_en": "Article 33 requires notification to the authority without undue delay and within 72 hours when feasible.",
                "expl_pt": "Art. 33 exige notificação à autoridade sem demora injustificada e em até 72 horas quando possível.",
            },
        ],
    },
    {
        "id": "kn_risk_management",
        "title": "Information Security Risk Management",
        "domain": "Security Governance, Risk & Compliance",
        "subdomain": "Risk Assessment and Treatment",
        "description": "Identify, analyze, evaluate, and treat information security risks using consistent methodology aligned to organizational context.",
        "learning_objective": "Select appropriate risk treatment options and align risk decisions with governance.",
        "concepts": ["Risk identification", "Risk analysis", "Risk treatment", "Risk acceptance"],
        "best_practices": ["Use a defined risk methodology", "Document risk owners", "Review risks periodically"],
        "common_errors": ["Risk transfer without vendor assessment", "Accepting all risks without approval"],
        "risks": ["Unmitigated threats", "Compliance gaps"],
        "controls": ["Risk register", "Risk committee", "KRIs"],
        "official_refs": ["ISACA CISM Domain 2", "ISC2 CISSP Domain 1.9", "ISO 27005"],
        "laws": [],
        "frameworks": ["ISO 31000", "NIST RMF"],
        "nist": ["ID.RA-P", "GV.RM-P"],
        "certs": ["ISACA-CISM", "ISC2-CISSP"],
        "templates": [
            {
                "stem_en": "Leadership accepts a known vulnerability in the {place} because fixing it would delay a product launch. This decision should be documented as:",
                "stem_pt": "A diretoria aceita vulnerabilidade conhecida no {place} porque corrigi-la atrasaria lançamento. Essa decisão deve ser documentada como:",
                "correct_en": "Risk acceptance with explicit approval and residual risk statement",
                "correct_pt": "Aceitação de risco com aprovação explícita e registro do risco residual",
                "distractors_en": ["Risk avoidance by ignoring the issue", "Automatic risk transfer to users", "Risk elimination without evidence"],
                "distractors_pt": ["Evitação ignorando o problema", "Transferência automática ao usuário", "Eliminação sem evidência"],
                "expl_en": "Accepted risks require documented approval from appropriate authority — core CISM/CISSP governance practice.",
                "expl_pt": "Riscos aceitos exigem aprovação documentada da autoridade competente — prática central CISM/CISSP.",
            },
        ],
    },
    {
        "id": "kn_security_governance",
        "title": "Information Security Governance",
        "domain": "Security Governance, Risk & Compliance",
        "subdomain": "Security Governance Principles",
        "description": "Align security with business objectives, define roles, and establish oversight structures.",
        "learning_objective": "Apply governance principles to security program decisions.",
        "concepts": ["Governance", "Strategy alignment", "Roles and responsibilities", "Metrics"],
        "best_practices": ["Board-level reporting", "Clear RACI for security", "Policy hierarchy"],
        "common_errors": ["Security operating in isolation from business", "Policies without enforcement"],
        "risks": ["Misaligned investments", "Accountability gaps"],
        "controls": ["Security steering committee", "Policy framework"],
        "official_refs": ["ISACA CISM Domain 1 17%", "ISC2 CISSP Domain 1.3"],
        "laws": [],
        "frameworks": ["COBIT", "ISO 27014"],
        "nist": ["GV.PO-P", "GV.MT-P"],
        "certs": ["ISACA-CISM", "ISC2-CISSP", "IAPP-CIPM"],
        "templates": [
            {
                "stem_en": "The board asks how security investments in the {place} support business goals. Which governance activity BEST answers this?",
                "stem_pt": "O conselho pergunta como investimentos de segurança no {place} suportam metas de negócio. Qual atividade de governança MELHOR responde?",
                "correct_en": "Map security strategy and metrics to business objectives and risk appetite",
                "correct_pt": "Mapear estratégia e métricas de segurança aos objetivos de negócio e apetite a risco",
                "distractors_en": ["List all firewall rules", "Report only number of patches applied", "Defer to vendor marketing materials"],
                "distractors_pt": ["Listar todas as regras de firewall", "Reportar apenas número de patches", "Encaminhar material de marketing do fornecedor"],
                "expl_en": "Governance requires demonstrating alignment between security function and organizational strategy.",
                "expl_pt": "Governança exige demonstrar alinhamento entre função de segurança e estratégia organizacional.",
            },
        ],
    },
    {
        "id": "kn_iam",
        "title": "Identity and Access Management",
        "domain": "Security Architecture, Engineering & Operations",
        "subdomain": "Identity and Access Management (IAM)",
        "description": "Manage identities, authentication, authorization, and access lifecycle including privileged access.",
        "learning_objective": "Recommend IAM controls for least privilege and strong authentication.",
        "concepts": ["Authentication", "Authorization", "Least privilege", "MFA", "PAM"],
        "best_practices": ["Enforce MFA for sensitive systems", "Review access periodically", "Use role-based access"],
        "common_errors": ["Shared admin accounts", "Permanent excessive privileges"],
        "risks": ["Account takeover", "Insider abuse"],
        "controls": ["MFA", "IAM/IAG tools", "PAM"],
        "official_refs": ["ISC2 CISSP Domain 5 13%", "IAPP CIPT BoK"],
        "laws": [],
        "frameworks": ["NIST Privacy Framework PR.AC-P"],
        "nist": ["PR.AC-P"],
        "certs": ["ISC2-CISSP", "IAPP-CIPT"],
        "templates": [
            {
                "stem_en": "Employees reuse one shared password for the {place}. Which control MOST directly reduces this risk?",
                "stem_pt": "Funcionários reutilizam uma senha compartilhada no {place}. Qual controle reduz MAIS diretamente esse risco?",
                "correct_en": "Individual accounts with MFA and role-based access control",
                "correct_pt": "Contas individuais com MFA e controle de acesso baseado em papéis",
                "distractors_en": ["Longer shared password changed annually", "Security awareness poster only", "Disable logging to reduce exposure"],
                "distractors_pt": ["Senha compartilhada mais longa trocada anualmente", "Apenas cartaz de conscientização", "Desativar logs para reduzir exposição"],
                "expl_en": "Individual accountability and MFA address shared-credential and weak authentication risks.",
                "expl_pt": "Responsabilização individual e MFA abordam riscos de credenciais compartilhadas e autenticação fraca.",
            },
        ],
    },
    {
        "id": "kn_ccpa_rights",
        "title": "California Consumer Privacy Act (CCPA/CPRA) Consumer Rights",
        "domain": "Privacy Law & Regulatory Frameworks",
        "subdomain": "State Privacy Laws",
        "description": "California residents have rights to know, delete, correct, opt-out of sale/sharing, and limit use of sensitive personal information under CCPA as amended by CPRA.",
        "learning_objective": "Identify applicable consumer rights and business obligations in US state privacy scenarios.",
        "concepts": ["Right to know", "Right to delete", "Opt-out of sale/sharing", "Sensitive PI limits"],
        "best_practices": ["Maintain privacy notice", "Honor opt-out signals", "Verify consumer requests"],
        "common_errors": ["Treating CCPA as GDPR identical", "Ignoring employee B2B exemption changes"],
        "risks": ["AG enforcement", "Private right of action for breaches"],
        "controls": ["Consumer request portal", "Do Not Sell/Share link"],
        "official_refs": ["California Civil Code §1798.100 et seq.", "IAPP CIPP/US BoK"],
        "laws": ["CCPA", "CPRA"],
        "frameworks": ["NIST Privacy Framework Communicate-P"],
        "nist": ["CM.AW-P", "CT.DM-P"],
        "certs": ["IAPP-CIPP-US"],
        "templates": [
            {
                "stem_en": "A California customer asks {actor} what personal information was collected via the {place} in the past 12 months. Which right applies?",
                "stem_pt": "Um cliente californiano pede a {actor} quais dados pessoais foram coletados via {place} nos últimos 12 meses. Qual direito se aplica?",
                "correct_en": "Right to know / right to access under CCPA",
                "correct_pt": "Direito de saber/acessar sob o CCPA",
                "distractors_en": ["GDPR Article 17 erasure only", "HIPAA portability", "PCI DSS chargeback right"],
                "distractors_pt": ["Apenas apagamento GDPR Art. 17", "Portabilidade HIPAA", "Direito de chargeback PCI DSS"],
                "expl_en": "CCPA grants consumers the right to know what personal information a business collects about them.",
                "expl_pt": "CCPA garante ao consumidor o direito de saber quais dados pessoais a empresa coleta.",
            },
        ],
    },
    {
        "id": "kn_pipeda",
        "title": "PIPEDA Fair Information Principles",
        "domain": "Privacy Law & Regulatory Frameworks",
        "subdomain": "Canadian Privacy Fundamentals",
        "description": "PIPEDA Schedule 1 sets ten fair information principles governing private-sector processing in Canada.",
        "learning_objective": "Apply PIPEDA principles to Canadian privacy scenarios.",
        "concepts": ["Accountability", "Consent", "Limiting collection", "Safeguards", "Openness"],
        "best_practices": ["Designate privacy officer", "Limit collection to identified purposes", "Use meaningful consent"],
        "common_errors": ["Assuming PIPEDA identical to GDPR", "Ignoring provincial equivalents"],
        "risks": ["OPC findings", "Reputational damage"],
        "controls": ["Privacy management program", "Breach reporting to OPC when required"],
        "official_refs": ["PIPEDA Schedule 1", "IAPP CIPP/C BoK"],
        "laws": ["PIPEDA"],
        "frameworks": ["NIST Privacy Framework Govern-P"],
        "nist": ["GV.PO-P", "CT.DM-P"],
        "certs": ["IAPP-CIPP-C"],
        "templates": [
            {
                "stem_en": "{actor} collects more customer data than needed for checkout in the {place}. Which PIPEDA principle is violated?",
                "stem_pt": "{actor} coleta mais dados de clientes do que necessário no checkout do {place}. Qual princípio PIPEDA é violado?",
                "correct_en": "Limiting collection — collect only what is necessary for identified purposes",
                "correct_pt": "Limitação da coleta — coletar apenas o necessário para finalidades identificadas",
                "distractors_en": ["Accountability only", "Challenging compliance", "Openness about office address"],
                "distractors_pt": ["Apenas responsabilização", "Contestação de conformidade", "Transparência sobre endereço"],
                "expl_en": "PIPEDA Principle 4 — Limiting Collection restricts collection to what is necessary.",
                "expl_pt": "Princípio 4 PIPEDA — Limitação da Coleta restringe coleta ao necessário.",
            },
        ],
    },
    {
        "id": "kn_privacy_by_design",
        "title": "Privacy by Design and Default",
        "domain": "Privacy in Technology",
        "subdomain": "Privacy Engineering",
        "description": "GDPR Article 25 and privacy engineering practice require proactive privacy embedded in systems and default settings.",
        "learning_objective": "Recognize privacy-by-design choices in product and architecture decisions.",
        "concepts": ["Data minimization", "Privacy by default", "Pseudonymization", "PETs"],
        "best_practices": ["Minimize data at collection", "Strongest privacy by default", "Document design decisions"],
        "common_errors": ["Opt-in privacy as default", "Collecting all data 'just in case'"],
        "risks": ["Scope creep", "Regulatory non-compliance"],
        "controls": ["PbD checklist", "DPIA integration in SDLC"],
        "official_refs": ["GDPR Article 25", "IAPP CIPT BoK", "Ann Cavoukian PbD principles"],
        "laws": ["GDPR Art. 25"],
        "frameworks": ["NIST Privacy Framework Control-P"],
        "nist": ["CT.DM-P", "CT.PO-P"],
        "certs": ["IAPP-CIPT", "IAPP-CIPP-E", "EXIN-PDPP"],
        "templates": [
            {
                "stem_en": "A new feature in the {place} shares location with partners by default; users must dig into settings to disable it. This MOST violates:",
                "stem_pt": "Um novo recurso no {place} compartilha localização com parceiros por padrão; usuários precisam cavar configurações para desativar. Isso viola MAIS:",
                "correct_en": "Privacy by default under GDPR Article 25",
                "correct_pt": "Privacidade por padrão (privacy by default) pelo Art. 25 GDPR",
                "distractors_en": ["Availability requirements", "PCI DSS tokenization", "ISO 9001 quality"],
                "distractors_pt": ["Requisitos de disponibilidade", "Tokenização PCI DSS", "Qualidade ISO 9001"],
                "expl_en": "Article 25 requires only necessary data processed by default with privacy-protective settings.",
                "expl_pt": "Art. 25 exige processar apenas dados necessários por padrão com configurações protetivas.",
            },
        ],
    },
    {
        "id": "kn_ai_governance_risk",
        "title": "AI Governance and Risk Assessment",
        "domain": "Artificial Intelligence Governance",
        "subdomain": "AI Risk Management",
        "description": "Responsible AI requires governance over data, models, transparency, human oversight, and regulatory alignment (EU AI Act, NIST AI RMF where applicable).",
        "learning_objective": "Identify governance controls for high-risk AI use cases.",
        "concepts": ["Human oversight", "Transparency", "Bias and fairness", "Documentation", "Risk classification"],
        "best_practices": ["Maintain model cards and data sheets", "Conduct AI impact assessments", "Define human-in-the-loop for critical decisions"],
        "common_errors": ["Deploying black-box models without review", "Ignoring training data provenance"],
        "risks": ["Discrimination", "Regulatory non-compliance", "Safety incidents"],
        "controls": ["AI governance committee", "Impact assessment", "Monitoring and drift detection"],
        "official_refs": ["IAPP AIGP BoK", "EU AI Act (verify classification)", "NIST AI RMF 1.0"],
        "laws": ["EU AI Act"],
        "frameworks": ["NIST AI RMF", "NIST Privacy Framework ID.RA-P"],
        "nist": ["ID.RA-P", "GV.RM-P", "GV.MT-P"],
        "certs": ["IAPP-AIGP"],
        "uncertainty": "Verify AIGP BoK domain mapping and EU AI Act risk tiers against latest official texts.",
        "templates": [
            {
                "stem_en": "{actor} deploys an AI model in the {place} to deny services with no human review or documentation. Which governance gap is MOST critical?",
                "stem_pt": "{actor} implanta modelo de IA no {place} para negar serviços sem revisão humana ou documentação. Qual lacuna de governança é MAIS crítica?",
                "correct_en": "Missing human oversight and accountability for automated decisions affecting individuals",
                "correct_pt": "Ausência de supervisão humana e responsabilização por decisões automatizadas que afetam pessoas",
                "distractors_en": ["Logo color non-compliance", "Need more training data only", "GDPR erasure not applicable to AI"],
                "distractors_pt": ["Cor de logo não conforme", "Precisa apenas de mais dados", "Apagamento GDPR não se aplica a IA"],
                "expl_en": "AI governance requires accountability, documentation, and appropriate human oversight for impactful decisions.",
                "expl_pt": "Governança de IA exige responsabilização, documentação e supervisão humana adequada para decisões impactantes.",
            },
        ],
    },
    {
        "id": "kn_nist_pf_identify",
        "title": "NIST Privacy Framework — Identify-P",
        "domain": "Frameworks (NIST PF)",
        "subdomain": "Inventory and Mapping (ID.IM-P)",
        "description": "Develop organizational understanding of data processing to manage privacy risk — inventory, mapping, and business context.",
        "learning_objective": "Relate data inventory activities to NIST Privacy Framework Identify-P outcomes.",
        "concepts": ["Data inventory", "Data mapping", "Business environment", "Processing ecosystem"],
        "best_practices": ["Maintain ROPA/data map", "Identify data flows to third parties", "Link inventory to risk assessment"],
        "common_errors": ["Inventory without purpose linkage", "Ignoring subprocessors"],
        "risks": ["Unknown data flows", "Third-party surprises"],
        "controls": ["ROPA", "Data flow diagrams", "Vendor inventory"],
        "official_refs": ["NIST Privacy Framework v1.0 Core ID-P", "NIST.CSWP.01162020"],
        "laws": [],
        "frameworks": ["NIST Privacy Framework"],
        "nist": ["ID.IM-P", "ID.BE-P", "ID.DE-P"],
        "certs": ["IAPP-CIPM", "IAPP-CIPP-E", "EXIN-PDPP"],
        "templates": [
            {
                "stem_en": "Before launching the {place}, {actor} cannot list which personal data fields are collected or shared with vendors. Which NIST PF Function is immature?",
                "stem_pt": "Antes de lançar o {place}, {actor} não consegue listar quais campos de dados pessoais são coletados ou compartilhados com fornecedores. Qual Função NIST PF está imatura?",
                "correct_en": "Identify-P — inventory and mapping of data processing",
                "correct_pt": "Identify-P — inventário e mapeamento do tratamento de dados",
                "distractors_en": ["Protect-P only — add encryption later", "Communicate-P — publish blog post", "Govern-P — rename privacy policy"],
            "distractors_pt": ["Apenas Protect-P — criptografar depois", "Communicate-P — publicar blog", "Govern-P — renomear política"],
                "expl_en": "Identify-P requires understanding what data is processed, where, and with whom before effective controls.",
                "expl_pt": "Identify-P exige entender quais dados são tratados, onde e com quem antes de controles efetivos.",
            },
        ],
    },
]

# Domain-to-node mapping for auto-assignment when expanding certification coverage
DOMAIN_NODE_MAP: dict[str, list[str]] = {
    "Security and Risk Management": ["kn_cia_triad", "kn_risk_management", "kn_security_governance"],
    "Asset Security": ["kn_cia_triad", "kn_risk_management"],
    "Security Architecture and Engineering": ["kn_iam", "kn_privacy_by_design"],
    "Communication and Network Security": ["kn_iam", "kn_cia_triad"],
    "Identity and Access Management (IAM)": ["kn_iam"],
    "Security Assessment and Testing": ["kn_risk_management"],
    "Security Operations": ["kn_breach_notification", "kn_iam"],
    "Software Development Security": ["kn_privacy_by_design"],
    "Information Security Governance": ["kn_security_governance"],
    "Information Security Risk Management": ["kn_risk_management"],
    "Information Security Program": ["kn_security_governance", "kn_dpo_role"],
    "Incident Management": ["kn_breach_notification"],
    "Data protection policies": ["kn_security_governance", "kn_dpo_role"],
    "Privacy information management system (PIMS)": ["kn_nist_pf_identify", "kn_dpo_role"],
    "Roles of the controller, processor, and DPO": ["kn_dpo_role"],
    "Data protection impact assessment (DPIA)": ["kn_gdpr_dpia"],
    "Data breaches, notification, and incident response": ["kn_breach_notification"],
    "Introduction to European Data Protection": ["kn_gdpr_lawful_basis"],
    "European Data Protection Law and Regulation": ["kn_gdpr_lawful_basis", "kn_gdpr_dsr"],
    "European Data Processing": ["kn_privacy_by_design", "kn_gdpr_lawful_basis"],
    "European Data Protection: Scope & Accountability": ["kn_dpo_role", "kn_gdpr_dpia"],
    "Compliance with European Data Protection Law and Regulation": ["kn_gdpr_dsr", "kn_breach_notification"],
    "Introduction to the U.S. Privacy Environment": ["kn_ccpa_rights"],
    "Limits on Private-sector Collection and Use of Data": ["kn_ccpa_rights"],
    "State Privacy Laws": ["kn_ccpa_rights"],
    "Canadian Privacy Fundamentals and PIPEDA": ["kn_pipeda"],
    "Privacy Program Governance": ["kn_security_governance", "kn_nist_pf_identify"],
    "Fundamentals of Privacy in Technology": ["kn_privacy_by_design", "kn_iam"],
    "Privacy in Emerging Technologies": ["kn_ai_governance_risk", "kn_privacy_by_design"],
    "AI Governance Foundations and Principles": ["kn_ai_governance_risk"],
    "AI Risk Management and Impact Assessment": ["kn_ai_governance_risk", "kn_gdpr_dpia"],
}


def _stable_id(prefix: str, *parts: str) -> str:
    h = hashlib.sha1("|".join(parts).encode()).hexdigest()[:10]
    return f"{prefix}_{h}"


def _pick_contexts(n: int, seed: str) -> list[dict]:
    rng = random.Random(seed)
    pool = SCENARIO_CONTEXTS.copy()
    rng.shuffle(pool)
    out = []
    while len(out) < n:
        out.extend(pool)
    return out[:n]


def expand_node(spec: dict, questions_per_node: int = 4) -> dict[str, Any]:
    """Expand a node spec into full node with questions and flashcards."""
    templates = spec.get("templates") or []
    contexts = _pick_contexts(max(questions_per_node, len(templates) * 2), spec["id"])
    questions = []
    used_stems = set()

    def add_question(tpl: dict, ctx: dict, variant: int):
        actor_en = ctx["actor_en"]
        actor_pt = ctx["actor_pt"]
        place_en = ctx["place_en"]
        place_pt = ctx["place_pt"]
        stem_en = tpl["stem_en"].format(actor=actor_en, place=place_en)
        stem_pt = tpl["stem_pt"].format(actor=actor_pt, place=place_pt)
        if variant:
            stem_en += f" (Scenario {variant + 1})"
            stem_pt += f" (Cenário {variant + 1})"
        key = stem_en[:80]
        if key in used_stems:
            return
        used_stems.add(key)
        opts_en = [tpl["correct_en"]] + tpl["distractors_en"][:3]
        opts_pt = [tpl["correct_pt"]] + tpl["distractors_pt"][:3]
        pairs = list(zip(opts_en, opts_pt))
        random.Random(spec["id"] + str(variant)).shuffle(pairs)
        correct_idx = next(i for i, p in enumerate(pairs) if p[0] == tpl["correct_en"])
        qid = _stable_id("q", spec["id"], stem_en, str(variant))
        wrong_expl_en = "; ".join(
            f"({chr(65+i)}) {pairs[i][0]} — incorrect because it does not address the core concept."
            for i in range(4) if i != correct_idx
        )
        wrong_expl_pt = "; ".join(
            f"({chr(65+i)}) {pairs[i][1]} — incorreta porque não aborda o conceito central."
            for i in range(4) if i != correct_idx
        )
        questions.append({
            "id": qid,
            "type": "single",
            "stemEn": stem_en,
            "stemPt": stem_pt,
            "optionsEn": [{"text": t, "correct": i == correct_idx} for i, (t, _) in enumerate(pairs)],
            "optionsPt": [{"text": t, "correct": i == correct_idx} for i, (_, t) in enumerate(pairs)],
            "explanationEn": tpl["expl_en"] + " Wrong options: " + wrong_expl_en,
            "explanationPt": tpl["expl_pt"] + " Alternativas incorretas: " + wrong_expl_pt,
            "level": "medio",
            "estimatedMinutes": 2,
            "scenarioContext": ctx["id"],
            "tags": [ctx["label_en"], spec["domain"], spec["subdomain"]],
        })

    ctx_i = 0
    variant = 0
    while len(questions) < questions_per_node and variant < questions_per_node * 4:
        for tpl in templates:
            if len(questions) >= questions_per_node:
                break
            ctx = contexts[ctx_i % len(contexts)]
            add_question(tpl, ctx, variant)
            ctx_i += 1
            variant += 1
    if not questions and templates:
        add_question(templates[0], contexts[0], 0)

    # Flashcards — multiple formats
    flashcards = [
        {"format": "qa", "frontEn": f"What is the focus of: {spec['title']}?", "frontPt": f"Qual o foco de: {spec['title']}?", "backEn": spec["description"], "backPt": spec["description"]},
        {"format": "definition", "frontEn": spec["concepts"][0] if spec["concepts"] else spec["title"], "frontPt": spec["concepts"][0] if spec["concepts"] else spec["title"], "backEn": spec["description"], "backPt": spec["description"]},
        {"format": "boolean", "frontEn": f"True or False: {spec['common_errors'][0] if spec['common_errors'] else 'This node has no errors.'}", "frontPt": f"V ou F: {spec['common_errors'][0] if spec['common_errors'] else 'Este nó não tem erros.'}", "backEn": "False — see best practices in node content.", "backPt": "Falso — veja boas práticas no conteúdo do nó."},
        {"format": "scenario", "frontEn": f"In a {contexts[0]['label_en']} scenario, which control applies?", "frontPt": f"Em cenário de {contexts[0]['label_pt']}, qual controle se aplica?", "backEn": spec["controls"][0] if spec["controls"] else "Apply relevant control from node.", "backPt": spec["controls"][0] if spec["controls"] else "Aplicar controle relevante do nó."},
    ]
    if len(spec.get("concepts", [])) >= 2:
        flashcards.append({
            "format": "comparison",
            "frontEn": f"Compare {spec['concepts'][0]} vs {spec['concepts'][1]}",
            "frontPt": f"Compare {spec['concepts'][0]} vs {spec['concepts'][1]}",
            "backEn": f"{spec['concepts'][0]} and {spec['concepts'][1]} are distinct concepts in {spec['title']}.",
            "backPt": f"{spec['concepts'][0]} e {spec['concepts'][1]} são conceitos distintos em {spec['title']}.",
        })

    analogy = f"Think of {spec['title']} like organizing a {contexts[0]['label_en']} situation: you need clear rules before sharing information."
    story = f"In a {contexts[0]['label_en']} context involving {contexts[0]['place_en']}, professionals apply {spec['title']} to protect individuals and the organization."

    return {
        "id": spec["id"],
        "kind": "concept",
        "title": spec["title"],
        "domain": spec["domain"],
        "subdomain": spec["subdomain"],
        "description": spec["description"],
        "learningObjective": spec["learning_objective"],
        "concepts": spec["concepts"],
        "bestPractices": spec["best_practices"],
        "commonErrors": spec["common_errors"],
        "risks": spec["risks"],
        "controls": spec["controls"],
        "examples": spec.get("examples", []),
        "scenarios": [story],
        "analogies": [analogy],
        "officialReferences": spec["official_refs"],
        "relatedLaws": spec.get("laws", []),
        "relatedFrameworks": spec.get("frameworks", []),
        "nistMappings": spec.get("nist", []),
        "certificationMappings": spec.get("certs", []),
        "uncertainty": spec.get("uncertainty"),
        "questions": questions,
        "flashcards": flashcards,
    }


def build_all_nodes(questions_per_node: int = 4) -> dict[str, dict]:
    nodes = {}
    for spec in NODE_SPECS:
        nodes[spec["id"]] = expand_node(spec, questions_per_node)
    return nodes


def auto_node_for_domain(cert_code: str, domain_name: str, domain_id: str, idx: int) -> dict:
    """Generate a supplementary node when domain needs more coverage."""
    slug = _stable_id("kn", cert_code, domain_id, str(idx))
    ctx = SCENARIO_CONTEXTS[idx % len(SCENARIO_CONTEXTS)]
    title = f"{domain_name} — applied practice"
    spec = {
        "id": slug,
        "title": title,
        "domain": domain_name,
        "subdomain": f"{cert_code} {domain_id}",
        "description": f"Applied understanding of {domain_name} for {cert_code} preparation. Verify details against the official exam outline.",
        "learning_objective": f"Apply {domain_name} concepts in realistic scenarios.",
        "concepts": [domain_name],
        "best_practices": ["Consult official exam outline", "Document decisions", "Use defense in depth"],
        "common_errors": ["Memorizing without application", "Ignoring organizational context"],
        "risks": ["Misapplication of controls", "Compliance gaps"],
        "controls": ["Policy framework", "Training", "Monitoring"],
        "official_refs": [f"{cert_code} official exam outline — {domain_name}"],
        "laws": [],
        "frameworks": [],
        "nist": ["GV.PO-P"],
        "certs": [cert_code],
        "templates": [{
            "stem_en": f"When {ctx['actor_en']} reviews privacy/security for the {ctx['place_en']}, which action BEST reflects {domain_name}?",
            "stem_pt": f"Quando {ctx['actor_pt']} revisa privacidade/segurança do {ctx['place_pt']}, qual ação MELHOR reflete {domain_name}?",
            "correct_en": f"Apply {domain_name} principles with documented risk-based decisions",
            "correct_pt": f"Aplicar princípios de {domain_name} com decisões documentadas baseadas em risco",
            "distractors_en": ["Ignore policy until audit", "Collect all data preemptively", "Delegate without oversight"],
            "distractors_pt": ["Ignorar política até auditoria", "Coletar todos os dados preventivamente", "Delegar sem supervisão"],
            "expl_en": f"Certification exams test application of {domain_name}, not rote memorization.",
            "expl_pt": f"Provas certificadoras testam aplicação de {domain_name}, não memorização mecânica.",
        }],
    }
    return expand_node(spec, questions_per_node=3)


def build_certifications(taxonomy: dict, nodes: dict[str, dict], target_questions: int = 720) -> tuple[list[dict], dict]:
    """Build certification exams with domain-grouped questions from knowledge nodes."""
    certifications = []
    stats = {"totalQuestions": 0, "byCert": {}}

    for cert in taxonomy["certifications"]:
        if cert.get("compositeOf"):
            comp_domains = {}
            comp_qs = []
            for comp_code in cert["compositeOf"]:
                comp_cert = next((c for c in taxonomy["certifications"] if c["code"] == comp_code), None)
                if not comp_cert:
                    continue
                sub = build_single_cert(comp_cert, nodes, target_per_cert=35)
                for dname, qlist in sub["domains"].items():
                    comp_domains.setdefault(dname, []).extend(qlist)
                    comp_qs.extend(qlist)
            certifications.append({
                **{k: cert[k] for k in ["code", "org", "title", "trackId", "materia", "timeMinutes"]},
                "description": cert.get("note", cert["title"]),
                "region": "global",
                "domains": comp_domains,
                "nodeIds": list({q.get("nodeId") for qs in comp_domains.values() for q in qs if q.get("nodeId")}),
            })
            stats["byCert"][cert["code"]] = len(comp_qs)
            stats["totalQuestions"] += len(comp_qs)
            continue

        built = build_single_cert(cert, nodes, target_per_cert=max(30, target_questions // max(len(taxonomy["certifications"]), 1)))
        certifications.append(built["cert"])
        stats["byCert"][cert["code"]] = built["count"]
        stats["totalQuestions"] += built["count"]

    return certifications, stats


def build_single_cert(cert: dict, nodes: dict[str, dict], target_per_cert: int = 50) -> dict:
    domains_out: dict[str, list] = {}
    total = 0
    domain_list = cert.get("domains") or []
    if not domain_list:
        return {"cert": cert, "domains": {}, "count": 0}

    weights = [d.get("weight") for d in domain_list]
    has_weights = any(w is not None for w in weights)
    wsum = sum(w for w in weights if w) if has_weights else float(len(domain_list))
    per_domain_map = {}
    for d in domain_list:
        w = d.get("weight") if has_weights else 1.0
        if has_weights and not w:
            w = 1.0 / len(domain_list)
        per_domain_map[d["name"]] = max(3, int(round((w / wsum) * target_per_cert)))

    for i, dom in enumerate(domain_list):
        dname = dom["name"]
        need = per_domain_map[dname]
        node_ids = DOMAIN_NODE_MAP.get(dname, [])
        qlist = []
        for nid in node_ids:
            node = nodes.get(nid)
            if not node:
                continue
            for q in node["questions"]:
                if len(qlist) >= need:
                    break
                entry = dict(q)
                entry["nodeId"] = nid
                entry["knowledgeNode"] = nid
                entry["domain"] = dname
                entry["subdomain"] = node["subdomain"]
                entry["certifications"] = list(set(node["certificationMappings"] + [cert["code"]]))
                entry["officialReferences"] = node["officialReferences"]
                entry["nistMappings"] = node["nistMappings"]
                qlist.append(entry)
        auto_idx = 0
        while len(qlist) < need and auto_idx < 30:
            auto = auto_node_for_domain(cert["code"], dname, dom.get("id", "d"), auto_idx)
            nodes[auto["id"]] = auto
            added = 0
            for q in auto["questions"]:
                if len(qlist) >= need:
                    break
                entry = dict(q)
                entry["nodeId"] = auto["id"]
                entry["knowledgeNode"] = auto["id"]
                entry["domain"] = dname
                entry["subdomain"] = auto["subdomain"]
                entry["certifications"] = [cert["code"]]
                entry["officialReferences"] = auto["officialReferences"]
                entry["nistMappings"] = auto["nistMappings"]
                qlist.append(entry)
                added += 1
            if added == 0:
                break
            auto_idx += 1

        domains_out[dname] = qlist
        total += len(qlist)

    cert_out = {
        "code": cert["code"],
        "org": cert["org"],
        "title": cert["title"],
        "trackId": cert["trackId"],
        "materia": cert["materia"],
        "timeMinutes": cert.get("timeMinutes", 90),
        "description": cert.get("note") or f"Preparation track for {cert['title']} aligned to official exam outline.",
        "region": "global",
        "domains": domains_out,
        "nodeIds": list({q.get("nodeId") for qs in domains_out.values() for q in qs}),
    }
    if cert.get("uncertainty"):
        cert_out["uncertainty"] = cert["uncertainty"]
    return {"cert": cert_out, "domains": domains_out, "count": total}
