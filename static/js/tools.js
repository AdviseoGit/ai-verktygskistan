/**
 * Verktygskatalogen – rendering och filtrering.
 *
 * Monteras på varje sida som har ett element med id "tools-grid". Om sidan
 * också har ett element med id "tool-filters" ritas hela filterpanelen dit,
 * annars visas bara griden.
 *
 * Filtren speglar det svenska företagens faktiska tveksamhet inför AI:
 * fungerar det på svenska, och vågar vi skicka data dit? Därför är "svenska"
 * och "GDPR" egna facetter och inte bara text i beskrivningen.
 */
(function () {
    'use strict';

    var CATEGORIES = [
        { id: 'all', label: 'Alla' },
        { id: 'text', label: 'Text & skrivande' },
        { id: 'bild', label: 'Bild & design' },
        { id: 'video', label: 'Video' },
        { id: 'ljud', label: 'Ljud & röst' },
        { id: 'kod', label: 'Kod & utveckling' },
        { id: 'affar', label: 'Affär & automation' },
        { id: 'marknadsforing', label: 'Marknadsföring' },
        { id: 'juridik', label: 'Juridik & HR' },
        { id: 'produktivitet', label: 'Produktivitet' },
        { id: 'sok', label: 'Sök & research' }
    ];

    var GDPR = {
        gdpr_klar: { label: 'GDPR-klar', cls: 'bg-emerald-50 text-emerald-700 border-emerald-200' },
        dpa: { label: 'DPA krävs', cls: 'bg-sky-50 text-sky-700 border-sky-200' },
        lokal: { label: 'Kan köras lokalt', cls: 'bg-violet-50 text-violet-700 border-violet-200' },
        oklart: { label: 'Oklart läge', cls: 'bg-slate-50 text-slate-600 border-slate-200' },
        varning: { label: 'Var försiktig', cls: 'bg-rose-50 text-rose-700 border-rose-200' }
    };

    var SWEDISH = {
        bra: { label: 'Bra på svenska', cls: 'bg-blue-50 text-blue-700 border-blue-200' },
        delvis: { label: 'Delvis svenska', cls: 'bg-slate-50 text-slate-600 border-slate-200' },
        svagt: { label: 'Svagt på svenska', cls: 'bg-amber-50 text-amber-700 border-amber-200' }
    };

    var PRICE = {
        gratis: { label: 'Gratis', cls: 'bg-emerald-50 text-emerald-700 border-emerald-200' },
        freemium: { label: 'Freemium', cls: 'bg-indigo-50 text-indigo-700 border-indigo-200' },
        betald: { label: 'Betald', cls: 'bg-amber-50 text-amber-700 border-amber-200' }
    };

    var state = {
        tools: [],
        category: 'all',
        swedishOnly: false,
        gdprSafeOnly: false,
        freeOnly: false,
        query: ''
    };

    function escapeHtml(value) {
        return String(value == null ? '' : value)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;')
            .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    /**
     * tags har historiskt varit både en lista och en kommaseparerad sträng.
     * Katalogen är normaliserad numera, men rendering av en hel sida ska inte
     * kunna dö på en enskild post – därför normaliseras det defensivt här.
     */
    function toTags(value) {
        if (Array.isArray(value)) return value;
        if (typeof value === 'string') {
            return value.split(',').map(function (t) { return t.trim(); })
                        .filter(Boolean);
        }
        return [];
    }

    function badge(config, extra) {
        if (!config) return '';
        return '<span class="text-[11px] font-semibold px-2.5 py-1 rounded-full border ' +
            config.cls + ' ' + (extra || '') + '">' + escapeHtml(config.label) + '</span>';
    }

    function matches(tool) {
        if (state.category !== 'all' && tool.category !== state.category) return false;
        if (state.swedishOnly && tool.swedish !== 'bra') return false;
        if (state.gdprSafeOnly &&
            tool.gdpr !== 'gdpr_klar' && tool.gdpr !== 'lokal') return false;
        if (state.freeOnly &&
            tool.price_tier !== 'gratis' && tool.price_tier !== 'freemium') return false;

        if (state.query) {
            var haystack = [tool.name, tool.description, toTags(tool.tags).join(' ')]
                .join(' ').toLowerCase();
            if (haystack.indexOf(state.query.toLowerCase()) === -1) return false;
        }
        return true;
    }

    function sortTools(a, b) {
        if (a.featured !== b.featured) return a.featured ? -1 : 1;
        return (b.rating || 0) - (a.rating || 0);
    }

    function toolCard(tool) {
        var tags = toTags(tool.tags).slice(0, 4);
        var categoryLabel = (CATEGORIES.filter(function (c) {
            return c.id === tool.category;
        })[0] || { label: tool.category }).label;

        // rel="sponsored" sätts bara när länken faktiskt är kommersiell, så att
        // redaktionella länkar inte devalveras i onödan.
        var rel = tool.affiliate ? 'sponsored noopener' : 'noopener';
        var link = tool.url
            ? '<a href="' + escapeHtml(tool.url) + '" target="_blank" rel="' + rel + '"' +
              ' data-tool="' + escapeHtml(tool.name) + '"' +
              ' class="tool-visit mt-auto inline-flex items-center gap-1 text-indigo-600 text-sm font-bold hover:gap-2 transition-all">' +
              'Besök ' + escapeHtml(tool.name) +
              '<span aria-hidden="true">→</span></a>'
            : '';

        return '' +
        '<article class="tool-card bg-white p-6 rounded-3xl border ' +
            (tool.featured ? 'border-indigo-200 ring-1 ring-indigo-100' : 'border-slate-100') +
            ' shadow-sm card-hover flex flex-col h-full">' +
            '<div class="flex items-start justify-between gap-3 mb-4">' +
                '<div class="flex items-center gap-3 min-w-0">' +
                    '<span class="text-2xl shrink-0" aria-hidden="true">' +
                        escapeHtml(tool.icon_emoji || '🤖') + '</span>' +
                    '<div class="min-w-0">' +
                        '<h3 class="text-lg font-bold truncate">' + escapeHtml(tool.name) + '</h3>' +
                        '<p class="text-xs text-slate-400">' + escapeHtml(categoryLabel) + '</p>' +
                    '</div>' +
                '</div>' +
                '<div class="text-right shrink-0">' +
                    '<div class="text-sm font-bold text-slate-700">★ ' +
                        escapeHtml(tool.rating) + '</div>' +
                    (tool.featured
                        ? '<div class="text-[10px] font-bold text-indigo-600 uppercase tracking-wide">Redaktionens val</div>'
                        : '') +
                '</div>' +
            '</div>' +
            '<div class="flex flex-wrap gap-1.5 mb-4">' +
                badge(PRICE[tool.price_tier]) +
                badge(SWEDISH[tool.swedish]) +
                badge(GDPR[tool.gdpr]) +
            '</div>' +
            '<p class="text-slate-500 text-sm mb-4 leading-relaxed flex-grow">' +
                escapeHtml(tool.description) + '</p>' +
            '<details class="mb-4 group">' +
                '<summary class="text-xs font-semibold text-slate-500 cursor-pointer hover:text-indigo-600 list-none flex items-center gap-1">' +
                    '<span class="group-open:rotate-90 transition-transform" aria-hidden="true">▸</span>' +
                    'Pris, GDPR och svenska</summary>' +
                '<dl class="mt-3 space-y-2 text-xs text-slate-500 border-l-2 border-slate-100 pl-3">' +
                    '<div><dt class="font-semibold text-slate-700 inline">Pris: </dt>' +
                        '<dd class="inline">' + escapeHtml(tool.pricing) + '</dd></div>' +
                    '<div><dt class="font-semibold text-slate-700 inline">GDPR: </dt>' +
                        '<dd class="inline">' + escapeHtml(tool.gdpr_note) + '</dd></div>' +
                    '<div><dt class="font-semibold text-slate-700 inline">Svenska: </dt>' +
                        '<dd class="inline">' + escapeHtml(tool.swedish_note) + '</dd></div>' +
                '</dl>' +
            '</details>' +
            (tags.length
                ? '<div class="flex flex-wrap gap-1.5 mb-4">' + tags.map(function (tag) {
                      return '<span class="text-[10px] bg-slate-50 text-slate-500 px-2 py-1 rounded-md border border-slate-100">' +
                             escapeHtml(tag) + '</span>';
                  }).join('') + '</div>'
                : '') +
            link +
        '</article>';
    }

    function filterPanel() {
        var chips = CATEGORIES.map(function (cat) {
            var active = cat.id === state.category;
            return '<button type="button" data-cat="' + cat.id + '" aria-pressed="' + active + '" ' +
                'class="cat-chip px-4 py-2 rounded-xl text-sm font-semibold border transition-all ' +
                (active
                    ? 'bg-indigo-600 text-white border-transparent'
                    : 'bg-white text-slate-600 border-slate-200 hover:border-indigo-300') +
                '">' + escapeHtml(cat.label) + '</button>';
        }).join('');

        function toggle(key, label, hint) {
            var active = state[key];
            return '<button type="button" data-toggle="' + key + '" aria-pressed="' + active + '" ' +
                'title="' + escapeHtml(hint) + '" ' +
                'class="px-4 py-2 rounded-xl text-sm font-semibold border transition-all ' +
                (active
                    ? 'bg-slate-900 text-white border-transparent'
                    : 'bg-white text-slate-600 border-slate-200 hover:border-slate-400') +
                '">' + escapeHtml(label) + '</button>';
        }

        return '' +
        '<div class="space-y-5">' +
            '<div>' +
                '<label for="tool-search" class="sr-only">Sök verktyg</label>' +
                '<input id="tool-search" type="search" value="' + escapeHtml(state.query) + '" ' +
                    'placeholder="Sök bland ' + state.tools.length + ' verktyg – t.ex. avtal, video, möten…" ' +
                    'class="w-full px-5 py-3.5 rounded-xl border border-slate-200 shadow-sm focus:ring-2 focus:ring-indigo-500 outline-none text-base">' +
            '</div>' +
            '<div class="flex flex-wrap gap-2 justify-center" id="cat-chips">' + chips + '</div>' +
            '<div class="flex flex-wrap gap-2 justify-center" id="facet-toggles">' +
                toggle('swedishOnly', '🇸🇪 Bra på svenska',
                       'Visar bara verktyg vi bedömt fungerar väl på svenska.') +
                toggle('gdprSafeOnly', '🔒 GDPR-säkert',
                       'Visar verktyg som är GDPR-klara eller kan köras lokalt.') +
                toggle('freeOnly', '💸 Gratis att börja med',
                       'Visar gratis- och freemium-verktyg.') +
            '</div>' +
            '<p class="text-center text-sm text-slate-500" id="tool-count" aria-live="polite"></p>' +
        '</div>';
    }

    function render() {
        var grid = document.getElementById('tools-grid');
        if (!grid) return;

        var visible = state.tools.filter(matches).sort(sortTools);

        grid.innerHTML = visible.length
            ? visible.map(toolCard).join('')
            : '<div class="col-span-full text-center py-16 px-6 bg-white rounded-3xl border border-dashed border-slate-200">' +
                  '<p class="text-lg font-bold mb-2">Inga verktyg matchar filtret</p>' +
                  '<p class="text-slate-500 text-sm mb-5">Prova att ta bort ett filter eller söka på något bredare.</p>' +
                  '<button type="button" id="reset-filters" class="text-indigo-600 font-bold text-sm hover:underline">Nollställ alla filter</button>' +
              '</div>';

        var count = document.getElementById('tool-count');
        if (count) {
            count.textContent = visible.length === state.tools.length
                ? 'Visar alla ' + state.tools.length + ' verktyg'
                : 'Visar ' + visible.length + ' av ' + state.tools.length + ' verktyg';
        }
    }

    function refreshPanel() {
        var panel = document.getElementById('tool-filters');
        if (!panel) return;
        var focused = document.activeElement;
        var caret = focused && focused.id === 'tool-search' ? focused.selectionStart : null;
        panel.innerHTML = filterPanel();
        if (caret !== null) {
            var search = document.getElementById('tool-search');
            if (search) {
                search.focus();
                search.setSelectionRange(caret, caret);
            }
        }
    }

    function update(changes) {
        Object.keys(changes).forEach(function (key) { state[key] = changes[key]; });
        refreshPanel();
        render();
    }

    function bindEvents() {
        document.addEventListener('click', function (event) {
            var chip = event.target.closest('[data-cat]');
            if (chip) {
                update({ category: chip.dataset.cat });
                return;
            }

            var toggle = event.target.closest('[data-toggle]');
            if (toggle) {
                var key = toggle.dataset.toggle;
                var change = {};
                change[key] = !state[key];
                update(change);
                return;
            }

            if (event.target.id === 'reset-filters') {
                update({
                    category: 'all', swedishOnly: false,
                    gdprSafeOnly: false, freeOnly: false, query: ''
                });
                return;
            }

            var visit = event.target.closest('.tool-visit');
            if (visit && typeof window.gtag === 'function') {
                window.gtag('event', 'tool_click', {
                    tool_name: visit.dataset.tool,
                    link_url: visit.href
                });
            }
        });

        document.addEventListener('input', function (event) {
            if (event.target.id !== 'tool-search') return;
            state.query = event.target.value;
            render();
            var count = document.getElementById('tool-count');
            if (count) {
                var visible = state.tools.filter(matches).length;
                count.textContent = 'Visar ' + visible + ' av ' + state.tools.length + ' verktyg';
            }
        });
    }

    /** Låter en sida länka in förfiltrerat, t.ex. /ai-verktyg.html#kategori=juridik */
    function applyHash() {
        var hash = window.location.hash.replace('#', '');
        if (!hash) return;
        hash.split('&').forEach(function (pair) {
            var parts = pair.split('=');
            if (parts[0] === 'kategori' && parts[1]) state.category = parts[1];
            if (parts[0] === 'svenska') state.swedishOnly = true;
            if (parts[0] === 'gdpr') state.gdprSafeOnly = true;
            if (parts[0] === 'gratis') state.freeOnly = true;
        });
    }

    async function init() {
        var grid = document.getElementById('tools-grid');
        if (!grid) return;

        try {
            var res = await fetch('/static/tools.json');
            if (!res.ok) throw new Error('HTTP ' + res.status);
            state.tools = await res.json();
        } catch (err) {
            console.error('Kunde inte ladda verktygskatalogen:', err);
            grid.innerHTML = '<div class="col-span-full text-center py-12 text-slate-500">' +
                'Verktygslistan kunde inte laddas just nu. Ladda om sidan så försöker vi igen.</div>';
            return;
        }

        applyHash();
        refreshPanel();
        bindEvents();
        render();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
