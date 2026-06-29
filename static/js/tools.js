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
                const gdpr = t.gdpr_status === 'GDPR-klar' ? '<span class="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">GDPR-klar</span>' : '';
                const url = t.url ? `<a href="${t.url}" target="_blank" rel="noopener" class="text-indigo-600 text-sm font-medium hover:underline mt-auto">Besök →</a>` : '';
                const rating = t.rating ? `<span class="text-xs font-bold text-slate-500 ml-2">⭐ ${t.rating}</span>` : '';
                const pricing = t.pricing ? `<p class="text-xs text-slate-400 mt-1">${t.pricing}</p>` : '';
                
                return `<article class="tool-card bg-white p-7 rounded-3xl border border-slate-100 shadow-sm card-hover flex flex-col h-full" data-cat="${t.category||''}">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center">
                            <span class="text-xs font-semibold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-full">${t.category||''}</span>
                            ${rating}
                        </div>
                        ${gdpr}
                    </div>
                    <div class="flex items-center gap-3 mb-2">
                        ${t.icon_emoji ? `<span class="text-2xl">${t.icon_emoji}</span>` : ''}
                        <h3 class="text-lg font-bold">${t.name||''}</h3>
                    </div>
                    ${pricing}
                    <p class="text-slate-500 text-sm mb-4 mt-2 flex-grow leading-relaxed">${t.description||''}</p>
                    <div class="flex flex-wrap gap-2 mb-4">
                        ${(t.tags ? t.tags.split(',') : []).map(tag => `<span class="text-[10px] bg-slate-50 text-slate-500 px-2 py-1 rounded-md border border-slate-100">${tag.trim()}</span>`).join('')}
                    </div>
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
                catFilter.querySelectorAll('button').forEach(b => b.classList.remove('active', 'bg-indigo-600', 'text-white', 'border-transparent'));
                catFilter.querySelectorAll('button').forEach(b => b.classList.add('bg-white', 'text-slate-600', 'border-slate-200'));
                btn.classList.add('active', 'bg-indigo-600', 'text-white', 'border-transparent');
                btn.classList.remove('bg-white', 'text-slate-600', 'border-slate-200');
                render(activeCat);
            });
        }
    } catch(e) {
        console.error('Failed to load tools:', e);
    }
}

document.addEventListener('DOMContentLoaded', loadTools);
