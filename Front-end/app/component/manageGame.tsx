"use client";

import { useState } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import FanoronteloScene from "./board3D";
import { useLoader } from "@react-three/fiber";
import { TextureLoader } from "three";
import { GAME_MODES, GameMode, ModeConfig } from "../utils/gameConfig";

function MenuBackground() {
  const [colorMap, roughnessMap, normalMap] = useLoader(TextureLoader, [
    "/texture/textures/wood_table_worn_diff_1k.jpg",
    "/texture/textures/wood_table_worn_rough_1k.png",
    "/texture/textures/wood_table_worn_disp_1k.png",
  ]);

  return (
    <>
      <ambientLight intensity={1.5} />
      <directionalLight position={[5, 10, 5]} intensity={2} />
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.1, 0]}>
        <boxGeometry args={[10, 10, 0.2]} />
        <meshStandardMaterial color="#ffffff" map={colorMap} roughnessMap={roughnessMap} normalMap={normalMap} />
      </mesh>
      <OrbitControls autoRotate autoRotateSpeed={1} enableZoom={false} enablePan={false} />
    </>
  );
}

export default function GameApp() {
  const [mode, setMode] = useState<GameMode | null>(null);

  if (mode === null) {
    return (
      <div className="relative w-full h-screen bg-neutral-950 font-serif overflow-hidden">
        <div className="absolute inset-0 blur-sm opacity-60 pointer-events-none">
          <Canvas camera={{ position: [0, 8, 12], fov: 45 }}>
            <MenuBackground />
          </Canvas>
        </div>

        <div className="absolute inset-0 flex flex-col items-center justify-center z-10">
          <div className="flex flex-col items-center p-10 rounded-2xl bg-neutral-900/80 backdrop-blur-md border-2 border-amber-800 shadow-[0_0_50px_rgba(180,83,9,0.2)]">
            <h1 className="text-5xl md:text-6xl font-bold text-amber-500 mb-2 tracking-widest uppercase drop-shadow-lg">
              Fanorontelo
            </h1>
            <p className="text-amber-200/60 italic mb-10 text-lg">Le jeu de stratégie traditionnel</p>

            {(Object.keys(GAME_MODES) as GameMode[]).map((mode) => (
              <button 
                key={mode}
                onClick={() => setMode(mode)}
                className={`w-72 py-4 mb-4 text-xl font-semibold rounded hover:scale-105 transition-all duration-300 ${
                  mode === "EvE" 
                    ? "text-neutral-300 bg-neutral-800/60 border border-neutral-600/80 hover:bg-neutral-700" 
                    : "text-amber-50 bg-amber-900/50 border border-amber-700/80 hover:bg-amber-700 hover:shadow-[0_0_15px_rgba(217,119,6,0.5)]"
                }`}
              >
                {GAME_MODES[mode].title}
              </button>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="relative w-full h-screen font-sans">
      <button 
        onClick={() => setMode(null)}
        className="absolute top-6 left-6 z-30 px-5 py-2 font-serif text-amber-100 bg-neutral-900/80 backdrop-blur-sm border border-amber-800 rounded-md shadow-lg hover:bg-red-900 hover:border-red-500 transition-colors duration-300"
      >
        ← Quitter la partie
      </button>

      <FanoronteloScene 
        mode={mode} 
        config={GAME_MODES[mode]} 
      />
    </div>
  );
}