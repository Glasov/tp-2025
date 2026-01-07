import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Button, Paper, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, Dialog,
  DialogTitle, DialogContent, DialogActions, TextField,
  Snackbar, Alert
} from '@mui/material';
import { courseApi } from '../../services/api';

const CoursesPage = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingCourse, setEditingCourse] = useState(null);
  const [formData, setFormData] = useState({ code: '', name: '', credits: 3 });
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  // Загружаем курсы
  const loadCourses = async () => {
    try {
      setLoading(true);
      const data = await courseApi.getAll();
      setCourses(data);
    } catch (error) {
      showSnackbar('Ошибка загрузки курсов', 'error');
      console.error('Ошибка загрузки курсов:', error);
      // Тестовые данные
      setCourses([
        { course_id: 'test-1', code: 'CS101', name: 'Программирование', credits: 4 },
        { course_id: 'test-2', code: 'MATH201', name: 'Математика', credits: 5 },
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCourses();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const showSnackbar = (message, severity = 'success') => {
    setSnackbar({ open: true, message, severity });
  };

  const handleOpenDialog = (course = null) => {
    setEditingCourse(course);
    setFormData(course ? { code: course.code, name: course.name, credits: course.credits } : { code: '', name: '', credits: 3 });
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingCourse(null);
    setFormData({ code: '', name: '', credits: 3 });
  };

  const handleSubmit = async () => {
    try {
      if (editingCourse) {
        await courseApi.update(editingCourse.course_id, formData);
        showSnackbar('Курс обновлен успешно');
      } else {
        await courseApi.create(formData);
        showSnackbar('Курс создан успешно');
      }
      handleCloseDialog();
      loadCourses();
    } catch (error) {
      showSnackbar(error.response?.data?.detail || 'Ошибка сохранения', 'error');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Вы уверены, что хотите удалить этот курс?')) {
      try {
        await courseApi.delete(id);
        showSnackbar('Курс удален успешно');
        loadCourses();
      } catch (error) {
        showSnackbar('Ошибка удаления курса', 'error');
      }
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          📚 Управление курсами
        </Typography>
        <Button
          variant="contained"
          onClick={() => handleOpenDialog()}
        >
          + Добавить курс
        </Button>
      </Box>

      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Код</TableCell>
                <TableCell>Название</TableCell>
                <TableCell>Кредиты</TableCell>
                <TableCell align="center">Действия</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={4} align="center">Загрузка...</TableCell>
                </TableRow>
              ) : courses.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={4} align="center">Нет курсов</TableCell>
                </TableRow>
              ) : (
                courses.map((course) => (
                  <TableRow key={course.course_id}>
                    <TableCell>{course.code}</TableCell>
                    <TableCell>{course.name}</TableCell>
                    <TableCell>{course.credits}</TableCell>
                    <TableCell align="center">
                      <Button
                        color="primary"
                        onClick={() => handleOpenDialog(course)}
                        size="small"
                        sx={{ mr: 1 }}
                      >
                        ✏️
                      </Button>
                      <Button
                        color="error"
                        onClick={() => handleDelete(course.course_id)}
                        size="small"
                      >
                        🗑️
                      </Button>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Диалог создания/редактирования */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>
          {editingCourse ? 'Редактировать курс' : 'Добавить курс'}
        </DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Код курса"
            fullWidth
            value={formData.code}
            onChange={(e) => setFormData({ ...formData, code: e.target.value })}
            sx={{ mt: 2 }}
          />
          <TextField
            margin="dense"
            label="Название курса"
            fullWidth
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Кредиты"
            type="number"
            fullWidth
            value={formData.credits}
            onChange={(e) => setFormData({ ...formData, credits: parseInt(e.target.value) || 1 })}
            inputProps={{ min: 1, max: 10 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Отмена</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingCourse ? 'Обновить' : 'Создать'}
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

export default CoursesPage;