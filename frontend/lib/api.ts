import axios from 'axios';
import type { Product, SearchResponse, ChatMessage, RecommendationResponse } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const searchProducts = async (
    query: string,
    limit: number = 10,
    category?: string,
    minPrice?: number,
    maxPrice?: number
): Promise<SearchResponse> => {
    const response = await api.post('/api/search', {
        query,
        limit,
        category,
        min_price: minPrice,
        max_price: maxPrice,
    });
    return response.data;
};

export const chatWithAssistant = async (
    question: string,
    contextLimit: number = 3,
    includeProducts: boolean = true
): Promise<ChatMessage> => {
    const response = await api.post('/api/chat', {
        question,
        context_limit: contextLimit,
        include_products: includeProducts,
    });
    return response.data;
};

export const getRecommendations = async (
    productId?: string,
    productName?: string,
    query?: string,
    limit: number = 5
): Promise<RecommendationResponse> => {
    const response = await api.post('/api/recommend', {
        product_id: productId,
        product_name: productName,
        query,
        limit,
    });
    return response.data;
};

export const getAllProducts = async (): Promise<Product[]> => {
    const response = await api.get('/api/products');
    return response.data;
};

export const getProduct = async (productId: string): Promise<Product> => {
    const response = await api.get(`/api/products/${productId}`);
    return response.data;
};

export const healthCheck = async () => {
    const response = await api.get('/api/health');
    return response.data;
};
