// Helper para usar toast
export const toast = {
  success: (message) => {
    if (typeof window !== 'undefined' && window.toast) {
      window.toast(message, { type: 'success' });
    }
  },
  error: (message) => {
    if (typeof window !== 'undefined' && window.toast) {
      window.toast(message, { type: 'error' });
    }
  },
  info: (message) => {
    if (typeof window !== 'undefined' && window.toast) {
      window.toast(message, { type: 'info' });
    }
  },
};
