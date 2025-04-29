// Bracket.tsx
import React, { useEffect, useState, useRef, ComponentProps as ReactComponentProps} from "react";
import {
  SingleEliminationBracket,
  DoubleEliminationBracket,
  Match,
  createTheme,
} from "@g-loot/react-tournament-brackets";
import { Streamlit, withStreamlitConnection, ComponentProps } from "streamlit-component-lib";

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
  nextLoserMatchId: number | null,
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

type MatchProps = ReactComponentProps<typeof Match>;

type CustomMatchProps = MatchProps & {
  onClick: (match: MatchData) => void;
};

const Modal = ({
  children,
  onClose,
}: {
  children: React.ReactNode;
  onClose: () => void;
}) => {
  return (
    <div
      style={{
        position: "fixed",
        top: 0, left: 0, right: 0, bottom: 0,
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 9999,
      }}
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: "black",
          padding: "2rem",
          borderRadius: "10px",
          maxWidth: "90%",
          maxHeight: "80%",
          overflowY: "auto",
          boxShadow: "0 2px 10px rgba(0,0,0,0.2)",
        }}
      >
        <button
          onClick={onClose}
          style={{
            position: "absolute",
            top: "1rem",
            right: "1rem",
            fontSize: "1.2rem",
            background: "none",
            border: "none",
            cursor: "pointer",
          }}
        >
          ✖
        </button>
        {children}
      </div>
    </div>
  );
};

const DoubleElimination = (props: ComponentProps) => {
  const matches = props.args.matches || [];
  const teams = props.args.teams || {};
  const scores = props.args.scores || {};

  const wrapperRef = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(1);
  const [selectedMatch, setSelectedMatch] = useState<MatchData | null>(null);

  useEffect(() => {
    const resize = () => {
      if (!wrapperRef.current) return;

      const parentWidth = wrapperRef.current.parentElement?.offsetWidth || 800;
      const bracketWidth = wrapperRef.current.scrollWidth;

      const newScale = Math.min(parentWidth / bracketWidth, 1);
      setScale(newScale);
      Streamlit.setFrameHeight();
    };

    resize();
    window.addEventListener("resize", resize);
    return () => window.removeEventListener("resize", resize);
  }, [props.args.matches]);

  const CustomMatch = ({ onClick, match, ...rest }: CustomMatchProps) => {
    return (
      <div onClick={() => onClick(match)} style={{ cursor: "pointer" }}>
        <Match match={match} {...rest} />
      </div>
    );
  };

  if (!matches || matches.length === 0) {
    return <div>No matches to display.</div>;
  }

  return (
    <div style={{ width: "95%", overflowX: "auto" }}>
      <div
        ref={wrapperRef}
        style={{
          transform: `scale(${scale})`,
          transformOrigin: "top left",
          display: "inline-block",
        }}
      >
        <DoubleEliminationBracket
          matches={matches}
          matchComponent={(matchProps: MatchProps) => (
            <CustomMatch
              {...matchProps}
              onClick={(match: MatchData) => setSelectedMatch(match)}
            />
          )}
        />
      </div>
      {selectedMatch && (
        <Modal onClose={() => setSelectedMatch(null)}>
          <div style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            textAlign: "center",
            gap: "0.5rem"
          }}>
            
            <div style={{ fontSize: "1.1rem", lineHeight: "1.8" }}>
              {/* <div>
                <strong>
                  {selectedMatch.participants[0]?.name || "TBD"} vs {selectedMatch.participants[1]?.name || "TBD"}
                </strong>
              </div> */}
              <div>
                {selectedMatch.participants[0]?.resultText || "0"} - {selectedMatch.participants[1]?.resultText || "0"}
              </div>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginTop: "1.5rem",
                  gap: "2rem",
                }}
              >
                {selectedMatch?.participants?.length > 0 ? (
                  selectedMatch.participants.map((p, idx) => {
                    const team = teams[p.name]; // Look up by team name
                    return (
                      <div key={p.id || idx}>
                        <div style={{ fontWeight: "bold", marginBottom: "0.5rem" }}>
                          {team?.header || p.name}
                        </div>
                        {team?.items?.length > 0 ? (
                          <ul
                            style={{
                              paddingLeft: "0",
                              listStyleType: "none",
                            }}
                          >
                            {team.items.map((player: string, i: number) => {
                              const matchScores = scores?.[selectedMatch.id] || {};
                              return (
                                <li key={`team-${idx}-player-${i}`}>
                                  {player} {matchScores[player] && 'X'}
                                </li>
                              );
                            })}
                          </ul>
                        ) : (
                          <div style={{ fontStyle: "italic" }}>No players listed</div>
                        )}
                      </div>
                    );
                  })
                ) : (
                  <div style={{ fontStyle: "italic" }}>Teams TBD</div>
                )}
              </div>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
};

export default withStreamlitConnection(DoubleElimination)