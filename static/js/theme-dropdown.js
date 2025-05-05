document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('themed-container');
  const items     = document.querySelectorAll('#theme-dropdown .dropdown-item');
  const btn       = document.getElementById('theme-button');
  let   theme     = localStorage.getItem('theme') || 'light';

  function applyTheme(t) {
    // 1. Establece el atributo y guarda
    container.setAttribute('data-theme', t);
    localStorage.setItem('theme', t);

    // 2. Cierra el dropdown (Bootstrap 5)
    const dd = bootstrap.Dropdown.getInstance(btn);
    if (dd) dd.hide();

    // 3. Cambia texto del botón al seleccionado
    const idx = Array.from(items).findIndex(el => el.dataset.theme === t);
    btn.textContent = items[idx].textContent;

    // 4. Ajusta la clase (color de fondo)
    btn.className = 'btn dropdown-toggle';
    if (t === 'light')  btn.classList.add('btn-info');
    if (t === 'dark')   btn.classList.add('btn-dark');
    if (t === 'matrix') btn.classList.add('btn-success');

    // 5. Arranca/detiene Matrix
    if (t === 'matrix') startMatrix();
    else                stopMatrix();
  }

  // 6. Click en cada opción
  items.forEach(el =>
    el.addEventListener('click', ev => {
      ev.preventDefault();
      applyTheme(el.dataset.theme);
    })
  );

  // 7. Al cargar, aplica tema guardado
  applyTheme(theme);
});