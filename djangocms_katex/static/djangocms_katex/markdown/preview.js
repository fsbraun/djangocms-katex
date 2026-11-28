// static/djangocms_katex/markdown/preview.js
//
// Preview processor for djangocms-markdown's editor: Renders formulae ($...$, $$...$$, \[...\])
// in the editor preview as djangocms_katex/markdown.py and render.js do on the page.
//
// Before the preview is rendered, formulae are replaced by tokens (plain text which markdown
// does not touch). Afterwards, the tokens are replaced by the rendered formulae - or by the
// formula's source if a token ended up within code.

(function () {
    'use strict';

    const script = document.currentScript || document.querySelector('script[data-djangocms-katex-preview]');
    const OPEN = String.fromCharCode(0xE000);  // Private use characters
    const CLOSE = String.fromCharCode(0xE001);
    const tokens = new RegExp('(' + OPEN + '\\d+' + CLOSE + ')');
    let config = {};
    let formulae = [];

    try {
        config = JSON.parse((script && script.dataset.config) || '{}');
    } catch (e) {
        console.error(e);
    }

    // Formulae and code spans end at blank lines: Markdown splits the text into blocks first
    const no_blank_line = '(?!\\n[ \\t]*\\n)';
    // Fenced code and code spans are matched to skip them: Whatever starts first wins. Indented
    // code depends on its context (e.g., lists) and is handled by restoring tokens within code.
    // Formula patterns: Keep in sync with FORMULA_RE and DISPLAY_RE in djangocms_katex/markdown.py
    const pattern = new RegExp([
        '(?:^|\\n)[ ]{0,3}(`{3,}|~{3,})[^\\n]*\\n[\\s\\S]*?(?:\\n[ ]{0,3}\\1[`~]*[ \\t]*(?=\\n|$)|$)',  // Fenced code
        '(?<![\\\\`])(`+)(?!`)(?:' + no_blank_line + '[\\s\\S])+?(?<!`)\\2(?!`)',  // Code span
        '(?:^|\\n)([ \\t]*)(?:\\$\\$((?:' + no_blank_line + '[\\s\\S])+?)\\$\\$' +  // Display formula: $$...$$
            '|\\\\\\[((?:' + no_blank_line + '(?:[^\\\\]|\\\\[\\s\\S]))+?)\\\\\\])[ \\t]*(?=\\n|$)',  // or \[...\]
        '(?<![\\\\$])\\$(?![\\s$])((?:' + no_blank_line + '(?:[^$\\\\]|\\\\[\\s\\S]))+?)(?<!\\s)\\$(?![\\d$])'  // Inline
    ].join('|'), 'g');

    function token(item) {
        formulae.push(item);
        return OPEN + (formulae.length - 1) + CLOSE;
    }

    function before(text) {
        formulae = [];
        return text.replace(pattern, function (match, fence, ticks, indent, dollars, brackets, inline) {
            const display = dollars !== undefined ? dollars : brackets;

            if (display !== undefined && display.trim()) {
                const newline = match.startsWith('\n') ? '\n' : '';
                const dedent = function (lines) {
                    return lines.split('\n').map(function (line) {
                        return indent && line.startsWith(indent) ? line.slice(indent.length) : line;
                    }).join('\n');
                };
                const placeholder = token({
                    source: dedent(match.slice(newline.length + indent.length)),
                    formula: dedent(display).trim(),
                    display: true
                });

                if (/^ {0,3}$/.test(indent)) {
                    return newline + '\n' + indent + placeholder + '\n\n';  // A block of its own
                }
                return newline + indent + placeholder;  // List content or indented code
            }
            if (inline !== undefined) {
                return token({source: match, formula: inline, display: false});
            }
            return match;
        });
    }

    function restore(text) {
        return text.split(tokens).map(function (part) {
            const item = tokens.test(part) && formulae[part.slice(1, -1)];

            return item ? item.source : part;
        }).join('');
    }

    function render(item, macros) {
        const element = document.createElement(item.display ? 'div' : 'span');

        try {
            window.katex.render(item.formula, element, Object.assign(
                {throwOnError: false},
                config.options,
                {displayMode: item.display, macros: macros}
            ));
            element.dataset.katexRendered = 'true';
        } catch (e) {
            element.textContent = item.source;  // KaTeX not available or failed: Show the source
            console.error(e);
        }
        return element;
    }

    function after(element) {
        // As on a page: Site-wide macros, \gdef'd macros are available in the following formulae
        const macros = Object.assign({}, config.macros);
        const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
        const nodes = [];

        while (walker.nextNode()) {
            if (walker.currentNode.nodeValue.includes(OPEN)) {
                nodes.push(walker.currentNode);
            }
        }
        for (const node of nodes) {
            const parent = node.parentElement;

            if (parent.closest('code, pre')) {
                node.nodeValue = restore(node.nodeValue);  // Code is not touched
                continue;
            }
            const fragment = document.createDocumentFragment();
            let only_display = true;

            for (const part of node.nodeValue.split(tokens)) {
                const item = tokens.test(part) && formulae[part.slice(1, -1)];

                if (item) {
                    fragment.appendChild(render(item, macros));
                    only_display = only_display && item.display;
                } else if (part) {
                    fragment.appendChild(document.createTextNode(part));
                    only_display = only_display && !part.trim();
                }
            }
            if (only_display && parent.tagName === 'P' && parent.childNodes.length === 1) {
                parent.replaceWith(fragment);  // Display formulae are not part of a paragraph
            } else {
                node.replaceWith(fragment);
            }
        }
        // Tokens which are not text, e.g., within the title of a link
        for (const child of element.querySelectorAll('*')) {
            for (const attribute of Array.from(child.attributes)) {
                if (attribute.value.includes(OPEN)) {
                    attribute.value = restore(attribute.value);
                }
            }
        }
    }

    window.djangocmsMarkdownPreview = window.djangocmsMarkdownPreview || [];
    window.djangocmsMarkdownPreview.push({before: before, after: after});
})();
