import { User as UserIcon } from "lucide-react";
import Image from "next/image";

interface MessageBubbleProps {
  role: string;
  content: string;
}

export function MessageBubble({ role, content }: MessageBubbleProps) {
  const isUser = role === "user";

  return (
    <div className={`flex items-start gap-3 ${isUser ? "flex-row-reverse" : ""}`}>
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 overflow-hidden ${
          isUser ? "bg-emerald-600 text-white" : "bg-slate-100 border border-slate-200"
        }`}
      >
        {isUser ? (
          <UserIcon size={16} />
        ) : (
          <Image 
            src="/bot-icon.webp" 
            alt="Bot" 
            width={32} 
            height={32} 
            className="w-full h-full object-cover"
          />
        )}
      </div>
      <div
        className={`p-3 rounded-lg max-w-[80%] shadow-sm ${
          isUser
            ? "bg-emerald-600 text-white rounded-tr-none"
            : "bg-slate-100 text-slate-700 rounded-tl-none"
        }`}
      >
        {content}
      </div>
    </div>
  );
}
