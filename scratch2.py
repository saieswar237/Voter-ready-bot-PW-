with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = lines[:18]

new_lines.append("\nHTML_TEMPLATE = \"\"\"\n")
new_lines.append(html_content)
if not html_content.endswith("\n"):
    new_lines.append("\n")
new_lines.append("\"\"\"\n\n")

new_lines.append("""import os
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, "frontend")
os.makedirs(frontend_dir, exist_ok=True)
index_path = os.path.join(frontend_dir, "index.html")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(HTML_TEMPLATE)

wizard_ui = components.declare_component("wizard_ui", path=frontend_dir)
\n""")

new_lines.extend(lines[19:23]) 

new_lines.extend(lines[25:])

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
