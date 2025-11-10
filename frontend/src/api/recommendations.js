import api from "../beConnection/api.jsx";

// GET /recommendations/cold_start?top_k=K
export async function getColdStart(topK = 5) {
    const res = await api.get(`/recommendations/cold_start`, {
        params: { top_k: topK },
    });
    return res.data; // { results: [...], count, elapsed_ms }
}

// POST /recommendations/search { query, top_k }
export async function searchRecommendations(query, topK = 5) {
    const res = await api.post(`/recommendations/search`, { query, top_k: topK });
    return res.data; // { results: [...], count, elapsed_ms }
}

// GET /recommendations/similar/:id?top_k=K
export async function getSimilarById(productId, topK = 3) {
    const res = await api.get(`/recommendations/similar/${productId}`, {
        params: { top_k: topK },
    });
    return res.data;
}

// POST /recommendations/answer { question, top_k }
export async function askRecommendation(question, topK = 5) {
    const res = await api.post(`/recommendations/answer`, {
        question,
        top_k: topK,
    });
    return res.data; // { answer, products, ... }
}
