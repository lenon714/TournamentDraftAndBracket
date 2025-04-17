// Bracket.tsx
import React, { useEffect, useState, useRef} from "react";
import {
  DoubleEliminationBracket,
  Match,
  createTheme,
} from "@g-loot/react-tournament-brackets";
import { Streamlit, withStreamlitConnection, ComponentProps } from "streamlit-component-lib";

// import type { BracketViewProps } from "@g-loot/react-tournament-brackets";

interface Participant {
  id: string;
  name: string;
  isWinner: boolean;
  status: string | null;
  resultText: string;
}

interface MatchData {
  id: number;
  name: string;
  nextMatchId: number | null;
  nextLooserMatchId: number | null,
  tournamentRoundText: string;
  startTime: string;
  state: string;
  participants: Participant[];
}

type SVGWrapperProps = {
  children: React.ReactNode;
  viewBox: string;
  [key: string]: any;
};

const DoubleElimination = (props: ComponentProps) => {
  const matches = props.args.matches || [];

  const wrapperRef = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(1);

  useEffect(() => {
    const resize = () => {
      if (!wrapperRef.current) return;

      const parentWidth = wrapperRef.current.parentElement?.offsetWidth || 800;
      const bracketWidth = wrapperRef.current.scrollWidth;

      const newScale = Math.min(parentWidth / bracketWidth, 1); // shrink only
      setScale(newScale);
      Streamlit.setFrameHeight();
    };

    resize();
    window.addEventListener("resize", resize);
    return () => window.removeEventListener("resize", resize);
  }, [props.args.matches]);

  if (!matches || matches.length === 0) {
    return <div>No matches to display.</div>;
  }

  return (
    <div style={{ width: "100%", overflowX: "auto" }}>
    <div
      ref={wrapperRef}
      style={{
        transform: `scale(${scale})`,
        transformOrigin: "top left",
        display: "inline-block",
      }}
    >
      <DoubleEliminationBracket
        matches={props.args.matches}
        matchComponent={Match}
      />
    </div>
  </div>
  );
};

export default withStreamlitConnection(DoubleElimination)