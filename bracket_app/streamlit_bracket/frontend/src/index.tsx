// index.tsx
import React from "react";
import { createRoot } from "react-dom/client";
import { withStreamlitConnection } from "streamlit-component-lib";
import DoubleElimination from "./Bracket";

const StreamlitBracket = (props: any) => {
  return <DoubleElimination {...props} />;
};

const container = document.getElementById("root") as HTMLElement;
const root = createRoot(container); // from "react-dom/client"
root.render(<StreamlitBracket />);
