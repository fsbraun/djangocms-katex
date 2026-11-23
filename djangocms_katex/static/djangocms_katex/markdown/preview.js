// static/djangocms_katex/markdown/preview.js
//
// Preview processor for djangocms-markdown's editor: Renders formulae ($...$ and $$...$$)
// in the editor preview as djangocms_katex/markdown.py and render.js do on the page.

(function () {
    'use strict';

    const script = document.currentScript || document.querySelector('script[data-djangocms-katex-preview]');
    let config = {};
    let formulae = [];

    try {
        config = JSON.parse((script && script.dataset.config) || '{}');
    } catch (e) {
        console.error(e);
    }

    // Code is matched first to leave it untouched. Formula patterns: Keep in sync with
    // INLINE_RE and DISPLAY_RE in djangocms_katex/markdown.py
    const pattern = new RegExp([
        '(?:^|\\n)[ ]{0,3}(`{3,}|~{3,})[^\\n]*\\n[\\s\\S]*?(?:\\n[ ]{0,3}\\1[`~]*[ \\t]*(?=\\n|$)|$)',  // Fenced code
        '(`+)(?!`)[\\s\\S]*?[^`]\\2(?!`)',  // Code span
        '(?:^|\\n)[ ]{0,3}\\$\\$([\\s\\S]+?)\\$\\$[ \\t]*(?=\\n|$)',  // Display formula
        '(?<![\\\\$])\\$(?![\\s$])((?:[^$\\\\]|\\\\[\\s\\S])+?)(?<!\\s)\\$(?![\\d$])'  // Inline formula
    ].join('|'), 'g');

    function before(text) {
        formulae = [];
        return text.replace(pattern, function (match, fence, ticks, display, inline) {
            if (display !== undefined && display.trim()) {
                formulae.push({source: match.trim(), formula: display.trim(), display: true});
                return (match.startsWith('\n') ? '\n' : '') +
                    '\n<div data-katex-preview="' + (formulae.length - 1) + '"></div>\n\n';
            }
            if (inline !== undefined) {
                formulae.push({source: match, formula: inline, display: false});
                return '<span data-katex-preview="' + (formulae.length - 1) + '"></span>';
            }
            return match;
        });
    }

    function after(element) {
        // As on a page: Site-wide macros, \gdef'd macros are available in the following formulae
        const macros = Object.assign({}, config.macros);

        for (const placeholder of element.querySelectorAll('[data-katex-preview]')) {
            const item = formulae[placeholder.dataset.katexPreview];

            placeholder.removeAttribute('data-katex-preview');
            if (!item) {
                continue;
            }
            try {
                window.katex.render(item.formula, placeholder, Object.assign(
                    {throwOnError: false},
                    config.options,
                    {displayMode: item.display, macros: macros}
                ));
                placeholder.dataset.katexRendered = 'true';
            } catch (e) {
                placeholder.textContent = item.source;  // KaTeX not available or failed: Show the source
                console.error(e);
            }
        }
    }

    window.djangocmsMarkdownPreview = window.djangocmsMarkdownPreview || [];
    window.djangocmsMarkdownPreview.push({before: before, after: after});
})();
