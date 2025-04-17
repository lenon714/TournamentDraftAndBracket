// Bracket.tsx
import React, { useEffect, useState } from "react";
import {
  SingleEliminationBracket,
  Match,
  SVGViewer,
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

const SingleElimination = (props: ComponentProps) => {
  // const width = 1250;
  // const height = 600;
  // const scale = 0.5;
  useEffect(() => Streamlit.setFrameHeight());

  const { matches } = props.args;

  if (!matches || matches.length === 0) {
    return <div>No matches to display.</div>;
  }

  return (
    <SingleEliminationBracket
      matches={matches}
      matchComponent={Match}
      // scaleFactor={scale}
    />
  );
};

export default withStreamlitConnection(SingleElimination)