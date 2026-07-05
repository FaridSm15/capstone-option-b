import json, sys, datetime, os, glob

STATE_FILE = ".claude/hooks/.chart_count"

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    tool_input = data.get("tool_input", {})
    command = str(tool_input.get("command", ""))[:120]
    tool_response = data.get("tool_response", {})
    if isinstance(tool_response, dict):
        interrupted = tool_response.get("interrupted", False)
        stderr = tool_response.get("stderr", "")
        status = "interrupted" if interrupted else ("error" if stderr else "ok")
    else:
        status = "unknown"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("session-log.md", "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | status:{status} | {command}\n")

    n = len(glob.glob("charts/*.png"))
    prev = 0
    if os.path.exists(STATE_FILE):
        try:
            prev = int(open(STATE_FILE).read().strip())
        except Exception:
            prev = 0
    if n > prev:
        with open(STATE_FILE, "w") as f:
            f.write(str(n))
        msg = f"Chart saved — {n}/5 charts complete"
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "systemMessage": msg}}))

if __name__ == "__main__":
    main()