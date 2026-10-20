import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Built into the Worker's static assets: https://exam.khmermath.org/teach/
export default defineConfig({
  base: '/teach/',
  plugins: [react()],
  build: { outDir: '../public/teach', emptyOutDir: true, sourcemap: false },
  server: { port: 5173, proxy: { '/api': 'http://localhost:8787' } },
});
