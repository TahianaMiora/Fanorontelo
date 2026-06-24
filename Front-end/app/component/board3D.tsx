"use client";

import { Canvas, useLoader } from "@react-three/fiber";
import { OrbitControls, Sparkles as Sparkles3D } from "@react-three/drei";
import { TextureLoader } from "three";
import { useEffect, useState } from "react";
import { Undo2, Redo2, RotateCcw, Sparkles } from "lucide-react";
import { useSpring, a } from "@react-spring/three";

import GrilleFanorontelo from "./elementBoard";
import Pion from "./point";
import { GameMode, ModeConfig } from "../utils/gameConfig";

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

interface FanoronteloProps { mode: GameMode, config: ModeConfig, aiConfig: { iaX: string, iaO: string }}

interface GameState {
  grid: number[];
  current_player: number;
  phase: number;
  pieces_placed: { [key: string]: number };
  winner: number;
  legal_moves: any[];
}

interface PieceData {
  id: string;
  joueur: number;
  index: number;
}

export default function FanoronteloScene({ mode, config, aiConfig }: FanoronteloProps) {
  console.log(mode, aiConfig)
  const API_URL = "http://127.0.0.1:8000/api";
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [selectedSrc, setSelectedSrc] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pieces, setPieces] = useState<PieceData[]>([]);

  // 1. Initialisation de la partie
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

  // 2. Réconciliation des pions pour l'animation
  useEffect(() => {
    if (!gameState) return;

    setPieces((prevPieces) => {
      const newPieces: PieceData[] = [];
      const currentGrid = gameState.grid;
      let availablePrev = [...prevPieces]; 

      currentGrid.forEach((joueur, index) => {
        if (joueur === 0) return; 

        let matchIdx = availablePrev.findIndex(p => p.joueur === joueur && p.index === index);

        if (matchIdx !== -1) {
          newPieces.push(availablePrev[matchIdx]);
          availablePrev.splice(matchIdx, 1);
        } else {
          matchIdx = availablePrev.findIndex(p => p.joueur === joueur);
          const count = pieces.filter((element) => element.id.startsWith('pion${joueur}')).length
          
          if (matchIdx !== -1) {
            newPieces.push({ ...availablePrev[matchIdx], index });
            availablePrev.splice(matchIdx, 1);
          } else {
            newPieces.push({
              id: `pion-${joueur}-${Date.now()}-${Math.random()}`,
              joueur,
              index
            });
          }
        }
      });

      return newPieces;
    });
  }, [gameState?.grid]);

  const handleClick = async (index: number) => {
    if (config.isAiTurn(gameState?.current_player || 0)) return;
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

  
  const { boardRotation } = useSpring({
    boardRotation: gameState?.winner !== 0 ? Math.PI * 2 : 0,
    config: { mass: 3, tension: 40, friction: 15 },
  });


  useEffect(() => {
    if (!gameState || gameState.winner !== 0) return;
  
    const isAiTurn = config.isAiTurn(gameState.current_player);
    
    if (isAiTurn) {
      const timer = setTimeout(async () => {
        try {
          let response;
          
          if (mode === 'EvE') {
            response = await fetch(`${API_URL}/ai-vs-ai`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ level_ia_x: aiConfig.iaX, level_ia_o: aiConfig.iaO }),
            });
          } else {
            response = await fetch(`${API_URL}/ai-move?niveau=${aiConfig.iaO}`, {
              method: "POST"
            });
          }
  
          if (!response.ok) throw new Error("Erreur lors du tour de l'IA");
          
          const data = await response.json();
          setGameState(data);
          setError(null);
        } catch (err: any) {
          setError("Erreur IA: " + err.message);
        }
      }, 1000);
  
      return () => clearTimeout(timer);
    }
  }, [gameState?.current_player, gameState?.winner, mode, config]);


  return (
    <div className="relative w-full h-screen bg-neutral-950 select-none text-neutral-200 overflow-hidden">
      <div/>
      <div className="bg-neutral-900/90 backdrop-blur-md px-6 py-3 shadow-2xl border-b border-amber-800/60 pointer-events-auto flex flex-col items-center w-full text-center z-20 absolute top-0">
          <h1 className="text-lg font-extrabold tracking-widest uppercase bg-gradient-to-r from-amber-500 via-orange-400 to-amber-600 bg-clip-text text-transparent flex items-center gap-2 drop-shadow-sm mb-1">
            Fanoron-telo <Sparkles className="w-4 h-4 text-amber-500 animate-spin" style={{ animationDuration: '6s' }} />
          </h1>
          
          {gameState && (
            <div className="flex items-center justify-center gap-3 mt-1">
              <span className="font-semibold text-sm text-neutral-300 tracking-wide">
                {gameState.winner !== 0 ? (
                  <span className="text-emerald-500 font-bold drop-shadow-[0_0_8px_rgba(16,185,129,0.5)]">
                    Partie Terminée
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
        </div>

        {/* NOUVEAU : Message de victoire en plein milieu de l'écran */}
        {gameState?.winner !== 0 && (
          <div className="absolute inset-0 z-10 flex items-center justify-center pointer-events-none">
            {/* L'arrière plan sombre */}
            <div className="absolute inset-0 bg-neutral-950/40 backdrop-blur-[2px] transition-all duration-1000"></div>
            
            {/* La carte de victoire animée */}
            <div className="relative bg-neutral-900/90 border border-amber-500/50 p-10 rounded-3xl shadow-[0_0_80px_rgba(245,158,11,0.2)] text-center animate-bounce duration-[2000ms]">
              <h2 className="text-5xl md:text-7xl font-black text-transparent bg-clip-text bg-gradient-to-br from-amber-300 via-orange-500 to-red-600 drop-shadow-xl uppercase tracking-widest">
                {gameState?.winner === 1 ? "Grenat" : "Blanc"}
              </h2>
              <div className="text-2xl font-bold text-amber-200 mt-4 tracking-widest uppercase">
                Remporte la victoire !
              </div>
            </div>
          </div>
        )}

        {/* Erreurs */}
        <div className="absolute top-24 w-full flex justify-center z-20 pointer-events-none">
            {error && (
            <div className="text-center bg-orange-950/90 text-orange-400 border border-orange-900 text-xs font-bold py-2 px-6 shadow-xl rounded-full animate-pulse">
                ⚠️ {error}
            </div>
            )}
        </div>

      {/* Boutons d'actions */}
      <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-30 bg-neutral-900/80 backdrop-blur-md rounded-2xl p-2 shadow-2xl border border-amber-900/30 flex gap-2 max-w-sm w-[calc(100%-2rem)]">
        <button
          onClick={handleUndo}
          className="flex-1 flex flex-col items-center justify-center gap-0.5 bg-neutral-800 hover:bg-neutral-700 active:bg-neutral-600 text-amber-400 font-bold py-2 rounded-xl transition-all text-[11px] border border-amber-900/20 disabled:opacity-50"
          disabled={gameState?.winner !== 0}
        >
          <Undo2 className="w-4 h-4" /> Annuler
        </button>
        <button
          onClick={handleRedo}
          className="flex-1 flex flex-col items-center justify-center gap-0.5 bg-neutral-800 hover:bg-neutral-700 active:bg-neutral-600 text-orange-400 font-bold py-2 rounded-xl transition-all text-[11px] border border-amber-900/20 disabled:opacity-50"
          disabled={gameState?.winner !== 0}
        >
          <Redo2 className="w-4 h-4" /> Refaire
        </button>
        <button
          onClick={handleReset}
          className="flex-1 flex flex-col items-center justify-center gap-0.5 bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 text-white font-bold py-2 rounded-xl transition-all shadow-md text-[11px] hover:shadow-orange-500/20"
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
        
        {gameState?.winner !== 0 && (
          <group position={[0, 2, 0]}>
            {/* Particules dorées rapides */}
            <Sparkles3D count={300} scale={15} size={8} speed={1.5} color="#fbbf24" opacity={0.8} />
            {/* Particules rouges/oranges flottantes */}
            <Sparkles3D count={200} scale={12} size={12} speed={0.8} color="#ea580c" opacity={0.6} />
            {/* Petites étincelles blanches */}
            <Sparkles3D count={150} scale={18} size={4} speed={2} color="#ffffff" opacity={0.9} />
          </group>
        )}

        <a.group rotation-y={boardRotation}>
          <TableBois />
          
          <GrilleFanorontelo 
            joueur={gameState?.current_player ?? 1} 
            onClickPoint={handleClick}
          />

          {pieces.map((pion) => {
            let statut: "selectionne" | "actif" | "sombre" = "actif";
            
            if (selectedSrc !== null) {
              statut = pion.index === selectedSrc ? "selectionne" : "sombre";
            } else if (pion.joueur !== gameState?.current_player) {
              statut = "sombre";
            }

            return (
              <Pion
                key={pion.id}
                position={POSITIONS_GRILLE[pion.index]}
                joueur={pion.joueur} 
                statut={statut}
                onClick={() => handleClick(pion.index)}
              />
            );
          })}
        </a.group>
        
        <OrbitControls enablePan={false} minPolarAngle={0} maxPolarAngle={Math.PI / 2.2} />
      </Canvas>
    </div>
  );
}