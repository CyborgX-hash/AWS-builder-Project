import React from 'react';
import { Calendar, Droplets, ArrowUp, ArrowDown } from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip } from 'recharts';

export const SevenDayForecast = ({ daily, language }) => {
  if (!daily || daily.length === 0) return null;

  const chartData = daily.map((d) => ({
    date: d.date.slice(5),
    tempMax: Math.round(d.temp_max),
    tempMin: Math.round(d.temp_min),
    rain: Number(d.rainfall_sum.toFixed(1)),
    prob: d.precipitation_probability_max
  }));

  const formatDateLabel = (dateStr) => {
    try {
      const dt = new Date(dateStr);
      return dt.toLocaleDateString(language === 'hi' ? 'hi-IN' : 'en-US', {
        weekday: 'short',
        day: 'numeric'
      });
    } catch {
      return dateStr;
    }
  };

  return (
    <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-100 shadow-sm space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-xl bg-krishi-light text-krishi-primary flex items-center justify-center">
            <Calendar className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-krishi-dark">
              {language === 'en' ? '7-Day Agro-Weather Forecast' : '7-दिवसीय कृषि मौसम पूर्वानुमान'}
            </h3>
            <p className="text-xs text-gray-500">
              {language === 'en' ? 'Daily Temperature & Precipitation Probabilities' : 'दैनिक तापमान एवं वर्षा की संभावना'}
            </p>
          </div>
        </div>
      </div>

      {/* Mini Temperature Chart */}
      <div className="h-44 w-full pt-2">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
            <defs>
              <linearGradient id="tempGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#237A45" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#237A45" stopOpacity={0.0}/>
              </linearGradient>
            </defs>
            <XAxis dataKey="date" stroke="#9ca3af" fontSize={11} tickLine={false} />
            <YAxis stroke="#9ca3af" fontSize={11} tickLine={false} unit="°" />
            <Tooltip
              contentStyle={{ backgroundColor: '#fff', borderRadius: '12px', border: '1px solid #e5e7eb', fontSize: '12px' }}
              formatter={(value, name) => [
                `${value}°C`,
                name === 'tempMax' ? (language === 'en' ? 'Max Temp' : 'अधिकतम') : (language === 'en' ? 'Min Temp' : 'न्यूनतम')
              ]}
            />
            <Area type="monotone" dataKey="tempMax" stroke="#237A45" strokeWidth={2.5} fillOpacity={1} fill="url(#tempGradient)" />
            <Area type="monotone" dataKey="tempMin" stroke="#93c5fd" strokeWidth={2} fillOpacity={0} />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* 7-Day Horizontal Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-3">
        {daily.map((item, idx) => {
          const isHeavyRain = item.rainfall_sum >= 25.0;
          return (
            <div
              key={idx}
              className={`p-3.5 rounded-2xl border text-center transition-all ${
                isHeavyRain
                  ? 'bg-blue-50/70 border-blue-200 shadow-sm'
                  : 'bg-gray-50/70 border-gray-100 hover:border-krishi-primary/30'
              }`}
            >
              <div className="text-xs font-semibold text-gray-500 mb-1">
                {formatDateLabel(item.date)}
              </div>
              
              <div className="text-sm font-bold text-gray-800 mb-1">
                {Math.round(item.temp_max)}° <span className="text-xs font-normal text-gray-400">{Math.round(item.temp_min)}°</span>
              </div>

              <div className="flex items-center justify-center gap-1 text-xs font-semibold text-blue-600 mb-1">
                <Droplets className="w-3.5 h-3.5" />
                <span>{item.rainfall_sum}mm</span>
              </div>

              <div className="text-[10px] text-gray-500 font-medium truncate">
                {item.precipitation_probability_max}% {language === 'en' ? 'rain' : 'बारिश'}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default SevenDayForecast;

