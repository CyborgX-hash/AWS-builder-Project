import React from 'react';
import { Link } from 'react-router-dom';
import {
  Sprout,
  CloudSun,
  ShieldAlert,
  CalendarCheck,
  Bot,
  ArrowRight,
  CheckCircle2,
  Users,
  Compass,
  Sparkles,
  Layers,
  ThermometerSnowflake
} from 'lucide-react';

export const Landing = ({ language, onOpenChat }) => {
  return (
    <div className="space-y-24 py-8 sm:py-12">
      
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-8 pb-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto space-y-6">
            
            {/* Tagline Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-krishi-light border border-krishi-primary/20 text-krishi-primary text-xs sm:text-sm font-bold shadow-2xs">
              <Sparkles className="w-4 h-4 text-emerald-600" />
              <span>
                {language === 'en'
                  ? 'AWS Strands Agents Social Good Hackathon 2026'
                  : 'एडब्ल्यूएस स्ट्रैंड्स एजेंट्स सोशल गुड हैकथॉन 2026'}
              </span>
            </div>

            <h1 className="text-4xl sm:text-6xl font-black text-krishi-dark tracking-tight leading-[1.15]">
              {language === 'en' ? (
                <>
                  Turning Weather Intelligence into <span className="text-krishi-primary underline decoration-emerald-300">Smarter Farming Decisions</span>.
                </>
              ) : (
                <>
                  मौसम की जानकारी को बनाएं <span className="text-krishi-primary underline decoration-emerald-300">सटीक कृषि फैसले</span>.
                </>
              )}
            </h1>

            <p className="text-base sm:text-lg text-gray-600 leading-relaxed max-w-2xl mx-auto">
              {language === 'en'
                ? "Traditional apps only show rain numbers. KrishiSathi's multi-agent AI translates forecasts into crop-specific precautions, waterlogging warnings, and 3-day action plans for smallholder farmers."
                : "साधारण मौसम ऐप केवल तापमान और बारिश दिखाते हैं। कृषिसार्थी का बहु-एजेंट एआई आपकी फसल और उसकी अवस्था के अनुसार जलभराव, लू और सिंचाई की सटीक सलाह देता है।"}
            </p>

            {/* CTAs */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <Link
                to="/dashboard"
                className="w-full sm:w-auto px-8 py-4 rounded-2xl bg-krishi-primary hover:bg-krishi-dark text-white font-bold text-base shadow-lg hover:shadow-xl transition-all flex items-center justify-center gap-2.5 group"
              >
                <span>{language === 'en' ? 'Check My Farm Weather' : 'अपने खेत का मौसम जांचें'}</span>
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>

              <button
                onClick={onOpenChat}
                className="w-full sm:w-auto px-7 py-4 rounded-2xl bg-white border border-gray-200 hover:border-krishi-primary text-gray-800 font-bold text-base shadow-sm hover:shadow-md transition-all flex items-center justify-center gap-2.5"
              >
                <Bot className="w-5 h-5 text-krishi-primary" />
                <span>{language === 'en' ? 'Ask AI Assistant' : 'एआई सहायक से पूछें'}</span>
              </button>
            </div>

            {/* Trust Badges */}
            <div className="pt-8 flex flex-wrap items-center justify-center gap-6 text-xs font-semibold text-gray-500">
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-krishi-primary" />
                {language === 'en' ? 'Deterministic Risk Engine' : 'सटीक गणितीय जोखिम मॉडल'}
              </span>
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-krishi-primary" />
                {language === 'en' ? 'ICAR & FAO Knowledge Base' : 'कृषि अनुसंधान आधारित थ्रेशोल्ड'}
              </span>
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-krishi-primary" />
                {language === 'en' ? 'Bilingual Hindi & English' : 'हिन्दी एवं अंग्रेजी भाषा'}
              </span>
            </div>

          </div>
        </div>
      </section>

      {/* How It Works - The 5 Agent Collaborative Pipeline */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-16 space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-krishi-primary bg-krishi-light px-3 py-1 rounded-full">
            {language === 'en' ? 'AWS Strands Multi-Agent Architecture' : 'एडब्ल्यूएस स्ट्रैंड्स बहु-एजेंट प्रणाली'}
          </span>
          <h2 className="text-3xl font-extrabold text-krishi-dark">
            {language === 'en' ? 'How KrishiSathi Works' : 'कृषिसार्थी कैसे कार्य करता है'}
          </h2>
          <p className="text-sm text-gray-600">
            {language === 'en'
              ? 'One master orchestrator collaborates with four specialist AI agents to evaluate farm risks.'
              : 'एक मुख्य ऑर्केस्ट्रेटर और चार विशेषज्ञ एआई एजेंट मिलकर खेत के जोखिमों का विश्लेषण करते हैं।'}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          
          <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm relative space-y-3">
            <div className="w-10 h-10 rounded-2xl bg-emerald-50 text-emerald-700 flex items-center justify-center font-bold text-sm">
              1
            </div>
            <h3 className="font-bold text-base text-gray-900">
              {language === 'en' ? 'Krishi Orchestrator' : 'कृषि ऑर्केस्ट्रेटर'}
            </h3>
            <p className="text-xs text-gray-600 leading-relaxed">
              {language === 'en'
                ? 'Understands farmer query, extracts location, crop, and intent, and delegates to specialist agents.'
                : 'किसान का प्रश्न समझकर स्थान, फसल और चिंता की पहचान कर विशेषज्ञ एजेंटों को कार्य सौंपता है।'}
            </p>
          </div>

          <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm relative space-y-3">
            <div className="w-10 h-10 rounded-2xl bg-blue-50 text-blue-700 flex items-center justify-center font-bold text-sm">
              2
            </div>
            <h3 className="font-bold text-base text-gray-900">
              {language === 'en' ? 'Weather Agent' : 'मौसम विशेषज्ञ एजेंट'}
            </h3>
            <p className="text-xs text-gray-600 leading-relaxed">
              {language === 'en'
                ? 'Retrieves hyperlocal live radar, 7-day numerical forecasts, and precipitation probabilities.'
                : 'ओपन-मेटियो और मौसम विभाग से लाइव मौसम व 7-दिवसीय वर्षा पूर्वानुमान प्राप्त करता है।'}
            </p>
          </div>

          <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm relative space-y-3">
            <div className="w-10 h-10 rounded-2xl bg-amber-50 text-amber-700 flex items-center justify-center font-bold text-sm">
              3
            </div>
            <h3 className="font-bold text-base text-gray-900">
              {language === 'en' ? 'Crop Intelligence' : 'फसल विशेषज्ञ एजेंट'}
            </h3>
            <p className="text-xs text-gray-600 leading-relaxed">
              {language === 'en'
                ? 'Matches growth stage sensitivity, optimal temperature windows, and water requirements.'
                : 'फसल की अवस्था के अनुसार तापमान सीमा और जल आवश्यकता (ICAR/FAO) का मिलान करता है।'}
            </p>
          </div>

          <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm relative space-y-3">
            <div className="w-10 h-10 rounded-2xl bg-red-50 text-red-700 flex items-center justify-center font-bold text-sm">
              4
            </div>
            <h3 className="font-bold text-base text-gray-900">
              {language === 'en' ? 'Risk Engine Agent' : 'जोखिम आकलन एजेंट'}
            </h3>
            <p className="text-xs text-gray-600 leading-relaxed">
              {language === 'en'
                ? 'Runs deterministic Python equations for heat stress, waterlogging, dry spells, and rainfall.'
                : 'बिना किसी भ्रम के गणितीय कोड से जलभराव, अत्यधिक बारिश और गर्मी के जोखिम की गणना करता है।'}
            </p>
          </div>

          <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm relative space-y-3">
            <div className="w-10 h-10 rounded-2xl bg-purple-50 text-purple-700 flex items-center justify-center font-bold text-sm">
              5
            </div>
            <h3 className="font-bold text-base text-gray-900">
              {language === 'en' ? 'Advisory Agent' : 'कृषि सलाह एजेंट'}
            </h3>
            <p className="text-xs text-gray-600 leading-relaxed">
              {language === 'en'
                ? 'Synthesizes practical 3-day action roadmaps and immediate precautions in Hindi & English.'
                : 'सरल भाषा में 3-दिवसीय कार्य योजना और तत्काल सावधानियां तैयार करता है।'}
            </p>
          </div>

        </div>
      </section>

      {/* Unique Capabilities Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-gradient-to-br from-krishi-dark to-[#0f3422] rounded-3xl p-8 sm:p-14 text-white">
          <div className="max-w-2xl mb-12 space-y-3">
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-400 bg-white/10 px-3 py-1 rounded-full">
              {language === 'en' ? 'Solving Real Farmer Problems' : 'किसानों की वास्तविक समस्याओं का समाधान'}
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
              {language === 'en' ? 'Beyond Traditional Weather Apps' : 'साधारण मौसम ऐप्स से आगे'}
            </h2>
            <p className="text-sm text-gray-300 leading-relaxed">
              {language === 'en'
                ? "Farmers don't need raw millimeter charts—they need to know if upcoming rain will drown their flowering soybean or if they should irrigate today."
                : "किसानों को केवल मिलीमीटर का चार्ट नहीं, बल्कि यह जानना है कि क्या आगामी बारिश से उनके सोयाबीन के फूल झड़ेंगे या क्या आज पानी लगाना चाहिए।"}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <div className="p-6 rounded-2xl bg-white/10 backdrop-blur-md border border-white/15 space-y-3">
              <CloudSun className="w-8 h-8 text-emerald-400" />
              <h3 className="font-bold text-lg text-white">
                {language === 'en' ? 'Hyperlocal Climate Data' : 'स्थानीय मौसम की सटीक जानकारी'}
              </h3>
              <p className="text-xs text-gray-300 leading-relaxed">
                {language === 'en'
                  ? 'Access real-time temperatures, rainfall probabilities, and 7-day outlooks for any village or block in India.'
                  : 'भारत के किसी भी गांव या ब्लॉक के लिए लाइव तापमान, बारिश की संभावना और 7-दिन का पूर्वानुमान।'}
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white/10 backdrop-blur-md border border-white/15 space-y-3">
              <ShieldAlert className="w-8 h-8 text-amber-400" />
              <h3 className="font-bold text-lg text-white">
                {language === 'en' ? 'Deterministic Risk Scores' : 'सटीक एवं पारदर्शी जोखिम स्कोर'}
              </h3>
              <p className="text-xs text-gray-300 leading-relaxed">
                {language === 'en'
                  ? 'Zero hallucinations. Risk calculations for heat, rain, and waterlogging are derived via mathematical algorithms.'
                  : 'कोई मनगढ़ंत स्कोर नहीं। गर्मी, वर्षा और जलभराव का जोखिम विशुद्ध गणितीय नियमों से निकाला जाता है।'}
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-white/10 backdrop-blur-md border border-white/15 space-y-3">
              <CalendarCheck className="w-8 h-8 text-blue-400" />
              <h3 className="font-bold text-lg text-white">
                {language === 'en' ? '3-Day Action Roadmaps' : '3-दिवसीय व्यावहारिक कार्य योजना'}
              </h3>
              <p className="text-xs text-gray-300 leading-relaxed">
                {language === 'en'
                  ? 'Step-by-step guidance on ditch drainage, irrigation pauses, and canopy monitoring before bad weather hits.'
                  : 'खराब मौसम से पहले नाली साफ करने, सिंचाई रोकने और फसल निगरानी के चरणबद्ध निर्देश।'}
              </p>
            </div>

          </div>
        </div>
      </section>

      {/* Social Good & Hackathon Impact */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-12 space-y-3">
          <h2 className="text-3xl font-extrabold text-krishi-dark">
            {language === 'en' ? 'Social Impact & Resilience' : 'सामाजिक प्रभाव एवं किसान संबल'}
          </h2>
          <p className="text-sm text-gray-600">
            {language === 'en'
              ? 'Empowering 140M+ Indian smallholders against accelerating climate volatility.'
              : 'जलवायु परिवर्तन की अनिश्चितता के बीच भारत के 14 करोड़ से अधिक छोटे किसानों का संबल।'}
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 text-center">
          <div className="p-8 rounded-3xl bg-white border border-gray-100 shadow-sm space-y-2">
            <div className="text-4xl font-extrabold text-krishi-primary">100%</div>
            <div className="text-sm font-bold text-gray-800">
              {language === 'en' ? 'Deterministic Logic' : 'पारदर्शी गणितीय तर्क'}
            </div>
            <p className="text-xs text-gray-500">
              {language === 'en' ? 'Zero fake numbers or fabricated predictions.' : 'कोई बनावटी या अनुमानित डेटा नहीं।'}
            </p>
          </div>

          <div className="p-8 rounded-3xl bg-white border border-gray-100 shadow-sm space-y-2">
            <div className="text-4xl font-extrabold text-krishi-primary">5 Core</div>
            <div className="text-sm font-bold text-gray-800">
              {language === 'en' ? 'Indian Staple Crops' : 'प्रमुख भारतीय फसलें'}
            </div>
            <p className="text-xs text-gray-500">
              {language === 'en' ? 'Soybean, Rice, Wheat, Maize, and Cotton.' : 'सोयाबीन, धान, गेहूं, मक्का और कपास।'}
            </p>
          </div>

          <div className="p-8 rounded-3xl bg-white border border-gray-100 shadow-sm space-y-2">
            <div className="text-4xl font-extrabold text-krishi-primary">24h / 48h / 72h</div>
            <div className="text-sm font-bold text-gray-800">
              {language === 'en' ? 'Actionable Roadmaps' : 'समयबद्ध कार्य योजनाएं'}
            </div>
            <p className="text-xs text-gray-500">
              {language === 'en' ? 'Practical field actions before extreme weather strikes.' : 'आपदा से पहले सुरक्षित रहने के व्यावहारिक कदम।'}
            </p>
          </div>
        </div>
      </section>

    </div>
  );
};

export default Landing;

