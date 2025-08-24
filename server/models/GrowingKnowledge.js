const mongoose = require('mongoose');

const growingKnowledgeSchema = new mongoose.Schema({
  category: {
    type: String,
    required: true,
    enum: [
      'hydroponic-systems', 'soil-growing', 'nutrients', 'lighting', 
      'environmental-control', 'plant-training', 'pest-management',
      'harvest-curing', 'genetics', 'troubleshooting'
    ]
  },
  subcategory: String,
  title: { type: String, required: true },
  content: { type: String, required: true },
  applicableStages: [{
    type: String,
    enum: ['seed', 'germination', 'seedling', 'vegetative', 'pre-flower', 'flowering', 'harvest', 'curing']
  }],
  growingMethods: [{
    type: String,
    enum: ['soil', 'hydroponic-dwc', 'hydroponic-ebb-flow', 'hydroponic-nft', 'aeroponic', 'coco-coir', 'mixed-media', 'greenhouse', 'outdoor']
  }],
  difficulty: {
    type: String,
    enum: ['beginner', 'intermediate', 'advanced', 'expert'],
    default: 'beginner'
  },
  timeRequired: String, // e.g., "15 minutes daily", "1 hour weekly"
  materials: [{
    name: String,
    optional: { type: Boolean, default: false },
    alternatives: [String]
  }],
  stepByStep: [{
    step: Number,
    instruction: String,
    tips: [String],
    warnings: [String]
  }],
  expectedResults: String,
  troubleshooting: [{
    problem: String,
    causes: [String],
    solutions: [String]
  }],
  references: [String],
  tags: [String],
  verified: { type: Boolean, default: false },
  rating: { type: Number, min: 1, max: 5 }
}, {
  timestamps: true
});

// Hydroponic Systems Knowledge
const hydroponicSystems = [
  {
    category: 'hydroponic-systems',
    subcategory: 'deep-water-culture',
    title: 'Deep Water Culture (DWC) Setup and Management',
    content: `Deep Water Culture is one of the most effective hydroponic methods for fast growth and high yields. 
    Plants sit in net pots with roots suspended in nutrient-rich, oxygenated water.`,
    applicableStages: ['seedling', 'vegetative', 'flowering'],
    growingMethods: ['hydroponic-dwc'],
    difficulty: 'intermediate',
    timeRequired: '30 minutes daily maintenance',
    materials: [
      { name: 'DWC bucket/reservoir', optional: false },
      { name: 'Air pump', optional: false },
      { name: 'Air stones', optional: false },
      { name: 'Net pots', optional: false },
      { name: 'Growing medium (hydroton/rockwool)', optional: false },
      { name: 'pH meter', optional: false },
      { name: 'EC/TDS meter', optional: false }
    ],
    stepByStep: [
      {
        step: 1,
        instruction: 'Set up reservoir with air pump and air stones for continuous oxygenation',
        tips: ['Use 1 watt of air pump per gallon of nutrient solution'],
        warnings: ['Never let roots sit in stagnant water - they will rot quickly']
      },
      {
        step: 2,
        instruction: 'Mix nutrient solution to appropriate EC/TDS for plant stage',
        tips: ['Start with lower concentrations and increase gradually'],
        warnings: ['Always adjust pH after mixing nutrients']
      }
    ],
    expectedResults: 'Faster growth rates, larger yields, precise nutrient control',
    troubleshooting: [
      {
        problem: 'Root rot (brown, slimy roots)',
        causes: ['Poor oxygenation', 'High water temperature', 'Contaminated reservoir'],
        solutions: ['Increase air flow', 'Keep water temp below 68°F', 'Clean and sterilize system', 'Use beneficial bacteria']
      }
    ],
    tags: ['hydroponic', 'dwc', 'advanced', 'high-yield'],
    verified: true,
    rating: 5
  }
];

// Nutrient Management Knowledge
const nutrientKnowledge = [
  {
    category: 'nutrients',
    subcategory: 'feeding-schedules',
    title: 'Professional Feeding Schedules by Growth Stage',
    content: `Proper nutrition timing is critical for maximizing plant health and yield potential.`,
    applicableStages: ['seedling', 'vegetative', 'flowering'],
    difficulty: 'intermediate',
    stepByStep: [
      {
        step: 1,
        instruction: 'Seedling stage (Weeks 1-2): EC 0.4-0.8, pH 5.8-6.2',
        tips: ['Start with quarter strength nutrients', 'Focus on root development'],
        warnings: ['Over-feeding seedlings causes nutrient burn and stunting']
      },
      {
        step: 2,
        instruction: 'Vegetative stage (Weeks 3-8): EC 0.8-1.4, pH 5.8-6.2',
        tips: ['Higher nitrogen for leaf development', 'Increase feeding frequency'],
        warnings: ['Monitor for nutrient deficiencies - yellowing lower leaves is normal']
      },
      {
        step: 3,
        instruction: 'Flowering stage (Weeks 9+): EC 1.2-1.8, pH 6.0-6.5',
        tips: ['Reduce nitrogen, increase phosphorus and potassium', 'Monitor trichome development'],
        warnings: ['Flush with plain water 1-2 weeks before harvest']
      }
    ],
    tags: ['nutrients', 'feeding', 'schedule', 'ec', 'pH'],
    verified: true,
    rating: 5
  }
];

// Environmental Control
const environmentalKnowledge = [
  {
    category: 'environmental-control',
    title: 'Optimal Environmental Parameters by Stage',
    content: 'Environmental control is crucial for preventing mold, pests, and maximizing growth rates.',
    applicableStages: ['vegetative', 'flowering'],
    stepByStep: [
      {
        step: 1,
        instruction: 'Vegetative: 75-80°F, 60-70% RH, Strong air circulation',
        tips: ['Higher humidity promotes faster growth', 'Ensure fresh air exchange'],
        warnings: ['Poor air circulation leads to mold and pest issues']
      },
      {
        step: 2,
        instruction: 'Flowering: 65-75°F, 40-50% RH, Continued air circulation',
        tips: ['Lower humidity prevents bud mold', 'Temperature swings can increase resin production'],
        warnings: ['High humidity during flowering causes mold - monitor closely']
      }
    ],
    tags: ['environment', 'temperature', 'humidity', 'airflow'],
    verified: true,
    rating: 5
  }
];

// Add more knowledge entries as needed
const allKnowledgeEntries = [
  ...hydroponicSystems,
  ...nutrientKnowledge,
  ...environmentalKnowledge
];

// Export schema and sample data
module.exports = {
  GrowingKnowledge: mongoose.model('GrowingKnowledge', growingKnowledgeSchema),
  knowledgeData: allKnowledgeEntries
};
