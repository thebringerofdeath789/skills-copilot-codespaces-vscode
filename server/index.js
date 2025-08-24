const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const cron = require('node-cron');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Database connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/grow_management', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Routes
app.use('/api/plants', require('./routes/plants'));
app.use('/api/tasks', require('./routes/tasks'));
app.use('/api/calendar', require('./routes/calendar'));
app.use('/api/nutrients', require('./routes/nutrients'));
app.use('/api/environment', require('./routes/environment'));
app.use('/api/schedules', require('./routes/schedules'));
app.use('/api/strains', require('./routes/strains'));
app.use('/api/growing-methods', require('./routes/growingMethods'));

// Automated task scheduling
cron.schedule('0 6 * * *', () => {
  console.log('Running daily grow tasks check...');
  // Auto-generate daily tasks based on plant stages and schedules
  require('./services/taskScheduler').generateDailyTasks();
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    message: 'Professional Grow Management API is running',
    timestamp: new Date().toISOString()
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

app.listen(PORT, () => {
  console.log(`🌱 Professional Grow Management Server running on port ${PORT}`);
});

module.exports = app;
