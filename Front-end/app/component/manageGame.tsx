"use client";

import { useState, useRef, useEffect } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import FanoronteloScene from "./board3D";
import { useLoader } from "@react-three/fiber";
import { TextureLoader } from "three";
import { GAME_MODES, GameMode } from "../utils/gameConfig";
import { ChevronLeft } from "lucide-react";

type Difficulty = "facile" | "moyen" | "difficile";
interface AIConfig {
  iaX: Difficulty;
  iaO: Difficulty;
}

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
  const [gameStarted, setGameStarted] = useState(false);
  const [aiConfig, setAiConfig] = useState<AIConfig>({ iaX: "moyen", iaO: "moyen" });
  
  const menuRef = useRef<HTMLDivElement>(null);

  // Fermer le menu au clic extérieur
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setMode(null);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  if (!gameStarted) {
    return (
      <div className="relative w-full h-screen bg-neutral-950 font-serif overflow-hidden">
        <div className="absolute inset-0 blur-sm opacity-60 pointer-events-none">
          <Canvas camera={{ position: [0, 8, 12], fov: 45 }}>
            <MenuBackground />
          </Canvas>
        </div>

        <div className="absolute inset-0 flex flex-col items-center justify-center z-10">
          <div className="flex flex-col items-center p-10 rounded-2xl bg-neutral-900/80 backdrop-blur-md border-2 border-amber-800 shadow-[0_0_50px_rgba(180,83,9,0.2)]">
            <h1 className="text-2xl md:text-6xl font-bold text-amber-500 mb-8 tracking-widest uppercase drop-shadow-lg">
              Fanorontelo
            </h1>

            {(Object.keys(GAME_MODES) as GameMode[]).map((m) => (
              <div key={m} ref={mode === m ? menuRef : null} className="relative mb-4 flex flex-col items-center">
                <button
                  onClick={() => {
                    setMode(m === mode ? null : m);
                    
                    if (m === "PvP") {
                      setGameStarted(true);
                    }
                  }}
                  className={`w-[70svw] md:w-72 py-2 md:py-4 text-md md:text-xl font-semibold rounded transition-all duration-300 ${
                    m === "EvE"
                      ? mode === m ? "bg-neutral-600 text-white border border-neutral-400" : "bg-neutral-800/60 text-neutral-300 border border-neutral-600/80 hover:bg-neutral-700"
                      : mode === m ? "bg-amber-700 text-white border border-amber-500" : "bg-amber-900/50 text-amber-50 border border-amber-700/80 hover:bg-amber-800"
                  }`}
                >
                  {GAME_MODES[m].title}
                </button>

                {mode === m && (
                  <div className="absolute md:left-full top-0 ml-4 z-50 p-4 bg-neutral-800/90 rounded-lg border border-amber-900/50 w-72 flex flex-col gap-3 shadow-2xl">
                    {m === "PvE" && (
                      <select className="bg-neutral-900 text-white p-2 rounded border border-amber-800" 
                        value={aiConfig.iaO}
                        onChange={(e) => setAiConfig({...aiConfig, iaO: e.target.value as Difficulty})}>
                        <option value="facile">IA : Facile</option>
                        <option value="moyen">IA : Moyen</option>
                        <option value="difficile">IA : Difficile</option>
                      </select>
                    )}
                    {m === "EvE" && (
                      <>
                        <select className="bg-neutral-900 text-white p-2 rounded border border-amber-800" value={aiConfig.iaX} onChange={(e) => setAiConfig({...aiConfig, iaX: e.target.value as Difficulty})}>
                          <option value="facile">Grenat : Facile</option>
                          <option value="moyen">Grenat : Moyen</option>
                          <option value="difficile">Grenat : Difficile</option>
                        </select>
                        <select className="bg-neutral-900 text-white p-2 rounded border border-amber-800" value={aiConfig.iaO} onChange={(e) => setAiConfig({...aiConfig, iaO: e.target.value as Difficulty})}>
                          <option value="facile">Blanc : Facile</option>
                          <option value="moyen">Blanc : Moyen</option>
                          <option value="difficile">Blanc : Difficile</option>
                        </select>
                      </>
                    )}
                    <button 
                      onClick={() => setGameStarted(true)}
                      className="bg-emerald-700 py-2 rounded text-sm font-bold text-white hover:bg-emerald-900 transition-colors"
                    >
                      Démarrer
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="relative w-full h-screen font-sans">
      <button 
        onClick={() => {setGameStarted(false), setMode(null)}}
        className="absolute top-3 md:top-6 md:left-6 z-30 px-3 md:px-5 md:py-2 font-serif text-amber-100 md:bg-neutral-900/80 md:backdrop-blur-sm md:border border-amber-800 md:rounded-md shadow-lg hover:bg-red-900 text-lg md:text-lg md:transition-colors"
      >
        <ChevronLeft width={24} height={24}/>
      </button>

      <FanoronteloScene mode={mode!} config={GAME_MODES[mode!]} aiConfig={aiConfig} />
    </div>
  );
}