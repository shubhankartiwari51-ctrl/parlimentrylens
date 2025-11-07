import { Github, Mail } from "lucide-react";

export default function Footer() {
  return (
    // --- THIS IS THE FIX ---
    // This makes the footer container 95% wide and centers it.
    // It's no longer full-width.
    <footer className="w-[95%] mx-auto mt-12 mb-6">
      
      {/* We use the same blurred card style as the main content 
        for a consistent, premium feel.
      */}
      <div className="rounded-3xl border border-white/10 bg-black/20 p-6 text-center shadow-2xl backdrop-blur-lg">
        {/* Gradient text for the main branding */}
        <h3 className="mb-2 bg-gradient-to-r from-purple-300 to-indigo-300 bg-clip-text text-lg font-semibold text-transparent">
          🌿 ParliamentLens AI
        </h3>

        {/* Subtitle text */}
        <p className="text-sm text-purple-200 max-w-md mx-auto mb-6">
          Analyze political speeches, media, and content using sentiment &
          summarization AI.
        </p>

        {/* Social Links using Lucide icons */}
        <div className="flex justify-center gap-6 mb-6">
          <a
            href="https://github.com/prabhankart"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="GitHub Profile"
            className="text-purple-300 transition-all duration-300 hover:scale-110 hover:text-white"
          >
            <Github className="h-6 w-6" />
          </a>
          <a
            href="mailto:prabhankar.tiwari@example.com"
            aria-label="Send Email"
            className="text-purple-300 transition-all duration-300 hover:scale-110 hover:text-white"
          >
            <Mail className="h-6 w-6" />
          </a>
        </div>

        {/* Copyright text, made subtle */}
        <p className="text-xs text-purple-300/60">
          © {new Date().getFullYear()} ParliamentLens. Built with 💙 by
          Prabhankar Tiwari.
        </p>
      </div>
    </footer>
  );
}