"use client";

import { useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
    Image as ImageIcon,
    Video,
    Type,
    X,
    Upload,
    Send,
    Save,
    Eye,
    MoreHorizontal
} from "lucide-react";
import { cn } from "@/lib/utils";

type PostType = "text" | "image" | "video";

interface PostCreatorProps {
    onPostCreated: () => void;
}

export default function PostCreator({ onPostCreated }: PostCreatorProps) {
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [postType, setPostType] = useState<PostType>("text");
    const [file, setFile] = useState<File | null>(null);
    const [previewUrl, setPreviewUrl] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const selectedFile = e.target.files[0];
            setFile(selectedFile);
            setPreviewUrl(URL.createObjectURL(selectedFile));
        }
    };

    const clearMedia = () => {
        setFile(null);
        setPreviewUrl(null);
        if (fileInputRef.current) fileInputRef.current.value = "";
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!title || !description) {
            alert("Please fill in the title and caption.");
            return;
        }

        setIsSubmitting(true);
        const formData = new FormData();
        formData.append("title", title);
        formData.append("description", description);
        formData.append("type", postType);
        if (file) {
            formData.append("file", file);
        }

        try {
            const res = await fetch("http://localhost:8000/posts/", {
                method: "POST",
                body: formData,
            });
            if (res.ok) {
                setTitle("");
                setDescription("");
                setFile(null);
                setPreviewUrl(null);
                onPostCreated();
            } else {
                alert("Failed to save post.");
            }
        } catch (error) {
            console.error("Error saving post:", error);
            alert("Error saving post.");
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full max-w-3xl mx-auto"
        >
            {/* Main Editor Card */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl shadow-xl overflow-hidden">

                {/* 1. Header & Type Selector */}
                <div className="border-b border-zinc-800 p-4 flex items-center justify-between bg-zinc-900/50 backdrop-blur-sm sticky top-0 z-10">
                    <div className="flex items-center gap-2">
                        <div className="flex bg-zinc-800/50 p-1 rounded-lg border border-zinc-700/50">
                            {(["text", "image", "video"] as PostType[]).map((type) => (
                                <button
                                    key={type}
                                    onClick={() => setPostType(type)}
                                    className={cn(
                                        "px-3 py-1.5 rounded-md text-xs font-medium transition-all duration-200 flex items-center gap-2",
                                        postType === type
                                            ? "bg-zinc-700 text-white shadow-sm"
                                            : "text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800"
                                    )}
                                >
                                    {type === "text" && <Type size={14} />}
                                    {type === "image" && <ImageIcon size={14} />}
                                    {type === "video" && <Video size={14} />}
                                    <span className="capitalize">{type}</span>
                                </button>
                            ))}
                        </div>
                    </div>

                    <div className="flex items-center gap-2">
                        <button className="p-2 text-zinc-400 hover:text-white transition-colors rounded-lg hover:bg-zinc-800">
                            <MoreHorizontal size={18} />
                        </button>
                    </div>
                </div>

                <form onSubmit={handleSubmit} className="p-6 md:p-8 space-y-6">

                    {/* 2. Title Input (Notion Style) */}
                    <div>
                        <input
                            type="text"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            placeholder="Post Title"
                            className="w-full bg-transparent text-3xl md:text-4xl font-bold text-white placeholder:text-zinc-600 border-none focus:ring-0 p-0"
                        />
                    </div>

                    {/* 3. Caption Editor (Main Focus) */}
                    <div>
                        <textarea
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            placeholder="What's on your mind? Draft your caption here..."
                            className="w-full bg-transparent text-lg text-zinc-300 placeholder:text-zinc-600 border-none focus:ring-0 p-0 resize-none min-h-[120px] leading-relaxed"
                        />
                    </div>

                    {/* 4. Media Dropzone */}
                    <AnimatePresence>
                        {postType !== "text" && (
                            <motion.div
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: "auto" }}
                                exit={{ opacity: 0, height: 0 }}
                                className="overflow-hidden"
                            >
                                <div
                                    onClick={() => fileInputRef.current?.click()}
                                    className={cn(
                                        "relative group cursor-pointer border-2 border-dashed rounded-xl transition-all duration-300 min-h-[200px] flex flex-col items-center justify-center bg-zinc-950/30",
                                        previewUrl
                                            ? "border-zinc-800 hover:border-zinc-700 p-0 overflow-hidden"
                                            : "border-zinc-800 hover:border-zinc-600 hover:bg-zinc-900"
                                    )}
                                >
                                    <input
                                        ref={fileInputRef}
                                        type="file"
                                        accept={postType === "image" ? "image/*" : "video/*"}
                                        className="hidden"
                                        onChange={handleFileChange}
                                    />

                                    {previewUrl ? (
                                        <>
                                            <button
                                                type="button"
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    clearMedia();
                                                }}
                                                className="absolute top-3 right-3 bg-black/60 text-white p-1.5 rounded-full hover:bg-red-500/80 transition-colors z-10 backdrop-blur-md"
                                            >
                                                <X size={16} />
                                            </button>
                                            {postType === "image" ? (
                                                <img src={previewUrl} alt="Preview" className="w-full h-full object-cover" />
                                            ) : (
                                                <video src={previewUrl} controls className="w-full h-full object-cover" />
                                            )}
                                        </>
                                    ) : (
                                        <div className="text-center p-8">
                                            <div className="w-12 h-12 rounded-full bg-zinc-800 flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform">
                                                <Upload size={20} className="text-zinc-400" />
                                            </div>
                                            <p className="text-sm font-medium text-zinc-300">
                                                Click to upload {postType}
                                            </p>
                                            <p className="text-xs text-zinc-500 mt-1">
                                                SVG, PNG, JPG or GIF (max. 800x400px)
                                            </p>
                                        </div>
                                    )}
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>

                    {/* 5. Action Bar */}
                    <div className="flex items-center justify-between pt-6 border-t border-zinc-800/50">
                        <div className="flex items-center gap-2 text-xs text-zinc-500">
                            <span>Markdown supported</span>
                        </div>

                        <div className="flex items-center gap-3">
                            <button
                                type="button"
                                className="px-4 py-2 text-sm font-medium text-zinc-400 hover:text-white transition-colors flex items-center gap-2"
                            >
                                <Eye size={16} />
                                Preview
                            </button>
                            <button
                                type="submit"
                                disabled={isSubmitting}
                                className="px-5 py-2 bg-white text-black rounded-lg text-sm font-bold hover:bg-zinc-200 transition-all flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {isSubmitting ? (
                                    <div className="w-4 h-4 border-2 border-black/30 border-t-black rounded-full animate-spin" />
                                ) : (
                                    <>
                                        <Save size={16} />
                                        Save Draft
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </motion.div>
    );
}
