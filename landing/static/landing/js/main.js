
const revealElements = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.14 });

revealElements.forEach(el => observer.observe(el));

const navToggle = document.querySelector('[data-nav-toggle]');
const nav = document.querySelector('[data-nav]');

if (navToggle && nav) {
  navToggle.addEventListener('click', () => {
    nav.classList.toggle('is-open');
    navToggle.classList.toggle('is-active');
  });
}



const glow = document.querySelector('.cursor-glow');
if (glow && window.matchMedia('(min-width: 821px)').matches) {
  window.addEventListener('mousemove', (e) => {
    glow.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
  });
}

window.addEventListener('scroll', () => {
  const y = window.scrollY * 0.05;
  document.querySelectorAll('.floating-card').forEach(el => {
    el.style.transform = `translateY(${Math.sin(y) * -6}px)`;
  });
}, { passive: true });
