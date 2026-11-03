import React from 'react';
import { CloudRain, Wind, Droplets, Thermometer, Clock, Sun, CloudFog, CloudLightning } from 'lucide-react';

export const CurrentWeatherCard = ({ weather, language }) => {
  if (!weather || !weather.current) return null;

  const current = weather.current;

  const getWeatherIcon = (code) => {
    if (code >= 95) return <CloudLightning className="w-12 h-12 text-amber-500 animate-pulse" />;
    if (code >= 61 || code >= 80) return <CloudRain className="w-12 h-12 text-blue-500" />;
    if (code >= 45) return <CloudFog className="w-12 h-12 text-gray-400" />;
    return <Sun className="w-12 h-12 text-amber-500" />;
  };

  return (
    <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-100 shadow-sm relative overflow-hidden">
      {/* Decorative gradient corner */}
      <div className="absolute top-0 right-0 w-48 h-48 bg-gradient-to-br from-krishi-light/60 to-transparent rounded-bl-full -z-0 pointer-events-none" />

      <div className="relative z-10">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-bold uppercase tracking-wider text-krishi-primary bg-krishi-light px-3 py-1 rounded-full">
                {language === 'en' ? 'Live Meteorological Radar' : 'लाइव मौसम रडार'}
              </span>
              <span className="text-xs text-gray-600 flex items-center gap-1">
                <Clock className="w-3.5 h-3.5" />
                {weather.retrieved_at}
              </span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-krishi-dark">
              {weather.location}
            </h2>
          </div>

          <div className="flex items-center gap-4 bg-gray-50/80 p-3 rounded-2xl border border-gray-100">
            {getWeatherIcon(current.weather_code)}
            <div>
              <div className="text-3xl font-extrabold text-gray-900">
                {Math.round(current.temperature)}°C
              </div>
              <div className="text-xs font-semibold text-gray-700">
                {current.weather_description}
              </div>
            </div>
          </div>
        </div>

        {/* Core Metrics Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-4 border-t border-gray-100">
          
          <div className="p-4 rounded-2xl bg-krishi-bg/60 border border-gray-100/80">
            <div className="flex items-center gap-2 text-xs font-semibold text-gray-600 mb-1">
              <Droplets className="w-4 h-4 text-blue-500" />
              <span>{language === 'en' ? 'Relative Humidity' : 'सापेक्ष आर्द्रता'}</span>
            </div>
            <div className="text-xl font-bold text-gray-800">
              {current.humidity}%
            </div>
            <p className="text-[11px] text-gray-600 mt-0.5">
              {current.humidity > 75 ? (language === 'en' ? 'High - fungal risk' : 'अधिक - फफूंद खतरा') : (language === 'en' ? 'Moderate' : 'सामान्य')}
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-krishi-bg/60 border border-gray-100/80">
            <div className="flex items-center gap-2 text-xs font-semibold text-gray-600 mb-1">
              <CloudRain className="w-4 h-4 text-blue-600" />
              <span>{language === 'en' ? 'Rainfall' : 'वर्तमान वर्षा'}</span>
            </div>
            <div className="text-xl font-bold text-gray-800">
              {current.rainfall} <span className="text-xs font-normal">mm</span>
            </div>
            <p className="text-[11px] text-gray-600 mt-0.5">
              {current.rainfall_probability}% {language === 'en' ? 'probability' : 'संभावना'}
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-krishi-bg/60 border border-gray-100/80">
            <div className="flex items-center gap-2 text-xs font-semibold text-gray-600 mb-1">
              <Wind className="w-4 h-4 text-teal-600" />
              <span>{language === 'en' ? 'Wind Speed' : 'हवा की गति'}</span>
            </div>
            <div className="text-xl font-bold text-gray-800">
              {current.wind_speed} <span className="text-xs font-normal">km/h</span>
            </div>
            <p className="text-[11px] text-gray-600 mt-0.5">
              {current.wind_speed > 25 ? (language === 'en' ? 'Strong winds' : 'तेज हवा') : (language === 'en' ? 'Gentle breeze' : 'हल्की हवा')}
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-krishi-bg/60 border border-gray-100/80">
            <div className="flex items-center gap-2 text-xs font-semibold text-gray-600 mb-1">
              <Thermometer className="w-4 h-4 text-amber-600" />
              <span>{language === 'en' ? 'Data Source' : 'डेटा स्रोत'}</span>
            </div>
            <div className="text-sm font-bold text-gray-800 truncate">
              Open-Meteo & IMD
            </div>
            <p className="text-[11px] text-emerald-600 font-semibold mt-0.5">
              ● {language === 'en' ? 'Verified Feed' : 'सत्यापित स्रोत'}
            </p>
          </div>

        </div>
      </div>
    </div>
  );
};

export default CurrentWeatherCard;

