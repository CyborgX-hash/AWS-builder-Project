import React from 'react';
import { CalendarCheck, ShieldAlert, AlertCircle, CheckCircle, Clock } from 'lucide-react';

export const ActionRoadmap = ({ advisory, language }) => {
  if (!advisory) return null;

  const immediates = language === 'hi' ? advisory.immediate_precautions_hi : advisory.immediate_precautions_en;
  const plan = advisory.action_plan_3d || [];
  const officialNote = language === 'hi' ? advisory.official_advisory_note_hi : advisory.official_advisory_note_en;

  return (
    <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-100 shadow-sm space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-10 h-10 rounded-xl bg-krishi-light text-krishi-primary flex items-center justify-center">
            <CalendarCheck className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-krishi-dark">
              {language === 'en' ? '3-Day Agricultural Action Roadmap' : '3-दिवसीय कृषि कार्य योजना'}
            </h3>
            <p className="text-xs text-gray-500">
              {language === 'en'
                ? `Specific recommendations for ${advisory.crop} (${advisory.growth_stage})`
                : `${advisory.crop_hi} (${advisory.growth_stage_hi}) हेतु विशेष कृषि सलाह`}
            </p>
          </div>
        </div>
      </div>

      {/* Immediate Precautions Callout */}
      {immediates && immediates.length > 0 && (
        <div className="p-5 rounded-2xl bg-amber-50/70 border border-amber-200">
          <div className="flex items-center gap-2 text-sm font-bold text-amber-900 mb-2">
            <AlertCircle className="w-4 h-4 text-amber-600" />
            <span>{language === 'en' ? 'Immediate Urgent Precautions' : 'तत्काल जरूरी सावधानियां'}</span>
          </div>
          <ul className="space-y-1.5 text-xs sm:text-sm text-amber-900/90 list-disc list-inside">
            {immediates.map((item, idx) => (
              <li key={idx} className="leading-relaxed">
                {item}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* 3 Days Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {plan.map((dayItem, idx) => {
          const actions = language === 'hi' ? dayItem.recommended_actions_hi : dayItem.recommended_actions_en;
          const forecast = language === 'hi' ? dayItem.forecast_summary_hi : dayItem.forecast_summary;
          const monitor = language === 'hi' ? dayItem.what_to_monitor_hi : dayItem.what_to_monitor_en;

          return (
            <div
              key={idx}
              className="p-5 rounded-2xl bg-gray-50/70 border border-gray-100 flex flex-col justify-between hover:border-krishi-primary/30 transition-all"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-krishi-primary bg-krishi-light px-2.5 py-0.5 rounded-full">
                    {dayItem.day_label}
                  </span>
                  <span className="text-[11px] text-gray-500">{dayItem.date_str}</span>
                </div>

                <div className="text-xs font-semibold text-gray-700 bg-white p-2.5 rounded-xl border border-gray-100 mb-3">
                  🌧️ {forecast}
                </div>

                <div className="space-y-2 mb-4">
                  <span className="text-xs font-bold text-gray-900 block">
                    {language === 'en' ? 'Recommended Action:' : 'कार्य योजना:'}
                  </span>
                  <ul className="space-y-1 text-xs text-gray-700 list-disc list-inside">
                    {actions.map((act, aIdx) => (
                      <li key={aIdx} className="leading-relaxed">{act}</li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="pt-3 border-t border-gray-200/60 text-[11px] text-gray-600">
                <span className="font-semibold text-gray-800">
                  {language === 'en' ? 'Monitor' : 'निगरानी'}:
                </span>{' '}
                {monitor}
              </div>
            </div>
          );
        })}
      </div>

      {/* Official Advisory Disclaimer Notice */}
      <div className="p-4 rounded-2xl bg-gray-50 border border-gray-100 text-xs text-gray-500 leading-relaxed flex items-start gap-2.5">
        <ShieldAlert className="w-4 h-4 text-gray-400 flex-shrink-0 mt-0.5" />
        <p>{officialNote}</p>
      </div>
    </div>
  );
};

export default ActionRoadmap;

