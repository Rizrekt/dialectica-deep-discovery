import json, sys
sys.path.insert(0, "/home/hatch/workspace/research/dialectica/skill-audit/pkg/dialectica/scripts")
import trued

lb = trued.call("/api/node/leaderboard", params={"limit": 5})
print("LEADERBOARD type:", type(lb), (list(lb.keys()) if isinstance(lb, dict) else len(lb)))
print(json.dumps(lb, ensure_ascii=False)[:800])

lst = trued.call("/api/node/isrs", params={"arenaId": "general", "offset": 0, "limit": 3})
print("\nISRS type:", type(lst), (list(lst.keys()) if isinstance(lst, dict) else len(lst)))
print(json.dumps(lst, ensure_ascii=False)[:800])
