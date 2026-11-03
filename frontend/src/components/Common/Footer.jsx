import React from 'react';
import { Sprout, ExternalLink, Heart, ShieldCheck, CloudRain } from 'lucide-react';

export const Footer = ({ language }) => {
  return (
    <footer className="bg-krishi-dark text-white pt-16 pb-12 border-t border-krishi-primary/30 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10">
          
          {/* Brand & Mission */}
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-krishi-primary flex items-center justify-center text-white">
                <Sprout className="w-6 h-6" />
              </div>
              <span className="text-2xl font-bold tracking-tight">KrishiSathi (कृषिसार्थी)</span>
            </div>
            <p className="text-gray-300 text-sm leading-relaxed max-w-md">
              {language === 'en'
                ? "Turning Weather Intelligence into Smarter Farming Decisions. Built for the AWS Strands Agents Social Good Hackathon 2026 to empower smallholder farmers across India."
                : "मौसम की जानकारी को बेहतर कृषि फैसलों में बदलना। भारत के छोटे एवं सीमांत किसानों के सशक्तिकरण हेतु एडब्ल्यूएस स्ट्रैंड्स एजेंट्स सोशल गुड हैकथॉन 2026 के लिए निर्मित।"}
            </p>
            <div className="flex items-center gap-2 text-xs text-krishi-light/80">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>
                {language === 'en'
                  ? "Deterministic Risk Calculations • No Hallucinated Risk Scores"
                  : "सटीक गणितीय जोखिम विश्लेषण • कोई अनुमानित स्कोर नहीं"}
              </span>
            </div>
          </div>

          {/* Meteorological & Agronomic Sources */}
          <div>
            <h4 className="text-sm font-semibold uppercase tracking-wider text-emerald-300 mb-4">
              {language === 'en' ? 'Data Sources' : 'डेटा एवं शोध स्रोत'}
            </h4>
            <ul className="space-y-2.5 text-xs text-gray-300">
              <li>
                <a href="https://open-meteo.com" target="_blank" rel="noreferrer" className="hover:text-white flex items-center gap-1.5 transition-colors">
                  <span>Open-Meteo Weather API</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </li>
              <li>
                <a href="https://mausam.imd.gov.in" target="_blank" rel="noreferrer" className="hover:text-white flex items-center gap-1.5 transition-colors">
                  <span>IMD Agromet (GKMS)</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </li>
              <li>
                <span className="text-gray-400">ICAR - IISR Indore (Soybean)</span>
              </li>
              <li>
                <span className="text-gray-400">ICAR - NRRI Cuttack (Rice/Paddy)</span>
              </li>
              <li>
                <span className="text-gray-400">ICAR - IIWBR Karnal (Wheat)</span>
              </li>
              <li>
                <span className="text-gray-400">FAO-56 Evapotranspiration Guidelines</span>
              </li>
            </ul>
          </div>

          {/* Hackathon & Compliance Disclaimer */}
          <div>
            <h4 className="text-sm font-semibold uppercase tracking-wider text-emerald-300 mb-4">
              {language === 'en' ? 'Disclaimer' : 'महत्वपूर्ण सूचना'}
            </h4>
            <p className="text-xs text-gray-400 leading-relaxed mb-4">
              {language === 'en'
                ? "KrishiSathi is a decision-support advisory tool. Farmers should always consult official state agromet bulletins and local Krishi Vigyan Kendras before initiating major chemical sprays."
                : "कृषिसार्थी निर्णय सहायता उपकरण है। महत्वपूर्ण रासायनिक छिड़काव या कटाई से पहले स्थानीय कृषि विज्ञान केंद्र या सरकारी बुलेटिन की पुष्टि अवश्य करें।"}
            </p>
            <div className="p-2.5 rounded-lg bg-black/20 border border-white/10 text-[11px] text-gray-300">
              AWS Strands Agents Social Good 2026
            </div>
          </div>

        </div>

        <div className="mt-12 pt-8 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between text-xs text-gray-400 gap-4">
          <p>© 2026 KrishiSathi Team. Open-source under MIT License.</p>
          <p className="flex items-center gap-1">
            <span>Crafted with</span>
            <Heart className="w-3.5 h-3.5 text-red-400 fill-red-400" />
            <span>for smallholder farmers across India</span>
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

