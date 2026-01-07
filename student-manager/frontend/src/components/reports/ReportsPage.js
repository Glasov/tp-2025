
import React, { useState, useEffect, useCallback } from 'react';
import {
  Box, Typography, Button, Paper, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, Dialog,
  DialogTitle, DialogContent, DialogActions, TextField,
  Snackbar, Alert, FormControl, InputLabel, Select, MenuItem
} from '@mui/material';
import { gradeApi, studentApi, courseApi } from '../../services/api';

const GradesPage = () => {
  const [grades, setGrades] = useState([]);
  const [students, setStudents] = useState([]);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingGrade, setEditingGrade] = useState(null);
  const [formData, setFormData] = useState({ student_id: '', course_id: '', score: 0 });
  const [filters, setFilters] = useState({ student_id: '', course_id: '', min_score: '', max_score: '' });
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  // Функция для очистки пустых параметров
  const cleanFilters = useCallback((filters) => {
    const cleaned = {};
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== '' && value !== null && value !== undefined) {
        cleaned[key] = value;
      }
    });
    return cleaned;
  }, []);

  // Загружаем данные
  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const cleanedFilters = cleanFilters(filters);
      const [gradesData, studentsData, coursesData] = await Promise.all([
        gradeApi.getAll(cleanedFilters),
        studentApi.getAll(),
        courseApi.getAll()
      ]);
      setGrades(gradesData);
      setStudents(studentsData);
      setCourses(coursesData);
    } catch (error) {
      showSnackbar('Ошибка загрузки данных', 'error');
      console.error('Ошибка загрузки:', error);
      // Тестовые данные
      setGrades([
        { grade_id: 'test-1', student_id: '1', course_id: '1', score: 85, letter_grade: 'B', date: new Date().toISOString() },
        { grade_id: 'test-2', student_id: '2', course_id: '1', score: 92, letter_grade: 'A', date: new Date().toISOString() },
      ]);
      setStudents([
        { student_id: '1', name: 'Иван Иванов' },
        { student_id: '2', name: 'Мария Петрова' },
      ]);
      setCourses([
        { course_id: '1', code: 'CS101', name: 'Программирование' },
        { course_id: '2', code: 'MATH201', name: 'Математика' },
      ]);
    } finally {
      setLoading(false);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters, cleanFilters]);

  const showSnackbar = useCallback((message, severity = 'success') => {
    setSnackbar({ open: true, message, severity });
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]); // Теперь все зависимости указаны

  const handleOpenDialog = (grade = null) => {
    setEditingGrade(grade);
    setFormData(grade ? { 
      student_id: grade.student_id, 
      course_id: grade.course_id, 
      score: grade.score 
    } : { student_id: '', course_id: '', score: 0 });
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingGrade(null);
    setFormData({ student_id: '', course_id: '', score: 0 });
  };

  const handleSubmit = async () => {
    try {
      if (editingGrade) {
        await gradeApi.update(editingGrade.grade_id, formData.score);
        showSnackbar('Оценка обновлена успешно');
      } else {
        await gradeApi.create(formData);
        showSnackbar('Оценка создана успешно');
      }
      handleCloseDialog();
      loadData();
    } catch (error) {
      showSnackbar(error.response?.data?.detail || 'Ошибка сохранения', 'error');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Вы уверены, что хотите удалить эту оценку?')) {
      try {
        await gradeApi.delete(id);
        showSnackbar('Оценка удалена успешно');
        loadData();
      } catch (error) {
        showSnackbar('Ошибка удаления оценки', 'error');
      }
    }
  };

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({ ...prev, [field]: value }));
  };

  const applyFilters = () => {
    loadData();
  };

  const clearFilters = () => {
    setFilters({ student_id: '', course_id: '', min_score: '', max_score: '' });
    loadData();
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          📝 Управление оценками
        </Typography>
        <Button
          variant="contained"
          onClick={() => handleOpenDialog()}
        >
          + Добавить оценку
        </Button>
      </Box>

      {/* Фильтры */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Фильтры
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, alignItems: 'center' }}>
          <FormControl size="small" sx={{ minWidth: 200 }}>
            <InputLabel>Студент</InputLabel>
            <Select
              value={filters.student_id}
              label="Студент"
              onChange={(e) => handleFilterChange('student_id', e.target.value)}
            >
              <MenuItem value="">Все студенты</MenuItem>
              {students.map(student => (
                <MenuItem key={student.student_id} value={student.student_id}>
                  {student.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          
          <FormControl size="small" sx={{ minWidth: 200 }}>
            <InputLabel>Курс</InputLabel>
            <Select
              value={filters.course_id}
              label="Курс"
              onChange={(e) => handleFilterChange('course_id', e.target.value)}
            >
              <MenuItem value="">Все курсы</MenuItem>
              {courses.map(course => (
                <MenuItem key={course.course_id} value={course.course_id}>
                  {course.code} - {course.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          
          <TextField
            size="small"
            label="Мин. балл"
            type="number"
            value={filters.min_score}
            onChange={(e) => handleFilterChange('min_score', e.target.value)}
            sx={{ width: 120 }}
          />
          
          <TextField
            size="small"
            label="Макс. балл"
            type="number"
            value={filters.max_score}
            onChange={(e) => handleFilterChange('max_score', e.target.value)}
            sx={{ width: 120 }}
          />
          
          <Button
            variant="contained"
            onClick={applyFilters}
            sx={{ height: 40 }}
          >
            Применить
          </Button>
          
          <Button
            variant="outlined"
            onClick={clearFilters}
            sx={{ height: 40 }}
          >
            Сбросить
          </Button>
        </Box>
      </Paper>

      {/* Таблица оценок */}
      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Студент</TableCell>
                <TableCell>Курс</TableCell>
                <TableCell>Балл</TableCell>
                <TableCell>Оценка</TableCell>
                <TableCell>Дата</TableCell>
                <TableCell align="center">Действия</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={6} align="center">Загрузка...</TableCell>
                </TableRow>
              ) : grades.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} align="center">Нет оценок</TableCell>
                </TableRow>
              ) : (
                grades.map((grade) => {
                  const student = students.find(s => s.student_id === grade.student_id);
                  const course = courses.find(c => c.course_id === grade.course_id);
                  return (
                    <TableRow key={grade.grade_id}>
                      <TableCell>{student?.name || grade.student_id}</TableCell>
                      <TableCell>{course ? `${course.code} - ${course.name}` : grade.course_id}</TableCell>
                      <TableCell>{grade.score}</TableCell>
                      <TableCell>{grade.letter_grade}</TableCell>
                      <TableCell>{new Date(grade.date).toLocaleDateString()}</TableCell>
                      <TableCell align="center">
                        <Button
                          color="primary"
                          onClick={() => handleOpenDialog(grade)}
                          size="small"
                          sx={{ mr: 1 }}
                        >
                          ✏️
                        </Button>
                        <Button
                          color="error"
                          onClick={() => handleDelete(grade.grade_id)}
                          size="small"
                        >
                          🗑️
                        </Button>
                      </TableCell>
                    </TableRow>
                  );
                })
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Диалог создания/редактирования */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>
          {editingGrade ? 'Редактировать оценку' : 'Добавить оценку'}
        </DialogTitle>
        <DialogContent>
          <FormControl fullWidth sx={{ mt: 2, mb: 2 }}>
            <InputLabel>Студент</InputLabel>
            <Select
              value={formData.student_id}
              label="Студент"
              onChange={(e) => setFormData({ ...formData, student_id: e.target.value })}
            >
              {students.map(student => (
                <MenuItem key={student.student_id} value={student.student_id}>
                  {student.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>Курс</InputLabel>
            <Select
              value={formData.course_id}
              label="Курс"
              onChange={(e) => setFormData({ ...formData, course_id: e.target.value })}
            >
              {courses.map(course => (
                <MenuItem key={course.course_id} value={course.course_id}>
                  {course.code} - {course.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            fullWidth
            label="Балл (0-100)"
            type="number"
            value={formData.score}
            onChange={(e) => setFormData({ ...formData, score: parseFloat(e.target.value) || 0 })}
            inputProps={{ min: 0, max: 100, step: 0.1 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Отмена</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingGrade ? 'Обновить' : 'Создать'}
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={3000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert severity={snackbar.severity}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default GradesPage;
