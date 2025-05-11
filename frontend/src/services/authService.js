import api from './api';

/**
 * Login a user
 * @param {string} username - Username
 * @param {string} password - Password
 * @returns {Promise<Object>} - User data and token
 */
export const loginUser = async (username, password) => {
  try {
    const response = await api.post('/auth/login', { username, password });
    return response.data.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.message || 
      'Login failed. Please check your credentials.'
    );
  }
};

/**
 * Register a new user
 * @param {string} username - Username
 * @param {string} email - Email
 * @param {string} password - Password
 * @returns {Promise<Object>} - User data and token
 */
export const registerUser = async (username, email, password) => {
  try {
    const response = await api.post('/auth/register', { username, email, password });
    return response.data.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.message || 
      'Registration failed. Please try again.'
    );
  }
};

/**
 * Get the current user's data
 * @returns {Promise<Object>} - User data
 */
export const getCurrentUser = async () => {
  try {
    // This endpoint doesn't exist yet, but we'll assume it will be implemented
    const response = await api.get('/auth/me');
    return response.data.data.user;
  } catch (error) {
    throw new Error(
      error.response?.data?.message || 
      'Failed to get user data.'
    );
  }
};
