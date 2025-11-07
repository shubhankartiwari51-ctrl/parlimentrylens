// in src/App.tsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import AnalyzeText from "./pages/AnalyzeText";
import AnalyzeYouTube from "./pages/AnalyzeYouTube";
import Mission from "./pages/Mission";
import AnalyzeNewspaper from "./pages/AnalyzeNewspaper"; // <-- Import new page
import Footer from "./components/Footer";
import Navbar from "./components/Navbar";

// ... (AnalyzeReels import if you have it)

function App() {
  return (
    <Router>
      <div className="flex min-h-screen w-full flex-col bg-gradient-to-br from-gray-900 via-purple-950 to-indigo-950 text-white">
        <Navbar />
        <main className="flex w-full flex-grow items-center justify-center pt-32 pb-16 px-4 mx-auto">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/text" element={<AnalyzeText />} />
            <Route path="/youtube" element={<AnalyzeYouTube />} />
            <Route path="/mission" element={<Mission />} />
            <Route path="/newspaper" element={<AnalyzeNewspaper />} /> {/* <-- Add new route */}
            {/* <Route path="/reels" element={<AnalyzeReels />} /> */}
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;