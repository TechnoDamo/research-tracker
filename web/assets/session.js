---
permalink: /assets/session.js
---
const backLink = document.querySelector('[data-session-return]');
const reportPath = new URLSearchParams(window.location.search).get('from');

if (backLink && reportPath) {
  const target = new URL(reportPath, window.location.origin);
  const basePath = window.location.pathname.split('/topics/')[0];
  if (
    target.origin === window.location.origin &&
    target.pathname.startsWith(basePath + '/topics/') &&
    !target.pathname.includes('/sessions/')
  ) {
    backLink.href = target.pathname + target.search + target.hash;
    backLink.hidden = false;
  }
}
