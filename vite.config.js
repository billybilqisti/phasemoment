import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vite';

const page = (path) => fileURLToPath(new URL(path, import.meta.url));

// Multi-page app: every HTML page must be listed here to be included in the build.
// Add new case studies as `work/<project>.html` and register them below.
export default defineConfig({
  server: {
    port: 3000,
  },
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        main: page('./index.html'),
        'work/kura': page('./work/kura.html'),
        'work/aloomah': page('./work/aloomah.html'),
      },
    },
  },
});
