"use client";

import { Canvas, useLoader } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { TextureLoader } from "three";
import { useEffect, useState } from "react";
import { Undo2, Redo2, RotateCcw, Sparkles } from "lucide-react";

import GrilleFanorontelo from "./elementBoard";
import Pion from "./point";
import { GameMode } from "./manageGame";

const POSITIONS_GRILLE: [number, number, number][] = [
  [-4.2, 0.1, -4.2], [0, 0.1, -4.2], [4.2, 0.1, -4.2],
  [-4.2, 0.1,  0.0], [0, 0.1,  0.0], [4.2, 0.1,  0.0],
  [-4.2, 0.1,  4.2], [0, 0.1,  4.2], [4.2, 0.1,  4.2],
];

function TableBois() {
  const [colorMap, roughnessMap, normalMap] = useLoader(TextureLoader, [
    "/texture/textures/wood_table_worn_diff_1k.jpg",
    "/texture/textures/wood_table_worn_rough_1k.png",
    "/texture/textures/wood_table_worn_disp_1k.png",
  ]);

  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.1, 0]}>
      <boxGeometry args={[10, 10, 0.2]} />
      <meshStandardMaterial 
        color="#ffffff"
        map={colorMap} 
        roughnessMap={roughnessMap} 
        normalMap={normalMap} 
        roughness={0.4}
      />
    </mesh>
  );
}

interface FanoronteloProps {
  mode: GameMode;
}

interface GameState {
  grid: number[];
  current_player: number;
  phase: number;
  pieces_placed: { [key: string]: number };
  winner: number;
  legal_moves: any[];
}

export default function FanoronteloScene({ mode }: FanoronteloProps) {
  const API_URL = "http://127.0.0.1:8000/api";
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [selectedSrc, setSelectedSrc] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Correction : On force un reset complet au premier montage pour nettoyer la grille
  useEffect(() => {
    const initializeGame = async () => {
      try {
        const res = await fetch(`${API_URL}/reset`, { method: "POST" });
        const data = await res.json();
        setGameState(data);
        setError(null);
      } catch (err) {
        setError("Impossible de réinitialiser. Le Back-end est-il bien allumé ? 🪵");
      }
    };
    initializeGame();
  }, []);

  const handleClick = async (index: number) => {
    if (!gameState || gameState.winner !== 0) return;

    if (gameState.phase === 1) {
      await sendMove(index);
    } else {
      if (selectedSrc === null) {
        if (gameState.grid[index] === gameState.current_player) {
          setSelectedSrc(index);
        }
      } else {
        if (index === selectedSrc) {
          setSelectedSrc(null);
        } else {
          await sendMove([selectedSrc, index]);
          setSelectedSrc(null);
        }
      }
    }
  };

  const sendMove = async (moveValue: any) => {
    try {
      const res = await fetch(`${API_URL}/move`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ move: moveValue }),
      });
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || "Coup invalide");
      }
      const data = await res.json();
      setGameState(data);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleReset = async () => {
    try {
      const res = await fetch(`${API_URL}/reset`, { method: "POST" });
      const data = await res.json();
      setGameState(data);
      setSelectedSrc(null);
      setError(null);
    } catch (err) {
      setError("Erreur lors de la réinitialisation 🪵");
    }
  };

  const handleUndo = async () => {
    try {
      const res = await fetch(`${API_URL}/undo`, { method: "POST" });
      if (!res.ok) throw new Error("Rien à annuler !");
      const data = await res.json();
      setGameState(data);
      setSelectedSrc(null);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleRedo = async () => {
    try {
      const res = await fetch(`${API_URL}/redo`, { method: "POST" });
      if (!res.ok) throw new Error("Rien à rétablir ! 🪵");
      const data = await res.json();
      setGameState(data);
      setSelectedSrc(null);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="relative w-full h-screen bg-neutral-950 select-none text-neutral-200">
      
      {/* 1. Interface HUD Superposée en thématique Bois / Orange / Cuivre */}
      <div className="bg-neutral-900/90 backdrop-blur-md px-6 py-3 shadow-2xl border-b border-amber-800/60 pointer-events-auto flex flex-col items-center w-full text-center">
          {/* Titre */}
          <h1 className="text-lg font-extrabold tracking-widest uppercase bg-gradient-to-r from-amber-500 via-orange-400 to-amber-600 bg-clip-text text-transparent flex items-center gap-2 drop-shadow-sm mb-1">
            Fanoron-telo <Sparkles className="w-4 h-4 text-amber-500 animate-spin" style={{ animationDuration: '6s' }} />
          </h1>
          
          {/* État du jeu */}
          {gameState && (
            <div className="flex items-center justify-center gap-3 mt-1">
              <span className="font-semibold text-sm text-neutral-300 tracking-wide">
                {gameState.winner !== 0 ? (
                  <span className="text-emerald-500 font-bold drop-shadow-[0_0_8px_rgba(16,185,129,0.5)]">
                    ✨ {gameState.winner === 1 ? "Grenat" : "Blanc"} Gagne ! ✨
                  </span>
                ) : (
                  <>Tour : <span className={gameState.current_player === 1 ? "text-amber-200 font-bold" : "text-orange-500 font-bold"}>{gameState.current_player === 1 ? "Grenat" : "Blanc"}</span></>
                )}
              </span>
              <span className="bg-amber-950/80 text-amber-400 text-[10px] font-bold px-2.5 py-0.5 rounded-full border border-amber-700/50 shadow-inner">
                {gameState.phase === 1 ? "🍁 Placement" : "✨ Mouvement"}
              </span>
            </div>
          )}
        </div>{/* Erreurs (s'affichent juste sous le panneau central si besoin) */}
        <div>
            {error && (
            <div className="text-center bg-orange-950/80 text-orange-400 border border-orange-900/50 text-xs font-medium py-2 px-4 shadow-lg pointer-events-auto animate-pulse">
                ⚠️ {error}
            </div>
            )}
        </div>

      {/* Boutons d'actions en bas */}
      <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-20 bg-neutral-900/80 backdrop-blur-md rounded-2xl p-2 shadow-2xl border border-amber-900/30 flex gap-2 max-w-sm w-[calc(100%-2rem)]">
        <button
          onClick={handleUndo}
          className="flex-1 flex flex-col items-center justify-center gap-0.5 bg-neutral-800 hover:bg-neutral-700 active:bg-neutral-600 text-amber-400 font-bold py-2 rounded-xl transition-all text-[11px] border border-amber-900/20"
        >
          <Undo2 className="w-4 h-4" /> Annuler
        </button>
        <button
          onClick={handleRedo}
          className="flex-1 flex flex-col items-center justify-center gap-0.5 bg-neutral-800 hover:bg-neutral-700 active:bg-neutral-600 text-orange-400 font-bold py-2 rounded-xl transition-all text-[11px] border border-amber-900/20"
        >
          <Redo2 className="w-4 h-4" /> Refaire
        </button>
        <button
          onClick={handleReset}
          className="flex-1 flex flex-col items-center justify-center gap-0.5 bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 text-white font-bold py-2 rounded-xl transition-all shadow-md text-[11px]"
        >
          <RotateCcw className="w-4 h-4" /> Reset
        </button>
      </div>

      {/* 2. Rendu Canvas 3D */}
      <Canvas camera={{ position: [0, 12, 12], fov: 45 }}>
        <ambientLight intensity={5} />
        <hemisphereLight args={["#ffffff", "#3a2512", 1.5]} />
        <directionalLight position={[8, 15, 8]} intensity={2.5} castShadow />
        <pointLight position={[-8, 8, -8]} intensity={1.0} />
        
        <TableBois />
        
        <GrilleFanorontelo 
          joueur={gameState?.current_player ?? 1} 
          onClickPoint={handleClick}
        />

        {gameState?.grid.map((joueur, index) => {
          if (joueur === 0) return null;
          
          let statut: "selectionne" | "actif" | "sombre" = "actif";
          
          if (selectedSrc !== null) {
            statut = index === selectedSrc ? "selectionne" : "sombre";
          } else if (joueur !== gameState.current_player) {
            statut = "sombre";
          }

          return (
            <Pion
              key={`pion-${index}`}
              position={POSITIONS_GRILLE[index]}
              joueur={joueur} 
              statut={statut}
              onClick={() => handleClick(index)}
            />
          );
        })}
        
        <OrbitControls enablePan={false} minPolarAngle={0} maxPolarAngle={Math.PI / 2.2} />
      </Canvas>
    </div>
  );
}