import React, { createContext, useContext, useState } from "react";

const TooltipCtx = createContext({});

export const TooltipProvider = ({ children }) => (
  <TooltipCtx.Provider value={{}}>{children}</TooltipCtx.Provider>
);

export const Tooltip = ({ children, content }) => {
  const [open, setOpen] = useState(false);
  return (
    <span
      className="relative inline-block"
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
    >
      {children}
      {open && (
        <span className="absolute left-1/2 -translate-x-1/2 mt-2 whitespace-nowrap rounded bg-foreground text-background text-xs px-2 py-1 shadow">
          {content}
        </span>
      )}
    </span>
  );
};
