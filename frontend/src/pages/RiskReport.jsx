import React, { useState, useEffect } from 'react';
import { ShieldAlert, Info, ArrowLeft, RefreshCw, BarChart3, CheckCircle2, AlertTriangle, FileSpreadsheet } from 'lucide-react';
import { Link } from 'react-router-dom';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from 'recharts';
import api from '../services/api';
import RiskCard from '../components/RiskIndicator/RiskCard';
import RiskBadge from '../components/RiskIndicator/RiskBadge';

export const RiskReport = ({ language, currentContext }) => {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);

  const loc = currentContext?.location || 'Balaghat';
  const crop = currentContext?.crop || 'Soybean';
  const stage = currentContext?.growthStage || 'Flowering';

  useEffect(() => {
    const fetchReport = async () => {
      setLoading(true);
      try {
        const coords = await api.getCoordinates(loc);
        const data = await api.getRiskReport(crop, stage, coords.name, coords.latitude, coords.longitude);
        setReport(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchReport();
  }, [loc, crop, stage]);

  const chartData = report?.assessments?.map((a) => ({
    name: language === 'hi' ? a.category_title_hi.split(' ')[0] : a.category_title.replace(' Risk', ''),
    score: a.risk_score,
    level: a.risk_level
  })) || [];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Top Navigation */}
      <div className="flex items-center justify-between">
        <Link
          to="/dashboard"
          className="inline-flex items-center gap-2 text-xs font-bold text-gray-600 hover:text-krishi-primary transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>{language === 'en' ? 'Back to Farm Dashboard' : 'डैशबोर्ड पर वापस जाएं'}</span>
        </Link>

        {report && (
          <div className="flex items-center gap-2">
            <span className="text-xs text-gray-500">{language === 'en' ? 'Overall Risk' : 'कुल जोखिम'}:</span>
            <RiskBadge level={report.overall_risk_level} size="lg" />
          </div>
        )}
      </div>

      {/* Header Banner */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-100 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-krishi-primary bg-krishi-light px-3 py-1 rounded-full">
              {language === 'en' ? 'Deterministic Screening Model' : 'सटीक गणितीय मॉडल'}
            </span>
            <h1 className="text-2xl sm:text-3xl font-black text-krishi-dark mt-2">
              {language === 'en' ? 'Agricultural Climate Risk Report' : 'कृषि जलवायु जोखिम विस्तृत रिपोर्ट'}
            </h1>
            <p className="text-xs sm:text-sm text-gray-600 mt-1">
              <strong>{report?.crop || crop}</strong> ({report?.growth_stage || stage}) • <strong>{loc}</strong>
            </p>
          </div>
          <div className="text-xs text-gray-500 sm:text-right">
            <p>{language === 'en' ? 'Evaluation Timestamp' : 'मूल्यांकन समय'}:</p>
            <p className="font-semibold text-gray-800">{report?.calculation_timestamp || 'Live'}</p>
          </div>
        </div>

        {/* Explainability Callout */}
        <div className="p-4 rounded-2xl bg-gray-50 border border-gray-100 text-xs text-gray-600 leading-relaxed flex items-start gap-2.5">
          <Info className="w-4 h-4 text-krishi-primary flex-shrink-0 mt-0.5" />
          <p>
            {language === 'en'
              ? "Every risk score is computed deterministically in Python using validated ICAR/FAO physiological thresholds and numerical weather predictions. LLMs do not decide numerical scores."
              : "प्रत्येक जोखिम स्कोर आईसीएआर और एफएओ के मान्य कृषि मानकों और मौसम मॉडल के आधार पर सीधे पायथन कोड द्वारा तय किया जाता है। भाषा मॉडल कोई मनगढ़ंत संख्या नहीं बनाते।"}
          </p>
        </div>
      </div>

      {/* Bar Chart Overview */}
      {report && (
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-100 shadow-sm space-y-4">
          <h3 className="font-bold text-base text-krishi-dark flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-krishi-primary" />
            <span>{language === 'en' ? 'Comparative Risk Index (0 - 100 Scale)' : 'तुलनात्मक जोखिम सूचकांक (0 - 100 पैमाना)'}</span>
          </h3>

          <div className="h-60 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <XAxis dataKey="name" stroke="#6b7280" fontSize={12} tickLine={false} />
                <YAxis stroke="#6b7280" fontSize={11} domain={[0, 100]} tickLine={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#fff', borderRadius: '12px', border: '1px solid #e5e7eb', fontSize: '12px' }}
                  formatter={(val) => [`${val} / 100`, language === 'en' ? 'Risk Score' : 'जोखिम स्कोर']}
                />
                <Bar dataKey="score" radius={[8, 8, 0, 0]}>
                  {chartData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={entry.level === 'HIGH' ? '#D9534F' : entry.level === 'MODERATE' ? '#E6A23C' : '#237A45'}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Detailed Risk Breakdown Cards */}
      {report && (
        <div className="space-y-4">
          <h3 className="text-lg font-bold text-krishi-dark">
            {language === 'en' ? 'Detailed Risk Vector Evaluations' : 'विस्तृत जोखिम विश्लेषण विवरण'}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {report.assessments.map((a, idx) => (
              <RiskCard key={idx} assessment={a} language={language} />
            ))}
          </div>
        </div>
      )}

      {/* Limitations Disclaimer */}
      {report && (
        <div className="p-5 rounded-3xl bg-white border border-gray-100 shadow-sm text-xs text-gray-500 leading-relaxed space-y-2">
          <span className="font-bold text-gray-800 block">
            {language === 'en' ? 'Screening Methodology & Scientific Integrity' : 'वैज्ञानिक पद्धति एवं सीमाएं'}:
          </span>
          <p>{report.limitations_disclaimer}</p>
        </div>
      )}

    </div>
  );
};

export default RiskReport;
