import React, { useState } from 'react';
import { MapPin, Sprout, Layers, Search } from 'lucide-react';

const CROPS_META = [
  {
    key: 'Soybean',
    nameEn: 'Soybean',
    nameHi: 'सोयाबीन',
    stages: [
      { en: 'Germination / Emergence', hi: 'अंकुरण एवं प्रारंभिक अवस्था' },
      { en: 'Vegetative', hi: 'वानस्पतिक वृद्धि' },
      { en: 'Flowering', hi: 'फूल आने की अवस्था' },
      { en: 'Pod Development / Seed Filling', hi: 'फली विकास एवं दाना भराव' },
      { en: 'Maturity / Harvest', hi: 'परिपक्वता एवं कटाई' }
    ]
  },
  {
    key: 'Rice',
    nameEn: 'Rice / Paddy',
    nameHi: 'धान / चावल',
    stages: [
      { en: 'Nursery / Seedling', hi: 'नर्सरी एवं पौध अवस्था' },
      { en: 'Tillering', hi: 'कल्ले फूटने की अवस्था' },
      { en: 'Panicle Initiation / Flowering', hi: 'बाली निकलना एवं फूल अवस्था' },
      { en: 'Grain Filling / Dough Stage', hi: 'दुग्धावस्था एवं दाना भराव' },
      { en: 'Maturity / Harvest', hi: 'परिपक्वता एवं कटाई' }
    ]
  },
  {
    key: 'Wheat',
    nameEn: 'Wheat',
    nameHi: 'गेहूं',
    stages: [
      { en: 'Crown Root Initiation (CRI)', hi: 'ताज जड़ निकलने की अवस्था (CRI)' },
      { en: 'Tillering & Jointing', hi: 'कल्ले फूटना एवं गांठ बनना' },
      { en: 'Flowering / Heading', hi: 'बाली निकलना एवं फूल अवस्था' },
      { en: 'Milking & Dough (Grain Filling)', hi: 'दूधिया एवं दाना भराव अवस्था' },
      { en: 'Maturity / Harvest', hi: 'परिपक्वता एवं कटाई' }
    ]
  },
  {
    key: 'Maize',
    nameEn: 'Maize',
    nameHi: 'मक्का',
    stages: [
      { en: 'Knee-High (Vegetative)', hi: 'घुटने तक की वृद्धि अवस्था' },
      { en: 'Tasseling & Silking', hi: 'मंजरी एवं भुट्टा रेशे निकलना' },
      { en: 'Grain Filling / Dough', hi: 'दाना भराव अवस्था' },
      { en: 'Maturity / Harvest', hi: 'परिपक्वता एवं तुड़ाई' }
    ]
  },
  {
    key: 'Cotton',
    nameEn: 'Cotton',
    nameHi: 'कपास',
    stages: [
      { en: 'Vegetative / Square Formation', hi: 'वानस्पतिक एवं कली अवस्था' },
      { en: 'Flowering & Boll Formation', hi: 'फूल एवं टिंडे बनने की अवस्था' },
      { en: 'Boll Maturation & Bursting', hi: 'टिंडे का पकना एवं खिलना' }
    ]
  }
];

const POPULAR_LOCATIONS = [
  'Balaghat, MP',
  'Indore, MP',
  'Seoni, MP',
  'Nagpur, MH',
  'Amravati, MH',
  'Ludhiana, PB',
  'Karnal, HR',
  'Varanasi, UP'
];

export const CropStageSelector = ({
  location,
  setLocation,
  crop,
  setCrop,
  growthStage,
  setGrowthStage,
  onRefresh,
  loading,
  language
}) => {
  const currentCropObj = CROPS_META.find((c) => c.key === crop) || CROPS_META[0];

  const handleCropChange = (e) => {
    const newCropKey = e.target.value;
    setCrop(newCropKey);
    const newObj = CROPS_META.find((c) => c.key === newCropKey) || CROPS_META[0];
    setGrowthStage(newObj.stages[1].en); // Default to vegetative stage
  };

  return (
    <div className="bg-white rounded-3xl p-6 sm:p-7 border border-gray-100 shadow-sm">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        
        {/* Location Input */}
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-gray-500 mb-2 flex items-center gap-1.5">
            <MapPin className="w-4 h-4 text-krishi-primary" />
            <span>{language === 'en' ? 'Farm Location / District' : 'खेत का स्थान / जिला'}</span>
          </label>
          <div className="relative">
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              list="popular-locations"
              placeholder={language === 'en' ? 'e.g. Balaghat' : 'उदा. बालाघाट'}
              className="w-full bg-gray-50 border border-gray-200 rounded-2xl px-4 py-3 text-sm font-semibold text-gray-800 focus:outline-none focus:ring-2 focus:ring-krishi-primary/30 focus:border-krishi-primary transition-all"
            />
            <datalist id="popular-locations">
              {POPULAR_LOCATIONS.map((loc, i) => (
                <option key={i} value={loc} />
              ))}
            </datalist>
          </div>
        </div>

        {/* Crop Select */}
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-gray-500 mb-2 flex items-center gap-1.5">
            <Sprout className="w-4 h-4 text-krishi-primary" />
            <span>{language === 'en' ? 'Crop' : 'फसल'}</span>
          </label>
          <select
            value={crop}
            onChange={handleCropChange}
            className="w-full bg-gray-50 border border-gray-200 rounded-2xl px-4 py-3 text-sm font-semibold text-gray-800 focus:outline-none focus:ring-2 focus:ring-krishi-primary/30 focus:border-krishi-primary transition-all"
          >
            {CROPS_META.map((c) => (
              <option key={c.key} value={c.key}>
                {language === 'en' ? c.nameEn : `${c.nameHi} (${c.nameEn})`}
              </option>
            ))}
          </select>
        </div>

        {/* Growth Stage Select */}
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-gray-500 mb-2 flex items-center gap-1.5">
            <Layers className="w-4 h-4 text-krishi-primary" />
            <span>{language === 'en' ? 'Growth Stage' : 'फसल की अवस्था'}</span>
          </label>
          <select
            value={growthStage}
            onChange={(e) => setGrowthStage(e.target.value)}
            className="w-full bg-gray-50 border border-gray-200 rounded-2xl px-4 py-3 text-sm font-semibold text-gray-800 focus:outline-none focus:ring-2 focus:ring-krishi-primary/30 focus:border-krishi-primary transition-all"
          >
            {currentCropObj.stages.map((st, i) => (
              <option key={i} value={st.en}>
                {language === 'en' ? st.en : `${st.hi} (${st.en})`}
              </option>
            ))}
          </select>
        </div>

        {/* Update Button */}
        <div className="flex items-end">
          <button
            onClick={onRefresh}
            disabled={loading}
            className="w-full bg-krishi-primary hover:bg-krishi-dark text-white font-bold py-3 px-5 rounded-2xl shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2 disabled:opacity-60"
          >
            <Search className="w-4 h-4" />
            <span>
              {loading
                ? (language === 'en' ? 'Analyzing...' : 'विश्लेषण जारी...')
                : (language === 'en' ? 'Analyze Farm Climate' : 'जलवायु विश्लेषण करें')}
            </span>
          </button>
        </div>

      </div>
    </div>
  );
};

export default CropStageSelector;
