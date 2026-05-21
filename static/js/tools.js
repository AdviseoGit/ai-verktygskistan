// Load tools from tools.json and render the grid
async function loadTools() {
    try {
        const res = await fetch('/static/tools.json');
        const tools = await res.json();
        const grid = document.getElementById('tools-grid');
        if (!grid) return;

        const catFilter = document.getElementById('cat-filter');
        let activeCat = 'all';

        function render(cat) {
            const filtered = cat === 'all' ? tools : tools.filter(t => t.category === cat);
            grid.innerHTML = filtered.map(t => {
                const gdpr = t.gdpr_ready ? '<span class="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">GDPR-redo</span>' : '';
                const url = t.url ? `<a href="${t.url}" target="_blank" rel="noopener" class="text-indigo-600 text-sm font-medium hover:underline">BesÃ¶k â†’</a>` : '';
                return `<article class="tool-card bg-white p-7 rounded-3xl border border-slate-100 shadow-sm card-hover" data-cat="${t.category||''}">
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-xs font-semibold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-full">${t.category||''}</span>
                        ${gdpr}
                    </div>
                    <h3 class="text-lg font-bold mb-2">${t.name||''}</h3>
                    <p class="text-slate-500 text-sm mb-4 leading-relaxed">${t.description||''}</p>
                    ${url}
                </article>`;
            }).join('');
        }

        render(activeCat);

        if (catFilter) {
            catFilter.addEventListener('click', e => {
                const btn = e.target.closest('[data-cat]');
                if (!btn) return;
                activeCat = btn.dataset.cat;
                catFilter.querySelectorAll('button').forEach(b => b.classList.remove('active', 'bg-indigo-600', 'text-white'));
                btn.classList.add('active', 'bg-indigo-600', 'text-white');
                render(activeCat);
            });
        }
    } catch(e) {
        console.error('Failed to load tools:', e);
    }
}

document.addEventListener('DOMContentLoaded', loadTools);
