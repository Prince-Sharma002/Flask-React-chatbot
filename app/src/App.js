import Home from "./Components/Home";
import GenerateFacts from "./Components/GenerateFacts";
import { BrowserRouter, Routes, Route } from "react-router-dom";



function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" exact element={<Home />} />
        <Route path="/generate-facts" element={<GenerateFacts />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
