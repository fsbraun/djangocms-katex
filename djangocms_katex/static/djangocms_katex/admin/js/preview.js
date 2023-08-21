// static/djangocms_katex/admin/js/preview.js
//

document.addEventListener("DOMContentLoaded", function () {
    'use strict';

    const display_style = document.getElementById('id_katex_display_style');
    const preview_area = document.getElementById('preview_area_id');
    const input_field = document.getElementById('id_katex');
    const error_field = document.getElementById('katex-error');
    const ace_field = document.getElementById('katex-ace-editor');

    // Prepare ace field and hide textarea
    ace_field.style.height = window.getComputedStyle(input_field).height;
    ace_field.style.width = "100%";
    input_field.style.display = "None";

    // init editor with settings
    var editor = ace.edit(ace_field, {
        mode: 'ace/mode/latex',
        fontSize: '14px'
    });
    var darkMode;
    if (window.parent.CMS.API.Helpers.getColorScheme) {
        darkMode = window.parent.CMS.API.Helpers.getColorScheme() === 'dark';
    } else {
        // django CMS pre-3.11.1
        darkMode =  window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    if (darkMode) {
        editor.setTheme('ace/theme/tomorrow_night');
    }  else {
        editor.setTheme('ace/theme/github');
    }
    editor.getSession().setValue(input_field.value);

    function update_formula() {
        const display_type = display_style.value !== '0';
        const fleqn = display_style.value === '2';
        preview_area.innerHTML = (display_type ? '<div></div>' : '<span></span>');
        input_field.value = editor.getSession().getValue();
        try {
            katex.render(input_field.value, preview_area.children[0], {
                throwOnError: true,
                displayMode: display_type,
                fleqn: fleqn
            });
            error_field.textContent = '';
        } catch(e) {
           katex.render(input_field.value, preview_area.children[0], {
                throwOnError: false,
                displayMode: display_type,
                fleqn: fleqn
            });
            let message = String(e);
            if (message.startsWith('ParseError: ')) {
                message = message.slice('ParseError: '.length);
            }
            error_field.textContent = message;
            console.error(e);
        }
    }
    editor.getSession().addEventListener('change', update_formula);
    editor.focus();
    display_style.addEventListener('change', update_formula);
    update_formula();
 });
