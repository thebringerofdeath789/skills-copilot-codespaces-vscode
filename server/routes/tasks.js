const express = require('express');
const router = express.Router();
const Task = require('../models/Task');
const Plant = require('../models/Plant');

// GET all tasks with filtering
router.get('/', async (req, res) => {
  try {
    const { 
      plantId, 
      completed, 
      type, 
      priority, 
      dateFrom, 
      dateTo,
      overdue 
    } = req.query;
    
    let filter = {};
    
    if (plantId) filter.plantId = plantId;
    if (completed !== undefined) filter.completed = completed === 'true';
    if (type) filter.type = type;
    if (priority) filter.priority = priority;
    
    if (dateFrom || dateTo) {
      filter.dueDate = {};
      if (dateFrom) filter.dueDate.$gte = new Date(dateFrom);
      if (dateTo) filter.dueDate.$lte = new Date(dateTo);
    }
    
    if (overdue === 'true') {
      filter.dueDate = { $lt: new Date() };
      filter.completed = false;
    }
    
    const tasks = await Task.find(filter)
      .populate('plantId', 'name strain currentStage')
      .sort({ dueDate: 1, priority: -1 });
    
    res.json(tasks);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// GET today's tasks
router.get('/today', async (req, res) => {
  try {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    const tasks = await Task.find({
      dueDate: {
        $gte: today.setHours(0, 0, 0, 0),
        $lt: tomorrow.setHours(0, 0, 0, 0)
      }
    })
    .populate('plantId', 'name strain currentStage location')
    .sort({ priority: -1, dueDate: 1 });
    
    res.json(tasks);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// GET upcoming tasks (next 7 days)
router.get('/upcoming', async (req, res) => {
  try {
    const today = new Date();
    const nextWeek = new Date(today);
    nextWeek.setDate(nextWeek.getDate() + 7);
    
    const tasks = await Task.find({
      dueDate: {
        $gte: today,
        $lte: nextWeek
      },
      completed: false
    })
    .populate('plantId', 'name strain currentStage')
    .sort({ dueDate: 1, priority: -1 });
    
    res.json(tasks);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// GET overdue tasks
router.get('/overdue', async (req, res) => {
  try {
    const now = new Date();
    
    const tasks = await Task.find({
      dueDate: { $lt: now },
      completed: false
    })
    .populate('plantId', 'name strain currentStage')
    .sort({ dueDate: 1 });
    
    res.json(tasks);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// GET single task
router.get('/:id', async (req, res) => {
  try {
    const task = await Task.findById(req.params.id)
      .populate('plantId');
    
    if (!task) {
      return res.status(404).json({ error: 'Task not found' });
    }
    
    res.json(task);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// CREATE new task
router.post('/', async (req, res) => {
  try {
    const task = new Task(req.body);
    await task.save();
    
    const populatedTask = await Task.findById(task._id)
      .populate('plantId', 'name strain currentStage');
    
    res.status(201).json(populatedTask);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// UPDATE task
router.put('/:id', async (req, res) => {
  try {
    const task = await Task.findByIdAndUpdate(
      req.params.id,
      { $set: req.body },
      { new: true, runValidators: true }
    ).populate('plantId', 'name strain currentStage');
    
    if (!task) {
      return res.status(404).json({ error: 'Task not found' });
    }
    
    res.json(task);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// COMPLETE task
router.post('/:id/complete', async (req, res) => {
  try {
    const task = await Task.findById(req.params.id);
    if (!task) {
      return res.status(404).json({ error: 'Task not found' });
    }
    
    task.completed = true;
    task.completedAt = new Date();
    
    // Save any completion results
    if (req.body.results) {
      task.results = { ...task.results, ...req.body.results };
    }
    
    if (req.body.actualDuration) {
      task.actualDuration = req.body.actualDuration;
    }
    
    await task.save();
    
    // If this is a recurring task, create the next occurrence
    if (task.recurring && task.recurring.enabled) {
      await this.createRecurringTask(task);
    }
    
    const populatedTask = await Task.findById(task._id)
      .populate('plantId', 'name strain currentStage');
    
    res.json(populatedTask);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Helper function to create recurring task
async function createRecurringTask(originalTask) {
  const nextDueDate = new Date(originalTask.dueDate);
  
  switch (originalTask.recurring.frequency) {
    case 'daily':
      nextDueDate.setDate(nextDueDate.getDate() + 1);
      break;
    case 'weekly':
      nextDueDate.setDate(nextDueDate.getDate() + 7);
      break;
    case 'bi-weekly':
      nextDueDate.setDate(nextDueDate.getDate() + 14);
      break;
    case 'monthly':
      nextDueDate.setMonth(nextDueDate.getMonth() + 1);
      break;
    case 'custom':
      nextDueDate.setDate(nextDueDate.getDate() + (originalTask.recurring.interval || 1));
      break;
  }
  
  // Don't create if past end date
  if (originalTask.recurring.endDate && nextDueDate > originalTask.recurring.endDate) {
    return;
  }
  
  const newTask = new Task({
    title: originalTask.title,
    description: originalTask.description,
    type: originalTask.type,
    priority: originalTask.priority,
    plantId: originalTask.plantId,
    dueDate: nextDueDate,
    estimatedDuration: originalTask.estimatedDuration,
    recurring: originalTask.recurring,
    instructions: originalTask.instructions,
    materials: originalTask.materials,
    autoGenerated: originalTask.autoGenerated,
    tags: originalTask.tags
  });
  
  await newTask.save();
}

// SNOOZE task
router.post('/:id/snooze', async (req, res) => {
  try {
    const task = await Task.findById(req.params.id);
    if (!task) {
      return res.status(404).json({ error: 'Task not found' });
    }
    
    const snoozeHours = req.body.hours || 24; // Default snooze 24 hours
    const newDueDate = new Date(task.dueDate);
    newDueDate.setHours(newDueDate.getHours() + snoozeHours);
    
    task.dueDate = newDueDate;
    await task.save();
    
    const populatedTask = await Task.findById(task._id)
      .populate('plantId', 'name strain currentStage');
    
    res.json(populatedTask);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// GET task statistics
router.get('/stats/summary', async (req, res) => {
  try {
    const now = new Date();
    const today = new Date(now.setHours(0, 0, 0, 0));
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    const stats = {
      total: await Task.countDocuments(),
      completed: await Task.countDocuments({ completed: true }),
      pending: await Task.countDocuments({ completed: false }),
      overdue: await Task.countDocuments({ 
        dueDate: { $lt: now }, 
        completed: false 
      }),
      today: await Task.countDocuments({
        dueDate: { $gte: today, $lt: tomorrow }
      }),
      thisWeek: await Task.countDocuments({
        dueDate: { 
          $gte: today,
          $lt: new Date(today.getTime() + 7 * 24 * 60 * 60 * 1000)
        },
        completed: false
      })
    };
    
    // Task completion rate
    stats.completionRate = stats.total > 0 ? 
      Math.round((stats.completed / stats.total) * 100) : 0;
    
    // Tasks by type
    const tasksByType = await Task.aggregate([
      { $group: { _id: '$type', count: { $sum: 1 } } }
    ]);
    stats.byType = tasksByType;
    
    // Tasks by priority
    const tasksByPriority = await Task.aggregate([
      { $group: { _id: '$priority', count: { $sum: 1 } } }
    ]);
    stats.byPriority = tasksByPriority;
    
    res.json(stats);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// DELETE task
router.delete('/:id', async (req, res) => {
  try {
    const task = await Task.findByIdAndDelete(req.params.id);
    
    if (!task) {
      return res.status(404).json({ error: 'Task not found' });
    }
    
    res.json({ message: 'Task deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// BULK operations
router.post('/bulk/complete', async (req, res) => {
  try {
    const taskIds = req.body.taskIds;
    
    await Task.updateMany(
      { _id: { $in: taskIds } },
      { 
        completed: true, 
        completedAt: new Date() 
      }
    );
    
    res.json({ message: `${taskIds.length} tasks marked as completed` });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

router.delete('/bulk/delete', async (req, res) => {
  try {
    const taskIds = req.body.taskIds;
    
    await Task.deleteMany({ _id: { $in: taskIds } });
    
    res.json({ message: `${taskIds.length} tasks deleted` });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

module.exports = router;
