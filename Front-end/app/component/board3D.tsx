"use client";

import { Canvas, useLoader } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { TextureLoader } from "three";
import GrilleFanorontelo from "./elementBoard";
import { useState } from "react";
import Pion from "./point";

type CaseContenu = -1 | 1 | null;

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
            {/* Ajout d'une couleur de base blanche pure pour éclaircir la texture */}
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

export default function FanoronteloScene() {
    const [boardPoint, setBoardPoint] = useState<CaseContenu[]>(Array(9).fill(null));
    const [pionSelectionne, setPionSelectionne] = useState<number | null>(null);
    const [tour, setTour] = useState<-1 | 1>(-1);

    const authorizedPlace: Record<number, number[]> = {
        0: [1, 3, 4], 1: [0, 2, 4], 2: [1, 4, 5],
        3: [0, 4, 6], 4: [0, 1, 2, 3, 5, 6, 7, 8], 5: [2, 4, 8],
        6: [3, 4, 7], 7: [4, 6, 8], 8: [4, 5, 7],
    };

    const handleClick = (index: number) => {
        const contenuCase = boardPoint[index];
        const nbPionsJoueur = boardPoint.filter((item) => item === tour).length;

        if (nbPionsJoueur < 3) {
            if (contenuCase !== null) return;
            const nouveauBoard = [...boardPoint];
            nouveauBoard[index] = tour;
            setBoardPoint(nouveauBoard);
            setTour(tour === -1 ? 1 : -1);
            return;
        }

        if (contenuCase === tour) {
            setPionSelectionne(index);
            return;
        }

        if (pionSelectionne !== null && contenuCase === null) {
            const voisinsDuPion = authorizedPlace[pionSelectionne];
            if (!voisinsDuPion.includes(index)) return;

            const nouveauBoard = [...boardPoint];
            nouveauBoard[pionSelectionne] = null;
            nouveauBoard[index] = tour;
                
            setBoardPoint(nouveauBoard);
            setPionSelectionne(null);
            setTour(tour === -1 ? 1 : -1);
        }
    };

    return (
        <div className="w-full h-screen">
            {/* Correction de camera : position attend un tableau [X, Y, Z] */}
            <Canvas camera={{ position: [0, 12, 12], fov: 45 }}>
                {/* 1. Lumière globale uniforme et intense */}
                <ambientLight intensity={2.5} />
                
                {/* 2. Lumière du ciel (blanche) et du sol (teinte bois) pour déboucher les ombres */}
                <hemisphereLight args={["#ffffff", "#3a2512", 1.5]} />
                
                {/* 3. Lumière directionnelle principale (simule le soleil) */}
                <directionalLight position={[8, 15, 8]} intensity={2.5} castShadow />
                
                {/* 4. Lumière d'appoint pour adoucir le côté opposé */}
                <pointLight position={[-8, 8, -8]} intensity={1.0} />
                
                <TableBois />
                <GrilleFanorontelo joueur={tour} onClickPoint={handleClick} />

                {boardPoint.map((joueur, index) => {
                    if (joueur === null) return null;
                    
                    let statut: "selectionne" | "actif" | "sombre" = "actif";
                    if (pionSelectionne !== null) {
                        statut = index === pionSelectionne ? "selectionne" : "sombre";
                    } else if (joueur !== tour) {
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