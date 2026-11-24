#!/usr/bin/env python3
"""Builds index.html (single self-contained page) from results_final/patterns/accuracy/human_queue JSON."""
import json, pathlib, os
ROOT = pathlib.Path(__file__).parent
ld = lambda n, d=None: json.load(open(ROOT / n)) if (ROOT / n).exists() else d
DATA = {"results": ld("results_final.json", []), "patterns": ld("patterns.json", {}), "accuracy": ld("accuracy.json"),
        "human_queue": ld("human_queue.json", []), "repo": os.getenv("REPO_URL", "#"), "notes": ld("human_notes.json", [])}
blob = json.dumps(DATA).replace("</", "<\\/")
HTML = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>100-App Toolkit Readiness Research</title>
<style>
:root{--bg:#fff;--fg:#14161a;--mut:#5b6270;--card:#f5f6f8;--bd:#dfe2e8;--ac:#4f46e5;--ok:#15803d;--bad:#b91c1c;--warn:#b45309}
@media(prefers-color-scheme:dark){:root{--bg:#0f1115;--fg:#e8eaee;--mut:#9aa1ad;--card:#181b22;--bd:#2a2f3a;--ac:#8b85ff;--ok:#4ade80;--bad:#f87171;--warn:#fbbf24}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif}
main{max-width:1150px;margin:auto;padding:24px 16px 80px}h1{font-size:26px;margin:0 0 4px}h2{font-size:19px;margin:36px 0 10px}
.mut{color:var(--mut)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}
.card{background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:12px 14px}.big{font-size:22px;font-weight:700}
nav a{margin-right:12px;color:var(--ac);text-decoration:none}.tw{overflow-x:auto;border:1px solid var(--bd);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:13px}th,td{padding:6px 8px;border-bottom:1px solid var(--bd);text-align:left;vertical-align:top}th{background:var(--card);position:sticky;top:0;cursor:pointer}
.tag{display:inline-block;padding:1px 7px;border-radius:99px;border:1px solid var(--bd);font-size:12px;margin:1px}
.yes{color:var(--ok)}.blocked{color:var(--bad)}.yes_with_caveats{color:var(--warn)}
input,select{background:var(--card);color:var(--fg);border:1px solid var(--bd);border-radius:8px;padding:6px 8px;margin:0 6px 8px 0}
.flow{display:flex;flex-wrap:wrap;gap:6px;align-items:center}.flow span.s{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:6px 10px}
.bar{height:10px;background:var(--ac);border-radius:5px}code{background:var(--card);padding:1px 5px;border-radius:4px}
</style></head><body><main>
<h1>Which of 100 apps can become an agent toolkit today?</h1>
<div class="mut">AI Product Ops take-home · researched by an agent, verified against real docs · <a id="repo" style="color:var(--ac)">source repo</a> · <a id="dl" download="results.json" style="color:var(--ac)">results.json (machine-readable)</a></div>
<nav style="margin-top:10px"><a href="#patterns">Patterns</a><a href="#table">Findings</a><a href="#agent">Agent</a><a href="#verify">Verification</a><a href="#proof">Proof</a></nav>

<h2 id="patterns">1 · Patterns (headline)</h2><div id="headlines" class="grid"></div>
<div class="grid" style="margin-top:10px"><div class="card"><b>Auth methods</b><div id="authbars"></div></div>
<div class="card"><b>Self-serve vs gated, by category</b><div id="catbars"></div></div>
<div class="card"><b>Blockers</b><div id="blbars"></div></div></div>
<div class="grid" style="margin-top:10px"><div class="card"><b>Easy wins (build now)</b><div id="easy"></div></div><div class="card"><b>Needs outreach / payment / approval</b><div id="out"></div></div></div>

<h2 id="table">2 · Findings (all 100, filterable)</h2>
<input id="q" placeholder="search app / text"><select id="fc"><option value="">all categories</option></select><select id="fb"><option value="">any buildability</option><option>yes</option><option>yes_with_caveats</option><option>blocked</option></select><select id="fs"><option value="">any access</option></select>
<div class="tw"><table id="t"><thead><tr><th>App</th><th>Category</th><th>What it does</th><th>Auth</th><th>Access</th><th>API</th><th>MCP</th><th>Buildable</th><th>Blocker</th><th>Evidence</th><th>Conf.</th></tr></thead><tbody></tbody></table></div>

<h2 id="agent">3 · The agent</h2>
<div class="flow"><span class="s">apps.csv (100)</span>→<span class="s">Composio search tool: find docs / pricing / MCP pages</span>→<span class="s">fetch + clean pages (cached)</span>→<span class="s">LLM extracts JSON + verbatim quote per claim</span>→<b>Pass 1</b>→<span class="s">code checks every quote exists on its cited page</span>→<span class="s">LLM critic: does the quote support the claim?</span>→<span class="s">targeted re-research on failures</span>→<span class="s">low confidence → human queue</span>→<b>Final</b></div>
<p class="mut">Human needed for: <span id="hq"></span></p><div id="notes"></div>

<h2 id="verify">4 · Verification</h2><div id="acc"></div>

<h2 id="proof">5 · Proof / run it</h2>
<div class="card"><code>pip install -r requirements.txt && export COMPOSIO_API_KEY=… ANTHROPIC_API_KEY=…</code><br><code>python research.py pass1 --app Slack</code> (single-app live trigger) · <code>python research.py pass1 &amp;&amp; python research.py pass2 &amp;&amp; python analyze.py &amp;&amp; python build_page.py</code></div>
</main>
<script id="data" type="application/json">__DATA__</script>
<script>
const D=JSON.parse(document.getElementById('data').textContent),R=D.results,P=D.patterns||{};
const $=id=>document.getElementById(id);
function el(t,txt,cls){const e=document.createElement(t);if(txt!=null)e.textContent=txt;if(cls)e.className=cls;return e}
$('repo').href=D.repo;$('dl').href='data:application/json,'+encodeURIComponent(JSON.stringify(R));
(P.headlines||['Run the pipeline to populate results.']).forEach(h=>{const c=el('div',null,'card');c.append(el('div',h,'big'));$('headlines').append(c)});
function bars(id,obj){const m=Math.max(1,...Object.values(obj||{}));Object.entries(obj||{}).sort((a,b)=>b[1]-a[1]).forEach(([k,v])=>{const r=el('div',null);r.append(el('span',k+' · '+v,'mut'));const b=el('div',null,'bar');b.style.width=(100*v/m)+'%';r.append(b);$(id).append(r)})}
bars('authbars',P.auth);bars('blbars',P.blockers);
Object.entries(P.by_category||{}).forEach(([c,v])=>{const g=Object.entries(v).filter(([k])=>!(k||'').startsWith('self_serve')).reduce((s,[,n])=>s+n,0);const r=el('div',c+': '+(10-g)+' self-serve / '+g+' gated','mut');$('catbars').append(r)});
(P.easy_wins||[]).forEach(a=>$('easy').append(el('span',a,'tag')));(P.needs_outreach||[]).forEach(a=>$('out').append(el('span',a,'tag')));
const cats=[...new Set(R.map(r=>r.category))],acc=[...new Set(R.map(r=>r.self_serve))];
cats.forEach(c=>$('fc').append(new Option(c,c)));acc.forEach(c=>$('fs').append(new Option(c,c)));
function draw(){const q=$('q').value.toLowerCase(),tb=$('t').tBodies[0];tb.replaceChildren();
R.filter(r=>(!$('fc').value||r.category==$('fc').value)&&(!$('fb').value||r.buildability==$('fb').value)&&(!$('fs').value||r.self_serve==$('fs').value)&&(!q||JSON.stringify(r).toLowerCase().includes(q))).forEach(r=>{
const tr=el('tr');[r.app,r.category,r.one_liner,(r.auth_methods||[]).join(', '),r.self_serve,(r.api_type||[]).join(', ')+' ('+(r.api_breadth||'?')+')',(r.existing_mcp||'?')].forEach(v=>tr.append(el('td',v)));
tr.append(el('td',r.buildability,r.buildability));tr.append(el('td',(r.blocker||'')+(r.blocker_note?' – '+r.blocker_note:'')));
const ev=el('td');Object.entries(r.evidence||{}).forEach(([f,e])=>{if(e&&/^https?:/.test(e.url||'')){const a=el('a',f.slice(0,4));a.href=e.url;a.target='_blank';a.rel='noopener';a.title=e.quote||'';a.style.marginRight='6px';ev.append(a)}});tr.append(ev);tr.append(el('td',(r.confidence??'')+(r.needs_human?' ⚠':'')));tb.append(tr)})}
['q','fc','fb','fs'].forEach(i=>$(i).addEventListener('input',draw));draw();
$('hq').textContent=(D.human_queue||[]).length?(D.human_queue.length+' apps flagged: '+D.human_queue.map(h=>h.app).join(', ')):'(run pass2)';
(D.notes||[]).forEach(n=>$('notes').append(el('div','• '+n.app+': '+n.issue,'mut')));
const A=D.accuracy,v=$('acc');
if(!A){v.append(el('p','Accuracy not yet scored: fill gold_labels.csv and run verify.py score.','mut'))}else{
v.append(el('p','Hand-checked '+A.n_apps+' apps (stratified, 2 per category) against real docs. Overall accuracy: pass 1 '+(A.overall_pass1*100).toFixed(0)+'% → final '+(A.overall_final*100).toFixed(0)+'%. Claims whose cited quote exists on the cited page: '+(A.evidence_quote_valid_rate.pass1*100).toFixed(0)+'% → '+(A.evidence_quote_valid_rate.final*100).toFixed(0)+'%.'));
const t=el('table');const h=el('tr');['Field','Pass 1','Final'].forEach(x=>h.append(el('th',x)));t.append(h);
Object.entries(A.fields).forEach(([f,s])=>{const r=el('tr');[f,(s.pass1*100).toFixed(0)+'%',(s.final*100).toFixed(0)+'%'].forEach(x=>r.append(el('td',x)));t.append(r)});v.append(t);
v.append(el('h3','Misses (shown honestly)'));A.misses.forEach(m=>v.append(el('div',`[${m.stage}] ${m.app} · ${m.field}: agent="${m.agent}" vs docs="${m.gold}"`,'mut')))}
</script></body></html>"""
(ROOT / "index.html").write_text(HTML.replace("__DATA__", blob)); print("index.html written")
