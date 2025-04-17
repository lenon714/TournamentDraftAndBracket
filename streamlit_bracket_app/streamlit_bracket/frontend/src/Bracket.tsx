// Bracket.tsx
import React, { useEffect } from "react";
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

interface Props {
  matches: MatchData[];
}

// Add a theme configuration
const theme = createTheme({
  textColor: { main: '#000000', highlighted: '#FFFFFF' },
  matchBackground: { wonColor: '#da96c6', lostColor: '#a4a4a4' },
  scoreBackground: { wonColor: '#da96c6', lostColor: '#a4a4a4' },
});

const SingleElimination = (props: ComponentProps) => {
  useEffect(() => Streamlit.setFrameHeight());
  const {matches} = props.args

  return (
    <SingleEliminationBracket
      matches={matches}
      matchComponent={Match}
      svgWrapper={({ children, ...props }: SVGWrapperProps) => (
        <SVGViewer width={2000} height={1600} {...props}>
          {children}
        </SVGViewer>
      )}
    />
  );
};

export default withStreamlitConnection(SingleElimination)
// export default SingleElimination