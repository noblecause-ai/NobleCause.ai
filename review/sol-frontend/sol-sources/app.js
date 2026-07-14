(() => {
  'use strict';

  const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
  const panels = Array.from(document.querySelectorAll('[role="tabpanel"]'));

  function activateTab(tab, updateHash = false) {
    tabs.forEach((item) => {
      const active = item === tab;
      item.setAttribute('aria-selected', String(active));
      item.tabIndex = active ? 0 : -1;
    });
    panels.forEach((panel) => {
      panel.hidden = panel.id !== tab.getAttribute('aria-controls');
    });
    if (updateHash) history.replaceState(null, '', `#${tab.getAttribute('aria-controls')}`);
  }

  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => activateTab(tab, true));
    tab.addEventListener('keydown', (event) => {
      if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      let nextIndex = index;
      if (event.key === 'ArrowRight') nextIndex = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') nextIndex = (index - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') nextIndex = 0;
      if (event.key === 'End') nextIndex = tabs.length - 1;
      tabs[nextIndex].focus();
      activateTab(tabs[nextIndex], true);
    });
  });

  const hashTarget = location.hash.slice(1);
  const hashTab = tabs.find((tab) => tab.getAttribute('aria-controls') === hashTarget);
  activateTab(hashTab || tabs[0]);

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', () => {
      const id = link.getAttribute('href').slice(1);
      const ownerTab = tabs.find((tab) => tab.getAttribute('aria-controls') === id);
      if (ownerTab) activateTab(ownerTab);
    });
  });
})();
