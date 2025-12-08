'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import type { ChatMessage } from '@/types';

interface ChatInterfaceProps {
  onSendMessage: (message: string) => Promise<ChatMessage>;
}

export default function ChatInterface({ onSendMessage }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input;
    setInput('');
    setLoading(true);

    try {
      const response = await onSendMessage(userMessage);
      setMessages([...messages, response]);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto glass-strong rounded-3xl p-6 h-[600px] flex flex-col">
      {/* Header */}
      <div className="flex items-center gap-3 pb-4 border-b border-white/10">
        <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-purple-500 rounded-full flex items-center justify-center text-2xl">
          🤖
        </div>
        <div>
          <h3 className="text-xl font-bold text-white">AI Shopping Assistant</h3>
          <p className="text-sm text-dark-500">Ask me anything about products!</p>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto py-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">💬</div>
            <p className="text-dark-500">Start a conversation by asking a question!</p>
            <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-3">
              {[
                'How do I choose rain gear?',
                'What makes a good capsule wardrobe?',
                'Best fitness gear for beginners?',
                'How to care for waterproof items?',
              ].map((q) => (
                <button
                  key={q}
                  onClick={() => setInput(q)}
                  className="p-3 glass rounded-lg text-sm text-left hover:bg-white/10 transition-colors"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        <AnimatePresence>
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="space-y-4"
            >
              {/* User Question */}
              <div className="flex justify-end">
                <div className="bg-primary-600 rounded-2xl rounded-tr-sm px-4 py-3 max-w-[80%]">
                  <p className="text-white">{msg.question}</p>
                </div>
              </div>

              {/* Assistant Answer */}
              <div className="flex justify-start">
                <div className="glass rounded-2xl rounded-tl-sm px-4 py-3 max-w-[80%]">
                  <p className="text-white whitespace-pre-wrap">{msg.answer}</p>
                  
                  {/* Sources */}
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-white/10">
                      <p className="text-xs text-dark-500 mb-2">Sources:</p>
                      {msg.sources.map((source, idx) => (
                        <div key={idx} className="text-xs text-primary-400 mb-1">
                          • {source.title} ({source.type})
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex justify-start"
          >
            <div className="glass rounded-2xl px-4 py-3">
              <div className="flex gap-2">
                <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </motion.div>
        )}
      </div>

      {/* Input */}
      <div className="pt-4 border-t border-white/10">
        <div className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question..."
            className="flex-1 px-4 py-3 glass rounded-xl text-white placeholder-dark-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
            disabled={loading}
          />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleSend}
            disabled={!input.trim() || loading}
            className="px-6 py-3 bg-gradient-to-r from-primary-600 to-purple-600 rounded-xl font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </motion.button>
        </div>
      </div>
    </div>
  );
}
