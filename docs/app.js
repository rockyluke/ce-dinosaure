// Design scaffold: no species data or network requests.
const input = document.querySelector('#search-input');
const filters = [...document.querySelectorAll('.filter-button')];
try { localStorage.setItem('ce-dinosaure-language', document.documentElement.lang); } catch {}
function render() {
  const active = input.value.trim() !== '' || filters.some(button => button.dataset.default === 'false' && button.getAttribute('aria-pressed') === 'true');
  document.querySelector('#dinosaur-grid').hidden = active;
  document.querySelector('#empty-state').hidden = !active;
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
