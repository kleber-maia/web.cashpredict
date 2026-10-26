/* Native disclosures and progressive navigation, no remote runtime. */
document.documentElement.classList.add('js');
const button = document.querySelector('.menu');
const navigation = document.getElementById('navigation');
if (button && navigation) {
  button.hidden = false;
  const close = () => { button.setAttribute('aria-expanded','false'); navigation.classList.remove('is-open'); button.querySelector('span').textContent = '+'; };
  button.addEventListener('click', () => {
    const opened = button.getAttribute('aria-expanded') === 'true';
    button.setAttribute('aria-expanded',String(!opened));
    navigation.classList.toggle('is-open',!opened);
    button.querySelector('span').textContent = opened ? '+' : '−';
  });
  navigation.addEventListener('click', event => { if (event.target.closest('a')) close(); });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') { close(); button.focus(); } });
}
const reveal = () => {
  let id; try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
  const target = id && document.getElementById(id);
  const details = target && target.closest('details');
  if (details) details.open = true;
};
window.addEventListener('hashchange',reveal);
reveal();
