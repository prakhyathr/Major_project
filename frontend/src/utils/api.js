import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add token
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Response interceptor to handle auth errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && (error.response.status === 401 || error.response.status === 403)) {
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default {
    // Auth
    login: (credentials) => api.post('/api/v1/auth/login', credentials),
    register: (userData) => api.post('/api/v1/auth/register', userData),

    // Vendors
    getVendorProfile: () => api.get('/api/v1/vendors/me'),
    updateVendorProfile: (data) => api.put('/api/v1/vendors/me', data),

    // Events
    getEvents: (params) => api.get('/api/v1/events/', { params }),
    getEvent: (id) => api.get(`/api/v1/events/${id}`),

    // Recommendations
    getRecommendations: () => api.get('/api/v1/recommendations/'),
};
