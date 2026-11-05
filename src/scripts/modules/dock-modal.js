/**
 * Bottom dock (Home / Work / About) + overlay modal.
 * @param {{ defaultTab?: string, onHomeClick?: (() => void) | null }} [options]
 * @returns {{ isOpen: () => boolean, open: (tab: string) => void, close: () => void }}
 */
export function initDockModal({ defaultTab = 'home', onHomeClick = null } = {}) {
  const dockTabs = document.querySelectorAll('.dock-item');
  const modal = document.getElementById('content-modal');
  const modalClose = document.getElementById('modal-close');
  const modalBackdrop = document.getElementById('modal-backdrop');
  const sections = {
    work: document.getElementById('modal-work-content'),
    about: document.getElementById('modal-about-content'),
  };

  let currentModalTab = null;
  const isOpen = () => modal?.classList.contains('open') ?? false;

  function setActiveTab(tabName) {
    dockTabs.forEach((tab) => tab.classList.toggle('active', tab.getAttribute('data-tab') === tabName));
  }

  function close() {
    if (!modal) return;
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    currentModalTab = null;
    setActiveTab(defaultTab);
  }

  function open(tabName) {
    if (tabName === 'home') {
      if (typeof onHomeClick === 'function') {
        onHomeClick();
        return;
      }
      close();
      return;
    }
    if (!modal || !sections[tabName]) {
      close();
      return;
    }
    if (isOpen() && currentModalTab === tabName) {
      close();
      return;
    }
    currentModalTab = tabName;
    setActiveTab(tabName);
    Object.entries(sections).forEach(([key, el]) => {
      if (el) el.style.display = key === tabName ? 'block' : 'none';
    });
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
  }

  dockTabs.forEach((tab) => tab.addEventListener('click', () => open(tab.getAttribute('data-tab'))));
  modalClose?.addEventListener('click', close);
  modalBackdrop?.addEventListener('click', close);

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && isOpen()) close();
  });

  return { isOpen, open, close };
}
