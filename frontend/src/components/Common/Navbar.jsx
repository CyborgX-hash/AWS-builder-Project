import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Sprout, Globe, CloudSun, ShieldAlert, FileText, MessageSquareQuote } from 'lucide-react';

export const Navbar = ({ language, setLanguage, onOpenChat }) => {
  const location = useLocation();

  const toggleLanguage = () => {
    setLanguage(language === 'en' ? 'hi' : 'en');
  };

  const navLinks = [
    { path: '/', labelEn: 'Home', labelHi: 'होम', icon: Sprout },
    { path: '/dashboard', labelEn: 'Dashboard', labelHi: 'डैशबोर्ड', icon: CloudSun },
    { path: '/risk-report', labelEn: 'Risk Analysis', labelHi: 'जोखिम रिपोर्ट', icon: ShieldAlert },
    { path: '/advisory', labelEn: 'Farming Advisory', labelHi: 'कृषि सलाह', icon: FileText },
  ];

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-gray-100 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-12 h-12 rounded-2xl bg-krishi-primary flex items-center justify-center text-white shadow-md group-hover:scale-105 transition-transform duration-200">
              <Sprout className="w-7 h-7" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-2xl font-extrabold text-krishi-dark tracking-tight">KrishiSathi</span>
                <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-krishi-light text-krishi-primary border border-krishi-primary/20">
                  {language === 'en' ? 'AI Agent' : 'कृषि साथी'}
                </span>
              </div>
              <p className="text-xs text-gray-700 hidden sm:block">
                {language === 'en' ? 'Climate Intelligence for Farmers' : 'किसानों के लिए मौसम एवं कृषि साथी'}
              </p>
            </div>
          </Link>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-1 bg-gray-50/80 p-1.5 rounded-2xl border border-gray-200">
            {navLinks.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-150 ${
                    isActive
                      ? 'bg-krishi-primary text-white shadow-sm'
                      : 'text-gray-700 hover:text-krishi-dark hover:bg-white'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{language === 'en' ? item.labelEn : item.labelHi}</span>
                </Link>
              );
            })}
          </nav>

          {/* Actions: Language Toggle & Chat Trigger */}
          <div className="flex items-center gap-3">
            <button
              onClick={toggleLanguage}
              className="flex items-center gap-2 px-3 py-2 rounded-xl border border-gray-200 bg-white hover:bg-gray-50 text-xs font-bold text-gray-800 transition-colors shadow-sm"
              title="Toggle Language"
            >
              <Globe className="w-4 h-4 text-krishi-primary" />
              <span>{language === 'en' ? 'हिन्दी' : 'English'}</span>
            </button>

            <button
              onClick={onOpenChat}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-krishi-primary hover:bg-krishi-dark text-white text-xs font-bold shadow-md hover:shadow-lg transition-all"
            >
              <MessageSquareQuote className="w-4 h-4" />
              <span className="hidden sm:inline">{language === 'en' ? 'AI Assistant' : 'कृषि सहायक'}</span>
            </button>
          </div>

        </div>
      </div>
    </header>
  );
};

export default Navbar;

