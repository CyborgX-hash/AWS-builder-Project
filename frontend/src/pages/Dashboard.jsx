import React, { useState, useEffect } from 'react';
import {
  Sprout,
  CloudSun,
  ShieldAlert,
  CalendarCheck,
  Bot,
  RefreshCw,
  AlertCircle,
  HelpCircle,
  Sparkles
} from 'lucide-react';
import api from '../services/api';
import CurrentWeatherCard from '../components/WeatherCard/CurrentWeatherCard';
import SevenDayForecast from '../components/WeatherCard/SevenDayForecast';
import CropStageSelector from '../components/CropSelector/CropStageSelector';
import RiskCard from '../components/RiskIndicator/RiskCard';
import ActionRoadmap from '../components/Dashboard/ActionRoadmap';

export const Dashboard = ({ language, onOpenChat, currentContext, setCurrentContext }) => {
  const [location, setLocation] = useState(currentContext?.location || 'Balaghat');
  const [crop, setCrop] = useState(currentContext?.crop || 'Soybean');
  const [growthStage, setGrowthStage] = useState(currentContext?.growthStage || 'Flowering');

  const [weatherData, setWeatherData] = useState(null);
  const [riskReport, setRiskReport] = useState(null);
  const [advisoryData, setAdvisoryData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchFarmIntelligence = async () => {
    setLoading(true);
    setError(null);
    try {
      // 1. Get coordinates
      const coords = await api.getCoordinates(location);
      
      // Update global context
      if (setCurrentContext) {
        setCurrentContext({
          location: coords.name,
          latitude: coords.latitude,
          longitude: coords.longitude,
          crop,
          growthStage
        });
      }

      // 2. Fetch Forecast
      const weather = await api.getWeatherForecast(coords.name, coords.latitude, coords.longitude);
      setWeatherData(weather);

      // 3. Fetch Deterministic Risk Report
      const risk = await api.getRiskReport(crop, growthStage, coords.name, coords.latitude, coords.longitude);
      setRiskReport(risk);

      // 4. Generate Practical Advisory
      const advisory = await api.generateAdvisory({
        location: coords.name,
        latitude: coords.latitude,
        longitude: coords.longitude,
        crop,
        growth_stage: growthStage,
        language
      });
      setAdvisoryData(advisory);

    } catch (err) {
      console.error("Error loading dashboard data:", err);
      setError("Failed to fetch climate intelligence. Using resilient cached baseline.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFarmIntelligence();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Header & Context Pill */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-krishi-dark flex items-center gap-2">
            <span>{language === 'en' ? 'Farmer Climate Intelligence Dashboard' : 'किसान कृषि एवं मौसम डैशबोर्ड'}</span>
          </h1>
          <p className="text-xs sm:text-sm text-gray-500 mt-1">
            {language === 'en'
              ? 'Real-time weather telemetry paired with crop phenological risk analysis'
              : 'लाइव मौसम डेटा एवं फसल अवस्था के अनुसार सटीक जोखिम विश्लेषण'}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchFarmIntelligence}
            disabled={loading}
            className="p-3 rounded-2xl bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 shadow-sm transition-all flex items-center gap-2 text-xs font-bold"
            title="Refresh Analysis"
          >
            <RefreshCw className={`w-4 h-4 text-krishi-primary ${loading ? 'animate-spin' : ''}`} />
            <span className="hidden sm:inline">{language === 'en' ? 'Refresh' : 'अपडेट करें'}</span>
          </button>

          <button
            onClick={onOpenChat}
            className="px-4 py-3 rounded-2xl bg-krishi-primary hover:bg-krishi-dark text-white shadow-md hover:shadow-lg transition-all flex items-center gap-2 text-xs font-bold"
          >
            <Sparkles className="w-4 h-4 text-emerald-300" />
            <span>{language === 'en' ? 'Ask AI Assistant' : 'एआई सहायक'}</span>
          </button>
        </div>
      </div>

      {/* Farm Location & Crop Profile Selector */}
      <CropStageSelector
        location={location}
        setLocation={setLocation}
        crop={crop}
        setCrop={setCrop}
        growthStage={growthStage}
        setGrowthStage={setGrowthStage}
        onRefresh={fetchFarmIntelligence}
        loading={loading}
        language={language}
      />

      {/* Error Notice if any */}
      {error && (
        <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 text-amber-800 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Weather Telemetry Row */}
      {weatherData && (
        <div className="space-y-6">
          <CurrentWeatherCard weather={weatherData} language={language} />
          <SevenDayForecast daily={weatherData.daily} language={language} />
        </div>
      )}

      {/* Deterministic Agricultural Risk Section */}
      {riskReport && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-krishi-light text-krishi-primary flex items-center justify-center font-bold">
                <ShieldAlert className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-krishi-dark flex items-center gap-2">
                  <span>{language === 'en' ? 'Crop-Specific Climate Risk Analysis' : 'फसल विशिष्ट जलवायु जोखिम विश्लेषण'}</span>
                  <span className={`text-xs px-2.5 py-0.5 rounded-full font-bold uppercase border ${
                    riskReport.overall_risk_level === 'HIGH'
                      ? 'bg-red-50 text-red-700 border-red-200'
                      : riskReport.overall_risk_level === 'MODERATE'
                      ? 'bg-amber-50 text-amber-700 border-amber-200'
                      : 'bg-emerald-50 text-emerald-700 border-emerald-200'
                  }`}>
                    {riskReport.overall_risk_level}
                  </span>
                </h3>
                <p className="text-xs text-gray-500">
                  {language === 'en'
                    ? `Deterministic algorithms evaluating 5 risk vectors for ${riskReport.crop} (${riskReport.growth_stage})`
                    : `${riskReport.crop} (${riskReport.growth_stage}) हेतु 5 प्रमुख मौसमी जोखिमों का गणितीय विश्लेषण`}
                </p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {riskReport.assessments.map((item, idx) => (
              <RiskCard key={idx} assessment={item} language={language} />
            ))}
          </div>
        </div>
      )}

      {/* 3-Day Action Roadmap */}
      {advisoryData && (
        <ActionRoadmap advisory={advisoryData} language={language} />
      )}

    </div>
  );
};

export default Dashboard;

