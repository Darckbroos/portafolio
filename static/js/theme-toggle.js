document.addEventListener('DOMContentLoaded', () => {
  const btn       = document.getElementById('theme-toggle');
  const container = document.getElementById('themed-container');
  let   theme     = localStorage.getItem('theme') || 'light';

  function apply(t) {
    container.setAttribute('data-theme', t);
    localStorage.setItem('theme', t);
    btn.textContent = t === 'light' ? '🌙' : '☀️';
  }

  btn.addEventListener('click', () => {
    theme = theme === 'light' ? 'dark' : 'light';
    apply(theme);
  });

  apply(theme);
});