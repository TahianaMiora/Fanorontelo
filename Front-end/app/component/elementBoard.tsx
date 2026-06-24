"use client";

import { Text } from "@react-three/drei";
import * as THREE from "three";

interface grilleProps {
  joueur: number;
  onClickPoint: (index: number) => void; 
}

export default function GrilleFanorontelo({joueur, 
  onClickPoint
}: grilleProps) {

  const taille = 4.2
  const points: [number, number, number][] = [
    [-taille, 0.02, -taille], [0, 0.02, -taille], [taille, 0.02, -taille], // Haut
    [-taille, 0.02,  0], [0, 0.02,  0], [taille, 0.02,  0], // Milieu
    [-taille, 0.02,  taille], [0, 0.02,  taille], [taille, 0.02, taille], // Bas
  ];

  // les lignes qui relient ces points (index de 0 à 8)
  const segments = [
    // Lignes horizontales, 
    [0, 1], [1, 2], [3, 4], [4, 5], [6, 7], [7, 8],
    // Lignes verticales, 
    [0, 3], [3, 6], [1, 4], [4, 7], [2, 5], [5, 8],
    // Grandes diagonales, 
    [0, 8], [2, 6], 
  ];

  const changePoint = (index : number) => {
    onClickPoint(index);
  }

  return (
    <group>
      {segments.map(([startIdx, endIdx], index) => {
        const start = new THREE.Vector3(...points[startIdx]);
        const end = new THREE.Vector3(...points[endIdx]);
        const pointsBuffer = new THREE.BufferGeometry().setFromPoints([start, end]);

        return (
          <line key={`line-${index}`}>
            <primitive object={pointsBuffer} attach="geometry" />
            <lineBasicMaterial color="#1a0f00" linewidth={4} toneMapped={false} />
          </line>
        );
      })}

      {/* TRACÉ DES 9 POINTS D'INTERSECTION (Emplacements des pions) */}
      {points.map((pos, index) => (
        <mesh key={`point-${index}`} 
          position={pos}
          onClick={() => changePoint(index)}
          >

            <cylinderGeometry args={[0.15, 0.15, 0.01, 32]} />
            <Text
              // On place le texte légèrement au-dessus du point (Y + 0.4) pour qu'il flotte
              position={[pos[0], pos[1] + 0.2, pos[2]]}
              fontSize={0.6}          // Taille de la police
              color="#ffffff"         // Couleur blanche pour bien ressortir sur le bois sombre
              anchorX="center"        // Centre le texte horizontalement
              anchorY="middle"        // Centre le texte verticalement
            >
              {index}
            </Text>
            <meshStandardMaterial 
                color="#3d2314" 
                roughness={0.2} 
                metalness={0.1}
            />
        </mesh>
      ))}
    </group>
  );
}
