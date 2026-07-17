'use strict';
/* =========================================================================
   VELORA — Knowledge Forge (motor de geração estruturada por IA)
   Não é chatbot: comando → intent → JSON schema → validação → persistência
   ========================================================================= */

const ForgeStorage = {
  KEYS: {
    HISTORY: 'ef_forge_history_v1',
    ARTIFACTS: 'ef_forge_artifacts_v1',
    DOCS: 'ef_forge_docs_v1',
    CONFIG: 'ef_forge_config_v1',
    TEMPLATES: 'ef_forge_templates_v1'
  },
  _get(k, fb){ try{ const r=localStorage.getItem(k); return r?JSON.parse(r):fb; }catch(e){ return fb; } },
  _set(k, v){ try{ localStorage.setItem(k, JSON.stringify(v)); return true; }catch(e){ return false; } },
  getConfig(){
    return {...{
      provider:'local', apiUrl:'https://api.openai.com/v1/chat/completions',
      model:'gpt-4o-mini', apiKey:'', maxRetries:3, useLibraryRag:true
    }, ...this._get(this.KEYS.CONFIG, {})};
  },
  saveConfig(c){ return this._set(this.KEYS.CONFIG, c); },
  getHistory(){ return this._get(this.KEYS.HISTORY, []); },
  addHistory(entry){
    const h = this.getHistory();
    h.unshift(entry);
    this._set(this.KEYS.HISTORY, h.slice(0, 100));
    return entry;
  },
  updateHistory(id, patch){
    const h = this.getHistory().map(x=>x.id===id?{...x,...patch}:x);
    this._set(this.KEYS.HISTORY, h);
  },
  getArtifacts(){ return this._get(this.KEYS.ARTIFACTS, []); },
  addArtifacts(items){
    const a = this.getArtifacts();
    this._set(this.KEYS.ARTIFACTS, [...items, ...a].slice(0, 500));
  },
  getDocs(){ return this._get(this.KEYS.DOCS, []); },
  upsertDoc(doc){
    const docs = this.getDocs().filter(d=>d.id!==doc.id);
    docs.unshift(doc);
    this._set(this.KEYS.DOCS, docs.slice(0, 50));
  },
  getTemplates(){ return this._get(this.KEYS.TEMPLATES, []); },
  saveTemplate(t){
    const list = this.getTemplates().filter(x=>x.id!==t.id);
    list.unshift(t);
    this._set(this.KEYS.TEMPLATES, list.slice(0, 30));
  }
};

const ForgeSchemas = {
  types: {
    flashcards: {
      label: {pt:'Flashcards', en:'Flashcards'},
      validate(data){
        if(!data?.items?.length) return 'items[] vazio';
        for(let i=0;i<data.items.length;i++){
          const it = data.items[i];
          if(!it.front?.trim()) return `items[${i}].front obrigatório`;
          if(!it.back?.trim()) return `items[${i}].back obrigatório`;
        }
        return null;
      },
      systemPrompt(en){
        return en
          ? 'You are a structured content generator. Return ONLY valid JSON matching the schema. No markdown.'
          : 'Você gera conteúdo estruturado. Retorne APENAS JSON válido conforme o schema. Sem markdown.';
      },
      userPrompt(intent, rag, en){
        const schema = `{ "type":"flashcards", "topic":"...", "language":"...", "items":[{"front":"...","back":"...","explanation":"...","category":"...","difficulty":"facil|medio|dificil","tags":["..."]}] }`;
        const ctx = rag?.length ? `\nContext (use when source=library):\n${rag.map(r=>`- ${r.text}`).join('\n')}` : '';
        return (en
          ? `Generate ${intent.quantity} flashcards about "${intent.topic}". Language: ${intent.language}. Difficulty: ${intent.difficulty}.${ctx}\nSchema:\n${schema}`
          : `Gere ${intent.quantity} flashcards sobre "${intent.topic}". Idioma: ${intent.language}. Dificuldade: ${intent.difficulty}.${ctx}\nSchema:\n${schema}`);
      }
    },
    quiz: {
      label: {pt:'Questões', en:'Questions'},
      validate(data){
        if(!data?.items?.length) return 'items[] vazio';
        for(let i=0;i<data.items.length;i++){
          const q = data.items[i];
          if(!q.stem?.trim()) return `items[${i}].stem obrigatório`;
          if(!Array.isArray(q.options)||q.options.length<2) return `items[${i}].options min 2`;
          if(!q.options.some(o=>o.correct)) return `items[${i}] sem resposta correta`;
        }
        return null;
      },
      systemPrompt(en){ return ForgeSchemas.types.flashcards.systemPrompt(en); },
      userPrompt(intent, rag, en){
        const schema = `{ "type":"quiz", "topic":"...", "language":"...", "items":[{"stem":"...","options":[{"text":"...","correct":true|false}],"explanation":"...","level":"facil|medio|dificil","category":"...","tags":["..."]}] }`;
        const ctx = rag?.length ? `\nContext:\n${rag.map(r=>`- ${r.text}`).join('\n')}` : '';
        return (en
          ? `Generate ${intent.quantity} multiple-choice questions about "${intent.topic}". Language: ${intent.language}. Level: ${intent.difficulty}.${ctx}\nSchema:\n${schema}`
          : `Gere ${intent.quantity} questões de múltipla escolha sobre "${intent.topic}". Idioma: ${intent.language}. Nível: ${intent.difficulty}.${ctx}\nSchema:\n${schema}`);
      }
    },
    exam: {
      label: {pt:'Simulado', en:'Exam'},
      validate(data){
        if(!data?.title?.trim()) return 'title obrigatório';
        if(!data?.items?.length) return 'items[] vazio';
        return ForgeSchemas.types.quiz.validate({items: data.items});
      },
      systemPrompt(en){ return ForgeSchemas.types.flashcards.systemPrompt(en); },
      userPrompt(intent, rag, en){
        const base = ForgeSchemas.types.quiz.userPrompt(intent, rag, en);
        return base + (en
          ? `\nAlso include: "title", "description", "passScore":70, "timeMinutes":60 at root.`
          : `\nInclua também: "title", "description", "passScore":70, "timeMinutes":60 na raiz.`);
      }
    },
    summary: {
      label: {pt:'Resumo', en:'Summary'},
      validate(data){
        if(!data?.title?.trim()) return 'title obrigatório';
        if(!data?.content?.trim()) return 'content obrigatório';
        return null;
      },
      systemPrompt(en){ return ForgeSchemas.types.flashcards.systemPrompt(en); },
      userPrompt(intent, rag, en){
        const schema = `{ "type":"summary", "title":"...", "content":"...", "keywords":["..."], "language":"...", "category":"..." }`;
        const ctx = rag?.length ? `\nContext:\n${rag.map(r=>`- ${r.text}`).join('\n')}` : '';
        return (en
          ? `Write a structured summary about "${intent.topic}". Language: ${intent.language}.${ctx}\nSchema:\n${schema}`
          : `Escreva um resumo estruturado sobre "${intent.topic}". Idioma: ${intent.language}.${ctx}\nSchema:\n${schema}`);
      }
    },
    timeline: {
      label: {pt:'Cronologia', en:'Timeline'},
      validate(data){
        if(!data?.title?.trim()) return 'title obrigatório';
        if(!data?.events?.length) return 'events[] vazio';
        for(let i=0;i<data.events.length;i++){
          if(!data.events[i].event?.trim()) return `events[${i}].event obrigatório`;
        }
        return null;
      },
      systemPrompt(en){ return ForgeSchemas.types.flashcards.systemPrompt(en); },
      userPrompt(intent, rag, en){
        const schema = `{ "type":"timeline", "title":"...", "language":"...", "events":[{"date":"...","event":"...","description":"..."}] }`;
        return (en
          ? `Generate a timeline with ${intent.quantity} events about "${intent.topic}". Language: ${intent.language}.\nSchema:\n${schema}`
          : `Gere uma linha do tempo com ${intent.quantity} eventos sobre "${intent.topic}". Idioma: ${intent.language}.\nSchema:\n${schema}`);
      }
    },
    study_plan: {
      label: {pt:'Plano de estudos', en:'Study plan'},
      validate(data){
        if(!data?.title?.trim()) return 'title obrigatório';
        if(!data?.modules?.length) return 'modules[] vazio';
        return null;
      },
      systemPrompt(en){ return ForgeSchemas.types.flashcards.systemPrompt(en); },
      userPrompt(intent, rag, en){
        const schema = `{ "type":"study_plan", "title":"...", "language":"...", "modules":[{"name":"...","objectives":["..."],"durationDays":7,"sequence":1}] }`;
        return (en
          ? `Create a study plan for "${intent.topic}" (${intent.quantity} modules). Language: ${intent.language}.\nSchema:\n${schema}`
          : `Crie um plano de estudos para "${intent.topic}" (${intent.quantity} módulos). Idioma: ${intent.language}.\nSchema:\n${schema}`);
      }
    },
    mind_map: {
      label: {pt:'Mapa mental', en:'Mind map'},
      validate(data){
        if(!data?.title?.trim()) return 'title obrigatório';
        if(!data?.nodes?.length) return 'nodes[] vazio';
        return null;
      },
      systemPrompt(en){ return ForgeSchemas.types.flashcards.systemPrompt(en); },
      userPrompt(intent, rag, en){
        const schema = `{ "type":"mind_map", "title":"...", "language":"...", "nodes":[{"id":"n1","label":"...","parentId":null}] }`;
        return (en
          ? `Generate a mind map about "${intent.topic}" with ~${intent.quantity} nodes. Language: ${intent.language}.\nSchema:\n${schema}`
          : `Gere um mapa mental sobre "${intent.topic}" com ~${intent.quantity} nós. Idioma: ${intent.language}.\nSchema:\n${schema}`);
      }
    },
    lesson: {
      label: {pt:'Lição', en:'Lesson'},
      validate(data){ if(!data?.title?.trim()) return 'title obrigatório'; if(!data?.sections?.length) return 'sections[] vazio'; return null; },
      systemPrompt(en){ return ForgeSchemas.types.flashcards.systemPrompt(en); },
      userPrompt(intent, rag, en){
        const ctx = rag?.length ? `\nContext:\n${rag.map(r=>r.text).join('\n')}` : '';
        const schema = `{ "type":"lesson", "title":"...", "language":"...", "sections":[{"heading":"...","content":"...","objectives":["..."]}] }`;
        return (en ? `Create a lesson about "${intent.topic}".${ctx}\nSchema:\n${schema}` : `Crie uma lição sobre "${intent.topic}".${ctx}\nSchema:\n${schema}`);
      }
    },
    exercise: {
      label: {pt:'Exercício discursivo', en:'Written exercise'},
      validate(data){ if(!data?.items?.length) return 'items[] vazio'; for(const it of data.items){ if(!it.prompt?.trim()) return 'prompt obrigatório'; } return null; },
      systemPrompt(en){ return ForgeSchemas.types.flashcards.systemPrompt(en); },
      userPrompt(intent, rag, en){
        const schema = `{ "type":"exercise", "topic":"...", "language":"...", "items":[{"prompt":"...","rubric":"...","sampleAnswer":"..."}] }`;
        return (en ? `Generate ${intent.quantity} written exercises about "${intent.topic}".\nSchema:\n${schema}` : `Gere ${intent.quantity} exercícios discursivos sobre "${intent.topic}".\nSchema:\n${schema}`);
      }
    },
    case_study: {
      label: {pt:'Caso clínico / estudo de caso', en:'Case study'},
      validate(data){ if(!data?.cases?.length) return 'cases[] vazio'; return null; },
      systemPrompt(en){ return ForgeSchemas.types.flashcards.systemPrompt(en); },
      userPrompt(intent, rag, en){
        const schema = `{ "type":"case_study", "topic":"...", "language":"...", "cases":[{"title":"...","scenario":"...","questions":["..."],"answers":["..."]}] }`;
        return (en ? `Generate ${intent.quantity} case studies about "${intent.topic}".\nSchema:\n${schema}` : `Gere ${intent.quantity} casos sobre "${intent.topic}".\nSchema:\n${schema}`);
      }
    },
    article: {
      label: {pt:'Artigo', en:'Article'},
      validate(data){ if(!data?.title?.trim()) return 'title obrigatório'; if(!data?.body?.trim()) return 'body obrigatório'; return null; },
      systemPrompt(en){ return ForgeSchemas.types.flashcards.systemPrompt(en); },
      userPrompt(intent, rag, en){
        const schema = `{ "type":"article", "title":"...", "language":"...", "body":"...", "keywords":["..."] }`;
        return (en ? `Write an article about "${intent.topic}".\nSchema:\n${schema}` : `Escreva um artigo sobre "${intent.topic}".\nSchema:\n${schema}`);
      }
    },
    certification: {
      label: {pt:'Prep. certificação', en:'Certification prep'},
      validate(data){ return ForgeSchemas.types.exam.validate(data); },
      systemPrompt(en){ return ForgeSchemas.types.exam.systemPrompt(en); },
      userPrompt(intent, rag, en){ return ForgeSchemas.types.exam.userPrompt({...intent, type:'exam'}, rag, en); }
    }
  },

  validate(type, data){
    const def = this.types[type];
    if(!def) return `Tipo desconhecido: ${type}`;
    if(type === 'certification'){
      const err = this.types.exam.validate({...data, type:'exam'});
      return err;
    }
    if(data?.type && data.type !== type && !(type==='certification' && data.type==='exam')) return `type esperado ${type}, recebido ${data.type}`;
    return def.validate(data);
  }
};

const ForgeIntentParser = {
  TYPE_PATTERNS: [
    {type:'flashcards', re:/flash\s*cards?|cart[oõ]es?|anki|cards?\s+sobre/i},
    {type:'quiz', re:/quest(ões|oes|ions?)|quiz|banco de quest|m[uú]ltipla escolha|exerc[ií]cios discursivos/i},
    {type:'exam', re:/simulado|prova completa|exam|certifica/i},
    {type:'summary', re:/resumo|summary|s[ií]ntese/i},
    {type:'timeline', re:/linha do tempo|timeline|cronolog/i},
    {type:'study_plan', re:/plano de estudos|study plan|trilha de estudo/i},
    {type:'mind_map', re:/mapa mental|mind map/i},
    {type:'lesson', re:/li[cç][aã]o|lesson|aula/i},
    {type:'exercise', re:/exerc[ií]cio/i},
    {type:'case_study', re:/casos?\s*cl[ií]nicos?|estudo de caso|case study/i},
    {type:'article', re:/artigo|article/i},
    {type:'certification', re:/certifica[cç][aã]o|certification prep|prep para/i}
  ],
  QTY_RE: /(\d{1,3})\s*(?:flashcards?|cart[oõ]es?|cards?|quest(ões|oes|ions?)|eventos?|m[oó]dulos?|n[oó]s?)?/i,
  TOPIC_RE: /(?:sobre|about|de|on|para|for)\s+(.+?)(?:\.|$|,|\s+em\s+|\s+in\s+)/i,
  LANG_RE: /(?:em|in)\s+(portugu[eê]s|ingl[eê]s|english|portuguese|pt|en)/i,
  DIFF_RE: /(f[aá]cil|easy|m[eé]dio|medium|dif[ií]cil|hard|avançad)/i,
  LIBRARY_RE: /(?:apenas|only|using|utilizando|com)\s+(?:os\s+)?(?:documentos?|conte[uú]do|biblioteca|library)/i,
  PDF_RE: /(?:pdf|documento|transforme|converta)/i,

  parse(command, filters={}){
    const raw = (command||'').trim();
    const en = typeof I18n !== 'undefined' && I18n.isEn();
    let type = filters.type || 'quiz';
    for(const p of this.TYPE_PATTERNS){ if(p.re.test(raw)){ type = p.type; break; } }
    if(/casos?\s*cl[ií]nicos?/i.test(raw)) type = 'case_study';
    if(/artigo/i.test(raw)) type = 'article';

    let quantity = filters.quantity;
    const qm = raw.match(this.QTY_RE);
    if(qm) quantity = Math.min(100, Math.max(1, parseInt(qm[1], 10)));
    if(!quantity){
      quantity = {flashcards:20, quiz:10, exam:20, summary:1, timeline:12, study_plan:6, mind_map:10}[type] || 10;
    }

    let topic = filters.topic || '';
    const tm = raw.match(this.TOPIC_RE);
    if(tm) topic = tm[1].trim();
    if(!topic){
      topic = raw.replace(this.QTY_RE,'').replace(/^(gere|gerar|create|crie|criar|transforme|generate)\s+/i,'').trim();
      topic = topic.slice(0, 120) || (en ? 'General topic' : 'Tema geral');
    }

    let language = filters.language || (en ? 'en' : 'pt-BR');
    const lm = raw.match(this.LANG_RE);
    if(lm){
      const l = lm[1].toLowerCase();
      language = /en|ingl/.test(l) ? 'en' : 'pt-BR';
    }

    let difficulty = filters.difficulty || 'medio';
    const dm = raw.match(this.DIFF_RE);
    if(dm){
      const d = dm[1].toLowerCase();
      if(/f[aá]cil|easy/.test(d)) difficulty = 'facil';
      else if(/dif|hard|avan/.test(d)) difficulty = 'dificil';
    }

    const source = this.LIBRARY_RE.test(raw) || filters.source === 'library' ? 'library'
      : (this.PDF_RE.test(raw) ? 'document' : (filters.source || 'model'));

    const category = filters.category || topic.split(/\s+/).slice(0, 3).join(' ');
    const tags = filters.tags || [category, type].filter(Boolean);

    return { type, topic, quantity, language, difficulty, format: type, category, tags, source, rawCommand: raw };
  }
};

const ForgeRAG = {
  retrieve(intent, limit=8){
    if(intent.source === 'document'){
      const docs = ForgeStorage.getDocs();
      const needle = (intent.topic||'').toLowerCase().split(/\s+/).filter(w=>w.length>2);
      const chunks = [];
      docs.forEach(d=>{
        const parts = String(d.text||'').split(/\n{2,}/).filter(p=>p.trim().length>40);
        parts.forEach((p,i)=>{
          const blob = p.toLowerCase();
          let score = needle.length ? 0 : 1;
          needle.forEach(w=>{ if(blob.includes(w)) score++; });
          if(score>0) chunks.push({id:`${d.id}-${i}`, text:p.slice(0,400), score, docName:d.name});
        });
      });
      return chunks.sort((a,b)=>b.score-a.score).slice(0, limit);
    }
    if(intent.source !== 'library') return [];
    const needle = (intent.topic||'').toLowerCase().split(/\s+/).filter(w=>w.length>2);
    if(!needle.length) return [];
    const qs = typeof StorageManager !== 'undefined' ? StorageManager.getQuestions() : [];
    const scored = qs.map(q=>{
      const blob = [q.text,q.stemPt,q.stemEn,q.explanation,q.category,...(q.tags||[])].join(' ').toLowerCase();
      let score = 0;
      needle.forEach(w=>{ if(blob.includes(w)) score++; });
      return {q, score, text: (q.text||q.stemPt||'').slice(0, 280)};
    }).filter(x=>x.score>0).sort((a,b)=>b.score-a.score).slice(0, limit);
    return scored.map(s=>({id:s.q.id, text:s.text, score:s.score, q:s.q}));
  },

  ingestTextFile(name, text){
    const doc = {id: Util.uid('fdoc'), name, text: String(text).slice(0, 500000), createdAt: new Date().toISOString()};
    ForgeStorage.upsertDoc(doc);
    return doc;
  }
};

const ForgeProviderLocal = {
  generate(intent, config){
    const type = intent.type;
    const topic = intent.topic || 'Conteúdo';
    const n = Math.min(Math.max(intent.quantity || 10, 1), 50);
    const rag = ForgeRAG.retrieve(intent, n);
    const qsFromLib = rag.filter(r=>r.q).map(r=>r.q);
    const allQs = qsFromLib.length
      ? qsFromLib
      : (typeof StorageManager !== 'undefined' ? StorageManager.getQuestions() : []);
    const needle = String(topic).toLowerCase().split(/\s+/).filter(w=>w.length>2);
    const matched = allQs.filter(q=>{
      const blob = [q.text,q.stemPt,q.stemEn,q.explanation,q.category,q.materia,q.submateria,...(q.tags||[])].join(' ').toLowerCase();
      return !needle.length || needle.some(w=>blob.includes(w));
    }).slice(0, n);

    if(type === 'flashcards' && matched.length){
      const items = matched.map(q=>{
        const ans = (q.options||[]).find(o=>o.correct)?.text || q.explanation || q.explanationPt || '';
        return {
          front: q.text || q.stemPt || q.stemEn || topic,
          back: ans || '—',
          explanation: q.explanation || q.explanationPt || '',
          category: q.category || q.submateria || topic,
          difficulty: q.level || intent.difficulty || 'medio',
          tags: [...new Set([...(q.tags||[]).slice(0,4), 'forge-local', topic])]
        };
      });
      return Promise.resolve({type:'flashcards', topic, language:intent.language, items});
    }

    if(['quiz','exam','certification'].includes(type) && matched.length >= 3){
      const items = matched.map(q=>({
        stem: q.text || q.stemPt || q.stemEn,
        options: (q.options||[]).length
          ? q.options.map(o=>({text:o.text || o.textPt || o.textEn, correct:!!o.correct}))
          : [{text:'Verdadeiro', correct:true},{text:'Falso', correct:false}],
        explanation: q.explanation || q.explanationPt || '',
        level: q.level || intent.difficulty,
        category: q.category || q.submateria || topic,
        tags: [...(q.tags||[]), 'forge-local']
      }));
      if(type === 'exam' || type === 'certification'){
        return Promise.resolve({
          type:'exam',
          title:`Simulado — ${topic}`,
          description:'Montado a partir da sua biblioteca Velora (sem API externa)',
          passScore:70, timeMinutes:60, language:intent.language, items
        });
      }
      return Promise.resolve({type:'quiz', topic, language:intent.language, items});
    }

    if(rag.length && ['summary','article','lesson'].includes(type)){
      const body = rag.map(r=>r.text).join('\n\n').slice(0, 4000);
      if(type === 'summary'){
        return Promise.resolve({type:'summary', title:`Resumo: ${topic}`, content:body, keywords:[topic], language:intent.language, category:topic});
      }
      if(type === 'article'){
        return Promise.resolve({type:'article', title:`Artigo: ${topic}`, language:intent.language, body, keywords:[topic]});
      }
      return Promise.resolve({
        type:'lesson', title:`Lição — ${topic}`, language:intent.language,
        sections:[{heading:topic, content:body.slice(0,1200), objectives:['Revisar conceitos da biblioteca']}]
      });
    }

    return null;
  }
};

const ForgeProviderOllama = {
  async generate(system, user, config){
    const url = config.apiUrl || 'http://localhost:11434/api/chat';
    const model = config.model || 'llama3.2';
    const res = await fetch(url, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({
        model,
        stream:false,
        format:'json',
        messages:[{role:'system', content:system},{role:'user', content:user}]
      })
    });
    if(!res.ok){
      const err = await res.text().catch(()=>res.statusText);
      throw new Error(`Ollama ${res.status}: ${err.slice(0,200)}`);
    }
    const json = await res.json();
    const content = json.message?.content || json.response || '';
    return ForgeProvider._parseJson(content);
  }
};

const ForgeProvider = {
  async generate(system, user, config, intent){
    const engineActive = typeof ForgeEngines !== 'undefined' && ForgeEngines.hasActiveEngine();
    if(engineActive){
      try{
        return await ForgeEngines.callAI(system, user);
      }catch(e){
        console.warn('[ForgeProvider] Engine error:', e.message);
        throw new Error(
          (typeof I18n !== 'undefined' && I18n.isEn?.())
            ? `AI engine failed: ${e.message}. Check connection or try another model.`
            : `Engine de IA falhou: ${e.message}. Verifique a conexão ou troque o modelo.`
        );
      }
    }
    const provider = config.provider || 'local';
    if(provider === 'ollama'){
      return ForgeProviderOllama.generate(system, user, config, intent);
    }
    if(!config.apiKey || provider === 'local' || provider === 'mock'){
      const local = await ForgeProviderLocal.generate(intent, config);
      if(local) return local;
      return ForgeProviderMock.generate(intent, config);
    }
    const res = await fetch(config.apiUrl, {
      method:'POST',
      headers:{'Content-Type':'application/json', 'Authorization': `Bearer ${config.apiKey}`},
      body: JSON.stringify({
        model: config.model,
        temperature: 0.4,
        response_format: {type:'json_object'},
        messages:[
          {role:'system', content: system},
          {role:'user', content: user}
        ]
      })
    });
    if(!res.ok){
      const err = await res.text().catch(()=>res.statusText);
      throw new Error(`API ${res.status}: ${err.slice(0,200)}`);
    }
    const json = await res.json();
    const content = json.choices?.[0]?.message?.content || '';
    return ForgeProvider._parseJson(content);
  },

  _parseJson(text){
    const t = String(text).trim();
    try{ return JSON.parse(t); }catch(e){}
    const m = t.match(/\{[\s\S]*\}/);
    if(m) return JSON.parse(m[0]);
    throw new Error('Resposta não é JSON válido');
  }
};

const ForgeProviderMock = {
  generate(intent, config){
    const type = intent.type;
    const topic = intent.topic;
    const n = Math.min(intent.quantity, 8);
    const items = [];
    for(let i=1;i<=n;i++){
      if(type==='flashcards'){
        items.push({
          front: `${topic} — conceito ${i}?`,
          back: `Resposta ${i} sobre ${topic}`,
          explanation: `Explicação demo ${i}. Configure API em Forja → Configurações para conteúdo real.`,
          category: topic, difficulty: intent.difficulty, tags: [topic, 'forge-demo']
        });
      } else if(['quiz','exam'].includes(type)){
        items.push({
          stem: `[Demo] Pergunta ${i} sobre ${topic}?`,
          options: [{text:'Alternativa A', correct:true},{text:'Alternativa B',correct:false},{text:'Alternativa C',correct:false}],
          explanation: 'Modo demo — adicione chave API para geração real.',
          level: intent.difficulty, category: topic, tags: ['forge-demo']
        });
      }
    }
    const payloads = {
      flashcards: {type:'flashcards', topic, language:intent.language, items},
      quiz: {type:'quiz', topic, language:intent.language, items},
      exam: {type:'exam', title:`Simulado — ${topic}`, description:'Gerado pela Forja (demo)', passScore:70, timeMinutes:60, language:intent.language, items},
      summary: {type:'summary', title:`Resumo: ${topic}`, content:`Resumo demonstrativo sobre ${topic}. Configure a API para texto completo.`, keywords:[topic], language:intent.language, category:topic},
      timeline: {type:'timeline', title:topic, language:intent.language, events: Array.from({length:n},(_,i)=>({date:`${1900+i*10}`, event:`Evento ${i+1}`, description:`Marco de ${topic}`}))},
      study_plan: {type:'study_plan', title:`Plano — ${topic}`, language:intent.language, modules: Array.from({length:Math.min(n,3)},(_,i)=>({name:`Módulo ${i+1}`, objectives:[`Objetivo ${i+1}`], durationDays:7, sequence:i+1}))},
      mind_map: {type:'mind_map', title:topic, language:intent.language, nodes:[{id:'root',label:topic,parentId:null},{id:'n1',label:'Subtema 1',parentId:'root'}]},
      lesson: {type:'lesson', title:`Lição — ${topic}`, language:intent.language, sections:Array.from({length:Math.min(n,3)},(_,i)=>({heading:`Seção ${i+1}`, content:`Conteúdo demo sobre ${topic}.`, objectives:[`Objetivo ${i+1}`]}))},
      exercise: {type:'exercise', topic, language:intent.language, items:Array.from({length:n},(_,i)=>({prompt:`[Demo] Exercício ${i+1} sobre ${topic}`, rubric:'Critérios demo', sampleAnswer:'Resposta modelo demo'}))},
      case_study: {type:'case_study', topic, language:intent.language, cases:Array.from({length:Math.min(n,3)},(_,i)=>({title:`Caso ${i+1}`, scenario:`Cenário demo ${topic}`, questions:['Pergunta 1?'], answers:['Resposta modelo']}))},
      article: {type:'article', title:`Artigo: ${topic}`, language:intent.language, body:`Artigo demonstrativo sobre ${topic}.`, keywords:[topic]},
      certification: {type:'exam', title:`Certificação — ${topic}`, description:'Prep demo', passScore:70, timeMinutes:90, language:intent.language, items}
    };
    const payload = payloads[type] || payloads.quiz;
    if(type==='certification') payload.type = 'certification';
    return Promise.resolve(payload);
  }
};

const ForgeRegistry = {
  generators: {},
  register(type, handler){ this.generators[type] = handler; },
  get(type){ return this.generators[type]; }
};

ForgeRegistry.register('flashcards', {
  persist(data, intent){
    const ids = [];
    (data.items||[]).forEach(it=>{
      const q = new Question({
        type:'single',
        text: it.front,
        explanation: [it.back, it.explanation].filter(Boolean).join('\n\n'),
        stemPt: it.front, explanationPt: it.explanation || it.back,
        level: it.difficulty || intent.difficulty,
        category: it.category || intent.category,
        tags: [...(it.tags||[]), 'forge', intent.topic, 'knowledge-node'],
        nodeMeta: { topic: intent.topic, source: 'forge', knowledgeNode: true, type: 'flashcard' },
        options:[{id:Util.uid('o'), text: it.back, correct:true},{id:Util.uid('o'), text:'—', correct:false}]
      });
      StorageManager.upsertQuestion(q);
      ids.push(q.id);
    });
    return {questionIds: ids, label: `${ids.length} flashcards → questões/cards`};
  }
});

ForgeRegistry.register('quiz', {
  persist(data, intent){
    const ids = [];
    (data.items||[]).forEach(it=>{
      const q = new Question({
        type:'single',
        text: it.stem,
        explanation: it.explanation||'',
        stemPt: it.stem, explanationPt: it.explanation||'',
        level: it.level || intent.difficulty,
        category: it.category || intent.category,
        tags: [...(it.tags||[]), 'forge', intent.topic, 'knowledge-node'],
        nodeMeta: { topic: intent.topic, source: 'forge', knowledgeNode: true, type: 'quiz' },
        options: (it.options||[]).map(o=>({id:Util.uid('o'), text:o.text, correct:!!o.correct}))
      });
      StorageManager.upsertQuestion(q);
      ids.push(q.id);
    });
    return {questionIds: ids, label: `${ids.length} questões salvas`};
  }
});

ForgeRegistry.register('exam', {
  persist(data, intent){
    const quizGen = ForgeRegistry.get('quiz');
    const r = quizGen.persist(data, intent);
    const exam = new Exam({
      title: data.title || `Simulado — ${intent.topic}`,
      description: data.description || 'Gerado pela Forja',
      category: intent.category,
      materia: intent.topic,
      timeMinutes: data.timeMinutes || 60,
      passScore: data.passScore || 70,
      questionIds: r.questionIds,
      tags: ['forge', intent.topic]
    });
    StorageManager.upsertExam(exam);
    return {examId: exam.id, questionIds: r.questionIds, label: `Simulado "${exam.title}" (${r.questionIds.length} questões)`};
  }
});

ForgeRegistry.register('certification', {
  persist(data, intent){
    return ForgeRegistry.get('exam').persist({...data, title: data.title || `Certificação — ${intent.topic}`}, intent);
  }
});

['summary','timeline','study_plan','mind_map','lesson','exercise','case_study','article'].forEach(type=>{
  ForgeRegistry.register(type, {
    persist(data, intent){
      const artifact = {
        id: Util.uid('fa'),
        type,
        title: data.title || intent.topic,
        payload: data,
        topic: intent.topic,
        createdAt: new Date().toISOString()
      };
      ForgeStorage.addArtifacts([artifact]);
      return {artifactId: artifact.id, label: `${ForgeSchemas.types[type].label.pt} salvo em artefatos`};
    }
  });
});

const ForgeOrchestrator = {
  async run(command, filters={}, onProgress){
    const config = ForgeStorage.getConfig();
    const intent = ForgeIntentParser.parse(command, filters);
    const schema = ForgeSchemas.types[intent.type];
    if(!schema) throw new Error(`Gerador não registrado: ${intent.type}`);

    onProgress?.('rag');
    const rag = ForgeRAG.retrieve(intent);

    const system = schema.systemPrompt(typeof I18n !== 'undefined' && I18n.isEn());
    let user = schema.userPrompt(intent, rag, typeof I18n !== 'undefined' && I18n.isEn());
    let lastError = null;
    let data = null;

    for(let attempt=1; attempt <= (config.maxRetries||3); attempt++){
      onProgress?.('generate', attempt);
      try{
        data = await ForgeProvider.generate(system, user, config, intent);
        const err = ForgeSchemas.validate(intent.type, data);
        if(err){
          lastError = err;
          user += `\n\nValidation error (fix JSON): ${err}`;
          continue;
        }
        lastError = null;
        break;
      }catch(e){
        lastError = e.message;
        const hasCloud = config.apiKey || (typeof ForgeEngines !== 'undefined' && ForgeEngines.hasActiveEngine());
        if(!hasCloud) break;
        user += `\n\nError: ${e.message}. Return valid JSON only.`;
      }
    }
    if(lastError) throw new Error(lastError);

    const demoPayload = JSON.stringify(data || '').includes('forge-demo');
    const engineOn = typeof ForgeEngines !== 'undefined' && ForgeEngines.hasActiveEngine();
    let providerLabel = config.apiKey ? (config.model || 'openai') : (config.provider || 'local');
    if(demoPayload) providerLabel = 'demo';
    else if(engineOn) providerLabel = ForgeEngines.getEngine(1)?.provider || ForgeEngines.getEngine(2)?.provider || 'engine';
    const entry = {
      id: Util.uid('fhist'),
      createdAt: new Date().toISOString(),
      command,
      intent,
      status: 'preview',
      data,
      provider: providerLabel
    };
    ForgeStorage.addHistory(entry);
    return {entry, intent, data};
  },

  persist(entry){
    const gen = ForgeRegistry.get(entry.intent.type);
    if(!gen) throw new Error('Persistência não disponível');
    const result = gen.persist(entry.data, entry.intent);
    ForgeStorage.updateHistory(entry.id, {status:'saved', persisted: result, savedAt: new Date().toISOString()});
    return result;
  }
};

Object.assign(window, {ForgeStorage, ForgeSchemas, ForgeIntentParser, ForgeRAG, ForgeProvider, ForgeRegistry, ForgeOrchestrator, ForgeProviderLocal, ForgeProviderMock});
