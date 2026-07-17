'use strict';
/* Velora GPS v1 — Learner Model · Route Optimizer · Readiness · Simulations */

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
    const meta = this._meta()[q.id] || { samples:0, avgConfidence:0, illusion:0 };
    return { mastery, retentionRisk, overdueDays, seen: s.seen||0, illusion: meta.illusion||0, avgConfidence: meta.avgConfidence||0 };
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
    row.illusion = row.wrongSamples
      ? Math.round((row.sumConfWrong / row.wrongSamples) * 20)
      : 0;
    m[qid] = row;
    this._saveMeta(m);
  },

  illusionLeaders(limit=8){
    const qs = this._sm().getQuestions();
    return qs
      .map(q=>{ const ns = this.nodeState(q); return { q, ...ns }; })
      .filter(x=>x.seen >= 2 && x.illusion >= 60)
      .sort((a,b)=>b.illusion - a.illusion)
      .slice(0, limit);
  },

  aggregateMetacog(){
    const m = this._meta();
    let highConfWrong = 0, samples = 0;
    Object.values(m).forEach(r=>{
      samples += r.samples||0;
      highConfWrong += r.wrongSamples||0;
    });
    return { samples, highConfWrong, illusionRate: samples ? Math.round(highConfWrong / samples * 100) : 0 };
  },

  simProgress(){
    try{ return JSON.parse(localStorage.getItem(this.SIM_KEY)||'{}'); }catch(e){ return {}; }
  },
  saveSimProgress(id, data){
    const all = this.simProgress();
    all[id] = { ...(all[id]||{}), ...data, updatedAt: new Date().toISOString() };
    try{ localStorage.setItem(this.SIM_KEY, JSON.stringify(all)); }catch(e){}
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
    const avgRisk = total ? Math.round(riskSum / total) : 0;
    const etaDays = this._etaDays(exam, mastered, total);
    return {
      examId: exam.id,
      title: exam.title,
      materia: exam.materia || exam.title,
      readiness,
      mastered,
      total,
      seenPct: Math.round((seen / total) * 100),
      avgRisk,
      etaDays,
      passScore: exam.passScore || 70
    };
  },

  _etaDays(exam, mastered, total){
    const remaining = Math.max(0, total - mastered);
    if(!remaining) return 0;
    const hist = window.StorageManager.getHistory().filter(h=>h.examId===exam.id && h.sessionKind !== 'flashcards');
    const last14 = hist.filter(h=> Date.now() - new Date(h.date).getTime() < 14 * 86400000);
    let velocity = 0;
    if(last14.length >= 2){
      const gain = last14.reduce((s,h)=> s + (h.correctCount||0), 0) / last14.length;
      velocity = Math.max(0.5, gain * 0.15);
    } else {
      velocity = 1.2;
    }
    return Math.max(1, Math.ceil(remaining / velocity));
  },

  topTracks(limit=6){
    return window.StorageManager.getExams()
      .filter(e=>e.questionIds?.length)
      .map(e=>this.forExam(e))
      .filter(Boolean)
      .sort((a,b)=>a.readiness - b.readiness)
      .slice(0, limit);
  }
};

const RouteOptimizer = {
  buildPlan(minutes=10){
    const en = window.I18n?.isEn?.();
    const qCount = Math.max(5, Math.round(minutes * 0.9));
    const fcCount = Math.min(6, Math.max(0, Math.round(minutes * 0.35)));
    const dueCards = this._dueFlashcards(fcCount);
    const questionIds = this._pickQuestionIds(qCount);
    const sim = this._nextSimulation();
    const gap = window.ProgressAnalytics?.topGap?.();
    const steps = [];
    if(dueCards.length){
      steps.push({
        type:'flashcards',
        count: dueCards.length,
        label: en ? `${dueCards.length} FSRS cards due` : `${dueCards.length} cards FSRS vencidos`
      });
    }
    if(questionIds.length){
      steps.push({
        type:'questions',
        count: questionIds.length,
        ids: questionIds,
        label: en ? `${questionIds.length} gap questions` : `${questionIds.length} questões de lacuna`
      });
    }
    if(sim){
      steps.push({
        type:'simulation',
        id: sim.id,
        label: sim.title
      });
    }
    let reason = en ? 'Balanced route: retention + gaps + practice.' : 'Rota equilibrada: retenção + lacunas + prática.';
    if(gap && gap.acc < 65){
      reason = en
        ? `Priority gap in ${gap.label} (${gap.acc}%). Reinforcing before you forget.`
        : `Lacuna prioritária em ${gap.label} (${gap.acc}%). Reforço antes do esquecimento.`;
    } else if(dueCards.length && !questionIds.length){
      reason = en ? 'FSRS cards are due — quick retention win.' : 'Cards FSRS vencidos — retenção rápida.';
    } else if(sim && !SimulationEngine.isDone(sim.id)){
      reason = en ? 'Apply knowledge in a decision scenario.' : 'Aplique o conhecimento em um cenário de decisão.';
    }
    return { minutes, steps, reason, questionIds, dueCards, simulationId: sim?.id };
  },

  _dueFlashcards(limit){
    const FSRS = window.FSRS;
    if(!FSRS || limit <= 0) return [];
    const now = Date.now();
    return FSRS.questions()
      .map(q=>({ q, p: FSRS.priority(q), c: FSRS.card(q) }))
      .filter(x=> !x.c.reps || x.c.due <= now || x.c.state === 'new')
      .sort((a,b)=>b.p-a.p)
      .slice(0, limit)
      .map(x=>x.q);
  },

  _pickQuestionIds(limit){
    const pool = new Map();
    const add = (q, score)=>{
      if(!q?.id) return;
      pool.set(q.id, (pool.get(q.id)||0) + score);
    };
    if(window.AITutor){
      window.AITutor.pickWeak(limit * 2).forEach((q,i)=> add(q, 100 - i));
    }
    LearnerModel.illusionLeaders(limit).forEach((x,i)=> add(x.q, 80 - i));
    if(window.FSRS){
      const now = Date.now();
      window.FSRS.questions().forEach(q=>{
        const s = window.StorageManager.getStat(q.id);
        if(s.seen && s.due <= now) add(q, 60);
      });
    }
    return [...pool.entries()]
      .sort((a,b)=>b[1]-a[1])
      .slice(0, limit)
      .map(([id])=>id);
  },

  _nextSimulation(){
    const list = SimulationEngine.list();
    const prog = LearnerModel.simProgress();
    return list.find(s=>!prog[s.id]?.completed) || list[0] || null;
  },

  execute(plan){
    if(!plan) plan = this.buildPlan(10);
    if(plan.dueCards?.length && window.FlashcardController){
      window.FlashcardController.start(plan.dueCards.length, { scope:'all', questionIds: plan.dueCards.map(q=>q.id) });
      return;
    }
    if(plan.questionIds?.length && window.PlayerController){
      window.PlayerController.startStudyRoute(plan.questionIds, plan.reason);
      return;
    }
    if(plan.simulationId && window.SimulationEngine){
      window.SimulationEngine.start(plan.simulationId);
      return;
    }
    window.PlayerController?.startStudyNow?.(10);
  }
};

const SimulationEngine = {
  SCENARIOS: {
    lgpd_breach_v1: {
      id: 'lgpd_breach_v1',
      titlePt: 'LGPD — Vazamento de dados',
      titleEn: 'LGPD — Data breach',
      domain: 'LGPD',
      phases: [
        {
          id: 'alert',
          promptPt: 'Segunda, 09:14. O time de infra detectou acesso não autorizado a uma planilha com 12.000 e-mails e CPFs de clientes. O diretor pede para "resolver sem alarde". Qual é sua primeira ação como DPO/responsável?',
          promptEn: 'Monday, 9:14 AM. Infra detected unauthorized access to a spreadsheet with 12,000 customer emails and IDs. The director asks to "handle it quietly". What is your first action as DPO?',
          choices: [
            { id:'a', textPt:'Acionar imediatamente o comitê de incidentes e iniciar contenção técnica', textEn:'Immediately activate the incident committee and start technical containment', score:100, feedbackPt:'Correto: Art. 48 LGPD exige tratamento estruturado; contenção e registro vêm antes de comunicação externa.', feedbackEn:'Correct: structured incident handling and containment before external comms.' },
            { id:'b', textPt:'Aguardar confirmação jurídica antes de qualquer registro interno', textEn:'Wait for legal confirmation before any internal record', score:20, feedbackPt:'Atrasar registro aumenta risco regulatório e dificulta prova de diligência.', feedbackEn:'Delaying records increases regulatory risk.' },
            { id:'c', textPt:'Apagar os logs para reduzir exposição', textEn:'Delete logs to reduce exposure', score:0, feedbackPt:'Destruir evidências agrava o incidente e pode caracterizar má-fé.', feedbackEn:'Destroying evidence worsens the incident.' }
          ]
        },
        {
          id: 'anpd',
          promptPt: 'Contenção feita. Análise preliminar indica risco relevante aos titulares. Prazo para comunicar a ANPD?',
          promptEn: 'Containment done. Preliminary analysis shows relevant risk to data subjects. Deadline to notify the ANPD?',
          choices: [
            { id:'a', textPt:'Comunicação em prazo razoável — orientação ANPD: em até 2 dias úteis na prática operacional', textEn:'Reasonable timeframe — ANPD guidance: often within ~2 business days operationally', score:90, feedbackPt:'Boa prática alinhada à orientação ANPD para incidentes relevantes.', feedbackEn:'Aligned with ANPD guidance for relevant incidents.' },
            { id:'b', textPt:'Somente se houver multa iminente', textEn:'Only if a fine is imminent', score:10, feedbackPt:'A comunicação não depende de multa — depende de risco ao titular.', feedbackEn:'Notification depends on risk, not on fines.' },
            { id:'c', textPt:'Nunca comunicar se os dados eram criptografados', textEn:'Never notify if data was encrypted', score:40, feedbackPt:'Criptografia reduz risco mas não elimina automaticamente o dever de avaliar e comunicar.', feedbackEn:'Encryption reduces risk but does not automatically remove duty to assess.' }
          ]
        },
        {
          id: 'titulares',
          promptPt: 'ANPD notificada. Titulares devem ser informados?',
          promptEn: 'ANPD notified. Should data subjects be informed?',
          choices: [
            { id:'a', textPt:'Sim, de forma clara, com medidas de mitigação e canais de contato', textEn:'Yes, clearly, with mitigation measures and contact channels', score:100, feedbackPt:'Transparência ao titular é central na LGPD e reduz dano reputacional.', feedbackEn:'Transparency to data subjects is central under LGPD.' },
            { id:'b', textPt:'Não, para evitar pânico', textEn:'No, to avoid panic', score:15, feedbackPt:'Omissão viola princípios e pode ampliar sanções.', feedbackEn:'Omission violates principles and may increase sanctions.' },
            { id:'c', textPt:'Publicar apenas nas redes sociais da empresa', textEn:'Post only on company social media', score:50, feedbackPt:'Comunicação deve ser direta e adequada ao titular afetado.', feedbackEn:'Communication should be direct and appropriate to affected subjects.' }
          ]
        }
      ]
    }
  },

  list(){
    const en = window.I18n?.isEn?.();
    return Object.values(this.SCENARIOS).map(s=>({
      id: s.id,
      title: en ? s.titleEn : s.titlePt,
      domain: s.domain
    }));
  },

  get(id){ return this.SCENARIOS[id] || null; },

  isDone(id){
    return !!LearnerModel.simProgress()[id]?.completed;
  },

  start(id){
    const scenario = this.get(id);
    const ToastRef = window.Toast;
    const ModalRef = window.Modal;
    const UtilRef = window.Util;
    if(!scenario){ ToastRef?.show?.('Simulação não encontrada.', 'warn'); return; }
    const en = window.I18n?.isEn?.();
    let phaseIdx = 0;
    let scoreSum = 0;
    let choices = [];

    const render = ()=>{
      const phase = scenario.phases[phaseIdx];
      if(!phase){
        const pct = Math.round(scoreSum / scenario.phases.length);
        LearnerModel.saveSimProgress(scenario.id, { completed:true, score:pct, choices });
        const body = en
          ? `<p><strong>Simulation complete — ${pct}%</strong></p><p>You practiced decision-making under pressure. Review weak choices in Progress.</p>`
          : `<p><strong>Simulação concluída — ${pct}%</strong></p><p>Você praticou tomada de decisão sob pressão. Revise escolhas fracas em Progresso.</p>`;
        ModalRef.open({
          title: en ? scenario.titleEn : scenario.titlePt,
          bodyHtml: body,
          footerHtml: `<button class="btn btn-primary" data-close type="button">${en?'Continue':'Continuar'}</button>`,
          onMount: (el, close)=> el.querySelector('[data-close]')?.addEventListener('click', ()=>{ close(); ToastRef?.show?.(en?'Simulation saved.':'Simulação salva.', 'success'); })
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
              const fb = en ? c.feedbackEn : c.feedbackPt;
              ModalRef.open({
                title: en ? 'Debrief' : 'Debriefing',
                bodyHtml: `<p style="line-height:1.55">${UtilRef.escapeHtml(fb)}</p>`,
                footerHtml: `<button class="btn btn-primary" data-next type="button">${en?'Next':'Próxima'}</button>`,
                onMount: (el2, close2)=>{
                  el2.querySelector('[data-next]')?.addEventListener('click', ()=>{ close2(); phaseIdx++; render(); });
                }
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
  window.LearnerModel = LearnerModel;
  window.ReadinessEngine = ReadinessEngine;
  window.RouteOptimizer = RouteOptimizer;
  window.SimulationEngine = SimulationEngine;
}
