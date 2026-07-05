2026-07-04 22:13:13 | status:ok | cd "C:\Users\Farid Simon\Documents\capstone-option-b" && ls scripts/ 2>&1 | head -20
2026-07-04 22:13:16 | status:ok | cd "C:\Users\Farid Simon\Documents\capstone-option-b" && ls venv 2>&1 | head; ls .venv 2>&1 | head
2026-07-04 22:13:22 | status:ok | cd "C:\Users\Farid Simon\Documents\capstone-option-b" && ./venv/Scripts/python.exe scripts/01_explore.py 2>&1 | tail -10
2026-07-04 22:15:07 | status:ok | cd "C:\Users\Farid Simon\Documents\capstone-option-b" && ls scripts/ 2>&1 && echo "---venv check---" && ls venv 2>&1 || 
2026-07-04 22:15:12 | status:ok | cd "C:\Users\Farid Simon\Documents\capstone-option-b" && source venv/Scripts/activate && python scripts/02_clean.py
2026-07-04 22:15:50 | status:ok | find . -iname "*log*" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | head -50
2026-07-04 22:16:00 | status:ok | cd "C:\Users\Farid Simon\Documents\capstone-option-b" && ./venv/Scripts/python.exe scripts/02_clean.py
