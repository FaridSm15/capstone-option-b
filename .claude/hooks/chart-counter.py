import json, sys, os, glob

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    normalized = file_path.replace("\\", "/")
    if "charts/" in normalized and normalized.endswith(".png"):
        n = len(glob.glob("charts/*.png"))
        print(f"Chart saved: {os.path.basename(file_path)} — {n}/5 charts complete")

if __name__ == "__main__":
    main()