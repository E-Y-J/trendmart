import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
  resolve: {
    alias: {
      '@styles': path.resolve(__dirname, './src/reusableStyles'),
      '@redux': path.resolve(__dirname, './src/redux'),
      '@main': path.resolve(__dirname, './src/layouts/mainComponents'),
      '@children': path.resolve(__dirname, './src/layouts/layoutChildren'),
      '@api': path.resolve(__dirname, './src/api'),
    },
  },
});
