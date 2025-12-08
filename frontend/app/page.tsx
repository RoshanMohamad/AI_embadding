'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import SearchBar from '@/components/SearchBar';
import ProductCard from '@/components/ProductCard';
import ChatInterface from '@/components/ChatInterface';
import { searchProducts, chatWithAssistant, getRecommendations } from '@/lib/api';
import type { Product, ChatMessage, RecommendationResponse } from '@/types';

type Tab = 'search' | 'chat' | 'recommend';

export default function Home() {
  const [activeTab, setActiveTab] = useState<Tab>('search');
  const [searchResults, setSearchResults] = useState<Product[]>([]);
  const [recommendations, setRecommendations] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);

  const handleSearch = async (query: string) => {
    setLoading(true);
    try {
      const response = await searchProducts(query, 12);
      setSearchResults(response.results);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChat = async (message: string): Promise<ChatMessage> => {
    return await chatWithAssistant(message);
  };

  const handleGetRecommendations = async (product: Product) => {
    setSelectedProduct(product);
    setLoading(true);
    try {
      const response = await getRecommendations(product.id, undefined, undefined, 6);
      setRecommendations(response);
      setActiveTab('recommend');
    } catch (error) {
      console.error('Recommendation error:', error);
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'search' as Tab, label: 'Search', icon: '🔍' },
    { id: 'chat' as Tab, label: 'Chat', icon: '💬' },
    { id: 'recommend' as Tab, label: 'Recommendations', icon: '✨' },
  ];

  return (
    <main className="min-h-screen bg-gradient-to-br from-dark-50 via-dark-100 to-dark-50 relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary-500/20 rounded-full blur-3xl animate-pulse-slow" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }} />
      </div>

      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h1 className="text-6xl font-bold mb-4">
            <span className="gradient-text">AI Shopping</span>
            <br />
            <span className="text-white">Assistant</span>
          </h1>
          <p className="text-xl text-dark-500 max-w-2xl mx-auto">
            Powered by semantic search, RAG, and intelligent recommendations
          </p>
        </motion.header>

        {/* Tab Navigation */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="flex justify-center gap-4 mb-8"
        >
          {tabs.map((tab) => (
            <motion.button
              key={tab.id}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setActiveTab(tab.id)}
              className={`px-6 py-3 rounded-xl font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-gradient-to-r from-primary-600 to-purple-600 text-white shadow-lg shadow-primary-500/30'
                  : 'glass text-dark-500 hover:text-white'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </motion.button>
          ))}
        </motion.div>

        {/* Content */}
        <div className="max-w-7xl mx-auto">
          {/* Search Tab */}
          {activeTab === 'search' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4 }}
            >
              <div className="mb-12">
                <SearchBar onSearch={handleSearch} loading={loading} />
              </div>

              {searchResults.length > 0 && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.2 }}
                >
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-2xl font-bold text-white">
                      Found {searchResults.length} products
                    </h2>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {searchResults.map((product, index) => (
                      <ProductCard
                        key={product.id}
                        product={product}
                        index={index}
                        onClick={() => handleGetRecommendations(product)}
                      />
                    ))}
                  </div>
                </motion.div>
              )}

              {!loading && searchResults.length === 0 && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-center py-20"
                >
                  <div className="text-8xl mb-6 animate-float">🛍️</div>
                  <h3 className="text-2xl font-bold text-white mb-2">
                    Discover Amazing Products
                  </h3>
                  <p className="text-dark-500 text-lg">
                    Try searching for "rain jacket", "black shirt", or "running shoes"
                  </p>
                </motion.div>
              )}
            </motion.div>
          )}

          {/* Chat Tab */}
          {activeTab === 'chat' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4 }}
            >
              <ChatInterface onSendMessage={handleChat} />
            </motion.div>
          )}

          {/* Recommendations Tab */}
          {activeTab === 'recommend' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4 }}
            >
              {recommendations ? (
                <div>
                  <div className="glass-strong rounded-2xl p-6 mb-8">
                    <h2 className="text-2xl font-bold text-white mb-2">
                      {recommendations.based_on}
                    </h2>
                    <p className="text-dark-500">
                      Here are products similar to what you&apos;re interested in
                    </p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {recommendations.recommendations.map((product, index) => (
                      <ProductCard
                        key={product.id}
                        product={product}
                        index={index}
                        onClick={() => handleGetRecommendations(product)}
                      />
                    ))}
                  </div>
                </div>
              ) : (
                <div className="text-center py-20 glass-strong rounded-3xl">
                  <div className="text-8xl mb-6 animate-float">✨</div>
                  <h3 className="text-2xl font-bold text-white mb-2">
                    No Recommendations Yet
                  </h3>
                  <p className="text-dark-500 text-lg mb-6">
                    Click on a product from search results to get personalized recommendations
                  </p>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setActiveTab('search')}
                    className="px-8 py-3 bg-gradient-to-r from-primary-600 to-purple-600 rounded-xl font-medium"
                  >
                    Go to Search
                  </motion.button>
                </div>
              )}
            </motion.div>
          )}

          {loading && (
            <div className="flex justify-center items-center py-20">
              <div className="text-center">
                <div className="w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
                <p className="text-dark-500">Loading amazing products...</p>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <motion.footer
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="text-center mt-20 py-8 border-t border-white/10"
        >
          <p className="text-dark-500">
            Powered by <span className="gradient-text-blue font-semibold">RAG</span>,{' '}
            <span className="gradient-text-blue font-semibold">Semantic Search</span>, and{' '}
            <span className="gradient-text-blue font-semibold">AI Recommendations</span>
          </p>
          <p className="text-dark-600 text-sm mt-2">
            Built with FastAPI, ChromaDB, Sentence Transformers & Next.js
          </p>
        </motion.footer>
      </div>
    </main>
  );
}
