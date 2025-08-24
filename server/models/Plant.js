const mongoose = require('mongoose');

const plantSchema = new mongoose.Schema({
  name: { type: String, required: true },
  strain: { 
    type: String, 
    required: true,
    enum: ['indica', 'sativa', 'hybrid', 'ruderalis', 'photoperiod', 'autoflower']
  },
  plantType: {
    type: String,
    required: true,
    enum: ['tomato', 'pepper', 'herb', 'leafy-green', 'flower', 'medicinal', 'other']
  },
  currentStage: {
    type: String,
    enum: ['seed', 'germination', 'seedling', 'vegetative', 'pre-flower', 'flowering', 'harvest', 'curing'],
    default: 'seed'
  },
  plantedDate: { type: Date, required: true },
  expectedHarvestDate: { type: Date },
  growingMethod: {
    type: String,
    enum: ['soil', 'hydroponic-dwc', 'hydroponic-ebb-flow', 'hydroponic-nft', 'aeroponic', 'coco-coir', 'mixed-media', 'greenhouse', 'outdoor'],
    required: true
  },
  lightCycle: {
    vegetative: { on: Number, off: Number }, // e.g., {on: 18, off: 6}
    flowering: { on: Number, off: Number }   // e.g., {on: 12, off: 12}
  },
  environmentalNeeds: {
    temperature: {
      min: { type: Number, default: 65 },
      max: { type: Number, default: 80 },
      optimal: { type: Number, default: 72 }
    },
    humidity: {
      vegetative: { type: Number, default: 60 },
      flowering: { type: Number, default: 45 }
    },
    ph: {
      min: { type: Number, default: 6.0 },
      max: { type: Number, default: 6.8 },
      optimal: { type: Number, default: 6.3 }
    },
    ec: {
      seedling: { type: Number, default: 0.4 },
      vegetative: { type: Number, default: 1.2 },
      flowering: { type: Number, default: 1.6 }
    }
  },
  nutrients: [{
    stage: String,
    schedule: [{
      week: Number,
      npk: { n: Number, p: Number, k: Number },
      supplements: [{ name: String, amount: Number, unit: String }],
      ec: Number,
      ph: Number
    }]
  }],
  notes: [{ 
    date: { type: Date, default: Date.now },
    content: String,
    type: { type: String, enum: ['observation', 'task', 'issue', 'milestone'] }
  }],
  photos: [{
    url: String,
    date: { type: Date, default: Date.now },
    stage: String,
    description: String
  }],
  isActive: { type: Boolean, default: true },
  location: String,
  container: {
    type: String,
    size: String,
    material: String
  }
}, {
  timestamps: true
});

// Calculate days in current stage
plantSchema.virtual('daysInStage').get(function() {
  const stageChanges = this.notes.filter(note => note.type === 'milestone');
  const lastStageChange = stageChanges[stageChanges.length - 1];
  const startDate = lastStageChange ? lastStageChange.date : this.plantedDate;
  return Math.floor((Date.now() - startDate) / (1000 * 60 * 60 * 24));
});

module.exports = mongoose.model('Plant', plantSchema);
