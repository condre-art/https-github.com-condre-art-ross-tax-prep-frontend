// Polyfill import.meta.env for Jest (Vite compatibility)
if (typeof import === 'undefined') {
  global.import = {};
}
if (typeof import.meta === 'undefined') {
  global.import.meta = { env: { VITE_API_BASE: '' } };
}
