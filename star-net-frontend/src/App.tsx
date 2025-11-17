import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import StarApp from "./pages/StarApp";
import StarInformation from "./pages/StarInformation";
import StarPredict from "./pages/StarPredict";
import { LanguageProvider } from "./context/LanguageContext";
import BottomBar from "./components/BottomBar";

import { AmbientSoundProvider } from "./context/AmbientSoundContext";

function App() {
  return (
    <AmbientSoundProvider>
      <LanguageProvider>
        <div className="w-[100%] flex justify-center bg-black">
          <div className="max-w-[900px] max-h-[900px] relative">
            <BottomBar />
            <BrowserRouter basename="">
              <Routes>
                <Route path="/" element={<StarApp />}></Route>
                <Route path="/info" element={<StarInformation />}></Route>
                <Route path="/predict" element={<StarPredict />}></Route>
              </Routes>
            </BrowserRouter>
          </div>
        </div>
      </LanguageProvider>
    </AmbientSoundProvider>
  );
}

export default App;
