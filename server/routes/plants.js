const express = require('express');
const router = express.Router();
const Plant = require('../models/Plant');
const TaskScheduler = require('../services/taskScheduler');

// GET all plants
router.get('/', async (req, res) => {
  try {
    const plants = await Plant.find({ isActive: true })
      .sort({ createdAt: -1 })
      .populate('notes')
      .populate('photos');
    res.json(plants);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// GET single plant
router.get('/:id', async (req, res) => {
  try {
    const plant = await Plant.findById(req.params.id);
    if (!plant) {
      return res.status(404).json({ error: 'Plant not found' });
    }
    res.json(plant);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// CREATE new plant
router.post('/', async (req, res) => {
  try {
    const plantData = req.body;
    
    // Set up default light cycles based on strain type
    if (!plantData.lightCycle) {
      if (plantData.strain === 'autoflower') {
        plantData.lightCycle = {
          vegetative: { on: 20, off: 4 },
          flowering: { on: 20, off: 4 } // Autos can handle 20/4 throughout
        };
      } else {
        plantData.lightCycle = {
          vegetative: { on: 18, off: 6 },
          flowering: { on: 12, off: 12 }
        };
      }
    }

    // Set expected harvest date based on strain
    if (!plantData.expectedHarvestDate && plantData.plantedDate) {
      const plantedDate = new Date(plantData.plantedDate);
      const harvestDate = new Date(plantedDate);
      
      if (plantData.strain === 'autoflower') {
        harvestDate.setDate(harvestDate.getDate() + 75); // ~11 weeks
      } else {
        harvestDate.setDate(harvestDate.getDate() + 120); // ~17 weeks
      }
      plantData.expectedHarvestDate = harvestDate;
    }

    const plant = new Plant(plantData);
    await plant.save();
    
    // Generate initial tasks for the new plant
    await TaskScheduler.generateTasksForPlant(plant);
    
    res.status(201).json(plant);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// UPDATE plant
router.put('/:id', async (req, res) => {
  try {
    const plant = await Plant.findByIdAndUpdate(
      req.params.id,
      { $set: req.body },
      { new: true, runValidators: true }
    );
    
    if (!plant) {
      return res.status(404).json({ error: 'Plant not found' });
    }
    
    res.json(plant);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// ADD note to plant
router.post('/:id/notes', async (req, res) => {
  try {
    const plant = await Plant.findById(req.params.id);
    if (!plant) {
      return res.status(404).json({ error: 'Plant not found' });
    }
    
    const note = {
      content: req.body.content,
      type: req.body.type || 'observation',
      date: req.body.date || new Date()
    };
    
    plant.notes.push(note);
    await plant.save();
    
    res.json(plant);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// ADD photo to plant
router.post('/:id/photos', async (req, res) => {
  try {
    const plant = await Plant.findById(req.params.id);
    if (!plant) {
      return res.status(404).json({ error: 'Plant not found' });
    }
    
    const photo = {
      url: req.body.url,
      description: req.body.description,
      stage: plant.currentStage,
      date: new Date()
    };
    
    plant.photos.push(photo);
    await plant.save();
    
    res.json(plant);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// CHANGE plant stage
router.post('/:id/change-stage', async (req, res) => {
  try {
    const plant = await Plant.findById(req.params.id);
    if (!plant) {
      return res.status(404).json({ error: 'Plant not found' });
    }
    
    const oldStage = plant.currentStage;
    const newStage = req.body.stage;
    
    plant.currentStage = newStage;
    
    // Add milestone note
    plant.notes.push({
      content: `Stage changed from ${oldStage} to ${newStage}`,
      type: 'milestone',
      date: new Date()
    });
    
    await plant.save();
    
    // Generate new stage-specific tasks
    await TaskScheduler.generateTasksForPlant(plant);
    
    res.json(plant);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// GET plant analytics/stats
router.get('/:id/analytics', async (req, res) => {
  try {
    const plant = await Plant.findById(req.params.id);
    if (!plant) {
      return res.status(404).json({ error: 'Plant not found' });
    }
    
    const daysAlive = Math.floor((Date.now() - plant.plantedDate) / (1000 * 60 * 60 * 24));
    const daysToHarvest = plant.expectedHarvestDate ? 
      Math.floor((plant.expectedHarvestDate - Date.now()) / (1000 * 60 * 60 * 24)) : null;
    
    const analytics = {
      daysAlive,
      daysToHarvest,
      currentStage: plant.currentStage,
      daysInCurrentStage: plant.daysInStage,
      totalNotes: plant.notes.length,
      totalPhotos: plant.photos.length,
      healthScore: this.calculateHealthScore(plant),
      stageProgress: this.calculateStageProgress(plant, daysAlive)
    };
    
    res.json(analytics);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Helper functions
function calculateHealthScore(plant) {
  let score = 100;
  
  // Deduct points for issues mentioned in notes
  const issueNotes = plant.notes.filter(note => 
    note.content.toLowerCase().includes('problem') ||
    note.content.toLowerCase().includes('issue') ||
    note.content.toLowerCase().includes('pest') ||
    note.content.toLowerCase().includes('deficiency')
  );
  
  score -= issueNotes.length * 10;
  
  return Math.max(score, 0);
}

function calculateStageProgress(plant, daysAlive) {
  const stageTimelines = {
    'autoflower': {
      'germination': 3,
      'seedling': 14,
      'vegetative': 35,
      'pre-flower': 42,
      'flowering': 77
    },
    'photoperiod': {
      'germination': 5,
      'seedling': 21,
      'vegetative': 56,
      'pre-flower': 70,
      'flowering': 126
    }
  };
  
  const timeline = stageTimelines[plant.strain] || stageTimelines['photoperiod'];
  const targetDays = timeline[plant.currentStage];
  
  if (targetDays) {
    const progress = Math.min((daysAlive / targetDays) * 100, 100);
    return Math.round(progress);
  }
  
  return 0;
}

// DELETE plant (soft delete)
router.delete('/:id', async (req, res) => {
  try {
    const plant = await Plant.findByIdAndUpdate(
      req.params.id,
      { isActive: false },
      { new: true }
    );
    
    if (!plant) {
      return res.status(404).json({ error: 'Plant not found' });
    }
    
    res.json({ message: 'Plant deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
