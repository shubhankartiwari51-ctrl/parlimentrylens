import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Newspaper, // <-- New Icon
  ArrowRight,
  Smile,
  Meh,
  Frown,
  ScrollText,
  AlertTriangle,
  Loader2,
  Target,
  UploadCloud, // <-- New Icon
  X, // <-- New Icon
} from "lucide-react";

// --- Type (Same as other pages) ---
type AnalysisResult = {
  sentiment: { label: "POSITIVE" | "NEGATIVE" | "NEUTRAL"; score: number };
  summary: string;
  key_topics: { label: string; score: number }[];
};

// --- All Helper Components (Copied from other pages) ---

const LoadingSpinner = () => <Loader2 className="h-5 w-5 animate-spin text-white" />;

const LoadingSkeleton = () => (
  <div className="mt-8 space-y-6">
    <div className="space-y-3"><div className="h-5 w-1/3 rounded-lg bg-white/20" /><div className="h-8 w-1/2 rounded-lg bg-white/20" /></div>
    <div className="space-y-3"><div className="h-5 w-1/4 rounded-lg bg-white/20" /><div className="h-32 w-full rounded-lg bg-white/20" /></div>
    <div className="absolute inset-0 -translate-x-full animate-shimmer rounded-3xl" />
  </div>
);

const StreamingSummary = ({ text }: { text: string }) => {
  const [displayedText, setDisplayedText] = useState("");
  const [isDone, setIsDone] = useState(false);
  useEffect(() => {
    setDisplayedText(""); setIsDone(false);
    let index = 0;
    const interval = setInterval(() => {
      if (index < text.length) {
        const chunk = text.substring(index, index + 5);
        setDisplayedText((prev) => prev + chunk);
        index += 5;
      } else {
        clearInterval(interval); setIsDone(true);
      }
    }, 15);
    return () => clearInterval(interval);
  }, [text]);
  return (
    <p className="mt-4 leading-relaxed text-purple-100">
      {displayedText}
      {!isDone && (<span className="inline-block w-2 h-5 bg-purple-300 animate-pulse ml-1" />)}
    </p>
  );
};

const ResultDisplay = ({ result }: { result: AnalysisResult }) => {
  const { sentiment, summary, key_topics } = result;
  const cfg =
    {
      POSITIVE: { Icon: Smile, color: "text-green-400", bg: "bg-green-500/10", br: "border-green-500/30" },
      NEUTRAL: { Icon: Meh, color: "text-yellow-400", bg: "bg-yellow-500/10", br: "border-yellow-500/30" },
      NEGATIVE: { Icon: Frown, color: "text-red-400", bg: "bg-red-500/10", br: "border-red-500/30" },
    }[sentiment.label] || { Icon: Meh, color: "text-gray-400", bg: "bg-gray-500/10", br: "border-gray-500/30" };

  return (
    <motion.div className="mt-8 space-y-6" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
      <motion.div className={`overflow-hidden rounded-3xl ${cfg.bg} border ${cfg.br} p-6 shadow-inner`} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 }}>
        <div className="flex items-center gap-3"><cfg.Icon className={`h-8 w-8 ${cfg.color}`} /><h2 className="text-2xl font-semibold text-white">Sentiment</h2></div>
        <div className="mt-4 flex items-baseline gap-2"><span className={`text-3xl font-bold ${cfg.color}`}>{sentiment.label}</span><span className="text-xl text-purple-200">({(sentiment.score * 100).toFixed(1)}%)</span></div>
      </motion.div>
      <motion.div className="overflow-hidden rounded-3xl bg-white/10 p-6 shadow-inner" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.4 }}>
        <div className="flex items-center gap-3"><Target className="h-8 w-8 text-purple-300" /><h2 className="text-2xl font-semibold text-white">Key Topics</h2></div>
        <div className="mt-4 flex flex-wrap gap-2">
          {key_topics.length > 0 ? (
            key_topics.map((topic) => (<span key={topic.label} className="rounded-full bg-purple-500/30 px-3 py-1 text-sm font-medium text-purple-200">{topic.label}</span>))
          ) : (<p className="text-purple-200/70">No specific topics detected.</p>)}
        </div>
      </motion.div>
      <motion.div className="overflow-hidden rounded-3xl bg-white/10 p-6 shadow-inner" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.6 }}>
        <div className="flex items-center gap-3"><ScrollText className="h-8 w-8 text-purple-300" /><h2 className="text-2xl font-semibold text-white">Summary</h2></div>
        <StreamingSummary text={summary} />
      </motion.div>
    </motion.div>
  );
};

// --- Main Component ---
export default function AnalyzeNewspaper() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Create image preview
  useEffect(() => {
    if (!file) {
      setPreview(null);
      return;
    }
    const objectUrl = URL.createObjectURL(file);
    setPreview(objectUrl);
    // Free memory when component unmounts
    return () => URL.revokeObjectURL(objectUrl);
  }, [file]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
      setResult(null);
    }
  };

  const handleAnalyze = async () => {
    if (!file || loading) return;
    setLoading(true);
    setResult(null);
    setError(null);

    // Must use FormData for file uploads
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8001/newspaper/analyze", {
        method: "POST",
        // DO NOT set Content-Type header, browser does it
        body: formData,
      });
      if (!res.ok) {
        let detail = `Server Error: ${res.status}`;
        try { const data = await res.json(); detail = data.detail || detail; } catch {}
        throw new Error(detail);
      }
      const data = await res.json();
      setResult(data);
    } catch (e: any) {
      setError(e.message || "Failed to analyze image.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div className="relative w-full max-w-2xl overflow-hidden rounded-3xl bg-black/20 p-8 shadow-2xl backdrop-blur-lg" initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.5 }}>
      <div className="flex items-center justify-center gap-3">
        <Newspaper className="h-8 w-8 text-purple-300" />
        <h1 className="bg-gradient-to-r from-purple-300 to-indigo-300 bg-clip-text text-3xl font-bold text-transparent">Newspaper Article Analyzer</h1>
      </div>

      {/* --- Image Uploader --- */}
      <div className="mt-8">
        {!preview ? (
          <label htmlFor="file-upload" className="flex flex-col items-center justify-center w-full h-48 border-2 border-purple-500/30 border-dashed rounded-xl cursor-pointer bg-white/10 hover:bg-white/20 transition-colors">
            <div className="flex flex-col items-center justify-center pt-5 pb-6">
              <UploadCloud className="w-10 h-10 mb-3 text-purple-300/70" />
              <p className="mb-2 text-sm text-purple-200/70"><span className="font-semibold">Click to upload</span> or drag and drop</p>
              <p className="text-xs text-purple-300/60">PNG, JPG, or GIF</p>
            </div>
            <input id="file-upload" type="file" className="hidden" onChange={handleFileChange} accept="image/png, image/jpeg, image/gif" />
          </label>
        ) : (
          // --- Image Preview ---
          <div className="relative w-full h-48 rounded-xl overflow-hidden border border-purple-500/30">
            <img src={preview} alt="Upload preview" className="w-full h-full object-contain" />
            <button
              onClick={() => { setFile(null); setPreview(null); }}
              className="absolute top-2 right-2 p-1.5 bg-black/50 rounded-full text-white/70 hover:text-white hover:bg-black/70 transition-all"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        )}
      </div>

      {/* --- Analyze Button --- */}
      <div className="mt-6 flex justify-center">
        <motion.button onClick={handleAnalyze} disabled={loading || !file} className="group relative flex w-full max-w-xs items-center justify-center rounded-xl bg-gradient-to-r from-purple-500 to-indigo-500 px-8 py-4 text-lg font-semibold text-white shadow-lg disabled:cursor-not-allowed disabled:opacity-50" whileHover={{ scale: loading ? 1 : 1.03 }} whileTap={{ scale: loading ? 1 : 0.98 }}>
          {loading ? (<><LoadingSpinner /><span className="ml-2">Scanning...</span></>) : (<><span>Scan Image</span><ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" /></>)}
        </motion.button>
      </div>

      {/* --- Result Section --- */}
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