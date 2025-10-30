function escapeHtml(unsafe: string): string {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// Very small markdown-to-HTML converter for headings, lists, bold, paragraphs
export function renderSimpleMarkdown(markdown: string): string {
  const lines = markdown.replace(/\r\n?/g, "\n").split("\n");
  let html: string[] = [];
  let inList = false;
  let paraBuffer: string[] = [];

  const flushParagraph = () => {
    if (paraBuffer.length > 0) {
      const text = paraBuffer.join(" ");
      const withBold = text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
      html.push(`<p>${withBold}</p>`);
      paraBuffer = [];
    }
  };

  for (const raw of lines) {
    const line = raw.trimEnd();
    if (line.trim() === "") {
      if (inList) {
        html.push("</ul>");
        inList = false;
      }
      flushParagraph();
      continue;
    }

    if (line.startsWith("### ")) {
      flushParagraph();
      if (inList) { html.push("</ul>"); inList = false; }
      html.push(`<h3>${escapeHtml(line.slice(4))}</h3>`);
      continue;
    }
    if (line.startsWith("## ")) {
      flushParagraph();
      if (inList) { html.push("</ul>"); inList = false; }
      html.push(`<h2>${escapeHtml(line.slice(3))}</h2>`);
      continue;
    }
    if (line.startsWith("# ")) {
      flushParagraph();
      if (inList) { html.push("</ul>"); inList = false; }
      html.push(`<h1>${escapeHtml(line.slice(2))}</h1>`);
      continue;
    }

    if (line.startsWith("- ")) {
      flushParagraph();
      if (!inList) {
        html.push("<ul>");
        inList = true;
      }
      const item = line.slice(2).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
      html.push(`<li>${escapeHtml(item)}</li>`);
      continue;
    }

    // table lines or code blocks are left as-is inside a paragraph
    paraBuffer.push(escapeHtml(line));
  }

  if (inList) html.push("</ul>");
  flushParagraph();

  return html.join("\n");
}

// Prefer a fully-featured converter if available
export function renderMarkdown(md: string): string {
  try {
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const { marked } = require('marked');
    return marked.parse(md, { breaks: true, mangle: false, headerIds: false });
  } catch (e) {
    return renderSimpleMarkdown(md);
  }
}
