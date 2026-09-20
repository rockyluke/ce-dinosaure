// Keep the selected period when changing language.
try { localStorage.setItem('ce-dinosaure-language', document.documentElement.lang); } catch {}
function updateLanguageLinks() {
  const hash = ['#triassic', '#jurassic', '#cretaceous'].includes(location.hash) ? location.hash : '';
  document.querySelectorAll('.language-switch a').forEach(link => {
    link.hash = hash;
  });
}
window.addEventListener('hashchange', updateLanguageLinks);
updateLanguageLinks();
