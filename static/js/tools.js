document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/tools');
        if (!response.ok) throw new Error('Failed to fetch tools');
        const tools = await response.json();
        
        const grid = document.getElementById('tools-grid');
        grid.innerHTML = ''; // Clear hardcoded tools
        
        tools.forEach(tool => {
            const tagsHtml = tool.tags.split(',').map(tag => 
                `<span class="bg-slate-100 text-slate-600 text-xs font-semibold px-3 py-1 rounded-full">${tag.trim()}</span>`
            ).join('');
            
            const gdprClass = tool.gdpr_status.includes('GDPR-klar') ? 'tag-gdpr' : 
                              (tool.gdpr_status.includes('EU-data') || tool.gdpr_status.includes('SE-baserat') ? 'tag-gdpr' : 'tag-paid');
            
            const ratingColor = tool.rating >= 9.0 ? 'text-emerald-600' : 
                               (tool.rating >= 8.0 ? 'text-emerald-500' : 'text-amber-600');

            const cardHtml = `
            <article class="tool-card bg-white p-7 rounded-3xl border border-slate-100 shadow-sm card-hover fade-in" data-cat="${tool.category}">
                <div class="flex justify-between items-start mb-4">
                    <div class="w-12 h-12 ${tool.icon_bg_color} rounded-2xl flex items-center justify-center text-2xl">${tool.icon_emoji}</div>
                    <span class="${gdprClass} text-xs font-bold px-3 py-1 rounded-full">${tool.gdpr_status}</span>
                </div>
                <h3 class="text-lg font-bold mb-2">${tool.name}</h3>
                <p class="text-slate-500 text-sm mb-4 leading-relaxed">${tool.description}</p>
                <div class="flex flex-wrap gap-2 mb-4">
                    ${tagsHtml}
                </div>
                <div class="pt-4 border-t border-slate-100 flex justify-between items-center">
                    <span class="text-sm font-bold">${tool.pricing}</span>
                    <span class="text-xs ${ratingColor} font-semibold">★ ${tool.rating}/10</span>
                </div>
            </article>`;
            
            grid.insertAdjacentHTML('beforeend', cardHtml);
        });
    } catch (err) {
        console.error(err);
    }
});
