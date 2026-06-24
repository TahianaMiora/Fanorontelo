export type GameMode = "PvP" | "PvE" | "EvE";

export interface ModeConfig {
    title: string, 
    humanPlayers: number;
    isAiTurn: (currentPlayer: number) => boolean;
}[]

export const GAME_MODES: Record<GameMode, ModeConfig> = {
  PvP: {
    title: 'Human vs Human',
    humanPlayers: 2,
    isAiTurn: () => false,
  },
  PvE: {
    title: 'Human vs AI',
    humanPlayers: 1,
    isAiTurn: (currentPlayer) => currentPlayer === -1,
  },
  EvE: {
    title: 'Demo : AI vs AI',
    humanPlayers: 0,
    isAiTurn: () => true,
  }
};