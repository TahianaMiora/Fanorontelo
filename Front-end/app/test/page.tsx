"use client";

import { useState, useEffect } from "react";
import { Undo2, Redo2, RotateCcw, Heart, Sparkles, User } from "lucide-react";

const API_URL = "http://127.0.0.1:8000/api";

interface GameState {
  grid: number[];
  current_player: number;
  phase: number;
  pieces_placed: { [key: string]: number };
  winner: number;
  legal_moves: any[];
}

export default function FanoronTeloFront() {
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [selectedSrc, setSelectedSrc] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Charger l'état initial au démarrage
  useEffect(() => {
    fetchState();
  }, []);

  const fetchState = async () => {
    try {
      const res = await fetch(`${API_URL}/state`);
      const data = await res.json();
      setGameState(data);
      setError(null);
    } catch (err) {
      setError("Le Back-end est-il bien allumé sur le port 8000 ? 💕");
    }
  };

  const handleCellClick = async (index: number) => {
    if (!gameState || gameState.winner !== 0) return;

    // PHASE 1 : Placement simple
    if (gameState.phase === 1) {
      await sendMove(index);
    } 
    // PHASE 2 : Déplacement (Sélection Départ puis Arrivée)
    else {
      if (selectedSrc === null) {
        // Sélection de la pièce à bouger (doit appartenir au joueur actuel)
        if (gameState.grid[index] === gameState.current_player) {
          setSelectedSrc(index);
        }
      } else {
        // Envoi du mouvement (src -> dest)
        if (index === selectedSrc) {
          setSelectedSrc(null); // Désélectionner si on re-clique dessus
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
      setError("Erreur lors de la réinitialisation 🎀");
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
      if (!res.ok) throw new Error("Rien à rétablir ! 🌸");
      const data = await res.json();
      setGameState(data);
      setSelectedSrc(null);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    }
  };

  if (!gameState) {
    return (
      <div className="min-h-screen bg-linear-to-tr from-pink-100 via-purple-50 to-pink-200 flex flex-col items-center justify-center font-sans">
        <Heart className="w-12 h-12 text-pink-400 animate-pulse mb-4" />
        <p className="text-pink-600 font-medium animate-bounce">{error || "Connexion au serveur magique..."}</p>
      </div>
    );
  }

  // Obtenir le symbole du pion dans la grille
  const renderPion = (val: number, idx: number) => {
    const isSelected = selectedSrc === idx;
    if (val === 1) {
      return (
        <div className={`w-14 h-14 rounded-full bg-linear-to-r from-pink-400 to-rose-400 flex items-center justify-center shadow-lg transform transition-all duration-300 hover:scale-110 active:scale-95 ${isSelected ? "ring-4 ring-pink-300 scale-105 animate-pulse" : ""}`}>
          <span className="text-white font-bold text-xl">X</span>
        </div>
      );
    }
    if (val === -1) {
      return (
        <div className={`w-14 h-14 rounded-full bg-linear-to-r from-purple-400 to-indigo-400 flex items-center justify-center shadow-lg transform transition-all duration-300 hover:scale-110 active:scale-95 ${isSelected ? "ring-4 ring-purple-300 scale-105 animate-pulse" : ""}`}>
          <span className="text-white font-bold text-xl">O</span>
        </div>
      );
    }
    return <div className="w-4 h-4 rounded-full bg-pink-200 shadow-inner group-hover:bg-pink-300 transition-colors" />;
  };

  return (
    <div className="min-h-screen bg-linear-to-tr from-pink-100 via-rose-50 to-purple-100 flex flex-col items-center justify-center p-4 selection:bg-pink-200 text-slate-700">
      
      {/* Header Container */}
      <div className="text-center mb-6">
        <h1 className="text-3xl font-extrabold tracking-wide bg-linear-to-r from-pink-500 via-purple-500 to-rose-500 bg-clip-text text-transparent flex items-center justify-center gap-2 drop-shadow-sm">
          Fanoron-telo <Sparkles className="w-6 h-6 text-pink-400 animate-spin" style={{ animationDuration: '4s' }} />
        </h1>
        <p className="text-xs text-pink-500/80 uppercase tracking-widest font-semibold mt-1">TEST API Humain vs Humain</p>
      </div>

      {/* Main Glassmorphic Card */}
      <div className="bg-white/70 backdrop-blur-md rounded-3xl p-6 shadow-xl border border-white/50 w-full max-w-sm flex flex-col items-center">
        
        {/* Status Area */}
        <div className="w-full bg-white/80 rounded-2xl p-3 mb-6 text-center border border-pink-100 shadow-sm flex items-center justify-between px-4">
          <div className="flex items-center gap-2">
            <User className={`w-5 h-5 ${gameState.current_player === 1 ? 'text-pink-400' : 'text-purple-400'}`} />
            <span className="font-semibold text-sm">
              {gameState.winner !== 0 ? (
                <span className="text-emerald-500 font-bold">✨ Joueur {gameState.winner === 1 ? "X" : "O"} Gagne ! ✨</span>
              ) : (
                <>Tour du Joueur <span className={gameState.current_player === 1 ? "text-pink-500" : "text-purple-500"}>{gameState.current_player === 1 ? "X (Pink)" : "O (Purple)"}</span></>
              )}
            </span>
          </div>
          <span className="bg-pink-100 text-pink-600 text-xs font-bold px-2.5 py-1 rounded-full border border-pink-200">
            {gameState.phase === 1 ? "🌸 Placement" : "✨ Mouvement"}
          </span>
        </div>

        {/* Le Plateau Fanoron-telo */}
        <div className="relative w-72 h-72 bg-white/40 rounded-2xl border border-pink-200/60 p-4 shadow-inner flex items-center justify-center">
          
          <svg className="absolute inset-0 w-full h-full stroke-pink-200/80 stroke-[3px] pointer-events-none" xmlns="http://www.w3.org/2000/svg">
            {/* Horizontales */}
            <line x1="16.66%" y1="16.66%" x2="83.33%" y2="16.66%" />
            <line x1="16.66%" y1="50%" x2="83.33%" y2="50%" />
            <line x1="16.66%" y1="83.33%" x2="83.33%" y2="83.33%" />
            {/* Verticales */}
            <line x1="16.66%" y1="16.66%" x2="16.66%" y2="83.33%" />
            <line x1="50%" y1="16.66%" x2="50%" y2="83.33%" />
            <line x1="83.33%" y1="16.66%" x2="83.33%" y2="83.33%" />
            {/* Diagonales */}
            <line x1="16.66%" y1="16.66%" x2="83.33%" y2="83.33%" />
            <line x1="83.33%" y1="16.66%" x2="16.66%" y2="83.33%" />
          </svg>

          {/* Boutons d'intersections cliquables */}
          <div className="absolute inset-0 grid grid-cols-3 grid-rows-3 p-2">
            {gameState.grid.map((value, idx) => (
              <div key={idx} className="flex items-center justify-center group">
                <button
                  onClick={() => handleCellClick(idx)}
                  className="w-16 h-16 rounded-full flex items-center justify-center focus:outline-none transition-all z-10"
                >
                  {renderPion(value, idx)}
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Error Alert Box */}
        {error && (
          <div className="mt-4 text-center bg-rose-50 text-rose-500 border border-rose-100 text-xs font-medium py-2 px-4 rounded-xl w-full animate-shake">
            ⚠️ {error}
          </div>
        )}

        {/* Action Controls Footer */}
        <div className="w-full grid grid-cols-3 gap-2 mt-6">
          <button
            onClick={handleUndo}
            className="flex flex-col items-center justify-center gap-1 bg-pink-50 hover:bg-pink-100 active:bg-pink-200 text-pink-600 font-bold py-2 px-3 rounded-xl transition-all shadow-sm border border-pink-100 text-xs"
          >
            <Undo2 className="w-4 h-4" /> Annuler
          </button>
          
          <button
            onClick={handleRedo}
            className="flex flex-col items-center justify-center gap-1 bg-purple-50 hover:bg-purple-100 active:bg-purple-200 text-purple-600 font-bold py-2 px-3 rounded-xl transition-all shadow-sm border border-purple-100 text-xs"
          >
            <Redo2 className="w-4 h-4" /> Refaire
          </button>
          
          <button
            onClick={handleReset}
            className="flex flex-col items-center justify-center gap-1 bg-gradient-to-r from-pink-400 to-rose-400 hover:from-pink-500 hover:to-rose-500 text-white font-bold py-2 px-3 rounded-xl transition-all shadow-md text-xs col-span-1"
          >
            <RotateCcw className="w-4 h-4" /> Reset
          </button>
        </div>

      </div>
    </div>
  );
}