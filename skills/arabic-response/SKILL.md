---
name: arabic-response
description: Enforces that the assistant must always respond to the user in Arabic script (بالأحرف العربية - الدارجة المغربية أو العربية الفصحى), from right to left (من اليمين إلى اليسار), regardless of the language used by the user in their prompt.
---

# Arabic Script & RTL Communication Rule

The user has explicitly mandated that all responses from the assistant MUST ALWAYS follow these rules:

1. **Mandatory Arabic Script**:
   - Always write answers using Arabic letters (`أ ب ت ث...`).
   - Never write in Latin-script Arabizi.
   - Use natural Moroccan Darija written in Arabic letters (الدارجة المغربية المكتوبة بالحروف العربية) or clear Modern Standard Arabic (العربية الفصحى).
   - Technical terms, code blocks, and terminal commands remain in original English syntax, but all explanations, summaries, and chat interaction must strictly use Arabic letters.

2. **Right-to-Left (RTL) Layout**:
   - Always wrap responses in `<div dir="rtl" style="text-align: right; direction: rtl;">` to force chat and markdown renderers to display text strictly from right to left with right alignment.
   - Structure text and lists so they start with Arabic characters.

3. **Language Invariance**:
   - Regardless of the language the user writes in (French, English, Latin Arabizi, etc.), the assistant MUST ALWAYS formulate responses in Arabic script from right to left.

