import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Common/Navbar';
import Footer from './components/Common/Footer';
import ChatModal from './components/ChatAssistant/ChatModal';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import RiskReport from './pages/RiskReport';
import Advisory from './pages/Advisory';

export function App() {
  const [language, setLanguage] = useState('en');
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [currentContext, setCurrentContext] = useState({
    location: 'Balaghat',
    latitude: 21.8129,
    longitude: 80.1838,
    crop: 'Soybean',
    growthStage: 'Flowering'
  });

  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-[#F7FAF7] text-[#26352B] selection:bg-emerald-100 selection:text-emerald-900">
        
        {/* Persistent Navigation */}
        <Navbar
          language={language}
          setLanguage={setLanguage}
          onOpenChat={() => setIsChatOpen(true)}
        />

        {/* Main Content Area */}
        <main className="flex-1">
          <Routes>
            <Route
              path="/"
              element={
                <Landing
                  language={language}
                  onOpenChat={() => setIsChatOpen(true)}
                />
              }
            />
            <Route
              path="/dashboard"
              element={
                <Dashboard
                  language={language}
                  onOpenChat={() => setIsChatOpen(true)}
                  currentContext={currentContext}
                  setCurrentContext={setCurrentContext}
                />
              }
            />
            <Route
              path="/risk-report"
              element={
                <RiskReport
                  language={language}
                  currentContext={currentContext}
                />
              }
            />
            <Route
              path="/advisory"
              element={
                <Advisory
                  language={language}
                  currentContext={currentContext}
                />
              }
            />
          </Routes>
        </main>

        {/* Global Multi-Agent AI Assistant Drawer */}
        <ChatModal
          isOpen={isChatOpen}
          onClose={() => setIsChatOpen(false)}
          language={language}
          currentContext={currentContext}
        />

        {/* Persistent Footer */}
        <Footer language={language} />

      </div>
    </Router>
  );
}

export default App;

