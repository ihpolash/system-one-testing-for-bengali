"""Write docs/PROMPTS.md: the exact question structure each task sends to every model (instructions, option names, descriptions), with the dataset text replaced by placeholders.
    python analysis/dump_prompts.py"""
import json, os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness"))
os.environ.setdefault("BN_QLANG", "en"); os.environ.setdefault("BN_ROT", "0")
from jev_benchmarking.tasks import get_tasks

def placeholder(q, name):   # Belebele's answer options are dataset text: show the slot, not the text
    q = json.loads(json.dumps(q))
    if name == "bn_belebele":
        q["answer"]["criteria"] = {k: f"<answer option {k}>" for k in q["answer"]["criteria"]}
    return q


out = ["# Prompts", "", "Each item is one typed single-choice question (`type: choice`) over a state. Dataset text appears only as `<field>`; option order is rotated by `BN_ROT` (0 here). "
       "Open models receive the same instructions, option names and descriptions through their own adapters (`harness/scripts/run_system_one_model.py`); Gemma scores each option label by next-token probability (`harness/jev_benchmarking/openmodel/prompts.py`).", ""]
for name in ("bn_sentnob", "bn_bnli", "bn_massive", "bn_belebele", "bn_sib200"):
    e = get_tasks([name])[0].examples("eval")[0]
    out += [f"## {name}", "", "State fields: " + ", ".join(f"`{k}`" for k in e.state), "", "```json",
            json.dumps(placeholder(e.questions, name), indent=1, ensure_ascii=False), "```", ""]
(ROOT / "docs").mkdir(exist_ok=True)
(ROOT / "docs" / "PROMPTS.md").write_text("\n".join(out))
print("wrote docs/PROMPTS.md", sum(len(x) for x in out), "chars")
