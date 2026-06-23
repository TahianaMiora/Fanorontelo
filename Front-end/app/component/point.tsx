interface PionProps {
  joueur: -1 | 1;
  statut: "selectionne" | "actif" | "sombre";
  onClick: () => void;
  position: [number, number, number];
}

export default function Pion({ joueur, statut, onClick, position }: PionProps) {
  // 1. Définir la couleur de base (ex: Blanc pour -1, Rouge pour 1)
  const baseColor = joueur === -1 ? "#ffffff" : "#bd1414";

  // 2. Ajuster la couleur et l'intensité selon le statut
  let finalColor = baseColor;
  let emissiveColor = "#000000";
  let emissiveIntensity = 0;

  if (statut === "selectionne") {
    emissiveColor = baseColor; // Fait "briller" la couleur du pion
    emissiveIntensity = 0.6;   // Effet ultra-vif
  } else if (statut === "sombre") {
    finalColor = joueur === -1 ? "#555555" : "#4a0808"; // Version très assombrie
  }

  return (
    <mesh position={position} onClick={onClick}>
      <cylinderGeometry args={[0.6, 0.6, 0.3, 32]} />
      <meshStandardMaterial 
        color={finalColor} 
        emissive={emissiveColor}
        emissiveIntensity={emissiveIntensity}
        roughness={0.2}
      />
    </mesh>
  );
}