import React from 'react';
import { Flame, CloudRain, Waves, SunMedium, Droplets, Info } from 'lucide-react';
import RiskBadge from './RiskBadge';

const CATEGORY_ICONS = {
  heat_stress: Flame,
  excessive_rainfall: CloudRain,
  waterlogging: Waves,
  dry_spell: SunMedium,
  water_stress: Droplets
};

export const RiskCard = ({ assessment, language }) => {
  if (!assessment) return null;

  const Icon = CATEGORY_ICONS[assessment.category] || Info;
  const isHigh = assessment.risk_level === 'HIGH';
  const isMod = assessment.risk_level === 'MODERATE';

  const title = language === 'hi' ? assessment.category_title_hi : assessment.category_title;
  const reason = language === 'hi' ? assessment.reason_hi : assessment.reason_en;
  const monitoring = language === 'hi' ? assessment.recommended_monitoring_hi : assessment.recommended_monitoring_en;

  return (
    <div className={`p-5 sm:p-6 rounded-3xl border transition-all ${
      isHigh
        ? 'bg-red-50/40 border-red-200 shadow-sm'
        : isMod
        ? 'bg-amber-50/30 border-amber-200 shadow-sm'
        : 'bg-white border-gray-100 hover:border-gray-200 shadow-sm'
    }`}>
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex items-center gap-3">
          <div className={`w-10 h-10 rounded-2xl flex items-center justify-center ${
            isHigh
              ? 'bg-red-100 text-red-600'
              : isMod
              ? 'bg-amber-100 text-amber-600'
              : 'bg-emerald-50 text-emerald-600'
          }`}>
            <Icon className="w-5 h-5" />
          </div>
          <div>
            <h4 className="font-bold text-sm sm:text-base text-gray-900">{title}</h4>
            <p className="text-[11px] text-gray-500 font-medium">
              {language === 'en' ? 'Deterministic Score' : 'गणितीय स्कोर'}: {assessment.risk_score}/100
            </p>
          </div>
        </div>

        <RiskBadge level={assessment.risk_level} />
      </div>

      {/* Progress Bar for Score */}
      <div className="w-full bg-gray-200/70 h-2 rounded-full overflow-hidden mb-3">
        <div
          className={`h-full rounded-full transition-all duration-500 ${
            isHigh ? 'bg-red-500' : isMod ? 'bg-amber-500' : 'bg-emerald-500'
          }`}
          style={{ width: `${Math.min(100, Math.max(5, assessment.risk_score))}%` }}
        />
      </div>

      {/* Explanation */}
      <p className="text-xs sm:text-sm text-gray-700 leading-relaxed mb-3">
        {reason}
      </p>

      {/* Monitoring tip footer */}
      <div className="pt-3 border-t border-gray-100/80 flex items-start gap-2 text-xs text-gray-600">
        <span className="font-semibold text-gray-900 flex-shrink-0">
          {language === 'en' ? 'Actionable Scout' : 'निगरानी सलाह'}:
        </span>
        <span className="text-gray-600">{monitoring}</span>
      </div>
    </div>
  );
};

export default RiskCard;

