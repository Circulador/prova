#!/usr/bin/env python3
"""Gera EnsinoMedio2Seeder e aplica em index.html / 404.html."""
import json, re, pathlib

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "em2_bank_data.json"

def js_str(s):
    return json.dumps(s, ensure_ascii=False)

def mk_opts_js(opts, correct):
    items = ", ".join(js_str(o) for o in opts)
    return f"BankHelpers.mkOpts([{items}], {correct})"

def q_js(text, opts, correct, expl, submateria, level="medio"):
    return (
        f"BankHelpers.q({js_str(text)}, "
        f"{mk_opts_js(opts, correct)}, "
        f"{correct}, {js_str(expl)}, {js_str(submateria)}, {js_str(level)})"
    )

SEEDER_HEADER = '''/* =========================================================================
   BANCO EM 2º ANO — prova → matéria → sub-matéria
   ========================================================================= */
class BankHelpers {
  static mkOpts(list, correctIdx){
    return list.map((text,i)=>({id:Util.uid('opt'), text, correct:i===correctIdx}));
  }
  static q(text, options, correctIdx, explanation, submateria, level='medio'){
    return {type:'single', text, options, explanation, submateria, level};
  }
}

class DataCleanup {
  static FLAG = 'ef_cleanup_em2_v2';
  static run(){
    if(localStorage.getItem(this.FLAG)) return;
    const cyber = /ciber|cyber|seguran[cç]a da informa|CYBER-/i;
    const legacyExam = e => /^(CYBER-|HIST-RF-50)/.test(e.code||'') || cyber.test([e.category,e.title,e.code,...(e.tags||[])].join(' '));
    const qs = StorageManager.getQuestions().filter(q=>{
      const blob = [q.category,q.materia,q.submateria,...(q.tags||[]),q.text].join(' ');
      return !cyber.test(blob);
    });
    StorageManager.saveQuestions(qs);
    const kept = new Set(qs.map(q=>q.id));
    const exams = StorageManager.getExams().filter(e=>!legacyExam(e)).map(e=>({...e, questionIds:(e.questionIds||[]).filter(id=>kept.has(id))}));
    StorageManager.saveExams(exams);
    ['ef_demo_seeded_v1','ef_french_rev_seeded_v2','ef_cleanup_em2_v1'].forEach(k=>localStorage.removeItem(k));
    localStorage.setItem(this.FLAG,'1');
  }
}

class BankHierarchy {
  static groupByExam(){
    const exams = StorageManager.getExams().filter(e=>e.questionIds?.length);
    const qmap = Object.fromEntries(StorageManager.getQuestions().map(q=>[q.id,q]));
    const used = new Set();
    const tree = exams.map(ex=>{
      const qs = ex.questionIds.map(id=>qmap[id]).filter(Boolean);
      qs.forEach(q=>used.add(q.id));
      return {exam:ex, materias:this._byMateria(qs)};
    });
    const orphan = StorageManager.getQuestions().filter(q=>!used.has(q.id));
    if(orphan.length) tree.push({exam:{id:'_orphan',title:'Sem prova vinculada',questionIds:[]}, materias:this._byMateria(orphan)});
    return tree;
  }
  static _byMateria(qs){
    const map = {};
    qs.forEach(q=>{
      const m = q.materia || 'Sem matéria';
      map[m] = map[m] || {};
      const s = q.submateria || q.category || 'Geral';
      map[m][s] = map[m][s] || [];
      map[m][s].push(q);
    });
    return Object.entries(map).sort((a,b)=>a[0].localeCompare(b[0],'pt-BR')).map(([materia,subs])=>({
      materia,
      submaterias:Object.entries(subs).sort((a,b)=>a[0].localeCompare(b[0],'pt-BR')).map(([submateria,questions])=>({submateria,questions}))
    }));
  }
  static count(qs){ return qs.length; }
}

class EnsinoMedio2Seeder {
  static FLAG_KEY = 'ef_em2_seeded_v1';
  static SERIE = '2º Ano EM';
'''

SEEDER_FOOTER = '''
  static subjects(){
    return this.SUBJECT_DATA;
  }
  static seed(){
    if(localStorage.getItem(this.FLAG_KEY)) return;
    DataCleanup.run();
    this.subjects().forEach(sub=>{
      const qs = [];
      Object.entries(sub.submaterias).forEach(([submateria, items])=>{
        items.forEach(d=>{
          const raw = typeof d === 'object' && d.text ? d : BankHelpers.q(d[0], BankHelpers.mkOpts(d[1], d[2]), d[2], d[3], submateria, d[4]||'medio');
          qs.push(new Question({
            ...raw,
            materia: sub.materia,
            submateria,
            category: submateria,
            tags: [sub.materia, submateria, this.SERIE]
          }));
        });
      });
      qs.forEach(q => StorageManager.upsertQuestion(q));
      const exam = new Exam({
        title: sub.title,
        description: sub.description,
        category: this.SERIE,
        materia: sub.materia,
        serie: this.SERIE,
        code: sub.code,
        language: 'pt-BR',
        timeMinutes: sub.timeMinutes,
        passScore: 70,
        author: 'ExamForge',
        version: '1.0',
        tags: [this.SERIE, sub.materia, 'simulado'],
        questionIds: qs.map(q => q.id)
      });
      StorageManager.upsertExam(exam);
    });
    localStorage.setItem(this.FLAG_KEY, '1');
  }
}
'''

def load_data():
    if DATA.exists():
        return json.loads(DATA.read_text(encoding='utf-8'))
    raise SystemExit(f'Missing {DATA} — run generate_em2_data.py first')

def build_subject_js(sub):
    lines = ['    {',
             f'      materia: {js_str(sub["materia"])},',
             f'      title: {js_str(sub["title"])},',
             f'      description: {js_str(sub["description"])},',
             f'      code: {js_str(sub["code"])},',
             f'      timeMinutes: {sub["timeMinutes"]},',
             '      submaterias: {']
    for submateria, items in sub['submaterias'].items():
        lines.append(f'        {js_str(submateria)}: [')
        for item in items:
            text, opts, correct, expl, *rest = item
            level = rest[0] if rest else 'medio'
            lines.append(f'          {q_js(text, opts, correct, expl, submateria, level)},')
        lines.append('        ],')
    lines.append('      }')
    lines.append('    },')
    return '\n'.join(lines)

def build_seeder_block(data):
    body = '  static SUBJECT_DATA = [\n' + '\n'.join(build_subject_js(s) for s in data) + '\n  ];\n'
    return SEEDER_HEADER + body + SEEDER_FOOTER

def patch_html(path, block):
    html = path.read_text(encoding='utf-8')
    pattern = r"/\* =+\s*\n\s*SAMPLE DATA \(DEMO\).*?\nclass SampleDataSeeder \{.*?\n\}\n+\n+/\* =+\s*\n\s*REVOLUÇÃO FRANCESA.*?\nclass FrenchRevolutionSeeder \{.*?\n\}\n"
    if not re.search(pattern, html, flags=re.DOTALL):
        pattern = r"/\* =+\s*\n\s*BANCO EM 2º ANO.*?\nclass BankHelpers \{.*?\nclass EnsinoMedio2Seeder \{.*?\n\}\n"
    html = re.sub(pattern, block, html, count=1, flags=re.DOTALL)
    html = html.replace('SampleDataSeeder.seed();\n    FrenchRevolutionSeeder.seed();',
                        'DataCleanup.run();\n    EnsinoMedio2Seeder.seed();')
    html = html.replace("SampleDataSeeder.seed();", "DataCleanup.run();\n    EnsinoMedio2Seeder.seed();")
    path.write_text(html, encoding='utf-8')
    print(f'Patched {path.name}')

def main():
    data = load_data()
    total = sum(len(v) for s in data for v in s['submaterias'].values())
    print(f'Subjects: {len(data)}, Questions: {total}')
    block = build_seeder_block(data)
    for name in ('index.html', '404.html'):
        p = ROOT / name
        if p.exists():
            patch_html(p, block)

if __name__ == '__main__':
    main()
