const Plant = require('../models/Plant');
const Task = require('../models/Task');
const { GrowingKnowledge } = require('../models/GrowingKnowledge');
const moment = require('moment');

class TaskScheduler {
  
  // Generate daily tasks based on plant stage and growing method
  static async generateDailyTasks() {
    try {
      const activePlants = await Plant.find({ isActive: true });
      
      for (const plant of activePlants) {
        await this.generateTasksForPlant(plant);
      }
      
      console.log(`Generated tasks for ${activePlants.length} active plants`);
    } catch (error) {
      console.error('Error generating daily tasks:', error);
    }
  }

  static async generateTasksForPlant(plant) {
    const currentDate = new Date();
    const daysFromPlanted = Math.floor((currentDate - plant.plantedDate) / (1000 * 60 * 60 * 24));
    
    // Determine current stage based on days and plant type
    const currentStage = this.determineStage(daysFromPlanted, plant.strain);
    
    // Update plant stage if needed
    if (plant.currentStage !== currentStage) {
      plant.currentStage = currentStage;
      await plant.save();
    }

    // Generate stage-specific tasks
    await this.generateStageSpecificTasks(plant, currentStage, daysFromPlanted);
    
    // Generate recurring maintenance tasks
    await this.generateMaintenanceTasks(plant);
    
    // Generate method-specific tasks
    await this.generateMethodSpecificTasks(plant);
  }

  static determineStage(daysFromPlanted, strain) {
    // Autoflower timeline (faster)
    if (strain === 'autoflower') {
      if (daysFromPlanted <= 3) return 'germination';
      if (daysFromPlanted <= 14) return 'seedling';
      if (daysFromPlanted <= 35) return 'vegetative';
      if (daysFromPlanted <= 42) return 'pre-flower';
      if (daysFromPlanted <= 77) return 'flowering';
      return 'harvest';
    }
    
    // Photoperiod timeline
    if (daysFromPlanted <= 5) return 'germination';
    if (daysFromPlanted <= 21) return 'seedling';
    if (daysFromPlanted <= 56) return 'vegetative'; // Usually manually triggered
    if (daysFromPlanted <= 70) return 'pre-flower';
    if (daysFromPlanted <= 126) return 'flowering';
    return 'harvest';
  }

  static async generateStageSpecificTasks(plant, stage, daysFromPlanted) {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    switch (stage) {
      case 'germination':
        await this.createTaskIfNotExists(plant._id, {
          title: 'Check Germination Progress',
          description: 'Monitor seed germination, ensure proper moisture and temperature',
          type: 'observation',
          dueDate: tomorrow,
          priority: 'high',
          estimatedDuration: 5,
          instructions: 'Check for tap root emergence, maintain 75-80°F temperature and high humidity'
        });
        break;

      case 'seedling':
        await this.createTaskIfNotExists(plant._id, {
          title: 'Seedling Care and Monitoring',
          description: 'Light watering, monitor for first true leaves',
          type: 'watering',
          dueDate: tomorrow,
          priority: 'high',
          estimatedDuration: 10,
          instructions: 'Light watering around seedling, not directly on stem. Monitor for stretching.'
        });
        break;

      case 'vegetative':
        // Daily tasks
        await this.createTaskIfNotExists(plant._id, {
          title: 'Vegetative Growth Check',
          description: 'Monitor growth, check for training opportunities',
          type: 'observation',
          dueDate: tomorrow,
          priority: 'medium',
          estimatedDuration: 15
        });

        // Weekly tasks
        if (daysFromPlanted % 7 === 0) {
          await this.createTaskIfNotExists(plant._id, {
            title: 'Plant Training Session',
            description: 'LST, topping, or defoliation as needed',
            type: 'training',
            dueDate: tomorrow,
            priority: 'medium',
            estimatedDuration: 30,
            instructions: 'Assess plant structure and apply appropriate training techniques'
          });
        }
        break;

      case 'flowering':
        await this.createTaskIfNotExists(plant._id, {
          title: 'Flowering Monitoring',
          description: 'Check bud development and trichome maturity',
          type: 'observation',
          dueDate: tomorrow,
          priority: 'high',
          estimatedDuration: 20,
          instructions: 'Use magnifying glass to check trichomes, monitor for deficiencies'
        });

        // Environmental checks more critical during flowering
        await this.createTaskIfNotExists(plant._id, {
          title: 'Humidity and Air Circulation Check',
          description: 'Ensure proper environmental conditions to prevent mold',
          type: 'environmental-check',
          dueDate: tomorrow,
          priority: 'critical',
          estimatedDuration: 10
        });
        break;

      case 'harvest':
        await this.createTaskIfNotExists(plant._id, {
          title: 'Harvest Readiness Assessment',
          description: 'Final trichome check and harvest preparation',
          type: 'harvest',
          dueDate: today,
          priority: 'critical',
          estimatedDuration: 60,
          instructions: 'Check trichomes are 20-30% amber for peak potency'
        });
        break;
    }
  }

  static async generateMaintenanceTasks(plant) {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);

    // Daily environmental checks
    await this.createTaskIfNotExists(plant._id, {
      title: 'Daily Environmental Check',
      description: 'Monitor temperature, humidity, and pH levels',
      type: 'environmental-check',
      dueDate: tomorrow,
      priority: 'medium',
      estimatedDuration: 10,
      recurring: { enabled: true, frequency: 'daily' }
    });

    // Pest inspection (every 3 days)
    const daysSincePlanted = Math.floor((Date.now() - plant.plantedDate) / (1000 * 60 * 60 * 24));
    if (daysSincePlanted % 3 === 0) {
      await this.createTaskIfNotExists(plant._id, {
        title: 'Pest and Disease Inspection',
        description: 'Check leaves, stems, and soil for signs of pests or disease',
        type: 'pest-inspection',
        dueDate: tomorrow,
        priority: 'medium',
        estimatedDuration: 15,
        instructions: 'Look for spider mites, aphids, fungus gnats, and leaf discoloration'
      });
    }
  }

  static async generateMethodSpecificTasks(plant) {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);

    switch (plant.growingMethod) {
      case 'hydroponic-dwc':
      case 'hydroponic-ebb-flow':
      case 'hydroponic-nft':
        // Daily EC/pH checks for hydro
        await this.createTaskIfNotExists(plant._id, {
          title: 'Hydroponic System Check',
          description: 'Check EC, pH, water level, and system function',
          type: 'ec-check',
          dueDate: tomorrow,
          priority: 'high',
          estimatedDuration: 15,
          instructions: 'Record EC and pH values, top off reservoir if needed',
          recurring: { enabled: true, frequency: 'daily' }
        });

        // Weekly reservoir change
        const weeksSincePlanted = Math.floor((Date.now() - plant.plantedDate) / (1000 * 60 * 60 * 24 * 7));
        if (weeksSincePlanted % 1 === 0) { // Every week
          await this.createTaskIfNotExists(plant._id, {
            title: 'Reservoir Change',
            description: 'Complete nutrient solution change',
            type: 'feeding',
            dueDate: tomorrow,
            priority: 'high',
            estimatedDuration: 45,
            instructions: 'Clean reservoir, mix fresh nutrients, adjust pH and EC'
          });
        }
        break;

      case 'soil':
        // Soil moisture checks
        await this.createTaskIfNotExists(plant._id, {
          title: 'Soil Moisture Check',
          description: 'Test soil moisture and water if needed',
          type: 'watering',
          dueDate: tomorrow,
          priority: 'medium',
          estimatedDuration: 10,
          instructions: 'Check soil 2 inches deep, water when top inch is dry'
        });
        break;

      case 'coco-coir':
        // Coco requires more frequent feeding
        await this.createTaskIfNotExists(plant._id, {
          title: 'Coco Coir Feed/Water',
          description: 'Daily feeding with nutrient solution',
          type: 'feeding',
          dueDate: tomorrow,
          priority: 'high',
          estimatedDuration: 15,
          instructions: 'Feed to 10-20% runoff, EC 1.2-1.6 depending on stage',
          recurring: { enabled: true, frequency: 'daily' }
        });
        break;
    }
  }

  static async createTaskIfNotExists(plantId, taskData) {
    // Check if similar task already exists for today/tomorrow
    const existingTask = await Task.findOne({
      plantId: plantId,
      type: taskData.type,
      dueDate: {
        $gte: new Date(),
        $lte: taskData.dueDate
      },
      completed: false
    });

    if (!existingTask) {
      const task = new Task({
        ...taskData,
        plantId: plantId,
        autoGenerated: true
      });
      await task.save();
      return task;
    }
    return existingTask;
  }

  // Calculate nutrient requirements based on stage and method
  static calculateNutrientSchedule(plant) {
    const stage = plant.currentStage;
    const method = plant.growingMethod;
    
    let baseEC, targetPH;
    
    // Base EC levels by stage
    switch (stage) {
      case 'seedling': baseEC = 0.4; break;
      case 'vegetative': baseEC = 1.2; break;
      case 'pre-flower': baseEC = 1.4; break;
      case 'flowering': baseEC = 1.6; break;
      default: baseEC = 0.8;
    }
    
    // Adjust for growing method
    if (method.includes('hydroponic')) {
      targetPH = 5.8;
    } else if (method === 'soil') {
      targetPH = 6.5;
      baseEC *= 0.8; // Soil holds nutrients longer
    } else if (method === 'coco-coir') {
      targetPH = 6.0;
    }
    
    return { ec: baseEC, ph: targetPH };
  }
}

module.exports = TaskScheduler;
