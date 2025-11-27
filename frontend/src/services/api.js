import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

export const getOptimalStrategy = async () => {
    try {
        const response = await axios.get(`${API_URL}/strategy/optimize`);
        return response.data;
    } catch (error) {
        console.error("Error fetching strategy:", error);
        return null;
    }
};