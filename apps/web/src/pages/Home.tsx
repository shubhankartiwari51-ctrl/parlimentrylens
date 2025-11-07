import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { ScanText, Youtube, Newspaper, Clapperboard, ArrowRight } from "lucide-react";

// Data for our tool cards
const tools = [
  {
    title: "Analyze Text",
    description: "Paste speeches, articles, or any text to get sentiment & summary.",
    icon: ScanText,
    path: "/text",
    color: "from-purple-500 to-indigo-500",
    comingSoon: false,
  },
  {
    title: "Analyze YouTube",
    description: "Get summaries and sentiment from any YouTube video link.",
    icon: Youtube,
    path: "/youtube",
    color: "from-red-500 to-pink-500",
    comingSoon: false,
  },
  {
    title: "Scan Newspaper",
    description: "Upload an image of a newspaper to extract and analyze its content.",
    icon: Newspaper,
    path: "/newspaper",
    color: "from-blue-500 to-cyan-500",
    comingSoon: true,
  },
  {
    title: "Analyze Reels/Shorts",
    description: "Analyze subtitles and content from short videos and reels.",
    icon: Clapperboard,
    path: "/reels",
    color: "from-green-500 to-teal-500",
    comingSoon: true,
  },
];

export default function Home() {
  const navigate = useNavigate();

  return (
    <motion.div
      className="flex w-full max-w-4xl flex-col items-center justify-center text-center"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
    >
      <h1 className="mb-4 bg-gradient-to-r from-purple-300 to-indigo-300 bg-clip-text text-5xl font-bold text-transparent">
        ParliamentLens AI Toolkit
      </h1>
      <p className="mb-12 max-w-2xl text-lg text-purple-200">
        Select a tool to begin your analysis. Empowering awareness, one
        analysis at a time.
      </p>

      {/* --- This is the "Busy Section" Grid --- */}
      <div className="grid w-full grid-cols-1 gap-8 md:grid-cols-2">
        {tools.map((tool) => (
          <motion.div
            key={tool.title}
            className={`group relative cursor-pointer overflow-hidden rounded-3xl border border-white/10 bg-black/20 p-8 text-left shadow-xl backdrop-blur-lg ${
              tool.comingSoon
                ? "opacity-60 grayscale"
                : "hover:border-white/30"
            }`}
            onClick={() => !tool.comingSoon && navigate(tool.path)}
            whileHover={{ scale: tool.comingSoon ? 1 : 1.03 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            {/* Coming Soon Badge */}
            {tool.comingSoon && (
              <span className="absolute top-4 right-4 rounded-full bg-yellow-500/20 px-3 py-1 text-xs font-medium text-yellow-300">
                Coming Soon
              </span>
            )}
            
            {/* Card Icon */}
            <div
              className={`flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-r ${tool.color} text-white`}
            >
              <tool.icon className="h-6 w-6" />
            </div>
            
            {/* Card Content */}
            <h2 className="mt-4 mb-2 text-2xl font-semibold text-white">
              {tool.title}
            </h2>
            <p className="text-purple-200">{tool.description}</p>
            
            {/* Arrow on Hover (if not disabled) */}
            {!tool.comingSoon && (
              <ArrowRight className="absolute bottom-8 right-8 h-6 w-6 text-purple-300 opacity-0 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-1" />
            )}
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}