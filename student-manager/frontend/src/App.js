import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Container, Button, Box } from '@mui/material';
import StudentsPage from './components/students/StudentsPage';
import CoursesPage from './components/courses/CoursesPage';
import GradesPage from './components/grades/GradesPage';
import ReportsPage from './components/reports/ReportsPage';

function App() {
  return (
    <Router>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              🎓 Student Manager
            </Typography>
            <Button color="inherit" component={Link} to="/students">
              Студенты
            </Button>
            <Button color="inherit" component={Link} to="/courses">
              Курсы
            </Button>
            <Button color="inherit" component={Link} to="/grades">
              Оценки
            </Button>
            <Button color="inherit" component={Link} to="/reports">
              Отчеты
            </Button>
          </Toolbar>
        </AppBar>
        
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
          <Routes>
            <Route path="/" element={<StudentsPage />} />
            <Route path="/students" element={<StudentsPage />} />
            <Route path="/courses" element={<CoursesPage />} />
            <Route path="/grades" element={<GradesPage />} />
            <Route path="/reports" element={<ReportsPage />} />
          </Routes>
        </Container>
      </Box>
    </Router>
  );
}

export default App;