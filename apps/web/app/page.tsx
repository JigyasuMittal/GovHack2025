"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const CATEGORIES = [
  {
    id: "transport",
    name: "Transport & Driving",
    description: "Driver licences, vehicle registration, public transport",
    icon: "🚗"
  },
  {
    id: "employment",
    name: "Employment & Work",
    description: "Job seeking, unemployment benefits, career support",
    icon: "💼"
  },
  {
    id: "housing",
    name: "Housing & Accommodation",
    description: "Public housing, rental assistance, homelessness support",
    icon: "🏠"
  },
  {
    id: "health",
    name: "Health & Medical",
    description: "Healthcare services, Medicare, mental health support",
    icon: "🏥"
  },
  {
    id: "education",
    name: "Education & Training",
    description: "Schools, universities, training programs, student support",
    icon: "🎓"
  },
  {
    id: "social_services",
    name: "Social Services",
    description: "Centrelink, welfare, community support, food assistance",
    icon: "🤝"
  },
  {
    id: "immigration",
    name: "Immigration & Citizenship",
    description: "Visa applications, citizenship, settlement services",
    icon: "🌏"
  },
  {
    id: "legal",
    name: "Legal & Justice",
    description: "Legal aid, court services, police assistance",
    icon: "⚖️"
  }
];

const STATES = [
  { id: "NSW", name: "New South Wales" },
  { id: "VIC", name: "Victoria" },
  { id: "QLD", name: "Queensland" },
  { id: "WA", name: "Western Australia" },
  { id: "SA", name: "South Australia" },
  { id: "TAS", name: "Tasmania" },
  { id: "ACT", name: "Australian Capital Territory" },
  { id: "NT", name: "Northern Territory" }
];

const SUBURBS_BY_STATE = {
  NSW: [
    "Sydney CBD", "Parramatta", "Newcastle", "Wollongong", "Central Coast",
    "Blue Mountains", "Hunter Valley", "Illawarra", "North Shore", "Western Sydney"
  ],
  VIC: [
    "Melbourne CBD", "Geelong", "Ballarat", "Bendigo", "Shepparton",
    "Mildura", "Warrnambool", "Albury-Wodonga", "Latrobe Valley", "Mornington Peninsula"
  ],
  QLD: [
    "Brisbane City", "Gold Coast", "Sunshine Coast", "Townsville", "Cairns",
    "Toowoomba", "Mackay", "Rockhampton", "Bundaberg", "Hervey Bay"
  ],
  WA: [
    "Perth CBD", "Fremantle", "Joondalup", "Rockingham", "Mandurah",
    "Albany", "Bunbury", "Geraldton", "Kalgoorlie", "Broome"
  ],
  SA: [
    "Adelaide CBD", "Mount Gambier", "Whyalla", "Murray Bridge", "Port Augusta",
    "Port Pirie", "Port Lincoln", "Renmark", "Berri", "Mount Barker"
  ],
  TAS: [
    "Hobart", "Launceston", "Devonport", "Burnie", "Ulverstone",
    "Kingston", "Clarence", "Glenorchy", "New Norfolk", "Bridgewater"
  ],
  ACT: [
    "Canberra City", "Belconnen", "Woden", "Tuggeranong", "Gungahlin",
    "Fyshwick", "Mitchell", "Fyshwick", "Dickson", "Braddon"
  ],
  NT: [
    "Darwin", "Alice Springs", "Palmerston", "Katherine", "Tennant Creek",
    "Jabiru", "Nhulunbuy", "Alyangula", "Jabiru", "Tennant Creek"
  ]
};

export default function HomePage() {
  const router = useRouter();
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedState, setSelectedState] = useState("");
  const [selectedSuburb, setSelectedSuburb] = useState("");
  const [userQuery, setUserQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [availableSuburbs, setAvailableSuburbs] = useState<string[]>([]);
  const [loadingSuburbs, setLoadingSuburbs] = useState(false);

  const fetchSuburbs = async (state: string) => {
    if (!state) {
      setAvailableSuburbs([]);
      return;
    }
    
    setLoadingSuburbs(true);
    try {
      const base = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/v1";
      const response = await fetch(`${base}/suburbs-list/${state}`);
      if (response.ok) {
        const data = await response.json();
        setAvailableSuburbs(data.suburbs || []);
      } else {
        setAvailableSuburbs(SUBURBS_BY_STATE[state as keyof typeof SUBURBS_BY_STATE] || []);
      }
    } catch (error) {
      console.error("Error fetching suburbs:", error);
      setAvailableSuburbs(SUBURBS_BY_STATE[state as keyof typeof SUBURBS_BY_STATE] || []);
    } finally {
      setLoadingSuburbs(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedCategory || !selectedState || !selectedSuburb || !userQuery.trim()) {
      alert("Please fill in all fields");
      return;
    }

    setIsLoading(true);
    
    const fullQuery = `Category: ${selectedCategory}, Location: ${selectedSuburb}, ${selectedState}, Query: ${userQuery}`;
    
    const params = new URLSearchParams({
      category: selectedCategory,
      state: selectedState,
      suburb: selectedSuburb,
      user_query: userQuery,
      fullQuery: fullQuery
    });
    
    router.push(`/results?${params.toString()}`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              GovMate AI Assistant
            </h1>
            <p className="text-lg text-gray-600">
              Your intelligent guide to Australian government services
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 px-8 py-6">
            <h2 className="text-2xl font-bold text-white mb-2">
              How can we help you today?
            </h2>
            <p className="text-blue-100">
              Select a category and tell us about your specific needs
            </p>
          </div>

          <form onSubmit={handleSubmit} className="p-8 space-y-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-3">
                What type of service do you need?
              </label>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {CATEGORIES.map((category) => (
                  <button
                    key={category.id}
                    type="button"
                    onClick={() => setSelectedCategory(category.id)}
                    className={`p-4 rounded-xl border-2 transition-all duration-200 text-left ${
                      selectedCategory === category.id
                        ? "border-blue-500 bg-blue-50 shadow-md"
                        : "border-gray-200 hover:border-gray-300 hover:shadow-sm"
                    }`}
                  >
                    <div className="flex items-center space-x-3">
                      <span className="text-2xl">{category.icon}</span>
                      <div>
                        <h3 className="font-semibold text-gray-900">{category.name}</h3>
                        <p className="text-sm text-gray-600">{category.description}</p>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  State or Territory
                </label>
                <select
                  value={selectedState}
                  onChange={(e) => {
                    setSelectedState(e.target.value);
                    setSelectedSuburb("");
                    fetchSuburbs(e.target.value);
                  }}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Select your state or territory</option>
                  {STATES.map((state) => (
                    <option key={state.id} value={state.id}>
                      {state.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  City or Suburb
                </label>
                <select
                  value={selectedSuburb}
                  onChange={(e) => setSelectedSuburb(e.target.value)}
                  disabled={!selectedState || loadingSuburbs}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                >
                  <option value="">
                    {!selectedState ? "Select state first" :
                     loadingSuburbs ? "Loading suburbs..." :
                     "Select your city or suburb"}
                  </option>
                  {availableSuburbs.map((suburb) => (
                    <option key={suburb} value={suburb}>
                      {suburb}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Tell us about your specific needs
              </label>
              <textarea
                value={userQuery}
                onChange={(e) => setUserQuery(e.target.value)}
                placeholder="e.g., I need help finding student accommodation, I'm looking for job assistance, I need information about public transport options..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                rows={4}
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-4 px-6 rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
            >
              {isLoading ? "Processing..." : "Get AI-Powered Assistance"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}