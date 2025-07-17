from pathlib import Path

from pathlib import Path

def load_all_docs_from_data(data_path="data"):
    all_text = []
    tried_encodings = ["utf-8", "windows-1252", "ISO-8859-1"]

    for file in Path(data_path).rglob("*"):
        if file.suffix in [".txt", ".md"]:
            content = None
            for enc in tried_encodings:
                try:
                    with open(file, "r", encoding=enc) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            if content is None:
                print(f"⚠️ Could not decode file: {file}")
                continue

            section_header = f"\n\n## Source: {file.relative_to(data_path)}\n"
            all_text.append(section_header + content)

    return "\n\n".join(all_text)

# Usage
context = load_all_docs_from_data("data")

print(f"\n✅ Loaded context with {len(context)} characters and {context.count('## Source:')} files.\n")
print(context[:500])   # First 500 characters
print("\n... (truncated) ...\n")
print(context[-500:])  # Last 500 characters
