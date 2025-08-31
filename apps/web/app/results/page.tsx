"use client";

import { useEffect, useState, Suspense, useMemo } from "react";
import { useSearchParams, useRouter } from "next/navigation";

interface Service {
  id?: number;
  name: string;
  description: string;
  agency?: string;
  address_norm?: string;
  suburb?: string;
  state?: string;
  lat?: number;
  lon?: number;
  distance_km?: number;
  phone?: string | null;
  website?: string | null;
  seifa_decile?: number | null;
  contact?: string;
}

interface RuleCard {
  category: string;
  suburb: string;
  rulecard: string;
  data_sources: string[];
}

interface SeifaData {
  location: string;
  seifa_decile: number;
  seifa_score: number;
  population: number;
  data_sources: string[];
}

interface LabourData {
  state: string;
  national_unemployment: number;
  national_employment_rate: number;
  youth_unemployment: number;
  data_sources: string[];
}

interface AIInsight {
  intent: string;
  confidence: number;
  ai_insight: string;
  detected_location: string;
  context?: any;
}

const CATEGORY_ICONS = {
  transport: "🚗",
  employment: "💼",
  housing: "🏠",
  health: "🏥",
  education: "🎓",
  social_services: "🤝",
  immigration: "🌏",
  legal: "⚖️"
};

const CATEGORY_COLORS = {
  transport: "from-blue-500 to-cyan-500",
  employment: "from-green-500 to-emerald-500",
  housing: "from-orange-500 to-red-500",
  health: "from-pink-500 to-rose-500",
  education: "from-purple-500 to-indigo-500",
  social_services: "from-teal-500 to-cyan-500",
  immigration: "from-yellow-500 to-orange-500",
  legal: "from-gray-500 to-slate-500"
};

function ResultsPageContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  
  const category = useMemo(() => searchParams.get("category") || "", [searchParams]);
  const state = useMemo(() => searchParams.get("state") || "", [searchParams]);
  const suburb = useMemo(() => searchParams.get("suburb") || "", [searchParams]);
  const userQuery = useMemo(() => searchParams.get("user_query") || "", [searchParams]);
  const fullQuery = useMemo(() => searchParams.get("fullQuery") || "", [searchParams]);
  
  const [services, setServices] = useState<Service[]>([]);
  const [seifa, setSeifa] = useState<SeifaData | null>(null);
  const [labour, setLabour] = useState<LabourData | null>(null);
  const [rulecard, setRulecard] = useState<RuleCard | null>(null);
  const [aiInsight, setAiInsight] = useState<AIInsight | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (category && state && suburb && userQuery) {
      fetchAll();
    }
  }, [category, state, suburb, userQuery]);

  async function fetchAll() {
    setLoading(true);
    setError(null);
    
    try {
      const base = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/v1";
      
      const [intentRes, servicesRes, seifaRes, labourRes, rulecardRes] = await Promise.allSettled([
        fetch(`${base}/intent`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ category, state, suburb, user_query: userQuery })
        }),
        fetch(`${base}/services?category=${category}&state=${state}&suburb=${encodeURIComponent(suburb)}&limit=5`),
        fetch(`${base}/seifa/${encodeURIComponent(suburb)}`),
        fetch(`${base}/labour/${state}`),
        fetch(`${base}/rulecards?category=${category}&suburb=${encodeURIComponent(suburb)}`)
      ]);

      if (intentRes.status === 'fulfilled' && intentRes.value.ok) {
        const intentData = await intentRes.value.json();
        setAiInsight(intentData);
      }

      if (servicesRes.status === 'fulfilled' && servicesRes.value.ok) {
        const servData = await servicesRes.value.json();
        setServices(servData.services || []);
      }

      if (seifaRes.status === 'fulfilled' && seifaRes.value.ok) {
        const seifaData = await seifaRes.value.json();
        setSeifa(seifaData);
      }

      if (labourRes.status === 'fulfilled' && labourRes.value.ok) {
        const labourData = await labourRes.value.json();
        setLabour(labourData);
      }

      if (rulecardRes.status === 'fulfilled' && rulecardRes.value.ok) {
        const rulecardData = await rulecardRes.value.json();
        setRulecard(rulecardData);
      }

    } catch (err) {
      setError("Error fetching data");
      console.error("Error fetching data:", err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Getting your personalized assistance...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={() => router.push('/')}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                GovMate AI Assistant
              </h1>
              <p className="text-gray-600">
                Your personalized government service recommendations
              </p>
            </div>
            <button
              onClick={() => router.push('/')}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              New Query
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <div className={`inline-flex items-center px-4 py-2 rounded-full bg-gradient-to-r ${CATEGORY_COLORS[category as keyof typeof CATEGORY_COLORS] || 'from-gray-500 to-gray-600'} text-white text-sm font-semibold`}>
            <span className="mr-2">{CATEGORY_ICONS[category as keyof typeof CATEGORY_ICONS] || "📋"}</span>
            {category.charAt(0).toUpperCase() + category.slice(1).replace('_', ' ')}
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mt-4 mb-2">
            {suburb}, {state}
          </h2>
          <p className="text-gray-600">{userQuery}</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="space-y-6">
            {aiInsight && (
              <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
                <div className="flex items-center mb-4">
                  <div className="text-2xl mr-3">🤖</div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">AI Analysis</h3>
                    <p className="text-sm text-gray-500">Confidence: {aiInsight.confidence * 100}%</p>
                  </div>
                </div>
                <p className="text-gray-700 leading-relaxed">{aiInsight.ai_insight}</p>
              </div>
            )}

            {services.length > 0 && (
              <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
                <div className="flex items-center mb-4">
                  <div className="text-2xl mr-3">🏛️</div>
                  <h3 className="text-lg font-semibold text-gray-900">Available Services</h3>
                </div>
                <div className="space-y-4">
                  {services.map((service, index) => (
                    <div key={index} className="border-l-4 border-blue-500 pl-4">
                      <h4 className="font-semibold text-gray-900">{service.name}</h4>
                      <p className="text-gray-600 text-sm mb-2">{service.description}</p>
                      {service.contact && (
                        <p className="text-blue-600 text-sm">Contact: {service.contact}</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="space-y-6">
            {seifa && (
              <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
                <div className="flex items-center mb-4">
                  <div className="text-2xl mr-3">📊</div>
                  <h3 className="text-lg font-semibold text-gray-900">Area Information</h3>
                </div>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium text-gray-700">SEIFA Decile:</span>
                    <span className={`text-sm font-semibold px-2 py-1 rounded-full ${
                      seifa.seifa_decile <= 3 ? 'bg-red-100 text-red-800' :
                      seifa.seifa_decile <= 6 ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {seifa.seifa_decile}/10
                    </span>
                  </div>
                  <p className="text-sm text-gray-600">
                    Population: {seifa.population.toLocaleString()}, SEIFA Score: {seifa.seifa_score}
                  </p>
                </div>
              </div>
            )}

            {labour && (
              <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
                <div className="flex items-center mb-4">
                  <div className="text-2xl mr-3">💼</div>
                  <h3 className="text-lg font-semibold text-gray-900">Employment Context</h3>
                </div>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Unemployment Rate:</span>
                    <span className="text-sm font-semibold">{labour.national_unemployment}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Employment Rate:</span>
                    <span className="text-sm font-semibold">{labour.national_employment_rate}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Youth Unemployment:</span>
                    <span className="text-sm font-semibold">{labour.youth_unemployment}%</span>
                  </div>
                </div>
              </div>
            )}

            {rulecard && (
              <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
                <div className="flex items-center mb-4">
                  <div className="text-2xl mr-3">📋</div>
                  <h3 className="text-lg font-semibold text-gray-900">Step-by-Step Guide</h3>
                </div>
                <div className="space-y-3">
                  {rulecard.rulecard.split('\n').map((step, index) => (
                    <div key={index} className="flex items-start">
                      <span className="bg-gradient-to-r from-blue-500 to-purple-500 text-white text-xs font-semibold rounded-full w-6 h-6 flex items-center justify-center mr-3 mt-0.5 flex-shrink-0">
                        {index + 1}
                      </span>
                      <p className="text-sm text-gray-700">{step}</p>
                    </div>
                  ))}
                </div>
                <div className="mt-6 pt-4 border-t border-gray-100">
                  <p className="text-xs text-gray-500">
                    <strong>Sources:</strong> {(rulecard.data_sources || []).join(', ')}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function ResultsPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    }>
      <ResultsPageContent />
    </Suspense>
  );
}