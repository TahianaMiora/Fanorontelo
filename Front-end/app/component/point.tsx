import { useSpring, a } from "@react-spring/three";

interface PionProps {
  joueur: number;
  statut: "selectionne" | "actif" | "sombre";
  onClick: () => void;
  position: [number, number, number];
}

export default function Pion({ position, joueur, statut, onClick }: PionProps) {
  const baseColor = joueur === -1 ? "#ffffff" : "#bd1414";

  let finalColor = baseColor;
  let emissiveColor = "#000000";
  let emissiveIntensity = 0;

  if (statut === "selectionne") {
    emissiveColor = baseColor; // Fait "briller" la couleur du pion
    emissiveIntensity = 0.6;   // Effet ultra-vif
  } else if (statut === "sombre") {
    finalColor = joueur === -1 ? "#555555" : "#4a0808"; // Version très assombrie
  }
  
  const { pos } = useSpring({
    pos: position,
    config: { 
      mass: 1, 
      tension: 170, // Plus c'est haut, plus c'est rapide
      friction: 20  // Plus c'est haut, moins ça rebondit
    }
  });

  return (
    <a.mesh position={pos} onClick={onClick}>
      <cylinderGeometry args={[0.6, 0.6, 0.3, 32]} />
      <meshStandardMaterial 
        color={finalColor} 
        emissive={emissiveColor}
        emissiveIntensity={emissiveIntensity}
        roughness={0.2}
      />
    </a.mesh>
  );
}