// index.tsx
import React from "react";
import { createRoot } from "react-dom/client";
import { withStreamlitConnection } from "streamlit-component-lib";
import SingleElimination from "./Bracket";

const StreamlitBracket = (props: any) => {
  return <SingleElimination {...props} />;
};

const container = document.getElementById("root") as HTMLElement;
const root = createRoot(container); // from "react-dom/client"
root.render(<StreamlitBracket />);
