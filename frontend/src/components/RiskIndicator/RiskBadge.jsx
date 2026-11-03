import React from 'react';
import { AlertTriangle, AlertCircle, CheckCircle2 } from 'lucide-react';

export const RiskBadge = ({ level, score, size = 'md' }) => {
  const isHigh = level === 'HIGH';
  const isMod = level === 'MODERATE';

  const badgeConfig = isHigh
    ? {
        bg: 'bg-red-50 text-red-700 border-red-200',
        icon: AlertCircle,
        dot: 'bg-red-500'
      }
    : isMod
    ? {
        bg: 'bg-amber-50 text-amber-700 border-amber-200',
        icon: AlertTriangle,
        dot: 'bg-amber-500'
      }
    : {
        bg: 'bg-emerald-50 text-emerald-700 border-emerald-200',
        icon: CheckCircle2,
        dot: 'bg-emerald-500'
      };

  const Icon = badgeConfig.icon;
  const padding = size === 'lg' ? 'px-3.5 py-1.5 text-sm font-extrabold' : 'px-2.5 py-1 text-xs font-bold';

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full border shadow-2xs ${badgeConfig.bg} ${padding}`}>
      <span className={`w-2 h-2 rounded-full ${badgeConfig.dot} animate-pulse`} />
      <Icon className={size === 'lg' ? 'w-4 h-4' : 'w-3.5 h-3.5'} />
      <span>{level}</span>
      {score !== undefined && (
        <span className="text-[10px] font-semibold opacity-80">({score})</span>
      )}
    </span>
  );
};

export default RiskBadge;
