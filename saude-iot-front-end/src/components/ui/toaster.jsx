import React, { useState, useEffect } from "react";

// Minimal toast system stub (queue + auto dismiss)
export const Toaster = () => {
  const [toasts, setToasts] = useState([]);

  // Expose a global helper (window.toast) for quick testing
  useEffect(() => {
    window.toast = (message, opts = {}) => {
      const id = Date.now() + Math.random();
      setToasts((t) => [...t, { id, message, ...opts }]);
      setTimeout(() => {
        setToasts((t) => t.filter((x) => x.id !== id));
      }, opts.duration || 4000);
    };
  }, []);

  if (toasts.length === 0) return null;

  return (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-2">
      {toasts.map((t) => (
        <div
          key={t.id}
          className="rounded-lg border bg-card shadow-md px-4 py-2 text-sm flex items-center gap-2"
        >
          <span>{t.message}</span>
          <button
            onClick={() => setToasts((ts) => ts.filter((x) => x.id !== t.id))}
            className="ml-auto text-muted-foreground hover:text-foreground"
          >
            ×
          </button>
        </div>
      ))}
    </div>
  );
};
