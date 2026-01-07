import axios from 'axios';

const API_BASE = 'http://localhost:8001';

// Student API
export const studentApi = {
  getAll: () => axios.get(`${API_BASE}/students`).then(res => res.data),
  getById: (id) => axios.get(`${API_BASE}/students/${id}`).then(res => res.data),
  create: (student) => 
    axios.post(`${API_BASE}/students`, student).then(res => res.data),
  update: (id, student) => 
    axios.put(`${API_BASE}/students/${id}`, student).then(res => res.data),
  delete: (id) => axios.delete(`${API_BASE}/students/${id}`),
};

// Course API
export const courseApi = {
  getAll: () => axios.get(`${API_BASE}/courses`).then(res => res.data),
  getById: (id) => axios.get(`${API_BASE}/courses/${id}`).then(res => res.data),
  create: (course) => 
    axios.post(`${API_BASE}/courses`, course).then(res => res.data),
  delete: (id) => axios.delete(`${API_BASE}/courses/${id}`),
};

// Grade API
export const gradeApi = {
  getAll: (params = {}) => 
    axios.get(`${API_BASE}/grades`, { params }).then(res => res.data),
  getById: (id) => axios.get(`${API_BASE}/grades/${id}`).then(res => res.data),
  create: (grade) => 
    axios.post(`${API_BASE}/grades`, grade).then(res => res.data),
  update: (id, score) => 
    axios.put(`${API_BASE}/grades/${id}`, null, { params: { score } }).then(res => res.data),
  delete: (id) => axios.delete(`${API_BASE}/grades/${id}`),
};

// Reports API
export const reportsApi = {
  getStudentsSummary: (params = {}) => 
    axios.get(`${API_BASE}/reports/students/summary`, { params }).then(res => res.data),
  getCoursesSummary: () => 
    axios.get(`${API_BASE}/reports/courses/summary`).then(res => res.data),
  getGradesStatistics: (params = {}) => 
    axios.get(`${API_BASE}/reports/grades/statistics`, { params }).then(res => res.data),
};