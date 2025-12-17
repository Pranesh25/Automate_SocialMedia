"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Save, Lock, User, Key, Mail, Hash, Shield } from "lucide-react";

export default function Settings() {
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [settings, setSettings] = useState({
        reddit_client_id: "",
        reddit_client_secret: "",
        reddit_username: "",
        reddit_password: "",
        reddit_default_subreddit: "",
        twitter_username: "",
        twitter_password: "",
        twitter_email: "",
    });

    useEffect(() => {
        fetch("http://localhost:8000/settings/")
            .then((res) => res.json())
            .then((data) => {
                const safeData = { ...data };
                Object.keys(safeData).forEach(key => {
                    if (safeData[key] === null) safeData[key] = "";
                });
                setSettings(safeData);
                setLoading(false);
            })
            .catch((err) => {
                console.error("Failed to fetch settings", err);
                setLoading(false);
            });
    }, []);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSettings({ ...settings, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setSaving(true);
        try {
            const res = await fetch("http://localhost:8000/settings/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(settings),
            });
            if (res.ok) {
                const btn = document.getElementById("save-settings-btn");
                if (btn) {
                    btn.innerText = "Saved Successfully!";
                    btn.classList.add("bg-green-500", "text-white");
                    btn.classList.remove("bg-white", "text-black");
                }
                setTimeout(() => {
                    if (btn) {
                        btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-save"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg> Save Settings';
                        btn.classList.remove("bg-green-500", "text-white");
                        btn.classList.add("bg-white", "text-black");
                    }
                }, 2000);
            } else {
                alert("Failed to save settings.");
            }
        } catch (error) {
            alert("Error saving settings.");
        } finally {
            setSaving(false);
        }
    };

    if (loading) return (
        <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
        </div>
    );

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="w-full max-w-4xl mx-auto"
        >
            <div className="bg-black rounded-3xl p-8 md:p-10 border border-white/20 relative overflow-hidden">

                <div className="flex items-center gap-4 mb-8">
                    <div className="p-3 bg-white text-black rounded-2xl">
                        <Lock className="w-6 h-6" />
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold text-white">API Configuration</h2>
                        <p className="text-gray-400 text-sm">Securely manage your social media credentials</p>
                    </div>
                </div>

                <form onSubmit={handleSubmit} className="space-y-10">
                    {/* Reddit Section */}
                    <div className="space-y-6">
                        <div className="flex items-center gap-3 border-b border-white/20 pb-4">
                            <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center text-black font-bold text-xs">
                                r/
                            </div>
                            <h3 className="text-lg font-bold text-white">Reddit Integration</h3>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <Input
                                label="Client ID"
                                name="reddit_client_id"
                                value={settings.reddit_client_id}
                                onChange={handleChange}
                                icon={<Shield size={16} />}
                                placeholder="e.g. 8k3...123"
                            />
                            <Input
                                label="Client Secret"
                                name="reddit_client_secret"
                                value={settings.reddit_client_secret}
                                onChange={handleChange}
                                type="password"
                                icon={<Key size={16} />}
                                placeholder="••••••••••••••••"
                            />
                            <Input
                                label="Username"
                                name="reddit_username"
                                value={settings.reddit_username}
                                onChange={handleChange}
                                icon={<User size={16} />}
                                placeholder="RedditUser123"
                            />
                            <Input
                                label="Password"
                                name="reddit_password"
                                value={settings.reddit_password}
                                onChange={handleChange}
                                type="password"
                                icon={<Lock size={16} />}
                                placeholder="••••••••"
                            />
                            <Input
                                label="Default Subreddit"
                                name="reddit_default_subreddit"
                                value={settings.reddit_default_subreddit}
                                onChange={handleChange}
                                icon={<Hash size={16} />}
                                placeholder="test"
                            />
                        </div>
                    </div>

                    {/* Twitter Section */}
                    <div className="space-y-6">
                        <div className="flex items-center gap-3 border-b border-white/20 pb-4">
                            <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center text-black font-bold text-xs">
                                X
                            </div>
                            <h3 className="text-lg font-bold text-white">X (Twitter) Integration</h3>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <Input
                                label="Username"
                                name="twitter_username"
                                value={settings.twitter_username}
                                onChange={handleChange}
                                icon={<User size={16} />}
                                placeholder="@username"
                            />
                            <Input
                                label="Password"
                                name="twitter_password"
                                value={settings.twitter_password}
                                onChange={handleChange}
                                type="password"
                                icon={<Key size={16} />}
                                placeholder="••••••••"
                            />
                            <Input
                                label="Email (Optional)"
                                name="twitter_email"
                                value={settings.twitter_email}
                                onChange={handleChange}
                                icon={<Mail size={16} />}
                                placeholder="user@example.com"
                            />
                        </div>
                    </div>

                    <div className="flex justify-end pt-6 border-t border-white/20">
                        <button
                            id="save-settings-btn"
                            type="submit"
                            disabled={saving}
                            className="bg-white text-black font-bold py-4 px-10 rounded-full shadow-lg hover:scale-105 transition-all duration-300 flex items-center gap-2 disabled:opacity-70 disabled:hover:scale-100"
                        >
                            {saving ? (
                                <>
                                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-black"></div>
                                    Saving...
                                </>
                            ) : (
                                <>
                                    <Save size={18} />
                                    Save Settings
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </motion.div>
    );
}

function Input({ label, name, value, onChange, type = "text", icon, placeholder }: any) {
    return (
        <div className="space-y-2 group">
            <label className="text-xs font-semibold text-white uppercase tracking-wider ml-1">
                {label}
            </label>
            <div className="relative">
                <div className="absolute left-4 top-1/2 -translate-y-1/2 text-black/50">
                    {icon}
                </div>
                <input
                    type={type}
                    name={name}
                    value={value || ""}
                    onChange={onChange}
                    placeholder={placeholder}
                    className="w-full bg-white border border-transparent rounded-xl pl-12 pr-4 py-4 focus:outline-none focus:ring-2 focus:ring-gray-300 transition-all text-black placeholder:text-gray-400"
                />
            </div>
        </div>
    );
}
