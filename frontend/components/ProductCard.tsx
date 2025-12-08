'use client';

import { motion } from 'framer-motion';
import type { Product } from '@/types';

interface ProductCardProps {
  product: Product;
  onClick?: () => void;
  index?: number;
}

export default function ProductCard({ product, onClick, index = 0 }: ProductCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.1 }}
      whileHover={{ scale: 1.03, y: -5 }}
      onClick={onClick}
      className="glass rounded-2xl p-5 cursor-pointer hover-lift glow-hover group relative overflow-hidden"
    >
      {/* Background gradient on hover */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      
      <div className="relative z-10">
        {/* Product Image Placeholder */}
        <div className="w-full h-48 bg-gradient-to-br from-primary-600 to-purple-600 rounded-xl mb-4 flex items-center justify-center overflow-hidden">
          <motion.div
            whileHover={{ scale: 1.1 }}
            transition={{ duration: 0.3 }}
            className="text-6xl"
          >
            {product.category === 'Outerwear' && '🧥'}
            {product.category === 'Footwear' && '👟'}
            {product.category === 'Accessories' && '🎒'}
            {product.category === 'Apparel' && '👕'}
            {product.category === 'Fitness' && '🏋️'}
            {product.category === 'Electronics' && '🎧'}
            {product.category === 'Bags' && '🎒'}
            {!['Outerwear', 'Footwear', 'Accessories', 'Apparel', 'Fitness', 'Electronics', 'Bags'].includes(product.category) && '🛍️'}
          </motion.div>
        </div>

        {/* Product Info */}
        <div className="space-y-2">
          {/* Brand & Category */}
          <div className="flex items-center justify-between text-sm">
            <span className="text-primary-400 font-medium">{product.brand || 'Brand'}</span>
            <span className="text-dark-500">{product.category}</span>
          </div>

          {/* Product Name */}
          <h3 className="text-lg font-bold text-white group-hover:text-primary-400 transition-colors line-clamp-2">
            {product.name}
          </h3>

          {/* Description */}
          <p className="text-dark-500 text-sm line-clamp-2">
            {product.description}
          </p>

          {/* Rating & Stock */}
          <div className="flex items-center gap-3">
            {product.rating && (
              <div className="flex items-center gap-1">
                <span className="text-yellow-400">⭐</span>
                <span className="text-sm text-white font-medium">{product.rating.toFixed(1)}</span>
              </div>
            )}
            {product.in_stock ? (
              <span className="text-xs text-green-400 font-medium">In Stock</span>
            ) : (
              <span className="text-xs text-red-400 font-medium">Out of Stock</span>
            )}
          </div>

          {/* Price */}
          <div className="flex items-center justify-between pt-3 border-t border-white/10">
            <span className="text-2xl font-bold gradient-text-blue">
              ${product.price.toFixed(2)}
            </span>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-4 py-2 bg-primary-600 hover:bg-primary-700 rounded-lg text-sm font-medium transition-colors"
            >
              View Details
            </motion.button>
          </div>

          {/* Tags */}
          <div className="flex flex-wrap gap-2 pt-2">
            {product.tags.slice(0, 3).map((tag, i) => (
              <span
                key={i}
                className="px-2 py-1 bg-white/5 rounded-md text-xs text-dark-600"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
