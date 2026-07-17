'use strict';
/* Velora GPS v2 — Learning OS: goal, chained routes, readiness, simulations, competencies */

const LearningGoal = {
  KEY: 'ef_gps_goal_v1',
  get(){
    try{
      return { examId:'', minutesPerDay:10, ...(JSON.parse(localStorage.getItem(this.KEY)||'{}')) };
    }catch(e){ return { examId:'', minutesPerDay:10 }; }
  },
  set(partial){
    const next = { ...this.get(), ...partial };
    try{ localStorage.setItem(this.KEY, JSON.stringify(next)); }catch(e){}
    return next;
  },
  getExam(){
    const id = this.get().examId;
    return id ? window.StorageManager?.getExam?.(id) : null;
  },
  label(){
    const e = this.getExam();
    if(!e) return null;
    return e.materia || e.title || null;
  }
};

const LearnerModel = {
  KEY: 'ef_metacog_v1',
  SIM_KEY: 'ef_sim_progress_v1',

  _sm(){ return window.StorageManager; },

  _meta(){
    try{ return JSON.parse(localStorage.getItem(this.KEY)||'{}'); }catch(e){ return {}; }
  },
  _saveMeta(m){ try{ localStorage.setItem(this.KEY, JSON.stringify(m)); }catch(e){} },

  masteryForStat(s){
    if(!s || !s.seen) return 0;
    const acc = (s.correct||0) / s.seen;
    const streakPart = Math.min(s.streak||0, 5) / 5;
    return Math.round(acc * 70 + streakPart * 30);
  },

  nodeState(q){
    const s = this._sm().getStat(q.id);
    const fc = window.FSRS ? window.FSRS.card(q) : {};
    const mastery = this.masteryForStat(s);
    const now = Date.now();
    const due = s.due || fc.due || 0;
    const overdueDays = due && s.seen ? Math.max(0, (now - due) / 86400000) : 0;
    const retentionRisk = Math.min(100, Math.round(
      (overdueDays > 0 ? 35 + Math.min(overdueDays, 14) * 4 : 0) +
      (mastery < 50 && s.seen >= 2 ? 25 : 0) +
      (fc.state === 'learning' ? 15 : 0)
    ));
    const meta = this._meta()[q.id] || { samples:0, avgConfidence:0, illusion:0, wrongSamples:0 };
    return { mastery, retentionRisk, overdueDays, seen: s.seen||0, illusion: meta.illusion||0, avgConfidence: Math.round(meta.avgConfidence||0), wrongSamples: meta.wrongSamples||0 };
  },

  recordConfidence(qid, level, correct){
    const m = this._meta();
    const row = m[qid] || { samples:0, sumConf:0, sumConfWrong:0, wrongSamples:0, illusion:0 };
    const conf = Math.max(1, Math.min(5, Number(level)||3));
    row.samples++;
    row.sumConf += conf;
    row.avgConfidence = row.sumConf / row.samples;
    if(!correct && conf >= 4){
      row.wrongSamples++;
      row.sumConfWrong += conf;
    }
    row.illusion = row.wrongSamples ? Math.round((row.sumConfWrong / row.wrongSamples) * 20) : 0;
    m[qid] = row;
    this._saveMeta(m);
  },

  illusionLeaders(limit=8){
    const m = this._meta();
    return this._sm().getQuestions()
      .map(q=>{
        const ns = this.nodeState(q);
        const meta = m[q.id] || {};
        return {
          q,
          label: (q.text || q.stemPt || q.stemEn || q.category || q.id).slice(0, 100),
          category: q.category || q.submateria || q.materia || '',
          ...ns,
          wrongSamples: meta.wrongSamples || 0
        };
      })
      .filter(x=>x.seen >= 2 && (x.illusion >= 55 || x.wrongSamples >= 2))
      .sort((a,b)=>(b.illusion-a.illusion) || (b.wrongSamples-a.wrongSamples))
      .slice(0, limit);
  },

  aggregateMetacog(){
    const m = this._meta();
    let highConfWrong = 0, samples = 0;
    Object.values(m).forEach(r=>{ samples += r.samples||0; highConfWrong += r.wrongSamples||0; });
    return { samples, highConfWrong, illusionRate: samples ? Math.round(highConfWrong / samples * 100) : 0 };
  },

  retentionForecast90(){
    const qs = this._sm().getQuestions();
    let sum = 0, n = 0;
    qs.forEach(q=>{
      const s = this._sm().getStat(q.id);
      if(!s.seen) return;
      const ns = this.nodeState(q);
      sum += Math.max(0, 100 - ns.retentionRisk);
      n++;
    });
    return n ? Math.round(sum / n) : null;
  },

  simProgress(){
    try{ return JSON.parse(localStorage.getItem(this.SIM_KEY)||'{}'); }catch(e){ return {}; }
  },
  saveSimProgress(id, data){
    const all = this.simProgress();
    all[id] = { ...(all[id]||{}), ...data, updatedAt: new Date().toISOString() };
    try{ localStorage.setItem(this.SIM_KEY, JSON.stringify(all)); }catch(e){}
    CompetencyEngine.checkSim(id, data);
  }
};

const CompetencyEngine = {
  KEY: 'ef_competencies_v1',
  DEFS: [
    { id:'lgpd_sim', ic:'LGPD', pt:'LGPD — Simulação', en:'LGPD — Simulation', domain:'LGPD', simId:'lgpd_breach_v1' },
    { id:'cissp_sim', ic:'IR', pt:'CISSP — Resposta a incidente', en:'CISSP — Incident response', domain:'CISSP', simId:'cissp_incident_v1' },
    { id:'cipp_sim', ic:'XFR', pt:'CIPP/E — Transferência', en:'CIPP/E — Cross-border', domain:'CIPP/E', simId:'cipp_transfer_v1' },
    { id:'route_chain', ic:'GPS', pt:'Rota GPS completa', en:'Full GPS route', event:'route_chain' },
    { id:'cold_retrieval', ic:'FRIO', pt:'Revisão fria', en:'Cold retrieval', event:'cold_retrieval' },
    { id:'mastery_70', ic:'70%', pt:'Domínio ≥70%', en:'Mastery ≥70%', check:g=> g && ProgressAnalytics?.masteryScore?.().score >= 70 }
  ],

  all(){
    try{ return JSON.parse(localStorage.getItem(this.KEY)||'{}'); }catch(e){ return {}; }
  },
  unlock(id){
    const all = this.all();
    if(all[id]) return false;
    all[id] = { at: new Date().toISOString() };
    try{ localStorage.setItem(this.KEY, JSON.stringify(all)); }catch(e){}
    const def = this.DEFS.find(d=>d.id===id);
    const en = window.I18n?.isEn?.();
    if(def && window.RewardPop){
      window.RewardPop.show(def.ic, en ? 'Competency unlocked' : 'Competência desbloqueada', en ? def.en : def.pt, 2000);
    }
    return true;
  },
  list(){
    const unlocked = this.all();
    const en = window.I18n?.isEn?.();
    return this.DEFS.map(d=>({
      ...d,
      label: en ? d.en : d.pt,
      unlocked: !!unlocked[d.id],
      at: unlocked[d.id]?.at
    }));
  },
  checkSim(simId, data){
    if(!data?.completed) return;
    const def = this.DEFS.find(d=>d.simId === simId);
    if(def) this.unlock(def.id);
    if((data.score||0) >= 85) this.unlock('mastery_70');
  },
  onRouteComplete(){ this.unlock('route_chain'); },
  onColdRetrieval(){ this.unlock('cold_retrieval'); },
  refresh(){
    const m = ProgressAnalytics?.masteryScore?.();
    if(m?.score >= 70) this.unlock('mastery_70');
  }
};

const ReadinessEngine = {
  forExam(exam){
    if(!exam?.questionIds?.length) return null;
    const SM = window.StorageManager;
    const qmap = new Map(SM.getQuestions().map(q=>[q.id, q]));
    let mastered = 0, seen = 0, riskSum = 0, total = exam.questionIds.length;
    exam.questionIds.forEach(id=>{
      const q = qmap.get(id);
      if(!q) return;
      const ns = LearnerModel.nodeState(q);
      if(ns.seen) seen++;
      if(ns.mastery >= 65) mastered++;
      riskSum += ns.retentionRisk;
    });
    const readiness = Math.round((mastered / total) * 100);
    return {
      examId: exam.id,
      title: exam.title,
      materia: exam.materia || exam.title,
      readiness,
      mastered,
      total,
      seenPct: Math.round((seen / total) * 100),
      avgRisk: total ? Math.round(riskSum / total) : 0,
      etaDays: this._etaDays(exam, mastered, total),
      passScore: exam.passScore || 70
    };
  },

  _etaDays(exam, mastered, total){
    const remaining = Math.max(0, total - mastered);
    if(!remaining) return 0;
    const goal = LearningGoal.get();
    const dailyMin = goal.minutesPerDay || 10;
    const velocity = Math.max(0.8, dailyMin / 8);
    if(goal.examId === exam.id) return Math.max(1, Math.ceil(remaining / velocity));
    const hist = window.StorageManager.getHistory().filter(h=>h.examId===exam.id && h.sessionKind !== 'flashcards');
    const last14 = hist.filter(h=> Date.now() - new Date(h.date).getTime() < 14 * 86400000);
    let v = velocity;
    if(last14.length >= 2){
      const gain = last14.reduce((s,h)=> s + (h.correctCount||0), 0) / last14.length;
      v = Math.max(0.5, gain * 0.15);
    }
    return Math.max(1, Math.ceil(remaining / v));
  },

  topTracks(limit=6){
    const goal = LearningGoal.get();
    let exams = window.StorageManager.getExams().filter(e=>e.questionIds?.length);
    if(goal.examId) exams = exams.sort((a,b)=>(a.id===goal.examId?-1:0)-(b.id===goal.examId?-1:0));
    return exams.map(e=>this.forExam(e)).filter(Boolean).sort((a,b)=>a.readiness-b.readiness).slice(0, limit);
  }
};

const RouteChainController = {
  KEY: 'ef_gps_chain_v1',

  load(){
    try{ return JSON.parse(sessionStorage.getItem(this.KEY)||'null'); }catch(e){ return null; }
  },
  save(c){ try{ sessionStorage.setItem(this.KEY, JSON.stringify(c)); }catch(e){} },
  clear(){ try{ sessionStorage.removeItem(this.KEY); }catch(e){} },
  isActive(){ return !!this.load(); },

  start(plan){
    if(!plan?.steps?.length) return;
    this.save({ plan, stepIndex: 0, startedAt: Date.now() });
    this._runCurrent(true);
  },

  _runCurrent(first){
    const chain = this.load();
    if(!chain) return;
    const step = chain.plan.steps[chain.stepIndex];
    if(!step){ this._finish(); return; }
    const en = window.I18n?.isEn?.();
    if(!first){
      window.Toast?.show?.(en ? `Step ${chain.stepIndex+1}/${chain.plan.steps.length}` : `Passo ${chain.stepIndex+1}/${chain.plan.steps.length}`, 'success');
    }
    if(step.type === 'flashcards' && window.FlashcardController){
      window.FlashcardController.start(step.count, { scope:'all', questionIds: step.cardIds || [] });
    } else if(step.type === 'questions' && window.PlayerController){
      window.PlayerController.startStudyRoute(step.ids || [], chain.plan.reason, { chainMode: true });
    } else if(step.type === 'simulation' && window.SimulationEngine){
      window.SimulationEngine.start(step.id, { chainMode: true });
    } else {
      this.onStepDone(step.type);
    }
  },

  onStepDone(type){
    const chain = this.load();
    if(!chain) return false;
    const cur = chain.plan.steps[chain.stepIndex];
    if(!cur || cur.type !== type) return false;
    chain.stepIndex++;
    if(chain.stepIndex >= chain.plan.steps.length){
      this._finish();
      return true;
    }
    this.save(chain);
    const next = chain.plan.steps[chain.stepIndex];
    const curN = chain.stepIndex + 1;
    const totN = chain.plan.steps.length;
    const msg = window.I18n?.t?.('gps.chainNext', { cur: curN, tot: totN, label: next.label })
      || (window.I18n?.isEn?.()
        ? `Next (${curN}/${totN}): ${next.label}`
        : `Próximo (${curN}/${totN}): ${next.label}`);
    window.Toast?.show?.(msg, 'success', 2200);
    setTimeout(()=> this._runCurrent(false), 700);
    return true;
  },

  _finish(){
    this.clear();
    CompetencyEngine.onRouteComplete();
    const en = window.I18n?.isEn?.();
    window.Toast?.show?.(en ? 'GPS route complete!' : 'Rota GPS concluída!', 'success');
    CompetencyEngine.refresh();
  }
};

const RouteOptimizer = {
  buildPlan(minutes){
    const goal = LearningGoal.get();
    const mins = minutes || goal.minutesPerDay || 10;
    const en = window.I18n?.isEn?.();
    const examId = goal.examId || null;
    const qCount = Math.max(4, Math.round(mins * 0.55));
    const fcCount = Math.min(5, Math.max(0, Math.round(mins * 0.25)));
    const dueCards = this._dueFlashcards(fcCount, examId);
    const questionIds = this._pickQuestionIds(qCount, examId);
    const sim = this._nextSimulation();
    const gap = window.ProgressAnalytics?.topGap?.();
    const steps = [];
    if(dueCards.length){
      steps.push({
        type:'flashcards', count: dueCards.length, cardIds: dueCards.map(q=>q.id),
        label: en ? `${dueCards.length} FSRS cards` : `${dueCards.length} cards FSRS`
      });
    }
    if(questionIds.length){
      steps.push({
        type:'questions', count: questionIds.length, ids: questionIds,
        label: en ? `${questionIds.length} gap questions` : `${questionIds.length} questões de lacuna`
      });
    }
    if(sim && !LearnerModel.simProgress()[sim.id]?.completed){
      steps.push({ type:'simulation', id: sim.id, label: sim.title });
    }
    let reason = en ? 'Chained route: retention → gaps → apply.' : 'Rota encadeada: retenção → lacunas → aplicar.';
    if(examId && LearningGoal.label()){
      const r = ReadinessEngine.forExam(LearningGoal.getExam());
      reason = en
        ? `Goal: ${LearningGoal.label()} · readiness ${r?.readiness||0}% · ETA ~${r?.etaDays||'?'} days`
        : `Meta: ${LearningGoal.label()} · prontidão ${r?.readiness||0}% · ETA ~${r?.etaDays||'?'} dias`;
    } else if(gap && gap.acc < 65){
      reason = en
        ? `Gap in ${gap.label} (${gap.acc}%). Reinforcing before forgetting.`
        : `Lacuna em ${gap.label} (${gap.acc}%). Reforço antes do esquecimento.`;
    }
    return { minutes: mins, steps, reason, questionIds, dueCards, simulationId: sim?.id, examId, retention90: LearnerModel.retentionForecast90() };
  },

  buildPlanForExam(examId, minutes=12){
    if(examId) LearningGoal.set({ examId });
    const plan = this.buildPlan(minutes);
    plan.reason = window.I18n?.isEn?.()
      ? `Closing gaps for this track (${plan.steps.length} steps).`
      : `Fechar lacunas desta trilha (${plan.steps.length} passos).`;
    return plan;
  },

  _dueFlashcards(limit, examId){
    const FSRS = window.FSRS;
    if(!FSRS || limit <= 0) return [];
    const now = Date.now();
    let pool = FSRS.questions().map(q=>({ q, p: FSRS.priority(q), c: FSRS.card(q) }))
      .filter(x=> !x.c.reps || x.c.due <= now || x.c.state === 'new');
    if(examId){
      const ids = new Set(window.StorageManager.getExam(examId)?.questionIds || []);
      pool = pool.filter(x=> ids.has(x.q.id));
    }
    return pool.sort((a,b)=>b.p-a.p).slice(0, limit).map(x=>x.q);
  },

  _pickQuestionIds(limit, examId){
    const pool = new Map();
    const add = (q, score)=>{
      if(!q?.id) return;
      if(examId){
        const ids = new Set(window.StorageManager.getExam(examId)?.questionIds || []);
        if(!ids.has(q.id)) return;
      }
      pool.set(q.id, (pool.get(q.id)||0) + score);
    };
    if(window.AITutor) window.AITutor.pickWeak(limit * 3).forEach((q,i)=> add(q, 100-i));
    LearnerModel.illusionLeaders(limit).forEach((x,i)=> add(x.q, 85-i));
    if(window.FSRS){
      const now = Date.now();
      window.FSRS.questions().forEach(q=>{
        const s = window.StorageManager.getStat(q.id);
        if(s.seen && s.due <= now) add(q, 55);
      });
    }
    return [...pool.entries()].sort((a,b)=>b[1]-a[1]).slice(0, limit).map(([id])=>id);
  },

  _nextSimulation(){
    const goal = LearningGoal.getExam();
    const domain = (goal?.materia || goal?.title || '').toLowerCase();
    const list = SimulationEngine.list();
    const prog = LearnerModel.simProgress();
    if(domain.includes('lgpd') || domain.includes('privac')){
      const hit = list.find(s=>s.id==='lgpd_breach_v1' && !prog[s.id]?.completed);
      if(hit) return hit;
    }
    if(domain.includes('cissp') || domain.includes('security')){
      const hit = list.find(s=>s.id==='cissp_incident_v1' && !prog[s.id]?.completed);
      if(hit) return hit;
    }
    if(domain.includes('cipp') || domain.includes('transfer')){
      const hit = list.find(s=>s.id==='cipp_transfer_v1' && !prog[s.id]?.completed);
      if(hit) return hit;
    }
    return list.find(s=>!prog[s.id]?.completed) || list[0] || null;
  },

  execute(plan){
    RouteChainController.start(plan || this.buildPlan());
  }
};

const ColdRetrievalController = {
  KEY: 'ef_cold_last_v1',
  TYPES: ['short', 'matching', 'sequence'],

  shouldOffer(){
    try{
      const last = Number(localStorage.getItem(this.KEY)||0);
      return !last || Date.now() - last > 7 * 86400000;
    }catch(e){ return true; }
  },
  _markDone(){
    try{ localStorage.setItem(this.KEY, String(Date.now())); }catch(e){}
    CompetencyEngine.onColdRetrieval();
  },

  pick(count=5){
    const qs = window.StorageManager.getQuestions().filter(q=> this.TYPES.includes(q.type));
    const scored = qs.map(q=>{
      const s = window.StorageManager.getStat(q.id);
      if(!s.seen) return null;
      const acc = s.correct / s.seen;
      return { q, score: (1-acc)*100 + (window.AITutor?.priority?.(q.id)||0) };
    }).filter(Boolean).sort((a,b)=>b.score-a.score);
    return scored.slice(0, count).map(x=>x.q.id);
  },

  start(){
    const ids = this.pick(5);
    if(!ids.length){
      window.Toast?.show?.(window.I18n?.isEn?.() ? 'Answer more questions first (short/matching/sequence).' : 'Responda mais questões primeiro (curta/relacionar/sequência).', 'warn');
      return;
    }
    this._markDone();
    window.PlayerController?.startStudyRoute?.(ids, window.I18n?.isEn?.() ? 'Cold retrieval — no multiple choice.' : 'Revisão fria — sem múltipla escolha.', { coldRetrieval: true, chainMode: false });
  }
};

const LearningProfileExport = {
  build(){
    return {
      version: 2,
      exportedAt: new Date().toISOString(),
      goal: LearningGoal.get(),
      game: window.StorageManager.getGame(),
      settings: window.StorageManager.getSettings(),
      stats: window.StorageManager.getStats(),
      fsrs: window.FSRS?.all?.() || {},
      metacog: LearnerModel._meta(),
      simProgress: LearnerModel.simProgress(),
      competencies: CompetencyEngine.all(),
      history: window.StorageManager.getHistory().slice(0, 100),
      mastery: window.ProgressAnalytics?.masteryScore?.(),
      retention90: LearnerModel.retentionForecast90()
    };
  },
  download(){
    const blob = new Blob([JSON.stringify(this.build(), null, 2)], { type:'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `velora-profile-${new Date().toISOString().slice(0,10)}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
    window.Toast?.show?.(window.I18n?.isEn?.() ? 'Profile exported.' : 'Perfil exportado.', 'success');
  },
  importFile(file){
    return file.text().then(raw=>{
      const data = JSON.parse(raw);
      if(data.goal) LearningGoal.set(data.goal);
      if(data.metacog) localStorage.setItem(LearnerModel.KEY, JSON.stringify(data.metacog));
      if(data.simProgress) localStorage.setItem(LearnerModel.SIM_KEY, JSON.stringify(data.simProgress));
      if(data.competencies) localStorage.setItem(CompetencyEngine.KEY, JSON.stringify(data.competencies));
      window.Toast?.show?.(window.I18n?.isEn?.() ? 'Profile imported (goal + GPS data).' : 'Perfil importado (meta + dados GPS).', 'success');
    }).catch(()=> window.Toast?.show?.(window.I18n?.isEn?.() ? 'Invalid profile file.' : 'Arquivo de perfil inválido.', 'error'));
  }
};

const GpsUi = {
  openGoalModal(){
    const exams = window.StorageManager.getExams().filter(e=>e.questionIds?.length);
    const goal = LearningGoal.get();
    const en = window.I18n?.isEn?.();
    const opts = exams.map(e=>`<option value="${e.id}" ${goal.examId===e.id?'selected':''}>${window.Util.escapeHtml(e.materia||e.title)}</option>`).join('');
    window.Modal.open({
      title: en ? 'Learning goal' : 'Meta de aprendizagem',
      bodyHtml: `
        <div class="field"><label>${en?'Certification / track':'Certificação / trilha'}</label>
          <select class="select" id="gps-goal-exam"><option value="">${en?'— None —':'— Nenhuma —'}</option>${opts}</select></div>
        <div class="field"><label>${en?'Minutes per day':'Minutos por dia'}</label>
          <select class="select" id="gps-goal-min">${[5,10,15,20,30].map(n=>`<option value="${n}" ${goal.minutesPerDay===n?'selected':''}>${n}</option>`).join('')}</select></div>`,
      footerHtml: `<button class="btn btn-ghost" data-cancel>${en?'Cancel':'Cancelar'}</button><button class="btn btn-primary" data-save>${en?'Save':'Salvar'}</button>`,
      onMount: (el, close)=>{
        el.querySelector('[data-cancel]')?.addEventListener('click', close);
        el.querySelector('[data-save]')?.addEventListener('click', ()=>{
          LearningGoal.set({
            examId: el.querySelector('#gps-goal-exam')?.value || '',
            minutesPerDay: Number(el.querySelector('#gps-goal-min')?.value) || 10
          });
          close();
          window.Toast?.show?.(en?'Goal saved.':'Meta salva.', 'success');
          if(window.App?.instance?.router?.current === 'home') window.App.instance.router.go('home');
          else if(window.App?.instance?.router?.current === 'progress') window.App.instance.router.go('progress');
        });
      }
    });
  }
};

const SimulationEngine = {
  SCENARIOS: {
    lgpd_breach_v1: {
      id: 'lgpd_breach_v1', titlePt: 'LGPD — Vazamento de dados', titleEn: 'LGPD — Data breach', domain: 'LGPD',
      phases: [
        { id:'alert',
          promptPt:'Segunda, 09:14. Acesso não autorizado a planilha com 12.000 e-mails e CPFs. Diretor pede "resolver sem alarde". Primeira ação?',
          promptEn:'Unauthorized access to 12,000 emails and IDs. Director says "handle quietly". First action?',
          choices:[
            { id:'a', textPt:'Acionar comitê de incidentes e contenção técnica', textEn:'Activate incident team and containment', score:100, feedbackPt:'Art. 48 LGPD: contenção e registro antes de comunicação externa.', feedbackEn:'Contain and record before external comms.' },
            { id:'b', textPt:'Aguardar jurídico antes de qualquer registro', textEn:'Wait for legal before any record', score:20, feedbackPt:'Atraso aumenta risco regulatório.', feedbackEn:'Delay increases regulatory risk.' },
            { id:'c', textPt:'Apagar logs', textEn:'Delete logs', score:0, feedbackPt:'Destruir evidências agrava o incidente.', feedbackEn:'Destroying evidence worsens the case.' }
          ]},
        { id:'anpd',
          promptPt:'Risco relevante aos titulares. Quando comunicar a ANPD?',
          promptEn:'Relevant risk to subjects. When to notify the ANPD?',
          choices:[
            { id:'a', textPt:'Prazo razoável (≈2 dias úteis na prática)', textEn:'Reasonable timeframe (~2 business days)', score:90, feedbackPt:'Alinhado à orientação ANPD.', feedbackEn:'Aligned with ANPD guidance.' },
            { id:'b', textPt:'Só se houver multa iminente', textEn:'Only if fine is imminent', score:10, feedbackPt:'Depende do risco, não da multa.', feedbackEn:'Depends on risk, not fines.' },
            { id:'c', textPt:'Nunca se criptografado', textEn:'Never if encrypted', score:40, feedbackPt:'Criptografia não elimina o dever de avaliar.', feedbackEn:'Encryption does not remove duty to assess.' }
          ]},
        { id:'titulares',
          promptPt:'Titulares devem ser informados?',
          promptEn:'Should data subjects be informed?',
          choices:[
            { id:'a', textPt:'Sim, com clareza e canais de contato', textEn:'Yes, clearly with contact channels', score:100, feedbackPt:'Transparência central na LGPD.', feedbackEn:'Transparency is central under LGPD.' },
            { id:'b', textPt:'Não, para evitar pânico', textEn:'No, to avoid panic', score:15, feedbackPt:'Omissão amplia sanções.', feedbackEn:'Omission increases sanctions.' },
            { id:'c', textPt:'Só nas redes sociais', textEn:'Social media only', score:50, feedbackPt:'Comunicação deve ser direta ao titular.', feedbackEn:'Must be direct to subjects.' }
          ]}
      ]
    },
    cissp_incident_v1: {
      id: 'cissp_incident_v1', titlePt: 'CISSP — Resposta a incidente', titleEn: 'CISSP — Incident response', domain: 'CISSP',
      phases: [
        { id:'detect',
          promptPt:'SIEM alerta: lateral movement em servidor crítico. Qual fase NIST IR primeiro?',
          promptEn:'SIEM: lateral movement on critical server. First NIST IR phase?',
          choices:[
            { id:'a', textPt:'Contenção — isolar host e preservar evidências', textEn:'Containment — isolate and preserve evidence', score:100, feedbackPt:'Contenção limita blast radius.', feedbackEn:'Containment limits blast radius.' },
            { id:'b', textPt:'Erradicar malware imediatamente', textEn:'Eradicate malware immediately', score:30, feedbackPt:'Sem contenção, eradicar pode destruir evidências.', feedbackEn:'Eradication without containment loses evidence.' },
            { id:'c', textPt:'Comunicar imprensa', textEn:'Notify press', score:0, feedbackPt:'Comunicação vem após triagem.', feedbackEn:'Comms follow triage.' }
          ]},
        { id:'evidence',
          promptPt:'Forense precisa de logs. O que garantir?',
          promptEn:'Forensics needs logs. What to ensure?',
          choices:[
            { id:'a', textPt:'Chain of custody e imagem forense imutável', textEn:'Chain of custody and immutable forensic image', score:100, feedbackPt:'Integridade probatória.', feedbackEn:'Evidentiary integrity.' },
            { id:'b', textPt:'Reiniciar servidor para limpar', textEn:'Reboot server to clean', score:0, feedbackPt:'Reboot destrói volátil.', feedbackEn:'Reboot destroys volatile evidence.' },
            { id:'c', textPt:'Apagar contas comprometidas', textEn:'Delete compromised accounts', score:40, feedbackPt:'Preservar antes de remover.', feedbackEn:'Preserve before removal.' }
          ]},
        { id:'recover',
          promptPt:'Contenção ok. Próximo passo?',
          promptEn:'Containment done. Next step?',
          choices:[
            { id:'a', textPt:'Recuperação controlada + lições aprendidas', textEn:'Controlled recovery + lessons learned', score:100, feedbackPt:'Fecha ciclo IR.', feedbackEn:'Closes IR cycle.' },
            { id:'b', textPt:'Voltar ao normal sem revisão', textEn:'Return to normal without review', score:20, feedbackPt:'Post-incident review é essencial.', feedbackEn:'Post-incident review is essential.' },
            { id:'c', textPt:'Pagar resgate se ransomware', textEn:'Pay ransom if ransomware', score:10, feedbackPt:'Política organizacional prevalece; não padrão.', feedbackEn:'Policy-driven; not default best practice.' }
          ]}
      ]
    },
    cipp_transfer_v1: {
      id: 'cipp_transfer_v1', titlePt: 'CIPP/E — Transferência internacional', titleEn: 'CIPP/E — Cross-border transfer', domain: 'CIPP/E',
      phases: [
        { id:'mechanism',
          promptPt:'Empresa EU envia dados de RH para processor nos EUA sem adequação. Mecanismo mais adequado?',
          promptEn:'EU HR data to US processor without adequacy. Best mechanism?',
          choices:[
            { id:'a', textPt:'SCCs + TIA + medidas suplementares se necessário', textEn:'SCCs + TIA + supplementary measures', score:100, feedbackPt:'Padrão pós-Schrems II.', feedbackEn:'Post-Schrems II standard.' },
            { id:'b', textPt:'Consentimento genérico no contrato', textEn:'Generic consent in contract', score:15, feedbackPt:'Consent rarely suffices for systematic transfers.', feedbackEn:'Consent rarely suffices.' },
            { id:'c', textPt:'Nenhum — cloud global isenta', textEn:'None — global cloud exempts', score:0, feedbackPt:'Transferência exige base legal.', feedbackEn:'Transfers require legal basis.' }
          ]},
        { id:'tia',
          promptPt:'TIA identifica risco de acesso governamental. Ação?',
          promptEn:'TIA shows government access risk. Action?',
          choices:[
            { id:'a', textPt:'Medidas suplementares (criptografia, pseudonimização, auditoria)', textEn:'Supplementary measures (encryption, pseudonymization)', score:100, feedbackPt:'Schrems II exige mitigação real.', feedbackEn:'Schrems II requires real mitigation.' },
            { id:'b', textPt:'Ignorar — SLA do vendor basta', textEn:'Ignore — vendor SLA enough', score:10, feedbackPt:'SLA não substitui TIA.', feedbackEn:'SLA does not replace TIA.' },
            { id:'c', textPt:'Parar transferência', textEn:'Stop transfer', score:70, feedbackPt:'Válido se risco não mitigável.', feedbackEn:'Valid if risk cannot be mitigated.' }
          ]},
        { id:'dpa',
          promptPt:'Cláusulas do DPA com processor devem incluir?',
          promptEn:'Processor DPA must include?',
          choices:[
            { id:'a', textPt:'Subprocessadores, auditoria, deleção pós-contrato, assistência DSR', textEn:'Subprocessors, audit, deletion, DSR assistance', score:100, feedbackPt:'Art. 28 GDPR essentials.', feedbackEn:'Art. 28 GDPR essentials.' },
            { id:'b', textPt:'Apenas preço e uptime', textEn:'Price and uptime only', score:0, feedbackPt:'DPA não é contrato comercial puro.', feedbackEn:'DPA is not purely commercial.' },
            { id:'c', textPt:'Indemnity ilimitada só', textEn:'Unlimited indemnity only', score:25, feedbackPt:'Insuficiente para conformidade.', feedbackEn:'Insufficient for compliance.' }
          ]}
      ]
    }
  },

  list(){
    const en = window.I18n?.isEn?.();
    return Object.values(this.SCENARIOS).map(s=>({ id:s.id, title: en?s.titleEn:s.titlePt, domain:s.domain }));
  },
  get(id){ return this.SCENARIOS[id] || null; },
  isDone(id){ return !!LearnerModel.simProgress()[id]?.completed; },

  start(id, opts={}){
    const scenario = this.get(id);
    const ToastRef = window.Toast, ModalRef = window.Modal, UtilRef = window.Util;
    if(!scenario){ ToastRef?.show?.('Simulação não encontrada.', 'warn'); return; }
    const en = window.I18n?.isEn?.();
    let phaseIdx = 0, scoreSum = 0, choices = [];

    const onComplete = ()=>{
      if(opts.chainMode) RouteChainController.onStepDone('simulation');
    };

    const render = ()=>{
      const phase = scenario.phases[phaseIdx];
      if(!phase){
        const pct = Math.round(scoreSum / scenario.phases.length);
        LearnerModel.saveSimProgress(scenario.id, { completed:true, score:pct, choices });
        ModalRef.open({
          title: en ? scenario.titleEn : scenario.titlePt,
          bodyHtml: en ? `<p><strong>${pct}%</strong> — Simulation saved.</p>` : `<p><strong>${pct}%</strong> — Simulação salva.</p>`,
          footerHtml: `<button class="btn btn-primary" data-close type="button">${en?'Continue':'Continuar'}</button>`,
          onMount: (el, close)=> el.querySelector('[data-close]')?.addEventListener('click', ()=>{ close(); ToastRef?.show?.(en?'Done.':'Concluído.', 'success'); onComplete(); })
        });
        return;
      }
      const prompt = en ? phase.promptEn : phase.promptPt;
      const choiceHtml = phase.choices.map(c=>`
        <button type="button" class="btn btn-sm" style="display:block;width:100%;text-align:left;margin-bottom:8px;white-space:normal;height:auto;padding:10px 12px" data-sim-choice="${c.id}">
          ${UtilRef.escapeHtml(en ? c.textEn : c.textPt)}
        </button>`).join('');
      ModalRef.open({
        title: `${en ? scenario.titleEn : scenario.titlePt} · ${phaseIdx+1}/${scenario.phases.length}`,
        wide: true,
        bodyHtml: `<p style="line-height:1.55;margin-bottom:12px">${UtilRef.escapeHtml(prompt)}</p>${choiceHtml}`,
        onMount: (el, close)=>{
          el.querySelectorAll('[data-sim-choice]').forEach(btn=>{
            btn.addEventListener('click', ()=>{
              const c = phase.choices.find(x=>x.id===btn.dataset.simChoice);
              if(!c) return;
              scoreSum += c.score;
              choices.push({ phase: phase.id, choice: c.id, score: c.score });
              close();
              ModalRef.open({
                title: en ? 'Debrief' : 'Debriefing',
                bodyHtml: `<p style="line-height:1.55">${UtilRef.escapeHtml(en ? c.feedbackEn : c.feedbackPt)}</p>`,
                footerHtml: `<button class="btn btn-primary" data-next type="button">${en?'Next':'Próxima'}</button>`,
                onMount: (el2, close2)=> el2.querySelector('[data-next]')?.addEventListener('click', ()=>{ close2(); phaseIdx++; render(); })
              });
            });
          });
        }
      });
    };
    render();
  }
};

if(typeof window !== 'undefined'){
  Object.assign(window, {
    LearningGoal, LearnerModel, ReadinessEngine, RouteOptimizer, RouteChainController,
    SimulationEngine, CompetencyEngine, ColdRetrievalController, LearningProfileExport, GpsUi
  });
}
