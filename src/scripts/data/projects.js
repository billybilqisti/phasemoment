/**
 * Project registry — single source of truth for the home showcase order,
 * Work modal metadata, and case-study page links.
 * Order must match the slide / project-nav order in index.html.
 */
export const projects = [
  { id: 'urbx', name: 'URBX', category: 'Spatial Architecture & Identity', href: null },
  { id: 'kura', name: 'KURA', category: 'Stage Design & Visual Identity', href: '/work/kura.html' },
  { id: 'aloomah', name: 'Aloomah', category: 'Brand + App Design', href: '/work/aloomah.html' },
  { id: 'streamline', name: 'Streamline Studio', category: 'Motion & Digital Product', href: null },
  { id: 'straightline', name: 'No Straightline', category: 'Editorial & Typography', href: null },
  { id: 'creatorloft', name: 'London Creatorloft', category: 'Packaging & Visual Direction', href: null },
];

/** Default active project (KURA), as specified in Figma Node 123:120. */
export const DEFAULT_PROJECT_INDEX = 1;

export const getProject = (id) => projects.find((p) => p.id === id) ?? null;
