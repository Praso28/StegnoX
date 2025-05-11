import api from './api';

/**
 * Create a new job
 * @param {File} file - Image file
 * @param {string} priority - Job priority (low, normal, high)
 * @returns {Promise<Object>} - Job data
 */
export const createJob = async (file, priority = 'normal') => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('priority', priority);
    
    const response = await api.post('/jobs', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return response.data.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.message || 
      'Failed to create job. Please try again.'
    );
  }
};

/**
 * Get a list of jobs
 * @param {string} status - Filter by status (optional)
 * @param {number} limit - Maximum number of jobs to return
 * @param {number} offset - Offset for pagination
 * @returns {Promise<Array>} - List of jobs
 */
export const getJobs = async (status = null, limit = 10, offset = 0) => {
  try {
    let url = `/jobs?limit=${limit}&offset=${offset}`;
    if (status) {
      url += `&status=${status}`;
    }
    
    const response = await api.get(url);
    return response.data.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.message || 
      'Failed to get jobs. Please try again.'
    );
  }
};

/**
 * Get a job by ID
 * @param {string} jobId - Job ID
 * @returns {Promise<Object>} - Job data
 */
export const getJob = async (jobId) => {
  try {
    const response = await api.get(`/jobs/${jobId}`);
    return response.data.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.message || 
      'Failed to get job. Please try again.'
    );
  }
};

/**
 * Cancel a job
 * @param {string} jobId - Job ID
 * @returns {Promise<boolean>} - Success status
 */
export const cancelJob = async (jobId) => {
  try {
    const response = await api.delete(`/jobs/${jobId}`);
    return response.data.success;
  } catch (error) {
    throw new Error(
      error.response?.data?.message || 
      'Failed to cancel job. Please try again.'
    );
  }
};
