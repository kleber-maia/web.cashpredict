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
  const desktop = window.matchMedia('(min-width: 761px)');
  if (desktop.addEventListener) desktop.addEventListener('change', close);
  navigation.addEventListener('click', event => { if (event.target.closest('a')) close(); });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') { close(); button.focus(); } });
}
const reveal = (hash = location.hash) => {
  let id; try { id = decodeURIComponent(hash.slice(1)); } catch { return; }
  const target = id && document.getElementById(id);
  const details = target && target.closest('details');
  if (details) details.open = true;
};
window.addEventListener('hashchange', () => reveal());
document.addEventListener('click', event => {
  const link = event.target.closest('a[href^="#"]');
  if (link) reveal(link.getAttribute('href'));
});
reveal();

// Reveal only copy and small cards, never device artwork or its ancestors.
// Content stays visible without JavaScript, IntersectionObserver, or motion.
if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal-in');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  document.querySelectorAll('.hero-copy, .section-copy, .manifesto h2, .section-heading, .principles article, .price-card').forEach(element => observer.observe(element));
}
