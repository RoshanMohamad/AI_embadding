export interface Product {
    id: string;
    name: string;
    description: string;
    category: string;
    price: number;
    tags: string[];
    image_url?: string;
    rating?: number;
    in_stock: boolean;
    brand?: string;
}

export interface SearchResponse {
    query: string;
    results: Product[];
    total: number;
    semantic_matches: boolean;
}

export interface ChatMessage {
    question: string;
    answer: string;
    sources: Array<{
        title: string;
        type: string;
        category: string;
        relevance: number;
    }>;
    related_products: Product[];
}

export interface RecommendationResponse {
    based_on: string;
    recommendations: Product[];
    similarity_scores?: number[];
}
