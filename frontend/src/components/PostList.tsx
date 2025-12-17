"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Share2, Check, Video, Type, Image as ImageIcon } from "lucide-react";
import { cn } from "@/lib/utils";

interface Post {
    id: number;
    title: string;
    description: string;
    type: "text" | "image" | "video";
    media_path: string | null;
    status: string;
}

export default function PostList() {
    const [posts, setPosts] = useState<Post[]>([]);
    const [loading, setLoading] = useState(true);
    const [publishing, setPublishing] = useState<number | null>(null);

    const [settings, setSettings] = useState<any>(null);

    const fetchPosts = async () => {
        try {
            const res = await fetch("http://localhost:8000/posts/");
            const data = await res.json();
            setPosts(data.reverse()); // Show newest first
        } catch (error) {
            console.error("Failed to fetch posts", error);
        } finally {
            setLoading(false);
        }
    };

    const fetchSettings = async () => {
        try {
            const res = await fetch("http://localhost:8000/settings/");
            if (res.ok) {
                setSettings(await res.json());
            }
        } catch (error) {
            console.error("Failed to fetch settings", error);
        }
    };

    useEffect(() => {
        fetchPosts();
        fetchSettings();
    }, []);

    const handlePublishReddit = async (post: Post) => {
        const s = settings || {};

        let clientId = s.reddit_client_id;
        if (!clientId) clientId = prompt("Enter Reddit Client ID:");
        if (!clientId) return;

        let clientSecret = s.reddit_client_secret;
        if (!clientSecret) clientSecret = prompt("Enter Reddit Client Secret:");
        if (!clientSecret) return;

        let username = s.reddit_username;
        if (!username) username = prompt("Enter Reddit Username:");
        if (!username) return;

        let password = s.reddit_password;
        if (!password) password = prompt("Enter Reddit Password:");
        if (!password) return;

        let subreddit = s.reddit_default_subreddit;
        if (!subreddit) subreddit = prompt("Enter Subreddit (e.g. test):", "test");
        if (!subreddit) return;

        setPublishing(post.id);

        try {
            const res = await fetch(`http://localhost:8000/publish/reddit/${post.id}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    client_id: clientId,
                    client_secret: clientSecret,
                    username,
                    password,
                    subreddit,
                }),
            });

            if (res.ok) {
                alert("Published to Reddit successfully!");
                fetchPosts(); // Refresh status
            } else {
                const err = await res.json();
                alert(`Failed: ${err.detail}`);
            }
        } catch (error) {
            alert("Error publishing");
        } finally {
            setPublishing(null);
        }
    };

    const handlePublishTwitter = async (post: Post) => {
        const s = settings || {};

        let username = s.twitter_username;
        if (!username) username = prompt("Enter X (Twitter) Username:");
        if (!username) return;

        let password = s.twitter_password;
        if (!password) password = prompt("Enter X (Twitter) Password:");
        if (!password) return;

        let email = s.twitter_email;
        if (!email && !s.twitter_username) email = prompt("Enter Email (Optional, for verification):");

        setPublishing(post.id);

        try {
            const res = await fetch(`http://localhost:8000/publish/twitter/${post.id}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    username,
                    password,
                    email: email || undefined,
                }),
            });

            if (res.ok) {
                alert("Published to X (Twitter) successfully!");
                fetchPosts();
            } else {
                const err = await res.json();
                alert(`Failed: ${err.detail}`);
            }
        } catch (error) {
            alert("Error publishing");
        } finally {
            setPublishing(null);
        }
    };

    if (loading) return <div className="text-center text-gray-500 mt-10">Loading posts...</div>;

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {posts.map((post) => (
                <motion.div
                    key={post.id}
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="bg-zinc-900 border border-zinc-800 rounded-2xl overflow-hidden hover:border-zinc-700 transition-all group flex flex-col"
                >
                    {/* Media Preview */}
                    <div className="h-48 bg-zinc-950 relative overflow-hidden border-b border-zinc-800/50">
                        {post.media_path ? (
                            post.type === "image" ? (
                                <img src={`http://localhost:8000/media/${post.media_path.split("\\").pop()?.split("/").pop()}`} alt={post.title} className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
                            ) : (
                                <video src={`http://localhost:8000/media/${post.media_path.split("\\").pop()?.split("/").pop()}`} className="w-full h-full object-cover" />
                            )
                        ) : (
                            <div className="w-full h-full flex items-center justify-center text-zinc-700">
                                <Type size={48} className="opacity-20" />
                            </div>
                        )}
                        <div className="absolute top-3 right-3">
                            <span className={cn(
                                "px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider backdrop-blur-md border",
                                post.status === "draft"
                                    ? "bg-zinc-800/80 text-zinc-400 border-zinc-700"
                                    : "bg-green-500/10 text-green-400 border-green-500/20"
                            )}>
                                {post.status}
                            </span>
                        </div>
                        <div className="absolute top-3 left-3">
                            <div className="w-8 h-8 rounded-full bg-black/40 backdrop-blur-sm flex items-center justify-center text-white border border-white/10">
                                {post.type === "text" && <Type size={14} />}
                                {post.type === "image" && <ImageIcon size={14} />}
                                {post.type === "video" && <Video size={14} />}
                            </div>
                        </div>
                    </div>

                    {/* Content */}
                    <div className="p-5 flex-1 flex flex-col">
                        <h3 className="text-lg font-bold text-zinc-100 mb-2 line-clamp-1">{post.title}</h3>
                        <p className="text-zinc-400 text-sm line-clamp-2 mb-6 h-10 leading-relaxed">{post.description}</p>

                        <div className="mt-auto flex gap-2 pt-4 border-t border-zinc-800/50">
                            <button
                                onClick={() => handlePublishReddit(post)}
                                disabled={publishing === post.id}
                                className="flex-1 bg-zinc-800 hover:bg-[#FF4500] hover:text-white text-zinc-400 py-2.5 rounded-lg font-medium text-xs transition-all flex items-center justify-center gap-2 disabled:opacity-50 group/btn"
                            >
                                {publishing === post.id ? (
                                    <div className="w-3 h-3 border-2 border-white/50 border-t-white rounded-full animate-spin" />
                                ) : (
                                    <>
                                        <Share2 size={14} className="group-hover/btn:scale-110 transition-transform" />
                                        Reddit
                                    </>
                                )}
                            </button>
                            <button
                                onClick={() => handlePublishTwitter(post)}
                                disabled={publishing === post.id}
                                className="flex-1 bg-zinc-800 hover:bg-black hover:text-white text-zinc-400 py-2.5 rounded-lg font-medium text-xs transition-all flex items-center justify-center gap-2 disabled:opacity-50 group/btn"
                            >
                                {publishing === post.id ? (
                                    <div className="w-3 h-3 border-2 border-white/50 border-t-white rounded-full animate-spin" />
                                ) : (
                                    <>
                                        <Share2 size={14} className="group-hover/btn:scale-110 transition-transform" />
                                        X
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                </motion.div>
            ))}
        </div>
    );
}
