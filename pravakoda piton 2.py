import pathlib
import re

crop_rec_path = pathlib.Path("modules/crop_rec/crop_rec.c")

if not crop_rec_path.exists():
    print("crop_rec.c not found; skipping preset injection.")
    exit(0)

code = crop_rec_path.read_text()

# Skip if 1584x1156 Academy preset is already present
if "1584" in code:
    print("1584x1156 Academy preset already exists.")
    exit(0)

# Match the existing 1544x1156 (4:3) preset line/entry and duplicate it as 1584x1156 (1.37:1 Academy)
pattern = re.compile(r'([^\n]*\b1544\b[^\n]*\b1156\b[^\n]*\n)')
match = pattern.search(code)

if match:
    original_line = match.group(1)
    academy_line = (
        original_line
        .replace("1544", "1584")
        .replace("4:3", "1.37:1 Academy")
        .replace("1.33:1", "1.37:1 Academy")
    )
    code = code.replace(original_line, original_line + academy_line, 1)
    crop_rec_path.write_text(code)
    print("Added 1584x1156 (1.37:1 Academy) alongside 1544x1156 (4:3).")
else:
    print("1544x1156 entry not matched automatically; keeping existing presets untouched.")