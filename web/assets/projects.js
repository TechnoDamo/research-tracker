---
permalink: /assets/projects.js
---
for (const panel of document.querySelectorAll('[data-report-url]')) {
  panel.addEventListener('toggle', async () => {
    if (!panel.open || panel.dataset.loaded) return;
    const body = panel.querySelector('[data-report-body]');
    panel.dataset.loaded = 'pending';
    try {
      const response = await fetch(panel.dataset.reportUrl);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const documentFromReport = new DOMParser().parseFromString(await response.text(), 'text/html');
      const article = documentFromReport.querySelector('article.document');
      if (!article) throw new Error('Report content was not found');
      body.replaceChildren(...Array.from(article.childNodes).map(node => document.importNode(node, true)));
      panel.dataset.loaded = 'true';
    } catch {
      body.textContent = 'The inline report could not be loaded. Use the link above to open it.';
      delete panel.dataset.loaded;
    }
  });
}
