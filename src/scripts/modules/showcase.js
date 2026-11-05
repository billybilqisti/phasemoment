import { projects, DEFAULT_PROJECT_INDEX } from '../data/projects.js';

/**
 * Full-screen project showcase: background slides + right-hand project nav,
 * driven by wheel, keyboard arrows, touch swipe, and clicks.
 *
 * @param {object} opts
 * @param {() => boolean} opts.isLocked  Returns true when input should be ignored (e.g. modal open).
 * @returns {{ goToProject: (index: number) => void, getCurrentIndex: () => number }}
 */
export function initShowcase({ isLocked = () => false } = {}) {
  const slides = document.querySelectorAll('.slide');
  const projectItems = document.querySelectorAll('.project-item');
  const projectNav = document.getElementById('project-nav');

  let currentIndex = DEFAULT_PROJECT_INDEX;
  let isThrottled = false;
  let touchStartY = 0;

  function syncSlideVideos() {
    slides.forEach((slide, idx) => {
      const video = slide.querySelector('video');
      if (!video) return;
      if (idx === currentIndex) {
        video.play().catch(() => {});
      } else {
        video.pause();
      }
    });
  }

  function goToProject(index) {
    if (index < 0) index = projects.length - 1;
    if (index >= projects.length) index = 0;
    currentIndex = index;

    slides.forEach((slide, idx) => slide.classList.toggle('active', idx === currentIndex));
    projectItems.forEach((item, idx) => item.classList.toggle('active', idx === currentIndex));
    syncSlideVideos();
  }

  syncSlideVideos();

  // Right-hand menu: clicking the already-active project opens its case study.
  projectItems.forEach((item) => {
    item.addEventListener('click', () => {
      const idx = parseInt(item.getAttribute('data-index'), 10);
      const href = projects[idx]?.href;
      if (idx === currentIndex && href) {
        window.location.href = href;
        return;
      }
      goToProject(idx);
    });
  });

  // Active slide with a case-study link is clickable.
  slides.forEach((slide) => {
    slide.addEventListener('click', () => {
      const href = slide.getAttribute('data-href');
      if (href && slide.classList.contains('active')) {
        window.location.href = href;
      }
    });
  });

  // Wheel / trackpad navigation with throttling
  window.addEventListener('wheel', (e) => {
    if (isLocked() || isThrottled) return;
    // Threshold to prevent oversensitivity on smooth trackpads
    if (Math.abs(e.deltaY) > 25) {
      isThrottled = true;
      goToProject(currentIndex + (e.deltaY > 0 ? 1 : -1));
      setTimeout(() => { isThrottled = false; }, 700);
    }
  }, { passive: true });

  // Keyboard arrows
  window.addEventListener('keydown', (e) => {
    if (isLocked()) return;
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight') goToProject(currentIndex + 1);
    else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') goToProject(currentIndex - 1);
  });

  // Touch swipe
  window.addEventListener('touchstart', (e) => {
    touchStartY = e.touches[0].clientY;
  }, { passive: true });

  window.addEventListener('touchend', (e) => {
    if (isLocked()) return;
    const diff = touchStartY - e.changedTouches[0].clientY;
    if (Math.abs(diff) > 50) goToProject(currentIndex + (diff > 0 ? 1 : -1));
  }, { passive: true });

  // Right-hand menu auto-expand on hover
  if (projectNav) {
    let hoverTimeout;
    projectNav.addEventListener('mouseenter', () => {
      clearTimeout(hoverTimeout);
      projectNav.classList.add('expanded');
    });
    projectNav.addEventListener('mouseleave', () => {
      hoverTimeout = setTimeout(() => projectNav.classList.remove('expanded'), 350);
    });
  }

  return { goToProject, getCurrentIndex: () => currentIndex };
}
