# djangocms_katex/markdown.py
#
r"""Python-Markdown extension for formulae: ``$...$`` (inline) and ``$$...$$`` (display).

Formulae are not rendered on the server. They are turned into the markup of the KaTeX
plugin and are rendered in the browser by ``djangocms_katex/js/render.js`` (see the
``katex_assets`` template tag).

* Inline: ``$a^2 + b^2 = c^2$``. The opening ``$`` must not be followed by white space,
  the closing ``$`` neither be preceded by white space nor be followed by a digit. Hence,
  "from $5 to $10" is not a formula. ``\$`` is a literal dollar sign.
* Display: ``$$`` at the beginning of a line up to ``$$`` at the end of a line. The
  formula may span several lines but must not contain blank lines.

With djangocms-markdown the extension is registered automatically (``cms_config.py``).
To use it elsewhere add ``"djangocms_katex.markdown"`` to Python-Markdown's extensions.

This module requires the ``markdown`` package which is not a dependency of
djangocms-katex. Do not import it from other modules of this package.
"""

import json
import re
from html import escape
from xml.etree.ElementTree import SubElement

from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.inlinepatterns import InlineProcessor

# Keep in sync with static/djangocms_katex/markdown/preview.js. Formulae cannot contain blank
# lines since markdown splits the text into blocks at blank lines first.
FORMULA_RE = r"(?<![\\$])\$(?![\s$])(?P<formula>(?:[^$\\]|\\.)+?)(?<!\s)\$(?![\d$])"
# Code spans are matched to skip them: Whatever starts first, code span or formula, wins.
CODE_RE = r"(?<![\\`])(?P<ticks>`+)(?!`).+?(?<!`)(?P=ticks)(?!`)"
INLINE_RE = f"{CODE_RE}|{FORMULA_RE}"
DISPLAY_RE = re.compile(r"(?:^|\n)[ ]{0,3}\$\$(.+?)\$\$[ \t]*(?=\n|$)", re.DOTALL)


def formula_html(formula, display):
    """The markup of the KaTeX plugin (see templates/djangocms_katex/formula.html)"""
    return '<{tag} data-katex-rendered="false" data-options="{options}">{formula}</{tag}>'.format(
        tag="div" if display else "span",
        options=escape(json.dumps({"displayMode": display})),
        formula=escape(formula),
    )


class InlineFormulaProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        if m.group("formula") is None:
            return None, None, None  # Code span: Left to markdown, continue searching behind it
        # Stashed as raw html: No other markdown rule touches the formula
        return self.md.htmlStash.store(formula_html(m.group("formula"), display=False)), m.start(0), m.end(0)


class DisplayFormulaProcessor(BlockProcessor):
    def test(self, parent, block):
        match = DISPLAY_RE.search(block)
        return bool(match and match.group(1).strip())

    def run(self, parent, blocks):
        block = blocks.pop(0)
        match = DISPLAY_RE.search(block)
        before, after = block[: match.start()], block[match.end() :]
        if before.strip():
            self.parser.parseBlocks(parent, [before])
        # A paragraph only containing stashed block-level html is replaced by that html
        paragraph = SubElement(parent, "p")
        paragraph.text = self.parser.md.htmlStash.store(formula_html(match.group(1).strip(), display=True))
        if after.strip():
            blocks.insert(0, after.lstrip("\n"))


class KaTexExtension(Extension):
    def extendMarkdown(self, md):
        if "$" not in md.ESCAPED_CHARS:
            md.ESCAPED_CHARS = [*md.ESCAPED_CHARS, "$"]  # \$ is a literal dollar sign
        # Before code spans (190): Backticks within a formula are part of the formula
        md.inlinePatterns.register(InlineFormulaProcessor(INLINE_RE, md), "katex-inline", 195)
        # Before indented code blocks (80) and all other block elements
        md.parser.blockprocessors.register(DisplayFormulaProcessor(md.parser), "katex-display", 85)


def makeExtension(**kwargs):
    return KaTexExtension(**kwargs)
