/**
 * Spin animation for the center sun emblem button.
 * @param {HTMLElement | null} btn
 */
export function initEmblemSpin(btn) {
  if (!btn) return;

  btn.addEventListener('click', () => {
    btn.style.transition = 'transform 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)';
    btn.style.transform = 'rotate(360deg) scale(1.25)';
    setTimeout(() => {
      btn.style.transition = '';
      btn.style.transform = '';
    }, 850);
  });
}
