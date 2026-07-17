# Velora — Inventário DPO Global

> **Status:** implementado v2.0 · banco em `data/dpo-global-bank.js` · seeder `GlobalDPOSeeder`  
> **Spec:** [PRIVACY-KNOWLEDGE-OS.md](PRIVACY-KNOWLEDGE-OS.md) · **Taxonomia:** [`data/knowledge-taxonomy.json`](../data/knowledge-taxonomy.json)

## Resumo

| Métrica | Valor |
|---------|-------|
| Versão do banco | `2.0` |
| Total de questões | **301** |
| Certificações | **19** |
| Trilhas (tracks) | **5** |
| Stubs (em desenvolvimento) | **2** (IAPP-AIGP, IAPP-CIPP-A) |
| Idioma padrão | Bilingue EN/PT (`dual`) |

## Trilhas (tracks)

| Track ID | Região | Nome na UI | Certificações |
|----------|--------|------------|---------------|
| `global` | global | Global — DPO | 11 |
| `brazil` | brazil | Brasil — DPO | 2 |
| `europe` | europe | Europa — DPO | 4 |
| `americas` | americas | Américas — DPO | 1 |
| `asia` | asia | Ásia — DPO | 1 |

## Certificações por trilha

### Global (`trackId: global`)

| Código | Org | Matéria | Domínios (submatérias) | ~Questões |
|--------|-----|---------|------------------------|-----------|
| EXIN-ISFS | EXIN | ISFS | Conceitos de SI, ISO/IEC 27001 | ~18 |
| EXIN-PDPF | EXIN | PDPF | Fundamentos privacidade, GDPR/LGPD | ~18 |
| EXIN-PDPP | EXIN | PDPP | Prática DPO, DPIA, incidentes | ~18 |
| EXIN-CDPO | EXIN | CDPO | Programa integrado EXIN | ~16 |
| IAPP-CIPP-E | IAPP | CIPP/E | GDPR, direitos, transferências | ~15 |
| IAPP-CIPM | IAPP | CIPM | Programas, governança, métricas | ~15 |
| IAPP-CIPT | IAPP | CIPT | PETs, engenharia, segurança | ~15 |
| IAPP-AIGP | IAPP | AIGP | Governança IA | ~15 **stub** |
| PECB-CDPO | PECB | CDPO | PECB CDPO | ~15 |
| ISACA-CDPSE | ISACA | CDPSE | Engenharia privacidade | ~15 |
| ISO-27701 | ISO | 27701 | PIMS, controles privacidade | ~16 |

### Brasil (`trackId: brazil`)

| Código | Org | Matéria | Domínios | ~Questões |
|--------|-----|---------|----------|-----------|
| IAPP-CDPO-BR | IAPP | CDPO/BR | LGPD no dia a dia, ANPD, titulares | ~18 |
| EXIN-LGPD | EXIN | LGPD | LGPD, bases legais, DPO | ~16 |

### Europa (`trackId: europe`)

| Código | Org | Matéria | Domínios | ~Questões |
|--------|-----|---------|----------|-----------|
| IAPP-CDPO-FR | IAPP | CDPO/FR | GDPR França, CNIL | ~15 |
| CNIL-DPO | CNIL | DPO | Papel DPO, CNIL | ~15 |
| TUV-DPO-DE | TÜV | DPO/DE | GDPR Alemanha, BfDI | ~15 |
| UK-GDPR | ICO | UK GDPR | UK GDPR pós-Brexit | ~15 |

### Américas (`trackId: americas`)

| Código | Org | Matéria | Domínios | ~Questões |
|--------|-----|---------|----------|-----------|
| IAPP-CIPP-US | IAPP | CIPP/US | HIPAA, CCPA, setorial US | ~15 |

### Ásia (`trackId: asia`)

| Código | Org | Matéria | Domínios | ~Questões |
|--------|-----|---------|----------|-----------|
| IAPP-CIPP-A | IAPP | CIPP/A | APPI, PDPA, PIPL | ~15 **stub** |

## Formato bilingue (v2)

Cada questão no banco inclui:

```json
{
  "stemEn": "Your mother shared your phone number...",
  "stemPt": "Sua mãe compartilhou seu número...",
  "optionsEn": [{"text": "...", "correct": true}],
  "optionsPt": [{"text": "...", "correct": true}],
  "explanationEn": "...",
  "explanationPt": "...",
  "submateria": "Conceitos de SI",
  "level": "medio"
}
```

### Campos v2 (pass-through — opcionais no bank)

Quando presentes, `GlobalDPOSeeder._normalizeQuestion` preserva em `Question.nodeMeta`:

- `primaryLaw`, `secondaryLaw`, `bloomLevel`, `estimatedMinutes`
- `examObjective`, `officialReference`, `knowledgeArea`, `country`, `continent`
- `story`, `analogy`, `feynman`, `mnemonic`, `visualAssociation`
- `learningViews` (objeto completo)

Ver [`node-schema.example.json`](../data/node-schema.example.json).

**Modos** (Ajustes → Idioma das questões): `dual` · `en` · `pt`

## Pipeline de dados

```
generate_dpo_global_bank.py  →  data/dpo-global-bank.js
index.html                   →  GlobalDPOSeeder.seed()
                             →  Question + Exam em localStorage
sync_dpo_global.py           →  404.html (mirror JS/CSS)
```

## UX implementada (v2)

- **Home:** Continuar, Sessão inteligente, presets (Completo/Rápido/Só erros), progresso, listagem por trilha
- **Modal:** exclusões (dominadas, hoje), embaralhar, filtro nunca respondidas
- **Player:** Pausar, Explicar, revisão pré-envio (simulado)
- **SessionConfig:** shuffle, exclusões, preSubmitReview

## Reset / reseed

```javascript
localStorage.removeItem('ef_global_dpo_seeded_v2');
localStorage.removeItem('ef_cleanup_global_dpo_v2');
location.reload();
```

Reset completo:

```javascript
['ef_questions','ef_exams','ef_qstats','ef_history','ef_session','ef_global_dpo_seeded_v2','ef_cleanup_global_dpo_v2'].forEach(k=>localStorage.removeItem(k));
location.reload();
```

## Regenerar banco

```bash
python generate_dpo_global_bank.py
python sync_dpo_global.py
```

## Próximo enriquecimento

1. Piloto: 5–10 questões com `learningViews` completas (ver example JSON)
2. Metadata `primaryLaw` + `bloomLevel` por domínio
3. Dual-write v2 via `KnowledgeNormalizer` (Fase 2)
