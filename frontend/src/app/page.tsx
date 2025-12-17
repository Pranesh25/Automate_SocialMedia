"use client";

import PostCreator from "@/components/PostCreator";
import PostList from "@/components/PostList";
import Settings from "@/components/Settings";
import { useState } from "react";
import { LayoutDashboard, PenSquare, Settings as SettingsIcon, Share2, Menu } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function Home() {
  const [refreshKey, setRefreshKey] = useState(0);
  const [currentView, setCurrentView] = useState("create");

  return (
    <div className="min-h-screen flex flex-col md:flex-row bg-zinc-950 text-zinc-100 font-sans selection:bg-zinc-800">
      {/* Desktop Sidebar */}
      <aside className="w-64 border-r border-zinc-800 bg-zinc-950 hidden md:flex flex-col p-6 fixed h-full z-10">
        <div className="flex items-center gap-3 mb-10 px-2">
          <div className="w-8 h-8 bg-zinc-100 rounded-lg flex items-center justify-center font-bold text-black shadow-lg shadow-white/10">
            B
          </div>
          <h1 className="text-lg font-bold tracking-tight text-white">Blur Social</h1>
        </div>

        <nav className="space-y-1 flex-1">
          <NavItem
            icon={<PenSquare size={18} />}
            label="Create Post"
            active={currentView === "create"}
            onClick={() => setCurrentView("create")}
          />
          <NavItem
            icon={<LayoutDashboard size={18} />}
            label="Dashboard"
            onClick={() => setCurrentView("create")}
          />
          <NavItem icon={<Share2 size={18} />} label="Automation" />
        </nav>

        <div className="mt-auto pt-6 border-t border-zinc-800">
          <NavItem
            icon={<SettingsIcon size={18} />}
            label="Settings"
            active={currentView === "settings"}
            onClick={() => setCurrentView("settings")}
          />
        </div>
      </aside>

      {/* Mobile Header */}
      <div className="md:hidden flex items-center justify-between p-4 border-b border-zinc-800 bg-zinc-950 sticky top-0 z-20">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center font-bold text-black">
            B
          </div>
          <span className="font-bold text-white">Blur Social</span>
        </div>
        <button
          onClick={() => setCurrentView("settings")}
          className="p-2 rounded-full hover:bg-zinc-800 transition-colors text-zinc-400 hover:text-white"
        >
          <SettingsIcon size={20} />
        </button>
      </div>

      {/* Main Content */}
      <main className="flex-1 md:ml-64 p-4 md:p-12 pb-24 md:pb-12 min-h-screen bg-zinc-950">
        <div className="max-w-5xl mx-auto">
          <header className="mb-8 md:mb-12 flex flex-col md:flex-row md:justify-between md:items-center gap-4">
            <div>
              <motion.h1
                key={currentView}
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-3xl font-bold mb-2 text-white tracking-tight"
              >
                {currentView === "create" ? "Create Content" : "Settings"}
              </motion.h1>
              <p className="text-zinc-400 text-sm">
                {currentView === "create"
                  ? "Draft your next viral post for all platforms."
                  : "Manage your API credentials securely."}
              </p>
            </div>

            {/* Desktop Header Actions */}
            <div className="hidden md:flex items-center gap-4">
              <button
                onClick={() => setCurrentView("settings")}
                className="p-2.5 rounded-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 transition-all hover:border-zinc-700 group"
                title="Settings"
              >
                <SettingsIcon size={18} className="text-zinc-400 group-hover:text-white transition-colors" />
              </button>
              <div className="w-9 h-9 rounded-full bg-zinc-800 ring-2 ring-zinc-900 border border-zinc-700" />
            </div>
          </header>

          <AnimatePresence mode="wait">
            {currentView === "create" ? (
              <motion.div
                key="create"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ duration: 0.2 }}
              >
                <PostCreator onPostCreated={() => setRefreshKey(prev => prev + 1)} />
                <div className="mt-16">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-lg font-bold text-white">Recent Drafts</h3>
                    <button className="text-xs font-medium text-zinc-500 hover:text-white transition-colors">View All</button>
                  </div>
                  <PostList key={refreshKey} />
                </div>
              </motion.div>
            ) : (
              <motion.div
                key="settings"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.2 }}
              >
                <Settings />
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>

      {/* Mobile Bottom Nav */}
      <nav className="md:hidden fixed bottom-0 left-0 w-full bg-zinc-950 border-t border-zinc-800 p-4 flex justify-around items-center z-30 pb-safe">
        <MobileNavItem
          icon={<PenSquare size={24} />}
          label="Create"
          active={currentView === "create"}
          onClick={() => setCurrentView("create")}
        />
        <MobileNavItem
          icon={<LayoutDashboard size={24} />}
          label="Posts"
          active={false}
          onClick={() => setCurrentView("create")}
        />
        <MobileNavItem
          icon={<SettingsIcon size={24} />}
          label="Settings"
          active={currentView === "settings"}
          onClick={() => setCurrentView("settings")}
        />
      </nav>
    </div>
  );
}

function NavItem({ icon, label, active = false, onClick }: { icon: React.ReactNode; label: string; active?: boolean; onClick?: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-all duration-200 group relative ${active
        ? "bg-zinc-900 text-white font-medium shadow-sm border border-zinc-800"
        : "text-zinc-500 hover:bg-zinc-900/50 hover:text-zinc-300"
        }`}
    >
      <span className="relative z-10">{icon}</span>
      <span className="relative z-10 text-sm">{label}</span>
    </button>
  );
}

function MobileNavItem({ icon, label, active = false, onClick }: { icon: React.ReactNode; label: string; active?: boolean; onClick?: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`flex flex-col items-center gap-1 transition-colors ${active ? "text-white" : "text-zinc-600"
        }`}
    >
      {icon}
      <span className="text-[10px] font-medium">{label}</span>
    </button>
  );
}
