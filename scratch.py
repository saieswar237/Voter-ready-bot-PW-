with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = lines[:18]
new_lines.extend([
    "\n",
    "# Initialize session state for response messages\n",
    "if \"messages\" not in st.session_state:\n",
    "    st.session_state.messages = []\n",
    "\n",
    "# Declare the custom component using the path\n",
    "wizard_ui = components.declare_component(\"wizard_ui\", path=\"frontend\")\n"
])
new_lines.extend(lines[339:])

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
