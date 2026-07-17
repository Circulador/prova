'use strict';
/* Velora — Forge Engines (OpenRouter + Gemini OAuth PKCE, client-side only) */

const ForgeEngines = {
  KEYS: {
    ENGINE_1: 'velora_engine_1',
    ENGINE_2: 'velora_engine_2',
    OR_KEY: 'velora_openrouter_key',
    OR_MODEL: 'velora_openrouter_model',
    OR_LABEL: 'velora_openrouter_label',
    GEMINI: 'velora_gemini_token',
    GEMINI_MODEL: 'velora_gemini_model',
    PKCE_VERIFIER: 'velora_oauth_verifier',
    PKCE_PROVIDER: 'velora_oauth_provider',
    FORGE_RETURN: 'velora_forge_return_ctx'
  },
  GEMINI_CLIENT_ID: '681255809395-u0kv5a0hg0e1tgq9e3aj8u6kgpc82g0g.apps.googleusercontent.com',
  OPENROUTER_MODELS: [
    'meta-llama/llama-3.3-70b-instruct:free',
    'google/gemini-flash-1.5:free',
    'deepseek/deepseek-chat:free',
    'mistralai/mistral-7b-instruct:free'
  ],
  GEMINI_MODELS: [
    'gemini-2.0-flash',
    'gemini-1.5-flash',
    'gemini-2.5-pro'
  ],

  /** Google OAuth with Gemini CLI client_id only works on localhost — not on GitHub Pages. */
  isGeminiOAuthSupported(){
    const h = (location.hostname || '').toLowerCase();
    return h === 'localhost' || h === '127.0.0.1' || h === '[::1]';
  },

  geminiUnavailableMessage(){
    return I18n?.t?.('forge.geminiUnavailable')
      || 'Login Google Gemini não está disponível neste site. Use OpenRouter (inclui Gemini gratuito).';
  },

  sanitizeSelections(){
    [1, 2].forEach(n=>{
      if(this.getEngineSelection(n) === 'gemini' && !this.isGeminiOAuthSupported()){
        this.setEngineSelection(n, 'none');
      }
    });
  },

  _redirectUri(){
    return window.location.origin + window.location.pathname;
  },

  _randBytes(n=32){
    const a = new Uint8Array(n);
    crypto.getRandomValues(a);
    return a;
  },

  _b64url(buf){
    const b = typeof buf === 'string' ? buf : String.fromCharCode(...new Uint8Array(buf));
    return btoa(b).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
  },

  async _pkceChallenge(verifier){
    const data = new TextEncoder().encode(verifier);
    const hash = await crypto.subtle.digest('SHA-256', data);
    return this._b64url(hash);
  },

  _get(key, fb=null){
    try{ const v = localStorage.getItem(key); return v == null ? fb : JSON.parse(v); }catch(e){ return fb; }
  },
  _set(key, val){
    try{ localStorage.setItem(key, typeof val === 'string' ? val : JSON.stringify(val)); return true; }catch(e){ return false; }
  },
  _del(key){ try{ localStorage.removeItem(key); }catch(e){} },

  getEngineSelection(n){
    const v = localStorage.getItem(n === 1 ? this.KEYS.ENGINE_1 : this.KEYS.ENGINE_2);
    return v || 'none';
  },
  setEngineSelection(n, provider){
    localStorage.setItem(n === 1 ? this.KEYS.ENGINE_1 : this.KEYS.ENGINE_2, provider || 'none');
  },

  getOpenRouterKey(){ return localStorage.getItem(this.KEYS.OR_KEY) || ''; },
  getOpenRouterModel(){ return localStorage.getItem(this.KEYS.OR_MODEL) || this.OPENROUTER_MODELS[0]; },
  getGeminiToken(){
    return this._get(this.KEYS.GEMINI, null);
  },
  getGeminiModel(){ return localStorage.getItem(this.KEYS.GEMINI_MODEL) || this.GEMINI_MODELS[0]; },

  isConnected(provider){
    if(provider === 'openrouter') return !!this.getOpenRouterKey();
    if(provider === 'gemini'){
      const t = this.getGeminiToken();
      return !!(t && t.access_token);
    }
    return false;
  },

  getEngine(n){
    const provider = this.getEngineSelection(n);
    if(!provider || provider === 'none') return null;
    if(!this.isConnected(provider)) return null;
    if(provider === 'openrouter'){
      return { provider, model: this.getOpenRouterModel(), token: this.getOpenRouterKey(), label: localStorage.getItem(this.KEYS.OR_LABEL) || 'OpenRouter' };
    }
    if(provider === 'gemini'){
      const t = this.getGeminiToken();
      return { provider, model: this.getGeminiModel(), token: t.access_token, refresh: t.refresh_token, label: t.email || 'Gemini' };
    }
    return null;
  },

  hasActiveEngine(){
    return !!(this.getEngine(1) || this.getEngine(2));
  },

  statusMeta(n){
    const sel = this.getEngineSelection(n);
    if(!sel || sel === 'none') return { cls:'badge-warn', text: I18n?.isEn?.() ? 'Not configured' : 'Não configurada', connected:false };
    if(!this.isConnected(sel)){
      return { cls:'badge-bad', text: I18n?.isEn?.() ? 'Not connected' : 'Não conectado', connected:false };
    }
    const eng = this.getEngine(n);
    const label = eng?.label || sel;
    return { cls:'badge-good', text: `🟢 ${label}`, connected:true };
  },

  _cleanOAuthQuery(){
    const u = new URL(window.location.href);
    ['code','state','scope','authuser','prompt'].forEach(k=>u.searchParams.delete(k));
    const clean = u.pathname + (u.search || '') + u.hash;
    history.replaceState({}, '', clean);
  },

  async handleOAuthCallback(){
    if(typeof crypto === 'undefined' || !crypto.subtle) return false;
    const url = new URL(window.location.href);
    const code = url.searchParams.get('code');
    const state = url.searchParams.get('state');
    const verifier = sessionStorage.getItem(this.KEYS.PKCE_VERIFIER);
    const pending = sessionStorage.getItem(this.KEYS.PKCE_PROVIDER);
    if(!code || !verifier || !pending) return false;

    try{
      if(pending === 'openrouter' && state !== 'gemini_oauth'){
        await this._exchangeOpenRouter(code, verifier);
      } else if(pending === 'gemini' && state === 'gemini_oauth'){
        await this._exchangeGemini(code, verifier);
      }
      this._cleanOAuthQuery();
      const retHash = sessionStorage.getItem('velora_oauth_return_hash');
      if(retHash){
        sessionStorage.removeItem('velora_oauth_return_hash');
        if(!window.location.hash || window.location.hash === '#') window.location.hash = retHash.replace(/^#/, '');
      }
      if(typeof Toast !== 'undefined') Toast.show(I18n?.isEn?.() ? 'AI engine connected.' : 'Engine de IA conectada.', 'success');
      return true;
    }catch(err){
      console.error('[ForgeEngines] OAuth', err);
      if(typeof Toast !== 'undefined') Toast.show(String(err.message || err), 'error');
      this._cleanOAuthQuery();
      return false;
    }finally{
      sessionStorage.removeItem(this.KEYS.PKCE_VERIFIER);
      sessionStorage.removeItem(this.KEYS.PKCE_PROVIDER);
    }
  },

  async connect(provider){
    if(!crypto?.subtle){
      throw new Error(I18n?.isEn?.() ? 'Browser does not support OAuth (Web Crypto).' : 'Navegador não suporta OAuth (Web Crypto).');
    }
    sessionStorage.setItem('velora_oauth_return_hash', window.location.hash || '#forge');
    if(!this.getReturnContext()) this.saveReturnContext({ returnTab: 'certificacoes', source: 'library' });
    const verifier = this._b64url(this._randBytes(32));
    sessionStorage.setItem(this.KEYS.PKCE_VERIFIER, verifier);
    sessionStorage.setItem(this.KEYS.PKCE_PROVIDER, provider);
    const redirect = this._redirectUri();
    const challenge = await this._pkceChallenge(verifier);

    if(provider === 'openrouter'){
      const params = new URLSearchParams({
        callback_url: redirect,
        code_challenge: challenge,
        code_challenge_method: 'S256'
      });
      window.location.href = `https://openrouter.ai/auth?${params}`;
      return;
    }
    if(provider === 'gemini'){
      if(!this.isGeminiOAuthSupported()){
        throw new Error(this.geminiUnavailableMessage());
      }
      const params = new URLSearchParams({
        response_type: 'code',
        client_id: this.GEMINI_CLIENT_ID,
        redirect_uri: redirect,
        scope: 'https://www.googleapis.com/auth/cloud-platform https://www.googleapis.com/auth/userinfo.email openid',
        code_challenge: challenge,
        code_challenge_method: 'S256',
        state: 'gemini_oauth'
      });
      window.location.href = `https://accounts.google.com/o/oauth2/v2/auth?${params}`;
    }
  },

  disconnect(provider){
    if(provider === 'openrouter'){
      this._del(this.KEYS.OR_KEY);
      localStorage.removeItem(this.KEYS.OR_MODEL);
      localStorage.removeItem(this.KEYS.OR_LABEL);
    } else if(provider === 'gemini'){
      this._del(this.KEYS.GEMINI);
      localStorage.removeItem(this.KEYS.GEMINI_MODEL);
    }
  },

  async _exchangeOpenRouter(code, verifier){
    const res = await fetch('https://openrouter.ai/api/v1/auth/keys', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ code, code_verifier: verifier, code_challenge_method: 'S256' })
    });
    if(!res.ok) throw new Error(`OpenRouter auth ${res.status}`);
    const data = await res.json();
    if(!data.key) throw new Error('OpenRouter: resposta sem chave');
    localStorage.setItem(this.KEYS.OR_KEY, data.key);
    await this._validateOpenRouter(data.key);
  },

  async _validateOpenRouter(key){
    const res = await fetch('https://openrouter.ai/api/v1/models', {
      headers:{ Authorization: `Bearer ${key}` }
    });
    if(!res.ok) throw new Error(`OpenRouter validate ${res.status}`);
    const model = this.OPENROUTER_MODELS.find(m=>true) || 'meta-llama/llama-3.3-70b-instruct:free';
    localStorage.setItem(this.KEYS.OR_MODEL, model);
    localStorage.setItem(this.KEYS.OR_LABEL, 'OpenRouter');
  },

  async _exchangeGemini(code, verifier){
    const body = new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      client_id: this.GEMINI_CLIENT_ID,
      redirect_uri: this._redirectUri(),
      code_verifier: verifier
    });
    const res = await fetch('https://oauth2.googleapis.com/token', {
      method:'POST',
      headers:{'Content-Type':'application/x-www-form-urlencoded'},
      body
    });
    if(!res.ok){
      const err = await res.text().catch(()=>res.statusText);
      throw new Error(`Gemini OAuth ${res.status}: ${err.slice(0,120)}`);
    }
    const tok = await res.json();
    let email = '';
    try{
      const ui = await fetch('https://www.googleapis.com/oauth2/v3/userinfo', {
        headers:{ Authorization: `Bearer ${tok.access_token}` }
      });
      if(ui.ok){ const j = await ui.json(); email = j.email || ''; }
    }catch(e){}
    this._set(this.KEYS.GEMINI, {
      access_token: tok.access_token,
      refresh_token: tok.refresh_token,
      expires_at: Date.now() + (tok.expires_in || 3600) * 1000,
      email
    });
    localStorage.setItem(this.KEYS.GEMINI_MODEL, this.GEMINI_MODELS[0]);
  },

  async _ensureGeminiToken(engine){
    const t = this.getGeminiToken();
    if(!t) throw new Error('Gemini não conectado');
    if(t.expires_at && t.expires_at > Date.now() + 60000) return t.access_token;
    if(!t.refresh_token) return t.access_token;
    const body = new URLSearchParams({
      grant_type: 'refresh_token',
      refresh_token: t.refresh_token,
      client_id: this.GEMINI_CLIENT_ID
    });
    const res = await fetch('https://oauth2.googleapis.com/token', {
      method:'POST',
      headers:{'Content-Type':'application/x-www-form-urlencoded'},
      body
    });
    if(!res.ok) throw new Error(`Gemini refresh ${res.status}`);
    const tok = await res.json();
    t.access_token = tok.access_token;
    t.expires_at = Date.now() + (tok.expires_in || 3600) * 1000;
    if(tok.refresh_token) t.refresh_token = tok.refresh_token;
    this._set(this.KEYS.GEMINI, t);
    return t.access_token;
  },

  _parseJson(text){
    const t = String(text).trim();
    try{ return JSON.parse(t); }catch(e){}
    const m = t.match(/\{[\s\S]*\}/);
    if(m) return JSON.parse(m[0]);
    throw new Error('Resposta não é JSON válido');
  },

  async callEngine(engine, system, user){
    if(!engine) throw new Error('Engine não configurada');
    const timeoutMs = 90000;
    const ctrl = new AbortController();
    const timer = setTimeout(()=>ctrl.abort(), timeoutMs);
    try{
      if(engine.provider === 'openrouter'){
        const res = await fetch('https://openrouter.ai/api/v1/chat/completions', {
          method:'POST',
          signal: ctrl.signal,
          headers:{
            'Content-Type':'application/json',
            Authorization: `Bearer ${engine.token}`,
            'HTTP-Referer': window.location.origin,
            'X-Title': 'Velora Forge'
          },
          body: JSON.stringify({
            model: engine.model,
            temperature: 0.4,
            response_format: { type: 'json_object' },
            messages:[{ role:'system', content: system }, { role:'user', content: user }]
          })
        });
        if(res.status === 429) throw new Error('429 quota');
        if(!res.ok){
          const err = await res.text().catch(()=>res.statusText);
          throw new Error(`OpenRouter ${res.status}: ${err.slice(0,180)}`);
        }
        const json = await res.json();
        return this._parseJson(json.choices?.[0]?.message?.content || '');
      }
      if(engine.provider === 'gemini'){
        const token = await this._ensureGeminiToken(engine);
        const model = engine.model || this.GEMINI_MODELS[0];
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`;
        const res = await fetch(url, {
          method:'POST',
          signal: ctrl.signal,
          headers:{
            'Content-Type':'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({
            systemInstruction: { parts:[{ text: system }] },
            contents:[{ role:'user', parts:[{ text: user }] }],
            generationConfig: { temperature: 0.4, responseMimeType: 'application/json' }
          })
        });
        if(res.status === 429) throw new Error('429 quota');
        if(!res.ok){
          const err = await res.text().catch(()=>res.statusText);
          throw new Error(`Gemini ${res.status}: ${err.slice(0,180)}`);
        }
        const json = await res.json();
        const text = json.candidates?.[0]?.content?.parts?.map(p=>p.text).join('') || '';
        return this._parseJson(text);
      }
      throw new Error('Provider desconhecido');
    }finally{
      clearTimeout(timer);
    }
  },

  async callAI(system, user){
    const e1 = this.getEngine(1);
    if(e1){
      try{ return await this.callEngine(e1, system, user); }
      catch(err){
        const e2 = this.getEngine(2);
        if(!e2) throw err;
        return await this.callEngine(e2, system, user);
      }
    }
    const e2 = this.getEngine(2);
    if(e2) return await this.callEngine(e2, system, user);
    throw new Error(I18n?.isEn?.() ? 'No AI engine connected' : 'Nenhuma engine de IA conectada');
  },

  renderEngineCard(num){
    const sel = this.getEngineSelection(num);
    const gemSupported = this.isGeminiOAuthSupported();
    const gemSel = (sel === 'gemini' && !gemSupported) ? 'none' : sel;
    const meta = this.statusMeta(num);
    const connected = this.isConnected(gemSel);
    const modelOpts = gemSel === 'gemini'
      ? this.GEMINI_MODELS
      : gemSel === 'openrouter' ? this.OPENROUTER_MODELS : [];
    const curModel = gemSel === 'gemini' ? this.getGeminiModel() : gemSel === 'openrouter' ? this.getOpenRouterModel() : '';
    const label = num === 1 ? (I18n?.t?.('forge.engine1') || 'Engine 1') : (I18n?.t?.('forge.engine2') || 'Engine 2');
    const none = I18n?.t?.('forge.engineNone') || 'Nenhuma';
    const or = I18n?.t?.('forge.engineOpenRouter') || 'OpenRouter';
    const gem = gemSupported
      ? (I18n?.t?.('forge.engineGemini') || 'Google Gemini')
      : (I18n?.t?.('forge.engineGeminiOff') || 'Google Gemini (indisponível neste site)');
    return `
      <div class="card card-compact forge-engine-card" data-engine-card="${num}" style="margin-bottom:10px">
        <div class="row between" style="margin-bottom:8px;gap:8px;flex-wrap:wrap">
          <span style="font-weight:600;font-size:13px">${label}</span>
          <span class="badge ${meta.cls}" id="forge-eng-status-${num}">${meta.text}</span>
        </div>
        <div class="form-grid">
          <div class="field full">
            <label>${I18n?.t?.('forge.provider') || 'Provedor'}</label>
            <select class="select" id="forge-eng-sel-${num}">
              <option value="none" ${gemSel==='none'?'selected':''}>${none}</option>
              <option value="openrouter" ${gemSel==='openrouter'?'selected':''}>${or}</option>
              <option value="gemini" ${gemSel==='gemini'?'selected':''} ${gemSupported?'':'disabled'}>${gem}</option>
            </select>
          </div>
          <div class="field full ${connected && modelOpts.length ? '' : 'hidden'}" id="forge-eng-model-wrap-${num}">
            <label>${I18n?.t?.('forge.model') || 'Modelo'}</label>
            <select class="select" id="forge-eng-model-${num}">
              ${modelOpts.map(m=>`<option value="${m}" ${m===curModel?'selected':''}>${m}</option>`).join('')}
            </select>
          </div>
        </div>
        <div class="row" style="gap:8px;margin-top:8px;flex-wrap:wrap">
          <button type="button" class="btn btn-sm btn-primary" id="forge-eng-connect-${num}" ${(!sel || sel==='none' || connected)?'hidden':''}>${I18n?.t?.('forge.connect') || 'Conectar'}</button>
          <button type="button" class="btn btn-sm btn-ghost" id="forge-eng-disconnect-${num}" ${connected?'':'hidden'}>${I18n?.t?.('forge.disconnect') || 'Desconectar'}</button>
        </div>
      </div>`;
  },

  bindEngineCards(root){
    this.sanitizeSelections();
    [1,2].forEach(num=>this._bindEngineCard(root, num));
    const hint = root.querySelector('#forge-gemini-hint');
    if(hint && !this.isGeminiOAuthSupported()){
      hint.classList.remove('hidden');
      hint.innerHTML = I18n?.t?.('forge.geminiHintOpenRouter') || hint.textContent;
    }
  },

  _bindEngineCard(root, num){
    const sel = root.querySelector(`#forge-eng-sel-${num}`);
    const connect = root.querySelector(`#forge-eng-connect-${num}`);
    const disconnect = root.querySelector(`#forge-eng-disconnect-${num}`);
    const modelWrap = root.querySelector(`#forge-eng-model-wrap-${num}`);
    const modelSel = root.querySelector(`#forge-eng-model-${num}`);
    const refresh = ()=>{
      const provider = sel?.value || 'none';
      this.setEngineSelection(num, provider);
      const meta = this.statusMeta(num);
      const badge = root.querySelector(`#forge-eng-status-${num}`);
      if(badge){ badge.className = `badge ${meta.cls}`; badge.textContent = meta.text; }
      const connected = provider !== 'none' && this.isConnected(provider);
      if(connect) connect.hidden = connected || provider === 'none';
      if(disconnect) disconnect.hidden = !connected;
      if(modelWrap && modelSel){
        const models = provider === 'gemini' ? this.GEMINI_MODELS : provider === 'openrouter' ? this.OPENROUTER_MODELS : [];
        if(connected && models.length){
          modelWrap.classList.remove('hidden');
          modelSel.innerHTML = models.map(m=>`<option value="${m}">${m}</option>`).join('');
          const cur = provider === 'gemini' ? this.getGeminiModel() : this.getOpenRouterModel();
          modelSel.value = cur;
        } else {
          modelWrap.classList.add('hidden');
        }
      }
    };
    sel?.addEventListener('change', ()=>{
      if(sel.value === 'gemini' && !ForgeEngines.isGeminiOAuthSupported()){
        sel.value = 'none';
        Toast?.show?.(ForgeEngines.geminiUnavailableMessage(), 'warn');
      }
      refresh();
    });
    connect?.addEventListener('click', async ()=>{
      const p = sel.value;
      if(p === 'none') return;
      try{
        connect.disabled = true;
        connect.textContent = I18n?.isEn?.() ? 'Connecting…' : 'Conectando…';
        await this.connect(p);
      }catch(e){
        Toast?.show?.(e.message, 'error');
        connect.disabled = false;
        connect.textContent = I18n?.t?.('forge.connect') || 'Conectar';
      }
    });
    disconnect?.addEventListener('click', ()=>{
      const p = sel.value;
      if(p && p !== 'none') this.disconnect(p);
      refresh();
      Toast?.show?.(I18n?.isEn?.() ? 'Disconnected.' : 'Desconectado.', 'success');
    });
    modelSel?.addEventListener('change', ()=>{
      const p = sel.value;
      if(p === 'openrouter') localStorage.setItem(this.KEYS.OR_MODEL, modelSel.value);
      if(p === 'gemini') localStorage.setItem(this.KEYS.GEMINI_MODEL, modelSel.value);
    });
    refresh();
  },

  saveReturnContext(ctx){
    try{ sessionStorage.setItem(this.KEYS.FORGE_RETURN, JSON.stringify(ctx || {})); }catch(e){}
  },
  getReturnContext(){
    try{
      const raw = sessionStorage.getItem(this.KEYS.FORGE_RETURN);
      return raw ? JSON.parse(raw) : null;
    }catch(e){ return null; }
  },
  popReturnContext(){
    const ctx = this.getReturnContext();
    try{ sessionStorage.removeItem(this.KEYS.FORGE_RETURN); }catch(e){}
    return ctx;
  }
};

if(typeof window !== 'undefined') window.ForgeEngines = ForgeEngines;
