---
permalink: /assets/external-links.js
---
window.researchTrackerExternalLinks = (root) => {
  for (const link of root.querySelectorAll('a[href]')) {
    const url = new URL(link.getAttribute('href'), window.location.href);
    if (['http:', 'https:'].includes(url.protocol) && url.origin !== window.location.origin) {
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
    }
  }
};
window.researchTrackerExternalLinks(document);
