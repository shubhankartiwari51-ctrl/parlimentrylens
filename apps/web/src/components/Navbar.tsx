import { NavLink } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ScanText,
  Youtube,
  Newspaper,      // <-- New Icon
  Clapperboard,   // <-- New Icon
  Target,         // <-- New Icon
} from "lucide-react";

// Updated list of links, "Home" is removed
const navLinks = [
  { path: "/text", label: "Analyze Text", Icon: ScanText },
  { path: "/youtube", label: "Analyze YouTube", Icon: Youtube },
  { path: "/newspaper", label: "Scan Article", Icon: Newspaper },
  { path: "/reels", label: "Analyze Reels", Icon: Clapperboard },
  { path: "/mission", label: "Our Mission", Icon: Target },
];

export default function Navbar() {
  return (
    <nav className="fixed top-6 left-1/2 z-50 -translate-x-1/2">
      <div className="flex items-center gap-6 rounded-full border border-white/20 bg-black/20 p-3 shadow-2xl backdrop-blur-lg">
        {/* Logo (Links to Home Hub) */}
        <NavLink
          to="/"
          className="ml-2 mr-2 flex items-center gap-2"
          style={{ textDecoration: "none" }}
        >
          <span className="text-xl font-bold tracking-wide text-purple-300">
            ⚡
          </span>
          <span className="bg-gradient-to-r from-purple-300 to-indigo-300 bg-clip-text text-xl font-bold text-transparent">
            ParliamentLens
          </span>
        </NavLink>

        {/* Navigation Links with Animated Pill */}
        <div className="flex items-center gap-2 rounded-full bg-white/10 px-3 py-1">
          {navLinks.map(({ path, label, Icon }) => (
            <NavLink
              key={path}
              to={path}
              className={({ isActive }) =>
                `relative z-10 flex items-center gap-2 rounded-full px-5 py-2.5 text-sm font-medium transition-colors duration-300
                ${
                  isActive
                    ? "text-white"
                    : "text-purple-200 hover:text-white"
                }`
              }
            >
              {({ isActive }) => (
                <>
                  {/* This span guarantees text/icon is on top of the pill */}
                  <span className="relative z-10 flex items-center gap-2">
                    <Icon className="h-5 w-5" />
                    <span>{label}</span>
                  </span>
                  
                  {isActive && (
                    <motion.div
                      layoutId="active-pill"
                      className="absolute inset-0 z-0 rounded-full bg-gradient-to-r from-purple-500 to-indigo-500 shadow-lg"
                      transition={{
                        type: "spring",
                        stiffness: 300,
                        damping: 30,
                      }}
                    ></motion.div>
                  )}
                </>
              )}
            </NavLink>
          ))}
        </div>
      </div>
    </nav>
  );
}