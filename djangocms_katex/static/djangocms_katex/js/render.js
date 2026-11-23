// static/djangocms_katex/js/render.js
//
// Renders all formulae on a page (elements marked with data-katex-rendered="false").
// KaTeX and its mhchem extension are loaded on demand if they are not available yet,
// e.g., after a formula has been added to a page in django CMS' edit mode.

(function () {
    'use strict';

    const script = document.currentScript || document.querySelector('script[data-djangocms-katex]');
    const selector = '[data-katex-rendered="false"]';
    const chem = /\\(ce|pu)\s*{/;
    const loading = {};
    let config = {};
    let mhchem_loaded = false;

    try {
        config = JSON.parse((script && script.dataset.config) || '{}');
    } catch (e) {
        console.error(e);
    }

    // Macros are persistent on a page: Site-wide macros first, \gdef'd macros are added by KaTeX
    window.djangocms_katex_macros = Object.assign({}, config.macros, window.djangocms_katex_macros);
    const macros_need_chem = chem.test(Object.values(config.macros || {}).join(' '));

    function load(url) {
        if (!loading[url]) {
            loading[url] = new Promise(function (resolve, reject) {
                const element = document.createElement('script');

                element.src = url;
                element.onload = resolve;
                element.onerror = function () {
                    delete loading[url];
                    reject(new Error('djangocms-katex: Failed to load ' + url));
                };
                document.head.appendChild(element);
            });
        }
        return loading[url];
    }

    function has_mhchem() {
        if (!mhchem_loaded) {
            try {
                window.katex.renderToString('\\ce{H}', {throwOnError: true});
                mhchem_loaded = true;
            } catch (e) {
                mhchem_loaded = false;
            }
        }
        return mhchem_loaded;
    }

    function ensure_libraries(needs_chem) {
        return (window.katex ? Promise.resolve() : load(config.katex)).then(function () {
            if (needs_chem && !has_mhchem()) {
                return load(config.mhchem);
            }
        });
    }

    function render() {
        const elements = Array.from(document.querySelectorAll(selector));

        if (!elements.length) {
            return;
        }
        const needs_chem = macros_need_chem || elements.some(function (element) {
            return chem.test(element.textContent);
        });

        ensure_libraries(needs_chem).then(function () {
            for (const element of elements) {
                if (element.dataset.katexRendered !== 'false') {
                    continue;  // Already rendered by a concurrent call
                }
                try {
                    const options = Object.assign(
                        {throwOnError: false},
                        config.options,
                        JSON.parse(element.dataset.options || '{}'),
                        {macros: window.djangocms_katex_macros}
                    );

                    window.katex.render(element.textContent, element, options);
                    element.dataset.katexRendered = 'true';
                } catch (e) {
                    element.dataset.katexRendered = 'error';  // Shows the formula's source
                    console.error(e);
                }
            }
        }).catch(function (e) {
            for (const element of elements) {
                element.dataset.katexRendered = 'error';
            }
            console.error(e);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', render);
    } else {
        render();  // Script has been added to an already loaded page
        document.addEventListener('DOMContentLoaded', render);  // django CMS re-dispatches this event
    }
    // django CMS' edit mode: Content has been updated without a page reload
    if (window.CMS && window.CMS.$) {
        window.CMS.$(window).on('cms-content-refresh', render);
    } else {
        window.addEventListener('cms-content-refresh', render);
    }
})();
