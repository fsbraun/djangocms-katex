import pytest

markdown = pytest.importorskip("markdown")

INLINE = '<span data-katex-rendered="false" data-options="{&quot;displayMode&quot;: false}">'
DISPLAY = '<div data-katex-rendered="false" data-options="{&quot;displayMode&quot;: true}">'


def render(text):
    return markdown.markdown(
        text, extensions=["markdown.extensions.extra", "markdown.extensions.sane_lists", "djangocms_katex.markdown"]
    )


def test_inline_formula():
    assert render("Let $a^2 + b^2 = c^2$ be.") == f"<p>Let {INLINE}a^2 + b^2 = c^2</span> be.</p>"


def test_display_formula():
    assert render("$$E = mc^2$$") == f"{DISPLAY}E = mc^2</div>"


def test_display_formula_in_brackets():
    assert render("\\[E = mc^2\\]") == f"{DISPLAY}E = mc^2</div>"
    assert render("Before\n\\[\na &= b \\\\[1em]\n[c \\\\]\n\\]\nAfter") == (
        f"<p>Before</p>\n{DISPLAY}a &amp;= b \\\\[1em]\n[c \\\\]</div>\n<p>After</p>"
    )
    assert render("- item\n\n    \\[\n    z_1\n    \\]") == f"<ul>\n<li>\n<p>item</p>\n{DISPLAY}z_1</div>\n</li>\n</ul>"


def test_escaped_brackets_in_text():
    assert render("an \\[escaped\\] bracket") == "<p>an [escaped] bracket</p>"
    assert render("\\[not a link\\](url)") == "<p>[not a link](url)</p>"
    assert render("\\[ \\]") == "<p>[ ]</p>"
    assert render("    \\[x_1\\]") == "<pre><code>\\[x_1\\]\n</code></pre>"


def test_multi_line_display_formula_within_paragraph():
    html = render("Before\n$$\n\\begin{aligned}\na &= b \\\\\nc &= d\n\\end{aligned}\n$$\nAfter *text*")

    assert html == (
        "<p>Before</p>\n"
        f"{DISPLAY}\\begin{{aligned}}\na &amp;= b \\\\\nc &amp;= d\n\\end{{aligned}}</div>\n"
        "<p>After <em>text</em></p>"
    )


@pytest.mark.parametrize(
    "formula",
    ["a_1 + b_1 + c_1", "a * b * c", "\\frac{1}{2} \\\\ \\{x\\}", "[a](b)", "x^{y_1}", "\\text{costs \\$5}", "a +\nb"],
)
def test_formula_is_not_touched_by_markdown(formula):
    assert render(f"${formula}$") == f"<p>{INLINE}{formula}</span></p>"
    assert render(f"$$\n{formula}\n$$") == f"{DISPLAY}{formula}</div>"


def test_formula_is_escaped():
    assert render("$a<b$ and $c>d$ and $x & y$") == (
        f"<p>{INLINE}a&lt;b</span> and {INLINE}c&gt;d</span> and {INLINE}x &amp; y</span></p>"
    )
    assert render('$$\n\\text{"<script>"}\n$$') == f"{DISPLAY}\\text{{&quot;&lt;script&gt;&quot;}}</div>"


@pytest.mark.parametrize(
    "text",
    [
        "costs $5 to $10",
        "from $5-$10 per unit",
        "a $ sign and another $ sign",
        "open $x and close y $ here",
        "empty $$ and $ $",
    ],
)
def test_dollar_signs_in_text(text):
    assert render(text) == f"<p>{text}</p>"


def test_escaped_dollar_sign():
    assert render("\\$5 and \\$x\\$") == "<p>$5 and $x$</p>"


def test_code_is_not_touched():
    assert render("`$x_1$`") == "<p><code>$x_1$</code></p>"
    assert render("```\n$x_1$\n$$\ny\n$$\n```") == "<pre><code>$x_1$\n$$\ny\n$$\n</code></pre>"
    assert render("    $x$ and\n    $$y$$") == "<pre><code>$x$ and\n$$y$$\n</code></pre>"


def test_backticks_within_formula():
    assert render("$\\text{`code`}$ and `code`") == f"<p>{INLINE}\\text{{`code`}}</span> and <code>code</code></p>"


def test_code_span_and_formula_whichever_starts_first():
    assert render("`a $x$ b` and $y$") == f"<p><code>a $x$ b</code> and {INLINE}y</span></p>"
    assert render("``a ` $x$`` and $y$") == f"<p><code>a ` $x$</code> and {INLINE}y</span></p>"
    assert render("$a ` b$ and `$c$`") == f"<p>{INLINE}a ` b</span> and <code>$c$</code></p>"
    assert render("\\`$x$\\`") == f"<p>`{INLINE}x</span>`</p>"


def test_formulae_do_not_cross_blank_lines():
    assert render("$$\na\n\nb\n$$") == "<p>$$\na</p>\n<p>b\n$$</p>"
    assert render("$a\n\nb$") == "<p>$a</p>\n<p>b$</p>"


def test_formulae_in_other_elements():
    html = render("# Head $x^2$\n\n- item $y$\n\n    $$\n    z_1\n    $$\n\n| a |\n|---|\n| $x_1$ |")

    assert f"<h1>Head {INLINE}x^2</span></h1>" in html
    assert f"<p>item {INLINE}y</span></p>\n{DISPLAY}z_1</div>\n</li>" in html
    assert f"<td>{INLINE}x_1</span></td>" in html


def test_formula_within_emphasis():
    assert render("*$a_1*b_1$*") == f"<p><em>{INLINE}a_1*b_1</span></em></p>"
