import { useState, useEffect } from "react"; // <-- Import useEffect
import { motion, AnimatePresence } from "framer-motion";
import {
  ScanText,
  ArrowRight,
  Smile,
  Meh,
  Frown,
  ScrollText,
  AlertTriangle,
  Loader2,
  Target, // <-- Added Target icon for topics
} from "lucide-react";

// --- UPDATED TYPE ---
// Now includes key_topics from your new "strong" backend
type AnalysisResult = {
  sentiment: { label: "POSITIVE" | "NEGATIVE" | "NEUTRAL"; score: number };
  summary: string;
  key_topics: { label: string; score: number }[];
};

// --- Helper Components ---

const LoadingSpinner = () => (
  <Loader2 className="h-5 w-5 animate-spin text-white" />
);

const LoadingSkeleton = () => (
  <div className="mt-8 space-y-6">
    <div className="space-y-3">
      <div className="h-5 w-1/3 rounded-lg bg-white/20" />
      <div className="h-8 w-1/2 rounded-lg bg-white/20" />
    </div>
    <div className="space-y-3">
      <div className="h-5 w-1/4 rounded-lg bg-white/20" />
      <div className="h-32 w-full rounded-lg bg-white/20" />
    </div>
    <div className="absolute inset-0 -translate-x-full animate-shimmer rounded-3xl" />
  </div>
);

// --- NEW "STREAMING" COMPONENT ---
// This gives the "typing" effect you wanted
const StreamingSummary = ({ text }: { text: string }) => {
  const [displayedText, setDisplayedText] = useState("");
  const [isDone, setIsDone] = useState(false);

  useEffect(() => {
    setDisplayedText(""); // Reset on new text
    setIsDone(false);

    let index = 0;
    const interval = setInterval(() => {
      if (index < text.length) {
        // "Types" 5 characters at a time for a fast, smooth effect
        const chunk = text.substring(index, index + 5);
        setDisplayedText((prev) => prev + chunk);
        index += 5;
      } else {
        clearInterval(interval);
        setIsDone(true);
      }
    }, 15); // 15ms interval

    return () => clearInterval(interval);
  }, [text]); // Re-run when the 'text' prop changes

  return (
    <p className="mt-4 leading-relaxed text-purple-100">
      {displayedText}
      {/* The "thinking" cursor */}
      {!isDone && (
        <span className="inline-block w-2 h-5 bg-purple-300 animate-pulse ml-1" />
      )}
    </p>
  );
};

// --- UPDATED RESULT DISPLAY ---
// Now shows all three sections: Sentiment, Topics, and Summary
const ResultDisplay = ({ result }: { result: AnalysisResult }) => {
  const { sentiment, summary, key_topics } = result; // Get all 3 props
  const cfg =
    {
      POSITIVE: { Icon: Smile, color: "text-green-400", bg: "bg-green-500/10", br: "border-green-500/30" },
      NEUTRAL: { Icon: Meh, color: "text-yellow-400", bg: "bg-yellow-500/10", br: "border-yellow-500/30" },
      NEGATIVE: { Icon: Frown, color: "text-red-400", bg: "bg-red-500/10", br: "border-red-500/30" },
    }[sentiment.label] || { Icon: Meh, color: "text-gray-400", bg: "bg-gray-500/10", br: "border-gray-500/30" };

  return (
    <motion.div className="mt-8 space-y-6" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
      {/* 1. Sentiment Card (No change) */}
      <motion.div className={`overflow-hidden rounded-3xl ${cfg.bg} border ${cfg.br} p-6 shadow-inner`} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 }}>
        <div className="flex items-center gap-3">
          <cfg.Icon className={`h-8 w-8 ${cfg.color}`} />
          <h2 className="text-2xl font-semibold text-white">Sentiment</h2>
        </div>
        <div className="mt-4 flex items-baseline gap-2">
          <span className={`text-3xl font-bold ${cfg.color}`}>{sentiment.label}</span>
          <span className="text-xl text-purple-200">({(sentiment.score * 100).toFixed(1)}%)</span>
        </div>
      </motion.div>

      {/* 2. NEW Key Topics Card */}
      <motion.div className="overflow-hidden rounded-3xl bg-white/10 p-6 shadow-inner" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.4 }}>
        <div className="flex items-center gap-3">
          <Target className="h-8 w-8 text-purple-300" />
          <h2 className="text-2xl font-semibold text-white">Key Topics</h2>
        </div>
        <div className="mt-4 flex flex-wrap gap-2">
          {key_topics.length > 0 ? (
            key_topics.map((topic) => (
              <span key={topic.label} className="rounded-full bg-purple-500/30 px-3 py-1 text-sm font-medium text-purple-200">
                {topic.label}
              </span>
            ))
          ) : (
            <p className="text-purple-200/70">No specific topics detected.</p>
          )}
        </div>
      </motion.div>

      {/* 3. UPDATED Summary Card (with streaming) */}
      <motion.div className="overflow-hidden rounded-3xl bg-white/10 p-6 shadow-inner" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.6 }}>
        <div className="flex items-center gap-3">
          <ScrollText className="h-8 w-8 text-purple-300" />
          <h2 className="text-2xl font-semibold text-white">Summary</h2>
        </div>
        {/* Use the new streaming component */}
        <StreamingSummary text={summary} />
      </motion.div>
    </motion.div>
  );
};

// --- Main Component (No change needed here) ---
export default function AnalyzeText() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!text.trim() || loading) return;
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const res = await fetch(`${import.meta.env.VITE_AI_BASE}/text/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      if (!res.ok) {
        let detail = `Server Error: ${res.status}`;
        try { const data = await res.json(); detail = data.detail || detail; } catch {}
        throw new Error(detail);
      }
      const data = await res.json();
      setResult(data);
    } catch (e: any) {
      setError(e.message || "Failed to analyze text.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div className="relative w-full max-w-2xl overflow-hidden rounded-3xl bg-black/20 p-8 shadow-2xl backdrop-blur-lg" initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.5 }}>
      <div className="flex items-center justify-center gap-3">
        <ScanText className="h-8 w-8 text-purple-300" />
        <h1 className="bg-gradient-to-r from-purple-300 to-indigo-300 bg-clip-text text-3xl font-bold text-transparent">AI Text Analyzer</h1>
      </div>

      <div className="mt-8">
        <label htmlFor="text-input" className="mb-2 block text-sm font-medium text-purple-200">Enter your text</label>
        <textarea id="text-input" value={text} onChange={(e) => setText(e.target.value)} placeholder="Type or paste your text here…" className="h-48 w-full rounded-xl border border-purple-500/30 bg-white/10 p-4 text-lg text-white placeholder-purple-300/60 focus:border-purple-400 focus:ring-2 focus:ring-purple-400" />
      </div>

      <div className="mt-6 flex justify-center">
        <motion.button onClick={handleAnalyze} disabled={loading || !text.trim()} className="group relative flex w-full max-w-xs items-center justify-center rounded-xl bg-gradient-to-r from-purple-500 to-indigo-500 px-8 py-4 text-lg font-semibold text-white shadow-lg disabled:cursor-not-allowed disabled:opacity-50" whileHover={{ scale: loading ? 1 : 1.03 }} whileTap={{ scale: loading ? 1 : 0.98 }}>
          {loading ? (<><LoadingSpinner /><span className="ml-2">Analyzing...</span></>) : (<><span>Analyze Text</span><ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" /></>)}
        </motion.button>
      </div>

      <div className="relative mt-6 min-h-[150px]">
        <AnimatePresence mode="wait">
          {loading && (<motion.div key="loader" className="relative overflow-hidden" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}><LoadingSkeleton /></motion.div>)}
          {error && (<motion.div key="error" className="mt-8 flex items-center gap-3 rounded-2xl bg-red-500/10 p-4" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
            <AlertTriangle className="h-6 w-6 text-red-400" /><div><h3 className="font-semibold text-red-300">Analysis Failed</h3><p className="text-sm text-red-300/80">{error}</p></div>
          </motion.div>)}
          {result && !loading && (<motion.div key="result" exit={{ opacity: 0 }}><ResultDisplay result={result} /></motion.div>)}
        </AnimatePresence>
      </div>
    </motion.div>
  );
}