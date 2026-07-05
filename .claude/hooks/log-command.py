import json, sys, datetime

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
        if interrupted:
            status = "interrupted"
        elif stderr:
            status = "error"
        else:
            status = "ok"
    else:
        status = "unknown"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("session-log.md", "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | status:{status} | {command}\n")

if __name__ == "__main__":
    main()