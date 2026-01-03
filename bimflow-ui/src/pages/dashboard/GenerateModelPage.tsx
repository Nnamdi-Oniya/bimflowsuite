// src/pages/dashboard/GenerateModelPage.tsx
import React, { useState, useRef, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import "../../assets/GenerateModelDash.css";

// Import placeholder images
import residentialBuilding from "../../assets/images/residential-building.png";
import commercialOffice from "../../assets/images/commercial-office.png";
import highwayBridge from "../../assets/images/highway-bridge.png";
import medicalFacility from "../../assets/images/medical-facility.png";

// --- TYPES & INTERFACES ---
interface BIMDetail {
  materials: string[];
  mep: string[];
  lighting: string;
  structure: string;
  specialFeatures: string[];
}

interface TourStop {
  name: string;
  position: THREE.Vector3;
  target: THREE.Vector3;
  description: string;
  details: BIMDetail;
}

interface TourConfig {
  [key: string]: TourStop[];
}

// --- ULTRA LUXURY TOUR CONFIGURATION ---
const TOUR_DATA: TourConfig = {
  residential: [
    {
      name: "Grand Entrance & Gates",
      position: new THREE.Vector3(0, 3, 25),
      target: new THREE.Vector3(0, 2, 0),
      description: "Impressive automated gates with luxury perimeter fencing and water features",
      details: {
        materials: ["Polished Granite", "Stainless Steel Automation", "Glass Panels"],
        mep: ["Automatic Gate System", "Perimeter Security", "LED Landscape Lighting"],
        lighting: "3000K Warm White, 1000 Lux",
        structure: "Reinforced concrete with steel frame",
        specialFeatures: ["Water Fountain", "Security System", "Intercom"]
      }
    },
    {
      name: "Grand Foyer & Staircase",
      position: new THREE.Vector3(0, 5, 8),
      target: new THREE.Vector3(0, 4, 0),
      description: "Double-height entrance with floating marble staircase and crystal chandelier",
      details: {
        materials: ["Italian Marble", "24K Gold Leaf", "Crystal", "Glass Balustrade"],
        mep: ["Smart Home Control", "Ambient LED Lighting", "Climate Control"],
        lighting: "Dimmable Chandelier, 800 Lux",
        structure: "Floating staircase design",
        specialFeatures: ["Floating Staircase", "Crystal Chandelier", "Marble Flooring"]
      }
    },
    {
      name: "Open Concept Living Area",
      position: new THREE.Vector3(8, 4, 5),
      target: new THREE.Vector3(5, 3, 0),
      description: "Spacious living area with panoramic windows and designer furniture",
      details: {
        materials: ["Oak Hardwood", "Italian Leather", "Silk Curtains", "Glass Walls"],
        mep: ["Built-in Sound System", "Motorized Blinds", "Smart Lighting"],
        lighting: "RGB Ambient LED, 600 Lux",
        structure: "Open plan with structural glass",
        specialFeatures: ["Panoramic Windows", "Home Theater", "Bar Area"]
      }
    },
    {
      name: "Luxury Gourmet Kitchen",
      position: new THREE.Vector3(-8, 3, 5),
      target: new THREE.Vector3(-6, 2, 2),
      description: "Chef's kitchen with marble island, premium appliances, and wine cellar",
      details: {
        materials: ["Marble Countertops", "Stainless Steel", "Custom Cabinetry"],
        mep: ["Professional Ventilation", "Smart Appliances", "Wine Cooling"],
        lighting: "Task + Ambient, 700 Lux",
        structure: "Island with waterfall edges",
        specialFeatures: ["Wine Cellar", "Breakfast Bar", "Premium Appliances"]
      }
    }
  ],
  healthcare: [
    {
      name: "Main Entrance & Emergency",
      position: new THREE.Vector3(0, 4, 20),
      target: new THREE.Vector3(0, 3, 0),
      description: "Modern hospital entrance with emergency bay and digital signage",
      details: {
        materials: ["Glass Curtain Walls", "Stainless Steel", "Granite Flooring"],
        mep: ["Digital Signage", "Emergency Power", "HVAC System"],
        lighting: "Daylight LED, 1000 Lux",
        structure: "Steel frame with glass facade",
        specialFeatures: ["Ambulance Bay", "Reception", "Waiting Area"]
      }
    },
    {
      name: "Advanced MRI Center",
      position: new THREE.Vector3(8, 3, 5),
      target: new THREE.Vector3(6, 2, 3),
      description: "State-of-the-art MRI and diagnostic imaging center",
      details: {
        materials: ["RF Shielding", "Non-magnetic Materials", "Easy-clean Surfaces"],
        mep: ["3T MRI System", "Cooling Systems", "Emergency Stop"],
        lighting: "Controlled Lighting, 500 Lux",
        structure: "Magnetic field containment",
        specialFeatures: ["3T Scanner", "Control Room", "Patient Prep"]
      }
    },
    {
      name: "Surgical Theater",
      position: new THREE.Vector3(-8, 3, 5),
      target: new THREE.Vector3(-6, 2, 3),
      description: "Hybrid operating room with advanced surgical technology",
      details: {
        materials: ["Stainless Steel", "Seamless Flooring", "Antimicrobial Walls"],
        mep: ["HEPA Filtration", "Medical Gases", "Surgical Lighting"],
        lighting: "Shadowless Surgical, 1500 Lux",
        structure: "Vibration isolation",
        specialFeatures: ["Robotic Surgery", "Imaging Integration", "Sterile Zone"]
      }
    },
    {
      name: "Luxury Patient Suites",
      position: new THREE.Vector3(12, 4, -5),
      target: new THREE.Vector3(10, 3, -3),
      description: "Premium patient rooms with hotel-like amenities",
      details: {
        materials: ["Wood Finishes", "Quality Bedding", "Marble Bathrooms"],
        mep: ["Patient Monitoring", "Nurse Call", "Entertainment"],
        lighting: "Tunable White, 400 Lux",
        structure: "Sound-insulated rooms",
        specialFeatures: ["Private Bathroom", "Visitor Area", "Smart Controls"]
      }
    }
  ],
  commercial: [
    {
      name: "Executive Lobby",
      position: new THREE.Vector3(0, 3, 15),
      target: new THREE.Vector3(0, 2, 0),
      description: "Premium corporate reception with digital displays and art installations",
      details: {
        materials: ["Polished Stone", "Glass Partitions", "Premium Finishes"],
        mep: ["Digital Displays", "Climate Control", "Security"],
        lighting: "Architectural LED, 1000 Lux",
        structure: "Double-height space",
        specialFeatures: ["Reception Desk", "Waiting Area", "Art Display"]
      }
    },
    {
      name: "Open Workspace",
      position: new THREE.Vector3(8, 8, 5),
      target: new THREE.Vector3(5, 7, 0),
      description: "Collaborative workspace with ergonomic furniture and natural light",
      details: {
        materials: ["Glass Partitions", "Wood Desks", "Acoustic Panels"],
        mep: ["Power Distribution", "Data Points", "Lighting Control"],
        lighting: "Daylight Harvesting, 500 Lux",
        structure: "Open floor plan",
        specialFeatures: ["Standing Desks", "Collaboration Zones", "Phone Booths"]
      }
    },
    {
      name: "Executive Boardroom",
      position: new THREE.Vector3(-8, 8, 5),
      target: new THREE.Vector3(-6, 7, 2),
      description: "Premium meeting space with advanced AV and video conferencing",
      details: {
        materials: ["Wood Paneling", "Leather Chairs", "Glass Walls"],
        mep: ["Video Conferencing", "Acoustic Treatment", "Climate Control"],
        lighting: "Tunable White, 750 Lux",
        structure: "Sound-insulated enclosure",
        specialFeatures: ["4K Display", "Conference System", "Smart Board"]
      }
    },
    {
      name: "Breakout Lounge",
      position: new THREE.Vector3(0, 8, -8),
      target: new THREE.Vector3(0, 7, -5),
      description: "Relaxation and collaboration space with premium amenities",
      details: {
        materials: ["Comfortable Seating", "Natural Materials", "Artwork"],
        mep: ["Coffee Station", "Charging Points", "Entertainment"],
        lighting: "Relaxed Ambient, 300 Lux",
        structure: "Open flexible space",
        specialFeatures: ["Coffee Bar", "Lounge Seating", "Games Area"]
      }
    }
  ],
  bridge: [
    {
      name: "Main Bridge Deck",
      position: new THREE.Vector3(0, 12, 0),
      target: new THREE.Vector3(0, 10, 5),
      description: "Primary structural deck with advanced composite materials",
      details: {
        materials: ["Reinforced Concrete", "Steel Girders", "Asphalt Pavement"],
        mep: ["Lighting System", "Drainage", "Expansion Joints"],
        lighting: "High Mast, 500 Lux",
        structure: "Composite deck system",
        specialFeatures: ["Anti-icing System", "Traffic Monitoring", "Safety Barriers"]
      }
    },
    {
      name: "Support Pillars",
      position: new THREE.Vector3(0, 8, 8),
      target: new THREE.Vector3(0, 15, 8),
      description: "Reinforced concrete pillars with seismic protection",
      details: {
        materials: ["High-Strength Concrete", "Reinforcement Steel", "Protective Coating"],
        mep: ["Monitoring Sensors", "Lighting", "Drainage"],
        lighting: "Flood Lighting, 400 Lux",
        structure: "Cylindrical reinforced columns",
        specialFeatures: ["Seismic Dampers", "Corrosion Protection", "Structural Monitoring"]
      }
    },
    {
      name: "Suspension System",
      position: new THREE.Vector3(0, 20, 0),
      target: new THREE.Vector3(5, 15, 0),
      description: "Advanced cable-stayed suspension system",
      details: {
        materials: ["High-Tensile Steel", "Galvanized Coating", "Anchorage Systems"],
        mep: ["Tension Monitoring", "Vibration Dampers", "Lighting"],
        lighting: "Architectural LED, 300 Lux",
        structure: "Cable-stayed design",
        specialFeatures: ["Wind Dampers", "Load Monitoring", "Maintenance Access"]
      }
    }
  ]
};

// --- 3D MODEL CREATION FUNCTIONS ---
const createUltraLuxuryMansion = (group: THREE.Group) => {
  // Main mansion structure
  const mainGeometry = new THREE.BoxGeometry(25, 12, 20);
  const mainMaterial = new THREE.MeshStandardMaterial({ 
    color: 0xF5F5DC,
    roughness: 0.4,
    metalness: 0.3
  });
  const mainBuilding = new THREE.Mesh(mainGeometry, mainMaterial);
  mainBuilding.position.y = 6;
  group.add(mainBuilding);

  // Luxury glass windows
  const windowMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x87CEEB,
    transparent: true,
    opacity: 0.2,
    metalness: 0.9,
    roughness: 0.1
  });

  // Panoramic windows
  for (let floor = 0; floor < 3; floor++) {
    for (let i = 0; i < 5; i++) {
      const windowGeometry = new THREE.PlaneGeometry(3, 2.5);
      const window = new THREE.Mesh(windowGeometry, windowMaterial);
      window.position.set(-8 + i * 4, 3 + floor * 3.5, 10.01);
      group.add(window);
    }
  }

  // Grand entrance
  const entranceGeometry = new THREE.BoxGeometry(6, 5, 4);
  const entranceMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  const entrance = new THREE.Mesh(entranceGeometry, entranceMaterial);
  entrance.position.set(0, 2.5, 10);
  group.add(entrance);

  // Luxury roof
  const roofGeometry = new THREE.ConeGeometry(15, 4, 4);
  const roofMaterial = new THREE.MeshStandardMaterial({ color: 0x2F4F4F });
  const roof = new THREE.Mesh(roofGeometry, roofMaterial);
  roof.position.y = 12.5;
  roof.rotation.y = Math.PI / 4;
  group.add(roof);

  // Infinity pool
  const poolGeometry = new THREE.BoxGeometry(10, 1, 5);
  const poolMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x00BFFF,
    transparent: true,
    opacity: 0.6
  });
  const pool = new THREE.Mesh(poolGeometry, poolMaterial);
  pool.position.set(0, 0.5, 15);
  group.add(pool);
};

const createFuturisticHospital = (group: THREE.Group) => {
  // Main hospital complex
  const mainGeometry = new THREE.BoxGeometry(30, 15, 25);
  const mainMaterial = new THREE.MeshStandardMaterial({ 
    color: 0xF8F8FF,
    roughness: 0.5,
    metalness: 0.3
  });
  const mainBuilding = new THREE.Mesh(mainGeometry, mainMaterial);
  mainBuilding.position.y = 7.5;
  group.add(mainBuilding);

  // Glass curtain walls
  const glassGeometry = new THREE.BoxGeometry(29.8, 14.8, 24.8);
  const glassMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x87CEEB,
    transparent: true,
    opacity: 0.2,
    metalness: 0.9,
    roughness: 0.1
  });
  const glass = new THREE.Mesh(glassGeometry, glassMaterial);
  glass.position.y = 7.5;
  group.add(glass);

  // Helipad
  const helipadGeometry = new THREE.CylinderGeometry(4, 4, 0.5, 32);
  const helipadMaterial = new THREE.MeshStandardMaterial({ color: 0x2F4F4F });
  const helipad = new THREE.Mesh(helipadGeometry, helipadMaterial);
  helipad.position.set(0, 15.5, 0);
  group.add(helipad);
};

const createWorldClassOfficeTower = (group: THREE.Group) => {
  // Main office tower
  const towerGeometry = new THREE.BoxGeometry(12, 60, 12);
  const glassMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x87CEEB,
    transparent: true,
    opacity: 0.2,
    metalness: 0.9,
    roughness: 0.1
  });
  const glassTower = new THREE.Mesh(towerGeometry, glassMaterial);
  glassTower.position.y = 30;
  group.add(glassTower);

  // Base structure
  const baseGeometry = new THREE.BoxGeometry(16, 3, 16);
  const baseMaterial = new THREE.MeshStandardMaterial({ color: 0x696969 });
  const base = new THREE.Mesh(baseGeometry, baseMaterial);
  base.position.y = 1.5;
  group.add(base);
};

const createEngineeringBridge = (group: THREE.Group) => {
  // Main bridge deck
  const deckGeometry = new THREE.BoxGeometry(40, 1, 8);
  const deckMaterial = new THREE.MeshStandardMaterial({ color: 0x696969 });
  const deck = new THREE.Mesh(deckGeometry, deckMaterial);
  deck.position.y = 10;
  group.add(deck);

  // Bridge pillars
  const pillarGeometry = new THREE.CylinderGeometry(1, 1, 20, 16);
  const pillarMaterial = new THREE.MeshStandardMaterial({ color: 0x808080 });
  
  for (let i = 0; i < 5; i++) {
    const pillar = new THREE.Mesh(pillarGeometry, pillarMaterial);
    pillar.position.set(-16 + i * 8, 5, 0);
    group.add(pillar);
  }
};

const GenerateModelPage: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    projectType: "",
    projectName: "",
    description: "",
    floors: "",
    area: "",
    location: "",
    budget: "",
    timeline: "",
    specialRequirements: "",
    contactEmail: ""
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [show3DViewer, setShow3DViewer] = useState(false);
  const [tourActive, setTourActive] = useState(false);
  const [tourStep, setTourStep] = useState(0);
  const [currentRoom, setCurrentRoom] = useState<TourStop | null>(null);

  const canvasRef = useRef<HTMLCanvasElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);
  const requestRef = useRef<number>(0);

  const projectTypes = [
    { value: "residential", label: "🏠 Residential Building", description: "Houses, apartments, condominiums", img: residentialBuilding },
    { value: "commercial", label: "🏢 Commercial Office", description: "Office buildings, retail spaces", img: commercialOffice },
    { value: "industrial", label: "🏭 Industrial Facility", description: "Factories, warehouses, plants", img: commercialOffice },
    { value: "healthcare", label: "🏥 Healthcare Facility", description: "Hospitals, clinics, medical centers", img: medicalFacility },
    { value: "educational", label: "🎓 Educational Building", description: "Schools, universities, libraries", img: commercialOffice },
    { value: "bridge", label: "🌉 Bridge Structure", description: "Highway bridges, pedestrian bridges", img: highwayBridge },
    { value: "road", label: "🛣️ Road Infrastructure", description: "Highways, streets, tunnels", img: highwayBridge },
    { value: "other", label: "🔧 Other Project", description: "Custom infrastructure projects", img: commercialOffice }
  ];

  // Create 3D models based on project type
  const createArchitecturalModel = useCallback((type: string) => {
    if (!sceneRef.current) return;

    // Clear previous model
    while(sceneRef.current.children.length > 0) { 
      sceneRef.current.remove(sceneRef.current.children[0]); 
    }

    const buildingGroup = new THREE.Group();

    // Different building types
    switch (type) {
      case 'residential':
        createUltraLuxuryMansion(buildingGroup);
        break;
      case 'healthcare':
        createFuturisticHospital(buildingGroup);
        break;
      case 'commercial':
      case 'industrial':
      case 'educational':
        createWorldClassOfficeTower(buildingGroup);
        break;
      case 'bridge':
      case 'road':
        createEngineeringBridge(buildingGroup);
        break;
      default:
        createUltraLuxuryMansion(buildingGroup);
    }
    sceneRef.current.add(buildingGroup);

    // Enhanced lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    sceneRef.current.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 5);
    directionalLight.castShadow = true;
    sceneRef.current.add(directionalLight);

    // Add grid helper
    const gridHelper = new THREE.GridHelper(40, 40);
    sceneRef.current.add(gridHelper);

    // Adjust camera based on building type
    if (cameraRef.current && controlsRef.current) {
      switch (type) {
        case 'residential':
          cameraRef.current.position.set(25, 12, 25);
          controlsRef.current.target.set(0, 5, 0);
          break;
        case 'healthcare':
          cameraRef.current.position.set(30, 15, 30);
          controlsRef.current.target.set(0, 7, 0);
          break;
        case 'commercial':
          cameraRef.current.position.set(20, 30, 20);
          controlsRef.current.target.set(0, 15, 0);
          break;
        case 'bridge':
          cameraRef.current.position.set(0, 15, 25);
          controlsRef.current.target.set(0, 10, 0);
          break;
        default:
          cameraRef.current.position.set(15, 10, 15);
          controlsRef.current.target.set(0, 5, 0);
      }
      controlsRef.current.update();
    }
  }, []);

  // Initialize Three.js scene
  const initThreeJS = useCallback(() => {
    if (!canvasRef.current) return;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x87CEEB);
    sceneRef.current = scene;

    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(25, 15, 25);
    cameraRef.current = camera;

    const renderer = new THREE.WebGLRenderer({ 
      canvas: canvasRef.current,
      antialias: true,
      alpha: true
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    rendererRef.current = renderer;

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 5;
    controls.maxDistance = 100;
    controlsRef.current = controls;

    // Enhanced lighting setup
    const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 5);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    scene.add(directionalLight);

    // Add grid helper
    const gridHelper = new THREE.GridHelper(40, 40, 0x000000, 0x000000);
    scene.add(gridHelper);

    // Animation loop
    const animate = () => {
      requestRef.current = requestAnimationFrame(animate);
      
      if (tourActive && currentRoom && cameraRef.current && controlsRef.current) {
        // Smoothly interpolate camera position
        cameraRef.current.position.lerp(currentRoom.position, 0.03);
        controlsRef.current.target.lerp(currentRoom.target, 0.03);
      }
      
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    // Handle window resize
    const handleResize = () => {
      if (camera && renderer) {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
      }
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      if (requestRef.current) cancelAnimationFrame(requestRef.current);
    };
  }, [tourActive, currentRoom]);

  // Tour navigation
  const startTour = () => {
    if (!formData.projectType || !TOUR_DATA[formData.projectType]) return;
    
    setTourActive(true);
    setTourStep(0);
    setCurrentRoom(TOUR_DATA[formData.projectType][0]);
  };

  const nextTourStep = () => {
    if (!formData.projectType || !TOUR_DATA[formData.projectType]) return;
    
    const nextStep = tourStep + 1;
    if (nextStep < TOUR_DATA[formData.projectType].length) {
      setTourStep(nextStep);
      setCurrentRoom(TOUR_DATA[formData.projectType][nextStep]);
    } else {
      setTourStep(0);
      setCurrentRoom(TOUR_DATA[formData.projectType][0]);
    }
  };

  const prevTourStep = () => {
    if (!formData.projectType || !TOUR_DATA[formData.projectType]) return;
    
    const prevStep = tourStep - 1;
    if (prevStep >= 0) {
      setTourStep(prevStep);
      setCurrentRoom(TOUR_DATA[formData.projectType][prevStep]);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleProjectTypeChange = (value: string) => {
    setFormData(prev => ({
      ...prev,
      projectType: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));
    setIsSubmitting(false);
    setIsSubmitted(true);
    console.log('Model generation submitted:', formData);
  };

  const handleNewProject = () => {
    setIsSubmitted(false);
    setFormData({
      projectType: "",
      projectName: "",
      description: "",
      floors: "",
      area: "",
      location: "",
      budget: "",
      timeline: "",
      specialRequirements: "",
      contactEmail: ""
    });
    setShow3DViewer(false);
    setTourActive(false);
  };

  const viewIn3D = () => {
    setShow3DViewer(true);
    // Initialize 3D viewer after a small delay to ensure DOM is ready
    setTimeout(() => {
      initThreeJS();
      if (formData.projectType) {
        createArchitecturalModel(formData.projectType);
      }
    }, 100);
  };

  // Mock download functions
  const handleDownload = (fileType: string) => {
    const fileName = `${formData.projectName || 'Project'}.${fileType.toLowerCase()}`;
    let content: string;
    let mimeType: string;
    
    switch (fileType) {
      case 'IFC':
        content = 'ISO-10303-21;\nHEADER;\n/* Generated by BIMFlow Suite */\nENDSEC;\nEND-ISO-10303-21;';
        mimeType = 'application/transfer-ifc';
        break;
      case 'DOCX':
        content = `<html><body><h1>${formData.projectName}</h1><p>${formData.description}</p></body></html>`;
        mimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
        break;
      case 'CSV':
        content = `Project Name,Type,Floors,Area\n${formData.projectName},${formData.projectType},${formData.floors},${formData.area}`;
        mimeType = 'text/csv';
        break;
      case 'PDF':
        content = `%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 44 >>\nstream\nBT\n/F1 24 Tf\n100 700 Td\n(${formData.projectName}) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000010 00000 n \n0000000075 00000 n \n0000000120 00000 n \n0000000200 00000 n \ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n300\n%%EOF`;
        mimeType = 'application/pdf';
        break;
      default:
        return;
    }
    
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const getDescriptionPlaceholder = () => {
    const type = projectTypes.find(t => t.value === formData.projectType);
    if (type) {
      return `Describe your ${type.label.split(' ')[2] || type.value} project in detail. E.g., 'A 5-story ${type.value} with open floor plans, glass facade, and rooftop garden.'`;
    }
    return "Describe your project requirements, features, and any specific needs.";
  };

  // 3D Model Viewer Component
  const ModelViewer: React.FC = () => (
    <div style={{
      position: "fixed",
      top: 0,
      left: 0,
      width: "100%",
      height: "100%",
      background: "rgba(0,0,0,0.95)",
      zIndex: 1000,
      display: "flex",
      flexDirection: "column",
    }}>
      <div style={{
        padding: "1rem",
        background: "#1a1a1a",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        color: "white",
      }}>
        <h3 style={{ margin: 0 }}>3D Model Preview - {formData.projectType}</h3>
        <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          
          {/* Tour Button */}
          {TOUR_DATA[formData.projectType] && (
            <button
              onClick={startTour}
              style={{
                background: tourActive ? "#F8780F" : "#4E443C",
                color: "white",
                border: "none",
                padding: "0.5rem 1rem",
                borderRadius: "4px",
                cursor: "pointer",
                fontWeight: 600,
              }}
            >
              🚶 {tourActive ? "Restart Tour" : "Start Guided Tour"}
            </button>
          )}
          
          <button
            onClick={() => setShow3DViewer(false)}
            style={{
              background: "#EF4444",
              color: "white",
              border: "none",
              padding: "0.5rem 1rem",
              borderRadius: "4px",
              cursor: "pointer",
              fontWeight: 600,
            }}
          >
            Close Viewer
          </button>
        </div>
      </div>
      
      <div style={{ flex: 1, position: "relative" }}>
        <canvas 
          ref={canvasRef} 
          style={{
            width: "100%",
            height: "100%",
            display: "block"
          }}
        />
        
        {/* BIM Insights Overlay */}
        {tourActive && currentRoom && (
          <div style={{
            position: "absolute",
            top: "20px",
            right: "20px",
            width: "350px",
            background: "rgba(255, 255, 255, 0.95)",
            borderRadius: "12px",
            padding: "1.5rem",
            boxShadow: "0 10px 30px rgba(0,0,0,0.2)",
            color: "#333",
          }}>
            <h3 style={{ color: "#F8780F", margin: "0 0 0.5rem" }}>
              {currentRoom.name}
            </h3>
            <p style={{ fontSize: "0.9rem", color: "#666", marginBottom: "1rem" }}>
              {currentRoom.description}
            </p>
            
            <div style={{ fontSize: "0.85rem" }}>
              <div style={{ marginBottom: "0.8rem" }}>
                <strong style={{ color: "#4E443C" }}>🏗️ Materials:</strong>
                {currentRoom.details.materials.join(", ")}
              </div>
              <div style={{ marginBottom: "0.8rem" }}>
                <strong style={{ color: "#4E443C" }}>⚡ MEP Systems:</strong>
                {currentRoom.details.mep.join(", ")}
              </div>
              <div style={{ marginBottom: "0.8rem" }}>
                <strong style={{ color: "#4E443C" }}>💡 Lighting:</strong>
                {currentRoom.details.lighting}
              </div>
              <div style={{ marginBottom: "0.8rem" }}>
                <strong style={{ color: "#4E443C" }}>🎯 Features:</strong>
                {currentRoom.details.specialFeatures.join(", ")}
              </div>
            </div>

            {/* Tour Navigation */}
            <div style={{ 
              display: "flex", 
              justifyContent: "space-between", 
              marginTop: "1.5rem",
              borderTop: "1px solid #eee",
              paddingTop: "1rem"
            }}>
              <button 
                onClick={prevTourStep}
                disabled={tourStep === 0}
                style={{
                  background: "#eee",
                  border: "none",
                  padding: "0.5rem 1rem",
                  borderRadius: "6px",
                  cursor: tourStep === 0 ? "not-allowed" : "pointer",
                  opacity: tourStep === 0 ? 0.5 : 1
                }}
              >
                ← Prev
              </button>
              <span style={{ alignSelf: "center", fontWeight: "bold", color: "#888" }}>
                {tourStep + 1} / {TOUR_DATA[formData.projectType]?.length || 0}
              </span>
              <button 
                onClick={nextTourStep}
                style={{
                  background: "#F8780F",
                  color: "white",
                  border: "none",
                  padding: "0.5rem 1rem",
                  borderRadius: "6px",
                  cursor: "pointer"
                }}
              >
                Next →
              </button>
            </div>
          </div>
        )}

        {/* Viewer Controls Help */}
        <div style={{
          position: "absolute",
          bottom: "20px",
          left: "20px",
          background: "rgba(0,0,0,0.7)",
          color: "white",
          padding: "1rem",
          borderRadius: "8px",
          fontSize: "0.9rem"
        }}>
          <div>🎮 Controls:</div>
          <div>• Left click + drag: Rotate</div>
          <div>• Right click + drag: Pan</div>
          <div>• Scroll: Zoom</div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="generate-page">
      {/* 3D Model Viewer */}
      {show3DViewer && <ModelViewer />}

      <div className="generate-header">
        <h1 className="page-title">Generate Model</h1>
        <p className="page-subtitle">Provide your project details to auto-generate compliant BIM models with 3D preview.</p>
      </div>
      
      <div className="generate-preview">
        <h2>Live Preview</h2>
        <div className="preview-container">
          {isSubmitting ? (
            <div className="preview-loading">
              <div className="spinner-large"></div>
              <p>Generating 3D preview...</p>
            </div>
          ) : isSubmitted ? (
            <div className="preview-success">
              <div className="model-preview">
                <div className="model-icon">🏗️</div>
                <p>Your model is ready! Use the download buttons below to get your files.</p>
                <div className="quick-stats">
                  <div className="stat-item">
                    <span className="stat-value">{formData.floors || 'N/A'}</span>
                    <span className="stat-label">Floors</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-value">{formData.area || 'N/A'} m²</span>
                    <span className="stat-label">Area</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-value">{formData.budget ? `$${parseInt(formData.budget).toLocaleString()}` : 'N/A'}</span>
                    <span className="stat-label">Budget</span>
                  </div>
                </div>
                <button 
                  onClick={viewIn3D}
                  className="btn btn--primary"
                  style={{ marginTop: '1rem' }}
                >
                  👁️ View in 3D
                </button>
              </div>
            </div>
          ) : formData.projectType ? (
            <div className="preview-placeholder">
              <div className="placeholder-content">
                <img 
                  src={projectTypes.find(t => t.value === formData.projectType)?.img} 
                  alt="Project type" 
                  className="demo-image"
                  style={{ width: '100%', height: '200px', objectFit: 'cover', borderRadius: '12px' }}
                />
                <p>Ready to generate your {formData.projectType} project</p>
                <p className="placeholder-sub">Fill in details and click generate to see 3D model</p>
              </div>
            </div>
          ) : (
            <div className="preview-placeholder">
              <div className="placeholder-content">
                <div className="placeholder-icon">📐</div>
                <p>Model preview will appear here once you generate your project.</p>
                <p className="placeholder-sub">Select project type and enter details to see a live 3D render.</p>
              </div>
            </div>
          )}
        </div>
      </div>
      
      <div className="generate-form">
        {isSubmitted ? (
          <div className="success-state">
            <div className="success-icon">🎉</div>
            <h2>Project Generated Successfully!</h2>
            <p>Your BIM model has been created based on your specifications. Download your files below.</p>
            
            <div className="submission-details">
              <h3>Project Summary</h3>
              <div className="details-grid">
                <div className="detail-item">
                  <span className="detail-label">Project Name:</span>
                  <span className="detail-value">{formData.projectName}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Project Type:</span>
                  <span className="detail-value">
                    {projectTypes.find(type => type.value === formData.projectType)?.label}
                  </span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Location:</span>
                  <span className="detail-value">{formData.location || 'Not specified'}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Timeline:</span>
                  <span className="detail-value">{formData.timeline || 'Not specified'}</span>
                </div>
              </div>
            </div>

            <div className="download-section">
              <h3>Download Your Generated Files</h3>
              <p className="download-subtitle">Choose the format that works best for your workflow</p>
              <div className="download-grid">
                <button className="download-btn ifc" onClick={() => handleDownload('IFC')}>
                  <div className="download-icon">📐</div>
                  <div className="download-info">
                    <strong>IFC Model</strong>
                    <span>3D BIM Model (IFC 4.3)</span>
                  </div>
                </button>
                <button className="download-btn docx" onClick={() => handleDownload('DOCX')}>
                  <div className="download-icon">📄</div>
                  <div className="download-info">
                    <strong>Project Document</strong>
                    <span>Detailed specifications (DOCX)</span>
                  </div>
                </button>
                <button className="download-btn csv" onClick={() => handleDownload('CSV')}>
                  <div className="download-icon">📊</div>
                  <div className="download-info">
                    <strong>Quantity Takeoff</strong>
                    <span>Material & cost data (CSV)</span>
                  </div>
                </button>
                <button className="download-btn pdf" onClick={() => handleDownload('PDF')}>
                  <div className="download-icon">📕</div>
                  <div className="download-info">
                    <strong>Compliance Report</strong>
                    <span>Code validation summary (PDF)</span>
                  </div>
                </button>
              </div>
            </div>

            <div className="next-steps">
              <h3>What Happens Next?</h3>
              <div className="steps-timeline">
                <div className="step">
                  <div className="step-number">1</div>
                  <div className="step-content">
                    <strong>Files Ready</strong>
                    <p>Your downloads are prepared with full compliance checks</p>
                  </div>
                </div>
                <div className="step">
                  <div className="step-number">2</div>
                  <div className="step-content">
                    <strong>Import to Software</strong>
                    <p>Load IFC into Revit, ArchiCAD, or any BIM tool</p>
                  </div>
                </div>
                <div className="step">
                  <div className="step-number">3</div>
                  <div className="step-content">
                    <strong>Customize & Build</strong>
                    <p>Refine your model and proceed to construction</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="success-actions">
              <button className="btn btn--secondary" onClick={handleNewProject}>
                Create Another Project
              </button>
              <button className="btn btn--primary" onClick={() => navigate('/dashboard')}>
                Back to Dashboard
              </button>
            </div>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            {/* Project Type Selection */}
            <div className="form-section">
              <h2>Select Project Type</h2>
              <div className="project-types">
                {projectTypes.map((type) => {
                  const icon = type.label.match(/^[^\s]+/)?.[0] || '🔧';
                  const cleanLabel = type.label.replace(icon, '').trim();
                  return (
                    <button
                      key={type.value}
                      type="button"
                      className={`project-type-btn ${formData.projectType === type.value ? 'active' : ''}`}
                      onClick={() => handleProjectTypeChange(type.value)}
                    >
                      <div className="project-icon">{icon}</div>
                      <h3>{cleanLabel}</h3>
                      <p>{type.description}</p>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Project Basics */}
            <div className="form-section">
              <h2>Project Basics</h2>
              <div className="form-grid">
                <div className="form-group">
                  <label htmlFor="projectName" className="form-label">
                    Project Name *
                  </label>
                  <input
                    type="text"
                    id="projectName"
                    name="projectName"
                    value={formData.projectName}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="e.g., Downtown Office Tower"
                    required
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="contactEmail" className="form-label">
                    Contact Email *
                  </label>
                  <input
                    type="email"
                    id="contactEmail"
                    name="contactEmail"
                    value={formData.contactEmail}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="your.email@company.com"
                    required
                  />
                </div>
              </div>
            </div>

            {/* Project Description */}
            <div className="form-section">
              <h2>Describe Your Project</h2>
              <div className="form-group">
                <label htmlFor="description" className="form-label">
                  Project Description *
                </label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  className="form-textarea"
                  placeholder={getDescriptionPlaceholder()}
                  rows={4}
                  maxLength={500}
                  required
                />
                <div className="character-count">
                  {formData.description.length}/500 characters
                </div>
              </div>
            </div>

            {/* Specifications */}
            <div className="form-section">
              <h2>Specifications</h2>
              <div className="form-grid">
                <div className="form-group">
                  <label htmlFor="floors" className="form-label">
                    Number of Floors
                  </label>
                  <input
                    type="number"
                    id="floors"
                    name="floors"
                    value={formData.floors}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="e.g., 10"
                    min="1"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="area" className="form-label">
                    Total Area (m²)
                  </label>
                  <input
                    type="number"
                    id="area"
                    name="area"
                    value={formData.area}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="e.g., 5000"
                    min="1"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="location" className="form-label">
                    Location
                  </label>
                  <input
                    type="text"
                    id="location"
                    name="location"
                    value={formData.location}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="e.g., New York, USA"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="budget" className="form-label">
                    Estimated Budget ($)
                  </label>
                  <input
                    type="number"
                    id="budget"
                    name="budget"
                    value={formData.budget}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="e.g., 5000000"
                    min="0"
                  />
                </div>
              </div>
            </div>

            {/* Timeline & Requirements */}
            <div className="form-section">
              <h2>Timeline & Requirements</h2>
              <div className="form-grid">
                <div className="form-group">
                  <label htmlFor="timeline" className="form-label">
                    Project Timeline
                  </label>
                  <select
                    id="timeline"
                    name="timeline"
                    value={formData.timeline}
                    onChange={handleInputChange}
                    className="form-select"
                  >
                    <option value="">Select timeline</option>
                    <option value="1-3 months">1-3 months</option>
                    <option value="3-6 months">3-6 months</option>
                    <option value="6-12 months">6-12 months</option>
                    <option value="12+ months">12+ months</option>
                  </select>
                </div>
              </div>
              <div className="form-group">
                <label htmlFor="specialRequirements" className="form-label">
                  Special Requirements
                </label>
                <textarea
                  id="specialRequirements"
                  name="specialRequirements"
                  value={formData.specialRequirements}
                  onChange={handleInputChange}
                  className="form-textarea"
                  placeholder="Any specific building codes, sustainability requirements, accessibility needs, or other special considerations..."
                  rows={3}
                />
              </div>
            </div>

            {/* Form Actions */}
            <div className="form-actions">
              <button 
                type="button" 
                className="btn btn--secondary"
                onClick={() => navigate('/dashboard')}
              >
                ← Back to Dashboard
              </button>
              <button 
                type="submit" 
                className="btn btn--primary generate-btn"
                disabled={isSubmitting || !formData.projectType || !formData.projectName || !formData.description.trim() || !formData.contactEmail}
              >
                {isSubmitting ? (
                  <>
                    <div className="loading-spinner"></div>
                    Generating Model...
                  </>
                ) : (
                  '🚀 Generate BIM Model'
                )}
              </button>
            </div>

            {/* Features Highlight */}
            <div className="features-highlight">
              <h3>What You'll Get</h3>
              <div className="features-grid">
                <div className="feature">
                  <span className="feature-icon">📐</span>
                  <div>
                    <strong>IFC 4.3 Compliant Model</strong>
                    <p>Industry-standard file format ready for any BIM software</p>
                  </div>
                </div>
                <div className="feature">
                  <span className="feature-icon">🛡️</span>
                  <div>
                    <strong>Automated Compliance</strong>
                    <p>Built-in checks for building codes and regulations</p>
                  </div>
                </div>
                <div className="feature">
                  <span className="feature-icon">👁️</span>
                  <div>
                    <strong>3D Model Preview</strong>
                    <p>Interactive 3D visualization with guided tours</p>
                  </div>
                </div>
              </div>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default GenerateModelPage;