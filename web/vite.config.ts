/// <reference types="vitest/config" />
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { defineConfig, loadEnv, type Plugin } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

const require = createRequire(import.meta.url);
const API_TARGET = process.env.KHATA_API_TARGET ?? 'http://localhost:8000';

/**
 * Serves MSW's worker script only when mocks are enabled. It is never copied
 * into `dist/`, so a production build cannot register it.
 */
function mockServiceWorker(enabled: boolean): Plugin {
  const serve = (
    req: { url?: string },
    res: { setHeader: (k: string, v: string) => void; end: (b: string) => void },
    next: () => void,
  ): void => {
    if (!enabled || req.url?.split('?')[0] !== '/mockServiceWorker.js') {
      next();
      return;
    }
    res.setHeader('Content-Type', 'application/javascript');
    res.end(readFileSync(require.resolve('msw/mockServiceWorker.js'), 'utf8'));
  };
  return {
    name: 'khata-mock-service-worker',
    configureServer(server) {
      server.middlewares.use(serve);
    },
    configurePreviewServer(server) {
      server.middlewares.use(serve);
    },
  };
}

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), 'VITE_');
  const mocksEnabled = (process.env.VITE_USE_MOCKS ?? env.VITE_USE_MOCKS) === '1';

  return {
    plugins: [
      react(),
      mockServiceWorker(mocksEnabled),
      VitePWA({
        registerType: 'autoUpdate',
        injectRegister: null,
        devOptions: { enabled: false },
        includeAssets: ['favicon.svg', 'icons/apple-touch-icon.png'],
        manifest: {
          name: 'খাতা — Khata',
          short_name: 'খাতা',
          description: 'খাতা মূল্যায়ন — Exam-script marking for teachers',
          lang: 'bn',
          dir: 'ltr',
          start_url: '/',
          scope: '/',
          display: 'standalone',
          background_color: '#FAFAF7',
          theme_color: '#0F6E6E',
          icons: [
            { src: '/icons/icon-192.png', sizes: '192x192', type: 'image/png' },
            { src: '/icons/icon-512.png', sizes: '512x512', type: 'image/png' },
            {
              src: '/icons/icon-maskable-512.png',
              sizes: '512x512',
              type: 'image/png',
              purpose: 'maskable',
            },
          ],
        },
        workbox: {
          // Static assets only. API responses (student data) are never cached:
          // there is no runtimeCaching entry, and /v1 is excluded from the
          // navigation fallback so the network always serves it.
          globPatterns: ['**/*.{js,css,html,svg,png,woff2}'],
          navigateFallback: '/index.html',
          navigateFallbackDenylist: [/^\/v1\//],
          runtimeCaching: [],
          cleanupOutdatedCaches: true,
        },
      }),
    ],
    server: {
      port: 5173,
      proxy: {
        '/v1': { target: API_TARGET, changeOrigin: true },
      },
    },
    preview: {
      port: 4173,
      proxy: {
        '/v1': { target: API_TARGET, changeOrigin: true },
      },
    },
    build: {
      target: 'es2022',
      sourcemap: true,
    },
    test: {
      globals: true,
      environment: 'jsdom',
      setupFiles: ['./src/test/setup.ts'],
      include: ['src/**/*.test.{ts,tsx}', 'scripts/**/*.test.mjs'],
      css: { modules: { classNameStrategy: 'non-scoped' } },
      coverage: {
        provider: 'v8',
        reporter: ['text-summary', 'text', 'html'],
        include: ['src/**/*.{ts,tsx}'],
        exclude: ['src/**/*.test.{ts,tsx}', 'src/test/**', 'src/main.tsx', 'src/**/*.d.ts'],
        thresholds: {
          'src/components/**': { lines: 80 },
          'src/api/**': { lines: 80 },
          'src/auth/**': { lines: 80 },
        },
      },
    },
  };
});
