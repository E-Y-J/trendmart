import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // allows access from Docker
    port: 5173,
  },
  define: {
    'process.env': import.meta.env,
  },
})
