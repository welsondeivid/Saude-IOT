import React from "react";
// Simple alias to reuse Toaster for now; could be replaced by external lib later.
import { Toaster as InternalToaster } from "./toaster";

export const Toaster = (props) => <InternalToaster {...props} />;
