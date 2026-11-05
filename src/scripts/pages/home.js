/**
 * Home page entry (Figma Node 123:120 — Home - Scrolled)
 */
import { projects, getProject } from '../data/projects.js';
import { initClock } from '../modules/clock.js';
import { initEmblemSpin } from '../modules/emblem.js';
import { initDockModal } from '../modules/dock-modal.js';
import { initShowcase } from '../modules/showcase.js';

initClock(document.getElementById('clock-display'));
initEmblemSpin(document.getElementById('symbol-btn'));

const modal = initDockModal();
const showcase = initShowcase({ isLocked: modal.isOpen });

// Support deep-linking to a project slide via ?project=<id>
const requestedProjectId = new URLSearchParams(window.location.search).get('project');
if (requestedProjectId) {
  const targetProject = getProject(requestedProjectId);
  if (targetProject) {
    showcase.goToProject(projects.indexOf(targetProject));
  }
}

// Work modal cards: open the case study if one exists, otherwise jump to the slide.
document.querySelectorAll('.grid-card').forEach((card) => {
  card.addEventListener('click', () => {
    const project = getProject(card.getAttribute('data-project'));
    if (!project) return;
    if (project.href) {
      window.location.href = project.href;
      return;
    }
    showcase.goToProject(projects.indexOf(project));
    modal.close();
  });
});
