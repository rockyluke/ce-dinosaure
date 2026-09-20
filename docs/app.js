const input = document.querySelector('#search-input');
const filters = [...document.querySelectorAll('.filter-button')];
const groups = [...document.querySelectorAll('[data-filter]')];
const cards = [...document.querySelectorAll('.dinosaur-card')];
const lang = document.documentElement.lang === 'en' ? 'en' : 'fr';
try { localStorage.setItem('ce-dinosaure-language', lang); } catch {}
const normalize = value => value.toLocaleLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]/g, '');
function render() {
  const query = normalize(input.value);
  const selected = Object.fromEntries(groups.map(group => [group.dataset.filter, group.querySelector('[aria-pressed="true"]').dataset.value]));
  let count = 0;
  cards.forEach(card => {
    const matches = normalize(card.dataset.search).includes(query) && Object.entries(selected).every(([key, value]) => value === 'all' || card.dataset[key] === value);
    card.hidden = !matches;
    if (matches) count++;
  });
  document.querySelector('#entry-count').textContent = count;
  document.querySelector('#entry-count-label').textContent = lang === 'fr' ? (count > 1 ? 'fiches' : 'fiche') : (count === 1 ? 'entry' : 'entries');
  document.querySelector('#dinosaur-grid').hidden = count === 0;
  document.querySelector('#empty-state').hidden = count !== 0;
}
document.querySelector('#search-form').addEventListener('submit', event => event.preventDefault());
input.addEventListener('input', render);
filters.forEach(button => button.addEventListener('click', () => {
  button.parentElement.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  render();
}));
document.querySelector('#reset-search').addEventListener('click', () => {
  input.value = '';
  filters.forEach(button => button.setAttribute('aria-pressed', button.dataset.default));
  render(); input.focus();
});
document.addEventListener('keydown', event => {
  if (event.key === '/' && !event.ctrlKey && !event.metaKey && !event.altKey && !event.target.closest('input, textarea, [contenteditable]')) {
    event.preventDefault(); input.focus();
  }
});
render();
