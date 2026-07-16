"use client";

import Placeholder from "@tiptap/extension-placeholder";
import Underline from "@tiptap/extension-underline";
import { EditorContent, useEditor } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import { useEffect } from "react";
import { sanitizeStudioHtml } from "@/lib/documentStudioHtml";

type DocumentTiptapEditorProps = {
  value: string;
  dir?: "ltr" | "rtl";
  onChange: (html: string) => void;
  placeholder?: string;
};

export function DocumentTiptapEditor({
  value,
  dir = "ltr",
  onChange,
  placeholder = "Write the official letter…",
}: DocumentTiptapEditorProps) {
  const editor = useEditor({
    extensions: [
      StarterKit.configure({
        heading: { levels: [1, 2, 3] },
      }),
      Underline,
      Placeholder.configure({ placeholder }),
    ],
    content: value || "<p></p>",
    editorProps: {
      attributes: {
        class: "mp-doc-editor mp-tiptap-editor",
        dir,
        role: "textbox",
        "aria-multiline": "true",
        "aria-label": "Document body",
      },
    },
    onUpdate: ({ editor: ed }) => {
      onChange(sanitizeStudioHtml(ed.getHTML()));
    },
    immediatelyRender: false,
  });

  useEffect(() => {
    if (!editor) return;
    editor.view.dom.setAttribute("dir", dir);
  }, [editor, dir]);

  useEffect(() => {
    if (!editor) return;
    const current = editor.getHTML();
    const next = value || "<p></p>";
    if (sanitizeStudioHtml(current) !== sanitizeStudioHtml(next)) {
      editor.commands.setContent(next, false);
    }
  }, [editor, value]);

  if (!editor) {
    return <div className="mp-doc-editor" aria-busy="true" />;
  }

  return (
    <div className="mp-tiptap-shell">
      <div className="mp-row" role="toolbar" aria-label="Formatting">
        <button
          type="button"
          className="mp-btn"
          aria-pressed={editor.isActive("bold")}
          onClick={() => editor.chain().focus().toggleBold().run()}
        >
          Bold
        </button>
        <button
          type="button"
          className="mp-btn"
          aria-pressed={editor.isActive("italic")}
          onClick={() => editor.chain().focus().toggleItalic().run()}
        >
          Italic
        </button>
        <button
          type="button"
          className="mp-btn"
          aria-pressed={editor.isActive("underline")}
          onClick={() => editor.chain().focus().toggleUnderline().run()}
        >
          Underline
        </button>
        <button
          type="button"
          className="mp-btn"
          aria-pressed={editor.isActive("bulletList")}
          onClick={() => editor.chain().focus().toggleBulletList().run()}
        >
          List
        </button>
        <button
          type="button"
          className="mp-btn"
          aria-pressed={editor.isActive("heading", { level: 2 })}
          onClick={() => editor.chain().focus().toggleHeading({ level: 2 }).run()}
        >
          Heading
        </button>
      </div>
      <EditorContent editor={editor} />
    </div>
  );
}
