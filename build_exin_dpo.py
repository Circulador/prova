#!/usr/bin/env python3
"""Generate ExinDPOSeeder block and patch index.html / 404.html."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "exin_dpo_bank_data.json"


def js_str(s):
    return json.dumps(s, ensure_ascii=False)


def mk_opts_js(opts):
    items = ", ".join(js_str(o["text"]) for o in opts)
    correct = next(i for i, o in enumerate(opts) if o.get("correct"))
    return f"BankHelpers.mkOpts([{items}], {correct})"


def q_js(q):
    return (
        f"BankHelpers.q({js_str(q['text'])}, "
        f"{mk_opts_js(q['options'])}, "
        f"{next(i for i, o in enumerate(q['options']) if o.get('correct'))}, "
        f"{js_str(q['explanation'])}, {js_str(q['submateria'])}, {js_str(q.get('level', 'medio'))})"
    )


HEADER = r'''/* =========================================================================
   TRILHA DPO — EXIN (ISFS, PDPF, PDPP)
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
  static FLAG = 'ef_cleanup_exin_dpo_v1';
  static run(){
    if(localStorage.getItem(this.FLAG)) return;
    const em2Exam = e => /^(EM2-)/.test(e.code||'') || e.serie==='2º Ano EM' || (e.tags||[]).includes('2º Ano EM');
    const cyber = /ciber|cyber|CYBER-/i;
    const legacyExam = e => /^(CYBER-|HIST-RF-50)/.test(e.code||'') || cyber.test([e.category,e.title,e.code,...(e.tags||[])].join(' ')) || em2Exam(e);
    const em2Q = q => (q.tags||[]).includes('2º Ano EM') || /^EM2-/.test(q.category||'');
    const qs = StorageManager.getQuestions().filter(q=>{
      if(em2Q(q)) return false;
      const blob = [q.category,q.materia,q.submateria,...(q.tags||[]),q.text].join(' ');
      return !cyber.test(blob);
    });
    StorageManager.saveQuestions(qs);
    const kept = new Set(qs.map(q=>q.id));
    const exams = StorageManager.getExams().filter(e=>!legacyExam(e)).map(e=>({...e, questionIds:(e.questionIds||[]).filter(id=>kept.has(id))}));
    StorageManager.saveExams(exams);
    ['ef_demo_seeded_v1','ef_french_rev_seeded_v2','ef_cleanup_em2_v1','ef_cleanup_em2_v2','ef_em2_seeded_v1'].forEach(k=>localStorage.removeItem(k));
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

class ExinDPOSeeder {
  static FLAG_KEY = 'ef_exin_dpo_seeded_v1';
  static TRILHA = ''' + js_str("Trilha DPO — EXIN") + ''';
  static TRILHA_DESC = ''' + js_str(
        "Trilha de Encarregado de Dados EXIN — LGPD e GDPR. Três certificações independentes: ISFS, PDPF e PDPP."
    ) + ''';
  static CERT_DATA = [
'''

FOOTER = r'''
  ];
  static seed(){
    if(localStorage.getItem(this.FLAG_KEY)) return;
    DataCleanup.run();
    this.CERT_DATA.forEach(cert=>{
      const qs = [];
      Object.entries(cert.submaterias).forEach(([submateria, items])=>{
        items.forEach(d=>{
          const raw = typeof d === 'object' && d.text ? d : d;
          qs.push(new Question({
            ...raw,
            options: raw.options || [],
            materia: cert.materia,
            submateria,
            category: submateria,
            tags: [this.TRILHA, cert.materia, cert.code, submateria]
          }));
        });
      });
      qs.forEach(q => StorageManager.upsertQuestion(q));
      const exam = new Exam({
        title: cert.title,
        description: cert.description,
        category: this.TRILHA,
        trilha: this.TRILHA,
        materia: cert.materia,
        serie: this.TRILHA,
        code: cert.code,
        language: 'pt-BR',
        timeMinutes: cert.timeMinutes,
        passScore: 70,
        author: 'Velora',
        version: '1.0',
        tags: [this.TRILHA, cert.materia, 'certificação', 'EXIN'],
        questionIds: qs.map(q => q.id)
      });
      StorageManager.upsertExam(exam);
    });
    localStorage.setItem(this.FLAG_KEY, '1');
  }
}
'''


def build_cert_js(cert):
    lines = [
        "    {",
        f"      materia: {js_str(cert['materia'])},",
        f"      title: {js_str(cert['title'])},",
        f"      description: {js_str(cert['description'])},",
        f"      code: {js_str(cert['code'])},",
        f"      timeMinutes: {cert['timeMinutes']},",
        "      submaterias: {",
    ]
    for sub, items in cert["submaterias"].items():
        lines.append(f"        {js_str(sub)}: [")
        for item in items:
            lines.append(f"          {q_js(item)},")
        lines.append("        ],")
    lines.append("      }")
    lines.append("    },")
    return "\n".join(lines)


def build_block(data):
    certs = data["certifications"]
    body = "\n".join(build_cert_js(c) for c in certs)
    return HEADER + body + FOOTER


def patch_html(path, block):
    html = path.read_text(encoding="utf-8")
    pattern = r"/\* =+\s*\n\s*BANCO EM 2º ANO.*?\nclass BankHelpers \{.*?\nclass EnsinoMedio2Seeder \{.*?\n\}\n"
    if not re.search(pattern, html, flags=re.DOTALL):
        pattern = r"/\* =+\s*\n\s*TRILHA DPO — EXIN.*?\nclass BankHelpers \{.*?\nclass ExinDPOSeeder \{.*?\n\}\n"
    html = re.sub(pattern, block, html, count=1, flags=re.DOTALL)
    html = html.replace("EnsinoMedio2Seeder.seed()", "ExinDPOSeeder.seed()")
    path.write_text(html, encoding="utf-8")
    print(f"Patched {path.name}")


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    total = sum(len(q) for c in data["certifications"] for q in c["submaterias"].values())
    print(f"Certs: {len(data['certifications'])}, Questions: {total}")
    block = build_block(data)
    for name in ("index.html", "404.html"):
        patch_html(ROOT / name, block)


if __name__ == "__main__":
    main()
