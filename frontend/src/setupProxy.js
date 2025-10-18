const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  // Auto-detect environment: if we're in Docker, use 'web' service name
  // Otherwise, use localhost for local development
  const isDocker = process.env.NODE_ENV === 'production' || process.env.DOCKER === 'true';
  const backendUrl = isDocker ? 'http://web:8000' : 'http://localhost:8000';

  console.log(`[HPM] Proxy target: ${backendUrl} (Docker: ${isDocker})`);

  app.use(
    '/api',
    createProxyMiddleware({
      target: backendUrl,
      changeOrigin: true,
    })
  );

  app.use(
    '/media',
    createProxyMiddleware({
      target: backendUrl,
      changeOrigin: true,
    })
  );
};
