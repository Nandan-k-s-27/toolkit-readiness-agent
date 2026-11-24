#!/usr/bin/env python3
"""python verify.py sample  -> gold_labels.csv template (stratified 20 apps, 2 per category) to fill BY HAND from real docs
   python verify.py score   -> accuracy.json (pass1 vs final vs your gold labels)"""
import json, csv, sys, random, pathlib
ROOT = pathlib.Path(__file__).parent
F = {"auth_methods": "gold_auth", "self_serve": "gold_self_serve", "existing_mcp": "gold_mcp", "buildability": "gold_buildability"}

def key(f, v):
    return frozenset(v or []) if f == "auth_methods" else (v or "").strip()
def gold_key(f, v):
    return frozenset(x.strip() for x in v.split(",") if x.strip()) if f == "auth_methods" else v.strip()

if sys.argv[1] == "sample":
    res = json.load(open(ROOT / "results_final.json")); random.seed(7)
    by = {}
    for r in res: by.setdefault(r["category"], []).append(r)
    pick = [x for c in by.values() for x in random.sample(c, 2)]
    with open(ROOT / "gold_labels.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["app", "evidence_url_to_check", *F.values(), "notes"])
        for r in pick: w.writerow([r["app"], (r.get("evidence", {}).get("auth_methods") or {}).get("url", ""), "", "", "", "", ""])
    print("fill gold_labels.csv from the real docs (auth comma-separated), then run: python verify.py score")
else:
    p1 = {r["app"]: r for r in json.load(open(ROOT / "results_pass1.json"))}
    fin = {r["app"]: r for r in json.load(open(ROOT / "results_final.json"))}
    gold = [g for g in csv.DictReader(open(ROOT / "gold_labels.csv")) if g["gold_self_serve"].strip()]
    if not gold: sys.exit("gold_labels.csv has no filled rows yet - label the sample by hand first")
    out = {"n_apps": len(gold), "fields": {}, "misses": []}
    for f, gc in F.items():
        s = {"pass1": 0, "final": 0}
        for g in gold:
            gk = gold_key(f, g[gc])
            for name, src in (("pass1", p1), ("final", fin)):
                ok = key(f, src[g["app"]].get(f)) == gk
                s[name] += ok
                if not ok: out["misses"].append({"stage": name, "app": g["app"], "field": f, "agent": str(src[g["app"]].get(f)), "gold": g[gc]})
        out["fields"][f] = {k: round(v / len(gold), 3) for k, v in s.items()}
    for st in ("pass1", "final"):
        out[f"overall_{st}"] = round(sum(v[st] for v in out["fields"].values()) / len(F), 3)
    out["evidence_quote_valid_rate"] = {st: round(sum(all(r.get("evidence_ok", {}).values()) for r in src.values()) / len(src), 3) for st, src in (("pass1", p1), ("final", fin))}
    json.dump(out, open(ROOT / "accuracy.json", "w"), indent=1); print(json.dumps(out["fields"], indent=1), out["overall_pass1"], "->", out["overall_final"])
