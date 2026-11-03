import React, { useState, useEffect } from 'react';
import { FileText, ArrowLeft, Printer, Share2, Sparkles, AlertCircle, CheckCircle } from 'lucide-react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import ActionRoadmap from '../components/Dashboard/ActionRoadmap';

export const Advisory = ({ language, currentContext }) => {
  const [advisory, setAdvisory] = useState(null);
  const [loading, setLoading] = useState(true);

  const loc = currentContext?.location || 'Balaghat';
  const crop = currentContext?.crop || 'Soybean';
  const stage = currentContext?.growthStage || 'Flowering';

  useEffect(() => {
    const fetchAdvisory = async () => {
      setLoading(true);
      try {
        const coords = await api.getCoordinates(loc);
        const data = await api.generateAdvisory({
          location: coords.name,
          latitude: coords.latitude,
          longitude: coords.longitude,
          crop,
          growth_stage: stage,
          language
        });
        setAdvisory(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchAdvisory();
  }, [loc, crop, stage, language]);

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 print:p-0">
      
      {/* Top Bar */}
      <div className="flex items-center justify-between print:hidden">
        <Link
          to="/dashboard"
          className="inline-flex items-center gap-2 text-xs font-bold text-gray-600 hover:text-krishi-primary transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>{language === 'en' ? 'Back to Dashboard' : 'डैशबोर्ड पर वापस जाएं'}</span>
        </Link>

        <div className="flex items-center gap-2">
          <button
            onClick={handlePrint}
            className="px-4 py-2 rounded-xl bg-white border border-gray-200 hover:bg-gray-50 text-xs font-bold text-gray-700 shadow-sm transition-all flex items-center gap-1.5"
          >
            <Printer className="w-4 h-4 text-gray-500" />
            <span>{language === 'en' ? 'Print Advisory' : 'प्रिंट करें'}</span>
          </button>
        </div>
      </div>

      {/* Advisory Header Banner */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-100 shadow-sm space-y-3">
        <div className="flex items-center gap-2">
          <div className="w-9 h-9 rounded-xl bg-krishi-light text-krishi-primary flex items-center justify-center font-bold">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-krishi-primary">
              {language === 'en' ? 'Official Farmer Advisory' : 'आधिकारिक कृषि परामर्श'}
            </span>
            <h1 className="text-2xl font-black text-krishi-dark">
              {language === 'en'
                ? `Agricultural Action Advisory: ${advisory?.crop || crop}`
                : `कृषि कार्य परामर्श: ${advisory?.crop_hi || crop}`}
            </h1>
          </div>
        </div>

        <p className="text-xs text-gray-500">
          <strong>{language === 'en' ? 'Farm Location' : 'स्थान'}</strong>: {loc} •{' '}
          <strong>{language === 'en' ? 'Crop Stage' : 'फसल अवस्था'}</strong>: {advisory?.growth_stage || stage} •{' '}
          <strong>{language === 'en' ? 'Generated' : 'जारी समय'}</strong>: {advisory?.forecast_timestamp || 'Live'}
        </p>

        {advisory && (
          <div className="p-4 rounded-2xl bg-krishi-bg border border-krishi-primary/10 text-xs sm:text-sm text-krishi-dark leading-relaxed font-medium">
            {language === 'hi' ? advisory.summary_hi : advisory.summary_en}
          </div>
        )}
      </div>

      {/* 3-Day Action Roadmap */}
      {advisory && (
        <ActionRoadmap advisory={advisory} language={language} />
      )}

      {/* General Best Practices */}
      {advisory && (
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-100 shadow-sm space-y-4">
          <h3 className="font-bold text-base text-krishi-dark flex items-center gap-2">
            <CheckCircle className="w-5 h-5 text-krishi-primary" />
            <span>{language === 'en' ? 'General Seasonal Precautions' : 'सामान्य मौसमी सावधानियां'}</span>
          </h3>
          <ul className="space-y-2 text-xs sm:text-sm text-gray-700 list-disc list-inside leading-relaxed">
            {(language === 'hi' ? advisory.general_precautions_hi : advisory.general_precautions_en).map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
      )}

    </div>
  );
};

export default Advisory;

