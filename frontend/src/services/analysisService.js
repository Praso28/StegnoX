import api from './api';

/**
 * Analyze an image for steganography
 * @param {File} file - Image file
 * @param {string} methods - Comma-separated list of methods or 'all'
 * @returns {Promise<Object>} - Analysis results
 */
export const analyzeImage = async (file, methods = 'all') => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('methods', methods);
    
    const response = await api.post('/analysis/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return response.data.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.message || 
      'Failed to analyze image. Please try again.'
    );
  }
};

/**
 * Encode a message in an image
 * @param {File} file - Image file
 * @param {string} message - Message to encode
 * @param {string} method - Encoding method
 * @returns {Promise<Object>} - Encoding results
 */
export const encodeMessage = async (file, message, method = 'lsb_encoding') => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('message', message);
    formData.append('method', method);
    
    const response = await api.post('/analysis/encode', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return response.data.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.message || 
      'Failed to encode message. Please try again.'
    );
  }
};

/**
 * Get the URL for an image
 * @param {string} filename - Image filename
 * @returns {string} - Image URL
 */
export const getImageUrl = (filename) => {
  return `${api.defaults.baseURL}/analysis/images/${filename}`;
};
