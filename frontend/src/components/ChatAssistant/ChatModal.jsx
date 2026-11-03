import React, { useState, useRef, useEffect } from 'react';
import { X, Send, Bot, User, Sparkles, AlertTriangle, ArrowRight, CheckCircle2, Loader2, RefreshCw } from 'lucide-react';
import api from '../../services/api';

export const ChatModal = ({ isOpen, onClose, language, currentContext }) => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: language === 'en'
        ? "Namaste! I am your KrishiSathi AI multi-agent assistant. Ask me anything about upcoming rainfall, heat risk, or farming action plans for your crop."
        : "नमस्ते किसान भाई! मैं आपका कृषिसार्थी बहु-एजेंट सहायक हूँ। मुझसे आगामी बारिश, गर्मी के खतरे या अपनी फसल की देखभाल के बारे में कोई भी प्रश्न पूछें।",
      traces: []
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeStep, setActiveStep] = useState(null);
  const messagesEndRef = useRef(null);

  const suggestedQuestions = language === 'en' ? [
    "Will upcoming rainfall affect my soybean crop in Balaghat?",
    "Should I irrigate my field today in Balaghat?",
    "Is the current temperature dangerous for wheat flowering?",
    "What precautions should I take before heavy rainfall?"
  ] : [
    "क्या बालाघाट में बारिश से मेरी सोयाबीन की फसल को नुकसान होगा?",
    "क्या मुझे आज अपने खेत में सिंचाई करनी चाहिए?",
    "क्या वर्तमान तापमान गेहूं की फसल के लिए खतरनाक है?",
    "भारी बारिश से पहले मुझे क्या सावधानियां बरतनी चाहिए?"
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  if (!isOpen) return null;

  const handleSend = async (queryText) => {
    const textToSend = queryText || input;
    if (!textToSend.trim() || loading) return;

    const userMsg = { role: 'user', content: textToSend };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const response = await api.sendChat({
        query: textToSend,
        location: currentContext?.location || 'Balaghat',
        crop: currentContext?.crop || 'Soybean',
        growth_stage: currentContext?.growthStage || 'Flowering',
        language: language,
        latitude: currentContext?.latitude,
        longitude: currentContext?.longitude
      });

      const assistantMsg = {
        role: 'assistant',
        content: response.response,
        traces: response.agent_traces || [],
        structuredData: response.structured_data
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: language === 'en'
            ? "I encountered an issue connecting to the multi-agent network. Please ensure the backend server is running and try again."
            : "मल्टी-एजेंट नेटवर्क से संपर्क करने में समस्या आई है। कृपया पुनः प्रयास करें।"
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-black/50 backdrop-blur-sm flex justify-end">
      <div className="w-full max-w-xl bg-white h-full shadow-2xl flex flex-col animate-in slide-in-from-right duration-200">
        
        {/* Header */}
        <div className="p-4 sm:p-5 bg-krishi-dark text-white flex items-center justify-between border-b border-krishi-primary/30">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-krishi-primary flex items-center justify-center text-white shadow-inner">
              <Bot className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-bold text-base flex items-center gap-2">
                <span>KrishiSathi Multi-Agent Assistant</span>
                <span className="text-[10px] font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 px-2 py-0.5 rounded-full">
                  5 Agents
                </span>
              </h3>
              <p className="text-xs text-gray-300">
                {currentContext ? `${currentContext.crop} • ${currentContext.growthStage} • ${currentContext.location}` : 'Live Climate Intelligence'}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-xl text-gray-300 hover:text-white hover:bg-white/10 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Messages Scroll Area */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 bg-gray-50/50">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-xl bg-krishi-light border border-krishi-primary/30 flex items-center justify-center text-krishi-primary flex-shrink-0 mt-1">
                  <Bot className="w-4 h-4" />
                </div>
              )}

              <div className={`max-w-[85%] rounded-2xl p-4 text-sm leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-krishi-primary text-white shadow-md'
                  : 'bg-white border border-gray-200 text-krishi-text shadow-sm'
              }`}>
                {/* Agent Traces Badge (if present) */}
                {msg.traces && msg.traces.length > 0 && (
                  <div className="mb-3 pb-3 border-b border-gray-100">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-krishi-primary flex items-center gap-1.5 mb-2">
                      <Sparkles className="w-3.5 h-3.5" />
                      Multi-Agent Verification Pipeline:
                    </span>
                    <div className="space-y-1.5">
                      {msg.traces.map((trace, tIdx) => (
                        <div key={tIdx} className="text-xs bg-gray-50 p-2 rounded-lg border border-gray-100 flex items-start gap-2">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0 mt-0.5" />
                          <div>
                            <span className="font-bold text-gray-800">{trace.agent}</span>: {trace.summary}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="whitespace-pre-line prose prose-sm max-w-none">
                  {msg.content}
                </div>
              </div>

              {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-xl bg-gray-200 flex items-center justify-center text-gray-700 flex-shrink-0 mt-1">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          ))}

          {/* Loading Indicator */}
          {loading && (
            <div className="flex gap-3 items-start animate-pulse">
              <div className="w-8 h-8 rounded-xl bg-krishi-light flex items-center justify-center text-krishi-primary">
                <Loader2 className="w-4 h-4 animate-spin" />
              </div>
              <div className="bg-white border border-gray-200 rounded-2xl p-4 text-xs text-gray-600 shadow-sm space-y-1.5">
                <p className="font-semibold text-krishi-primary flex items-center gap-2">
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  <span>Strands Multi-Agent Team Coordinating...</span>
                </p>
                <p className="text-[11px] text-gray-500">
                  Weather Agent fetching live radar • Risk Agent computing deterministic equations • Advisory Agent formatting recommendations.
                </p>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Suggested Queries */}
        <div className="p-3 bg-white border-t border-gray-100">
          <p className="text-[11px] font-semibold text-gray-600 mb-2 px-1">
            {language === 'en' ? 'Suggested Farmer Questions:' : 'अक्सर पूछे जाने वाले सवाल:'}
          </p>
          <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-none">
            {suggestedQuestions.map((q, i) => (
              <button
                key={i}
                onClick={() => handleSend(q)}
                disabled={loading}
                className="whitespace-nowrap px-3 py-1.5 rounded-full bg-gray-50 hover:bg-krishi-light hover:text-krishi-primary text-xs text-gray-700 border border-gray-200 transition-colors flex-shrink-0"
              >
                {q}
              </button>
            ))}
          </div>
        </div>

        {/* Input Bar */}
        <div className="p-4 bg-white border-t border-gray-200 flex items-center gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder={
              language === 'en'
                ? "Ask about rainfall, irrigation, temperature..."
                : "मौसम, सिंचाई या फसल के बारे में पूछें..."
            }
            disabled={loading}
            className="flex-1 bg-gray-50 border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-krishi-primary/30 focus:border-krishi-primary transition-all"
          />
          <button
            onClick={() => handleSend()}
            disabled={!input.trim() || loading}
            className="p-2.5 rounded-xl bg-krishi-primary hover:bg-krishi-dark text-white disabled:opacity-50 disabled:cursor-not-allowed shadow-md transition-all"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>

      </div>
    </div>
  );
};

export default ChatModal;

