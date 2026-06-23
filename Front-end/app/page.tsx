import FanoronteloScene from "./component/board3D";
import GameApp from "./component/manageGame";

export default function Home() {
  return (
    <div className="flex flex-col flex-1 items-center justify-center font-sans bg-foreground">
      {/* <FanoronteloScene/> */}
      <GameApp/>
    </div>
  );
}


