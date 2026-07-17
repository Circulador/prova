#!/usr/bin/env python3
"""Replace ExinDPOSeeder block in index.html with GlobalDPOSeeder."""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent

SEEDER_BLOCK = r'''/* =========================================================================
   DPO GLOBAL — tracks by region (loaded from data/dpo-global-bank.js)
   ========================================================================= */
class BankHelpers {
  static mkOpts(list, correctIdx, listPt=null){
    const pt = listPt || list;
    return list.map((text,i)=>({
      id:Util.uid('opt'),
      text: pt[i] || text,
      textEn: text,
      textPt: pt[i] || text,
      correct:i===correctIdx
    }));
  }
  static qBilingual(stemEn, stemPt, optsEn, optsPt, correctIdx, explEn, explPt, submateria, level='medio'){
    return {
      type:'single',
      text: stemPt || stemEn,
      stemEn, stemPt,
      options: this.mkOpts(optsEn, correctIdx, optsPt),
      explanation: explPt || explEn,
      explanationEn: explEn,
      explanationPt: explPt,
      submateria, level
    };
  }
  static q(text, options, correctIdx, explanation, submateria, level='medio'){
    return {type:'single', text, options, explanation, submateria, level};
  }
}

class QuestionDisplay {
  static mode(settings){
    return settings?.bilingualMode || 'dual';
  }
  static stem(q, settings){
    const en = q.stemEn || q.text || '';
    const pt = q.stemPt || q.text || en;
    const m = this.mode(settings);
    if(m === 'en') return en;
    if(m === 'pt') return pt;
    return en && pt && en !== pt ? en + '\\n\\n— ' + pt : (pt || en);
  }
  static optionLabel(opt, settings){
    const en = opt.textEn || opt.text || '';
    const pt = opt.textPt || opt.text || en;
    const m = this.mode(settings);
    if(m === 'en') return en;
    if(m === 'pt') return pt;
    return en && pt && en !== pt ? en + ' / ' + pt : (pt || en);
  }
  static explanation(q, settings){
    const en = q.explanationEn || q.explanation || '';
    const pt = q.explanationPt || q.explanation || en;
    const m = this.mode(settings);
    if(m === 'en') return en;
    if(m === 'pt') return pt;
    return pt && en && en !== pt ? en + '\\n\\n— ' + pt : (pt || en);
  }
}

class SessionConfig {
  constructor(data={}){
    this.examId = data.examId || '';
    this.candidateName = data.candidateName || '';
    this.questionIds = data.questionIds || [];
    this.trainingMode = !!data.trainingMode;
    this.timerOn = data.timerOn !== false;
    this.timeMinutes = data.timeMinutes ?? 60;
    this.configMode = data.configMode || 'full';
    this.preset = data.preset || null;
    this.excludeMastered = !!data.excludeMastered;
    this.excludeToday = !!data.excludeToday;
    this.unseenOnly = !!data.unseenOnly;
    this.shuffleQuestions = data.shuffleQuestions !== false;
    this.shuffleAlternatives = !!data.shuffleAlternatives;
    this.preSubmitReview = data.preSubmitReview !== false;
  }
  toPlayerConfig(){
    return {
      examId: this.examId,
      candidateName: this.candidateName,
      questionIds: this.questionIds,
      trainingMode: this.trainingMode,
      timerOn: this.timerOn,
      timeMinutes: this.timeMinutes,
      configMode: this.configMode,
      preset: this.preset,
      shuffleQuestions: this.shuffleQuestions,
      shuffleAlternatives: this.shuffleAlternatives,
      preSubmitReview: this.preSubmitReview
    };
  }
}

class DataCleanup {
  static FLAG = 'ef_cleanup_global_dpo_v2';
  static run(){
    if(localStorage.getItem(this.FLAG)) return;
    const em2Exam = e => /^(EM2-)/.test(e.code||'') || e.serie==='2º Ano EM' || (e.tags||[]).includes('2º Ano EM');
    const cyber = /ciber|cyber|CYBER-/i;
    const legacyExam = e => {
      if(/^(CYBER-|HIST-RF-50)/.test(e.code||'')) return true;
      if(cyber.test([e.category,e.title,e.code,...(e.tags||[])].join(' '))) return true;
      if(em2Exam(e)) return true;
      if((e.trilha||'').includes('Trilha DPO — EXIN') && !e.region) return true;
      if(/^EXIN-/.test(e.code||'') && !e.region) return true;
      return false;
    };
    const em2Q = q => (q.tags||[]).includes('2º Ano EM') || /^EM2-/.test(q.category||'');
    const legacyQ = q => {
      if(em2Q(q)) return true;
      const blob = [q.category,q.materia,q.submateria,...(q.tags||[]),q.text].join(' ');
      if(cyber.test(blob)) return true;
      if((q.tags||[]).includes('Trilha DPO — EXIN') && !q.stemEn) return true;
      return false;
    };
    const qs = StorageManager.getQuestions().filter(q=>!legacyQ(q));
    StorageManager.saveQuestions(qs);
    const kept = new Set(qs.map(q=>q.id));
    const exams = StorageManager.getExams().filter(e=>!legacyExam(e)).map(e=>({...e, questionIds:(e.questionIds||[]).filter(id=>kept.has(id))}));
    StorageManager.saveExams(exams);
    ['ef_demo_seeded_v1','ef_french_rev_seeded_v2','ef_cleanup_em2_v1','ef_cleanup_em2_v2','ef_em2_seeded_v1','ef_exin_dpo_seeded_v1','ef_cleanup_exin_dpo_v1','ef_global_dpo_seeded_v2'].forEach(k=>localStorage.removeItem(k));
    localStorage.setItem(this.FLAG,'1');
  }
}

class BankHierarchy {
  static groupByExam(){
    const exams = StorageManager.getExams().filter(e=>e.questionIds?.length);
    const qmap = Object.fromEntries(StorageManager.getQuestions().map(q=>[q.id,q]));
    const used = new Set();
    const byTrilha = {};
    exams.forEach(ex=>{
      const qs = ex.questionIds.map(id=>qmap[id]).filter(Boolean);
      qs.forEach(q=>used.add(q.id));
      const trilha = ex.trilha || ex.serie || ex.category || 'Outros';
      byTrilha[trilha] = byTrilha[trilha] || [];
      byTrilha[trilha].push({exam:ex, submaterias:this._bySubmateria(qs)});
    });
    const tree = Object.entries(byTrilha).sort((a,b)=>a[0].localeCompare(b[0],'pt-BR')).map(([trilha,certs])=>({trilha,certs}));
    const orphan = StorageManager.getQuestions().filter(q=>!used.has(q.id));
    if(orphan.length) tree.push({trilha:'Sem trilha', certs:[{exam:{id:'_orphan',title:'Sem prova vinculada',questionIds:[]}, submaterias:this._bySubmateria(orphan)}]});
    return tree;
  }
  static _bySubmateria(qs){
    const map = {};
    qs.forEach(q=>{
      const s = q.submateria || q.category || 'Geral';
      map[s] = map[s] || [];
      map[s].push(q);
    });
    return Object.entries(map).sort((a,b)=>a[0].localeCompare(b[0],'pt-BR')).map(([submateria,questions])=>({submateria,questions}));
  }
  static count(qs){ return qs.length; }
}

class GlobalDPOSeeder {
  static FLAG_KEY = 'ef_global_dpo_seeded_v2';
  static get BANK(){ return typeof DPO_GLOBAL_BANK !== 'undefined' ? DPO_GLOBAL_BANK : null; }
  static get TRACKS(){ return this.BANK?.tracks || []; }
  static TRILHA_DESC = "Trilha global de Encarregado de Dados — certificações por continente, ludic e bilingue EN/PT.";

  static trilhaLabel(cert){
    const track = this.TRACKS.find(t=>t.id===cert.trackId || t.region===cert.region);
    return track ? `${track.name} — DPO` : 'Global — DPO';
  }

  static _normalizeOpts(raw){
    if(raw.options?.length) return raw.options.map(o=>({
      id: Util.uid('opt'),
      text: o.text || o.textPt || o.textEn || '',
      textEn: o.textEn || (raw.optionsEn && raw.optionsEn.find(x=>x.text===o.text)?.text) || o.text,
      textPt: o.textPt || o.text,
      correct: !!o.correct
    }));
    const en = raw.optionsEn || [];
    const pt = raw.optionsPt || en;
    const correctIdx = en.findIndex(o=>o.correct);
    return BankHelpers.mkOpts(en.map(o=>o.text), correctIdx >= 0 ? correctIdx : 0, pt.map(o=>o.text));
  }

  static _normalizeQuestion(raw, cert, submateria){
    const stemEn = raw.stemEn || raw.text || '';
    const stemPt = raw.stemPt || raw.text || stemEn;
    return {
      type: raw.type || 'single',
      text: stemPt || stemEn,
      stemEn, stemPt,
      options: this._normalizeOpts(raw),
      explanation: raw.explanationPt || raw.explanation || raw.explanationEn || '',
      explanationEn: raw.explanationEn || raw.explanation || '',
      explanationPt: raw.explanationPt || raw.explanation || '',
      level: raw.level || 'medio',
      materia: cert.materia,
      submateria,
      category: submateria,
      tags: [this.trilhaLabel(cert), cert.materia, cert.code, submateria, cert.region || 'global']
    };
  }

  static seed(){
    if(localStorage.getItem(this.FLAG_KEY)) return;
    const bank = this.BANK;
    if(!bank?.certifications?.length){
      console.warn('[GlobalDPOSeeder] DPO_GLOBAL_BANK not loaded');
      return;
    }
    DataCleanup.run();
    bank.certifications.forEach(cert=>{
      const domains = cert.domains || cert.submaterias || {};
      const qs = [];
      Object.entries(domains).forEach(([submateria, items])=>{
        (items || []).forEach(raw=>{
          qs.push(new Question(this._normalizeQuestion(raw, cert, submateria)));
        });
      });
      qs.forEach(q => StorageManager.upsertQuestion(q));
      const trilha = this.trilhaLabel(cert);
      const exam = new Exam({
        title: cert.title,
        description: cert.description || '',
        category: trilha,
        trilha,
        region: cert.region || 'global',
        trackId: cert.trackId || cert.region || 'global',
        materia: cert.materia,
        serie: trilha,
        code: cert.code,
        org: cert.org || '',
        language: 'dual',
        timeMinutes: cert.timeMinutes || 60,
        passScore: 70,
        author: 'Velora',
        version: bank.version || '2.0',
        tags: [trilha, cert.materia, 'certificação', cert.org || '', cert.region || 'global'],
        questionIds: qs.map(q => q.id),
        stub: !!cert.stub
      });
      StorageManager.upsertExam(exam);
    });
    localStorage.setItem(this.FLAG_KEY, '1');
  }

  /** Dev helper: localStorage.removeItem('ef_global_dpo_seeded_v2') then reload */
  static resetFlag(){ localStorage.removeItem(this.FLAG_KEY); }
}
'''

SCRIPT_TAG = '<script src="data/dpo-global-bank.js"></script>\n<script>'


def patch_file(path: pathlib.Path):
    html = path.read_text(encoding='utf-8')

    # Add external bank script
    if 'dpo-global-bank.js' not in html:
        html = html.replace('<script>', SCRIPT_TAG, 1)

    # Replace seeder block
    pattern = r"/\* =+\s*\n\s*TRILHA DPO — EXIN.*?\nclass BankHelpers \{.*?\nclass ExinDPOSeeder \{.*?\n\}\n"
    if not re.search(pattern, html, flags=re.DOTALL):
        pattern = r"/\* =+\s*\n\s*DPO GLOBAL — tracks.*?\nclass BankHelpers \{.*?\nclass GlobalDPOSeeder \{.*?\n\}\n"
    html = re.sub(pattern, SEEDER_BLOCK, html, count=1, flags=re.DOTALL)

    html = html.replace('ExinDPOSeeder.seed()', 'GlobalDPOSeeder.seed()')
    html = html.replace('ExinDPOSeeder.TRILHA_DESC', 'GlobalDPOSeeder.TRILHA_DESC')
    html = html.replace('ExinDPOSeeder.TRILHA', 'GlobalDPOSeeder.trilhaLabel')
    # Fix bad replace for trilhaLabel call - revert static refs
    html = html.replace('GlobalDPOSeeder.trilhaLabel||', 'GlobalDPOSeeder.TRILHA_DESC||')
    html = html.replace("GlobalDPOSeeder.trilhaLabel || 'Trilha DPO — EXIN'", "GlobalDPOSeeder.TRILHA_DESC.split('—')[0].trim() + '— DPO'")

    path.write_text(html, encoding='utf-8')
    print(f"Patched {path.name}")


def main():
    for name in ('index.html', '404.html'):
        patch_file(ROOT / name)


if __name__ == '__main__':
    main()
