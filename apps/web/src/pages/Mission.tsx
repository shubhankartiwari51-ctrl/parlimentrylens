import { motion } from "framer-motion";
import { ScanText, Youtube, Target } from "lucide-react";

// Animation variants for staggering items
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
} as const; // <-- FIX 1: Added 'as const'

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { type: "spring", stiffness: 100 },
  },
} as const; // <-- FIX 1: Added 'as const'

export default function Mission() {
  return (
    <motion.div
      className="flex w-full max-w-4xl flex-col items-center justify-center text-center"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* --- 1. Social Impact / Motivation Section --- */}
      <motion.div
        variants={itemVariants}
        className="w-full rounded-3xl border border-white/10 bg-black/20 p-8 shadow-xl backdrop-blur-lg"
      >
        <div className="flex flex-col items-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-r from-purple-500 to-indigo-500 text-white">
            <Target className="h-6 w-6" />
          </div>
          <h1 className="mt-4 mb-4 text-5xl font-bold text-white">
            Our Mission
          </h1>
          <p className="max-w-3xl text-lg leading-relaxed text-purple-200">
            In an age of information overload, understanding political discourse
            is vital. ParliamentLens provides unbiased, AI-driven tools to help
            citizens, journalists, and researchers quickly analyze and
            comprehend complex topics.
          </p>
          <p className="mt-4 max-w-3xl text-lg leading-relaxed text-purple-200">
            By making political media more accessible and transparent, we aim to
            foster a more informed and engaged public.
          </p>
        </div>
      </motion.div>

      {/* --- 2. "What We Do" Features Section --- */}
      <motion.div
        variants={itemVariants}
        className="mt-16 grid w-full grid-cols-1 gap-8 md:grid-cols-2"
      >
        {/* Feature Card: Text */}
        <div className="rounded-3xl border border-white/10 bg-black/20 p-8 shadow-xl backdrop-blur-lg">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-r from-purple-500 to-indigo-500 text-white">
            <ScanText className="h-6 w-6" />
          </div>
          <h2 className="mt-4 mb-2 text-2xl font-semibold text-white">
            AI-Powered Text Analysis
          </h2>
          <p className="text-purple-200">
            Paste any text—like a speech or news article—to instantly get an
            unbiased sentiment score and a concise summary.
          </p>
        </div>

        {/* Feature Card: YouTube */}
        <div className="rounded-3xl border border-white/10 bg-black/20 p-8 shadow-xl backdrop-blur-lg">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-r from-purple-500 to-indigo-500 text-white">
            <Youtube className="h-6 w-6" />
          </div>
          <h2 className="mt-4 mb-2 text-2xl font-semibold text-white">
            YouTube Video Insights
          </h2>
          <p className="text-purple-200">
            Got a long video? Just paste the YouTube link. Our AI will analyze
            the transcript and give you the key points and overall tone.
          </p>
        </div>
      </motion.div>
    </motion.div>
  );
}
// <-- FIX 2: Removed the extra text and '}' from here.