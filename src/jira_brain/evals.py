import json
from pathlib import Path

from jira_brain.rag import answer

cases = json.loads(Path("evals/questions.json").read_text(encoding="utf-8"))

passed = 0
for case in cases:
    result = answer(case["question"])

    sources_ok = set(case["expected_sources"]) <= set(result.sources)
    keywords_ok = all(k.lower() in result.answer.lower() for k in case["expected_keywords"])
    ok = sources_ok and keywords_ok
    passed += ok

    status = "PASS" if ok else "FAIL"
    print(f"{status}  {case['question']}")
    if not ok:
        print(f"      sources={result.sources}  confidence={result.confidence:.2f}")
        print(f"      answer={result.answer[:120]}")

print(f"\n{passed}/{len(cases)} passed")
