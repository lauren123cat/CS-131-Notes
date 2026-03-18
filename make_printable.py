#!/usr/bin/env python3
"""Generate condensed printable copies of lecture HTML files."""

import os
import re

OVERRIDE_CSS = """
<style>
/* === Printable Override === */

/* Hide non-content elements */
.sidebar, .sidebar-toggle, .progress-bar, .quiz, .quiz-btn { display: none !important; }

/* Base typography */
html { font-size: 12px !important; }
body { line-height: 1.3 !important; }

/* Layout */
.main {
  margin-left: 0 !important;
  padding: 0.5rem !important;
  max-width: 100% !important;
}

/* Headings */
h1 { font-size: 1.4rem !important; }
h2 { font-size: 1.15rem !important; margin-top: 0.5rem !important; }
h3 { font-size: 1.05rem !important; margin-top: 0.4rem !important; }

/* Spacing */
p { margin-bottom: 0.25rem !important; }
ul, ol { margin-bottom: 0.25rem !important; }
li { margin-bottom: 0.1rem !important; }

.callout {
  padding: 0.3rem 0.5rem !important;
  margin: 0.3rem 0 !important;
}

.code-block {
  margin: 0.3rem 0 !important;
  overflow: visible !important;
}
.code-block pre {
  white-space: pre-wrap !important;
  word-wrap: break-word !important;
}
.code-body, .code-block code {
  padding: 0.3rem 0.5rem !important;
  font-size: 0.85rem !important;
}

section, .section { margin-bottom: 0.3rem !important; }
.subtitle { margin-bottom: 0.3rem !important; }

/* Force expandables open and remove toggle UI */
.expandable-content {
  display: block !important;
  max-height: none !important;
  overflow: visible !important;
}
.expandable-arrow { display: none !important; }
.expandable-header { cursor: default !important; }

/* Kill animations */
* {
  animation: none !important;
  opacity: 1 !important;
  transform: none !important;
  transition: none !important;
}
</style>
"""

src_dir = os.path.dirname(os.path.abspath(__file__))
out_dir = os.path.join(src_dir, "printable")
os.makedirs(out_dir, exist_ok=True)

for i in range(1, 19):
    fname = f"lec{i}.html"
    src = os.path.join(src_dir, fname)
    if not os.path.exists(src):
        print(f"SKIP: {fname} not found")
        continue

    with open(src, "r", encoding="utf-8") as f:
        html = f.read()

    # Insert override CSS right before </head>
    html = html.replace("</head>", OVERRIDE_CSS + "\n</head>", 1)

    # Remove <script>...</script> blocks (interactive JS not needed)
    html = re.sub(r'<script\b[^>]*>.*?</script>', '', html, flags=re.DOTALL)

    dst = os.path.join(out_dir, fname)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK: {fname}")

print(f"\nDone. Files written to {out_dir}/")
