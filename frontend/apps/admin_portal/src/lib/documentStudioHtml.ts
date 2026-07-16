/** Constrained HTML helpers for Document Studio — no TipTap dependency. */

const ALLOWED_TAGS = new Set([
  "p",
  "br",
  "strong",
  "b",
  "em",
  "i",
  "u",
  "ul",
  "ol",
  "li",
  "h1",
  "h2",
  "h3",
  "span",
  "div",
]);

export function wrapPlainAsHtml(text: string): string {
  const escaped = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
  return `<p>${escaped.replace(/\n/g, "<br>")}</p>`;
}

export function ensureHtmlDocument(content: string, contentType?: string | null): string {
  const raw = (content || "").trim();
  if (!raw) return "<p></p>";
  if (contentType?.includes("html") || /<\/?[a-z][\s\S]*>/i.test(raw)) {
    return sanitizeStudioHtml(raw);
  }
  return wrapPlainAsHtml(raw);
}

export function sanitizeStudioHtml(html: string): string {
  if (typeof window === "undefined") {
    return html.replace(/<script[\s\S]*?>[\s\S]*?<\/script>/gi, "");
  }
  const template = document.createElement("template");
  template.innerHTML = html;
  const walk = (node: Node) => {
    const children = Array.from(node.childNodes);
    for (const child of children) {
      if (child.nodeType === Node.ELEMENT_NODE) {
        const el = child as HTMLElement;
        const tag = el.tagName.toLowerCase();
        if (!ALLOWED_TAGS.has(tag)) {
          el.replaceWith(...Array.from(el.childNodes));
          continue;
        }
        for (const attr of Array.from(el.attributes)) {
          const name = attr.name.toLowerCase();
          if (name.startsWith("on") || name === "href" || name === "src" || name === "style") {
            el.removeAttribute(attr.name);
          }
        }
        walk(el);
      } else if (child.nodeType === Node.COMMENT_NODE) {
        child.parentNode?.removeChild(child);
      }
    }
  };
  walk(template.content);
  return template.innerHTML || "<p></p>";
}

export function htmlFileName(name: string): string {
  const base = name.replace(/\.(txt|html|htm)$/i, "") || "letter";
  return `${base}.html`;
}
