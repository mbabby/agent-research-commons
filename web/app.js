'use strict';
const filters = document.querySelectorAll('[data-filter]');
filters.forEach(button => button.addEventListener('click', () => {
  filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  let visible = 0;
  document.querySelectorAll('[data-status]').forEach(row => {
    row.hidden = button.dataset.filter !== 'all' && row.dataset.status !== button.dataset.filter;
    if (!row.hidden) visible++;
  });
  const empty = document.querySelector('#filter-empty');
  if (empty) empty.hidden = visible > 0;
}));
