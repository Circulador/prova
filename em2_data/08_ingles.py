#!/usr/bin/env python3
"""Banco de questões — Inglês (2º EM)."""

def q(text, opts, correct, expl, level="medio"):
    return [text, opts, correct, expl, level]

def pack(materia, code, title, desc, subs, minutes=75):
    total = sum(len(v) for v in subs.values())
    assert total == 50, f"{materia}: {total} questões"
    return {
        "materia": materia, "code": code, "title": title,
        "description": desc, "timeMinutes": minutes, "submaterias": subs
    }

ING = pack("Inglês", "EM2-ING", "Simulado — Inglês (2º EM)",
    "50 questões de múltipla escolha organizadas por sub-matéria.", {
    "Grammar": [
        q("Choose the correct sentence:", ["She don't like coffee.", "She doesn't like coffee.", "She not like coffee.", "She doesn't likes coffee."], 1, "3rd person singular: doesn't + base verb."),
        q("The plural of 'child' is:", ["childs", "children", "childes", "childrens"], 1, "Irregular plural: child → children."),
        q("'There ___ many books on the shelf.'", ["is", "are", "be", "was"], 1, "'Many books' is plural → are."),
        q("Which is a correct question?", ["Where you live?", "Where do you live?", "Where does you live?", "Where live you?"], 1, "Do/Does inversion for questions."),
        q("Comparative form of 'good' is:", ["gooder", "more good", "better", "best"], 2, "Irregular comparative: good → better."),
        q("'I have ___ finished my homework.' (already/yet)", ["already", "yet", "since", "for"], 0, "'Already' with present perfect affirmative."),
        q("Possessive of 'John' is:", ["Johns", "John's", "Johns'", "Johnes"], 1, "Singular possessive: 's."),
        q("Correct article: '___ apple a day keeps the doctor away.'", ["A", "An", "The", "No article"], 1, "'Apple' starts with vowel sound → an."),
        q("'If it rains, we ___ at home.'", ["stay", "will stay", "stayed", "staying"], 1, "First conditional: if + present, will + base."),
        q("Tag question: 'You are a student, ___?'", ["aren't you", "are you", "don't you", "isn't it"], 0, "Positive statement → negative tag."),
    ],
    "Vocabulary": [
        q("Synonym of 'happy':", ["sad", "joyful", "angry", "tired"], 1, "Joyful means happy."),
        q("Antonym of 'expensive':", ["costly", "cheap", "rich", "pricey"], 1, "Cheap is the opposite of expensive."),
        q("'To postpone' means:", ["to cancel forever", "to delay to a later time", "to start immediately", "to forget"], 1, "Postpone = adiar."),
        q("A person who treats sick people is a:", ["engineer", "doctor", "lawyer", "chef"], 1, "Doctor treats patients."),
        q("'Environment' refers to:", ["only buildings", "natural surroundings and conditions", "computer software", "school subjects"], 1, "Meio ambiente / surroundings."),
        q("'Reliable' means:", ["trustworthy", "dangerous", "noisy", "temporary"], 0, "Confiável = reliable."),
        q("The word 'deadline' means:", ["a line that is dead", "the final date to complete something", "a type of sport", "a holiday"], 1, "Prazo final."),
        q("'Borrow' means:", ["to lend something to someone", "to take something temporarily with permission", "to steal", "to buy"], 1, "Pegar emprestado."),
        q("'Lend' is the opposite action of 'borrow' from the owner's view:", ["True — lend means give temporarily", "False — they mean the same", "False — lend means take", "False — neither relates to loans"], 0, "Emprestar (to lend) vs. pegar emprestado (to borrow)."),
        q("'Achieve' is closest in meaning to:", ["fail", "accomplish", "ignore", "destroy"], 1, "Achieve = alcançar, realizar."),
    ],
    "Reading": [
        q("Read: 'Tom wakes up at 6 a.m. every day to go to school.' When does Tom wake up?", ["At night", "At 6 a.m.", "At noon", "Never"], 1, "Explicit information in the text."),
        q("Read: 'Although it was raining, Maria went for a walk.' Why is this surprising?", ["Maria hates rain", "People usually avoid walking in rain", "It was sunny", "Maria stayed home"], 1, "'Although' shows contrast — she walked despite rain."),
        q("The main idea of a paragraph is usually found in:", ["The title only", "The topic sentence", "Page numbers", "Footnotes"], 1, "Topic sentence introduces main idea."),
        q("Read: 'Recycling helps reduce pollution.' What helps reduce pollution?", ["Burning trash", "Recycling", "Throwing plastic in rivers", "Using more paper"], 1, "Direct comprehension."),
        q("Inference: 'John's hands were shaking and his face was pale before the exam.' John was probably:", ["confident", "nervous", "sleepy", "hungry"], 1, "Physical signs suggest anxiety."),
        q("'According to the text' means you should:", ["use outside knowledge only", "base answer on the passage", "guess randomly", "ignore the passage"], 1, "Evidence-based reading."),
        q("Read: 'The library closes at 8 p.m. on weekdays.' When does it close on Monday?", ["8 a.m.", "8 p.m.", "Midnight", "It doesn't close"], 1, "Weekdays include Monday."),
        q("A 'headline' in a news article tells:", ["The main topic briefly", "The author's biography", "Every detail", "Only the date"], 0, "Manchete resume o assunto."),
        q("Read: 'She not only sings but also plays the guitar.' She:", ["only sings", "sings and plays guitar", "only plays guitar", "neither sings nor plays"], 1, "'Not only... but also' = both."),
        q("Skimming a text means:", ["reading every word slowly", "reading quickly for general idea", "translating word by word", "memorizing"], 1, "Leitura rápida para ideia geral."),
    ],
    "Verbs": [
        q("Past tense of 'go' is:", ["goed", "went", "gone", "going"], 1, "Irregular: go → went."),
        q("'She ___ to the mall yesterday.' (go)", ["go", "goes", "went", "gone"], 2, "Past simple for completed past action."),
        q("Present continuous: 'They ___ football now.'", ["play", "are playing", "played", "plays"], 1, "Now → am/is/are + -ing."),
        q("Past participle of 'write' is:", ["wrote", "written", "writed", "writing"], 1, "write – wrote – written."),
        q("'I ___ here since 2020.' (live)", ["live", "lived", "have lived", "am living"], 2, "Since + point → present perfect."),
        q("Modal for ability: 'I ___ swim when I was five.'", ["can", "could", "must", "should"], 1, "Past ability → could."),
        q("'He ___ his keys. He can't find them.' (lose)", ["loses", "has lost", "lose", "losing"], 1, "Present perfect: past action with present result."),
        q("Infinitive form of 'ran' is:", ["run", "running", "runs", "runned"], 0, "Base form: run."),
        q("'We ___ dinner when the phone rang.' (have)", ["had", "were having", "have", "has"], 1, "Past continuous interrupted by past simple."),
        q("Passive voice: 'The cake ___ by Mary.'", ["baked", "was baked", "is baking", "bakes"], 1, "Past passive: was/were + past participle."),
    ],
    "Phrasal Verbs": [
        q("'Give up' means:", ["to start", "to quit / stop trying", "to give a gift", "to stand up"], 1, "Desistir."),
        q("'Look after' means:", ["to search for", "to take care of", "to look behind", "to ignore"], 1, "Cuidar de alguém/algo."),
        q("'Turn on' the light means:", ["to switch it off", "to switch it on", "to rotate it", "to break it"], 1, "Ligar / acender."),
        q("'Find out' means:", ["to discover information", "to lose something", "to go outside", "to finish"], 0, "Descobrir, averiguar."),
        q("'Take off' (plane) means:", ["to land", "to leave the ground", "to remove clothes only", "to slow down"], 1, "Decolar."),
        q("'Run out of' means:", ["to have plenty", "to use all of something", "to escape", "to exercise"], 1, "Ficar sem (acabar o estoque)."),
        q("'Put off' a meeting means:", ["to schedule earlier", "to postpone", "to cancel the building", "to attend"], 1, "Adiar."),
        q("'Get along with' means:", ["to fight", "to have a good relationship", "to walk together only", "to separate"], 1, "Dar-se bem com."),
        q("'Break down' (car) means:", ["to start working", "to stop functioning", "to break into pieces deliberately", "to accelerate"], 1, "Quebrar, avariar."),
        q("'Look forward to' means:", ["to fear", "to anticipate with pleasure", "to look backward", "to forget"], 1, "Ansiar por, esperar com prazer."),
    ],
})

print("ING OK", len([x for s in ING["submaterias"].values() for x in s]))
