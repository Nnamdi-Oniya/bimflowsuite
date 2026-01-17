import React, { useState, useRef, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import "../assets/DemoPage.css";

// Import placeholder images
import heroBim from "../assets/images/hero-bim2.jpg";
import residentialBuilding from "../assets/images/residential-building.png";
import commercialOffice from "../assets/images/commercial-office.png";
import highwayBridge from "../assets/images/highway-bridge.png";
import medicalFacility from "../assets/images/medical-facility.png";

// --- TYPES & INTERFACES ---
interface Example {
  id: string;
  title: string;
  img: string;
  prompt: string;
}

interface FileFormat {
  name: string;
  extension: string;
  type: string;
  icon: string;
  description: string;
  isBinary?: boolean;
}

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
  mansion: [
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
    },
    {
      name: "Private Cinema Room",
      position: new THREE.Vector3(0, 3, -8),
      target: new THREE.Vector3(0, 2, -5),
      description: "State-of-the-art home theater with recliner seats and acoustic treatment",
      details: {
        materials: ["Acoustic Panels", "Velvet Upholstery", "Carpet Flooring"],
        mep: ["4K Projection", "Dolby Atmos", "Motorized Screen"],
        lighting: "Theater Mode, 50 Lux",
        structure: "Sound-insulated room",
        specialFeatures: ["Recliner Seats", "Acoustic Walls", "Popcorn Machine"]
      }
    },
    {
      name: "Master Suite",
      position: new THREE.Vector3(12, 4, -5),
      target: new THREE.Vector3(10, 3, -3),
      description: "Luxurious master bedroom with walk-in closet and spa bathroom",
      details: {
        materials: ["Wool Carpet", "Marble Bathroom", "Custom Wardrobes"],
        mep: ["Heated Floors", "Steam Shower", "Smart Mirrors"],
        lighting: "Warm White, 400 Lux",
        structure: "Suite layout with privacy",
        specialFeatures: ["Walk-in Closet", "Spa Bathroom", "Private Balcony"]
      }
    },
    {
      name: "Personal Gym & Spa",
      position: new THREE.Vector3(-12, 3, -5),
      target: new THREE.Vector3(-10, 2, -3),
      description: "Fully equipped gym with premium equipment and relaxation area",
      details: {
        materials: ["Rubber Flooring", "Mirror Walls", "Teak Sauna"],
        mep: ["HVAC Special", "Audio System", "Lighting Control"],
        lighting: "Cool White, 500 Lux",
        structure: "Reinforced floor for equipment",
        specialFeatures: ["Cardio Zone", "Weight Area", "Sauna", "Jacuzzi"]
      }
    },
    {
      name: "Infinity Pool & Gardens",
      position: new THREE.Vector3(0, 2, -20),
      target: new THREE.Vector3(0, 1, -15),
      description: "Stunning infinity pool with landscaped gardens and outdoor kitchen",
      details: {
        materials: ["Glass Tile Pool", "Teak Decking", "Natural Stone"],
        mep: ["Pool Heating", "LED Lighting", "Outdoor Kitchen"],
        lighting: "Color Changing, 300 Lux",
        structure: "Cantilevered pool design",
        specialFeatures: ["Infinity Edge", "Water Features", "Fire Pit", "Gazebo"]
      }
    },
    {
      name: "Rooftop Lounge",
      position: new THREE.Vector3(0, 12, 0),
      target: new THREE.Vector3(0, 11, 5),
      description: "Premium rooftop entertainment area with city views",
      details: {
        materials: ["Weather-resistant Furniture", "Glass Railings", "Outdoor Kitchen"],
        mep: ["Bar Facilities", "Entertainment System", "Lighting"],
        lighting: "Mood Lighting, 200 Lux",
        structure: "Reinforced roof structure",
        specialFeatures: ["360° Views", "Bar Area", "Lounge Seating", "Green Wall"]
      }
    }
  ],
  hospital: [
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
    },
    {
      name: "ICU & Critical Care",
      position: new THREE.Vector3(-12, 4, -5),
      target: new THREE.Vector3(-10, 3, -3),
      description: "Intensive care unit with advanced life support systems",
      details: {
        materials: ["Antimicrobial Surfaces", "Glass Partitions", "Medical Grade"],
        mep: ["Ventilators", "Monitors", "Emergency Power"],
        lighting: "24/7 Controlled, 600 Lux",
        structure: "Open plan with isolation",
        specialFeatures: ["Vital Monitoring", "Central Station", "Isolation Rooms"]
      }
    },
    {
      name: "Research Laboratory",
      position: new THREE.Vector3(0, 3, -12),
      target: new THREE.Vector3(0, 2, -8),
      description: "Advanced medical research and testing facilities",
      details: {
        materials: ["Chemical-resistant", "Lab Grade", "Easy-clean"],
        mep: ["Fume Hoods", "Special Gases", "Pure Water"],
        lighting: "High CRI, 800 Lux",
        structure: "Reinforced lab benches",
        specialFeatures: ["Bio-safety Cabinets", "Analytical Equipment", "Cold Storage"]
      }
    }
  ],
  office: [
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
    },
    {
      name: "Server Room",
      position: new THREE.Vector3(12, 3, -5),
      target: new THREE.Vector3(10, 2, -3),
      description: "Secure data center with enterprise-level infrastructure",
      details: {
        materials: ["Raised Floor", "Rack Systems", "Cable Management"],
        mep: ["Cooling System", "UPS", "Fire Suppression"],
        lighting: "Emergency + Task, 400 Lux",
        structure: "Secure access control",
        specialFeatures: ["Server Racks", "Network Infrastructure", "Monitoring"]
      }
    },
    {
      name: "Rooftop Terrace",
      position: new THREE.Vector3(0, 15, 0),
      target: new THREE.Vector3(0, 14, 5),
      description: "Premium outdoor space for meetings and relaxation",
      details: {
        materials: ["Outdoor Furniture", "Planters", "Weather-resistant"],
        mep: ["Lighting", "Power Outlets", "WiFi"],
        lighting: "Mood Lighting, 200 Lux",
        structure: "Reinforced deck",
        specialFeatures: ["City Views", "Meeting Pods", "Green Space"]
      }
    }
  ]
};

// --- ULTRA LUXURY MANSION CREATION ---
const createUltraLuxuryMansion = (group: THREE.Group) => {
  // Main mansion structure - 3 floors
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

  // Panoramic windows on all floors
  for (let floor = 0; floor < 3; floor++) {
    for (let i = 0; i < 5; i++) {
      const windowGeometry = new THREE.PlaneGeometry(3, 2.5);
      const window = new THREE.Mesh(windowGeometry, windowMaterial);
      window.position.set(-8 + i * 4, 3 + floor * 3.5, 10.01);
      group.add(window);
    }
  }

  // Grand entrance with double doors
  const entranceGeometry = new THREE.BoxGeometry(6, 5, 4);
  const entranceMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  const entrance = new THREE.Mesh(entranceGeometry, entranceMaterial);
  entrance.position.set(0, 2.5, 10);
  group.add(entrance);

  // Luxury roof design
  const roofGeometry = new THREE.ConeGeometry(15, 4, 4);
  const roofMaterial = new THREE.MeshStandardMaterial({ color: 0x2F4F4F });
  const roof = new THREE.Mesh(roofGeometry, roofMaterial);
  roof.position.y = 12.5;
  roof.rotation.y = Math.PI / 4;
  group.add(roof);

  // Balconies on each floor
  for (let floor = 0; floor < 3; floor++) {
    const balconyGeometry = new THREE.BoxGeometry(8, 0.3, 3);
    const balconyMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
    const balcony = new THREE.Mesh(balconyGeometry, balconyMaterial);
    balcony.position.set(0, 2 + floor * 3.5, 8);
    group.add(balcony);

    // Glass railings
    const railingGeometry = new THREE.BoxGeometry(8, 1, 0.1);
    const railingMaterial = new THREE.MeshStandardMaterial({ 
      color: 0x87CEEB,
      transparent: true,
      opacity: 0.3
    });
    const railing = new THREE.Mesh(railingGeometry, railingMaterial);
    railing.position.set(0, 2.5 + floor * 3.5, 6.5);
    group.add(railing);
  }

  // Infinity pool at the front
  const poolGeometry = new THREE.BoxGeometry(10, 1, 5);
  const poolMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x00BFFF,
    transparent: true,
    opacity: 0.6
  });
  const pool = new THREE.Mesh(poolGeometry, poolMaterial);
  pool.position.set(0, 0.5, 15);
  group.add(pool);

  // Pool deck with premium seating
  const deckGeometry = new THREE.BoxGeometry(16, 0.2, 8);
  const deckMaterial = new THREE.MeshStandardMaterial({ color: 0xDEB887 });
  const deck = new THREE.Mesh(deckGeometry, deckMaterial);
  deck.position.set(0, 0.1, 15);
  group.add(deck);

  // Pool loungers
  const loungerGeometry = new THREE.BoxGeometry(2, 0.1, 0.8);
  const loungerMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  for (let i = 0; i < 4; i++) {
    const lounger = new THREE.Mesh(loungerGeometry, loungerMaterial);
    lounger.position.set(-6 + i * 4, 0.2, 17);
    lounger.rotation.z = Math.PI * 0.1;
    group.add(lounger);
  }

  // Water features - cascading fountain
  const fountainGeometry = new THREE.CylinderGeometry(2, 2, 0.5, 32);
  const fountainMaterial = new THREE.MeshStandardMaterial({ color: 0x00BFFF });
  const fountain = new THREE.Mesh(fountainGeometry, fountainMaterial);
  fountain.position.set(0, 0.3, 12);
  group.add(fountain);

  // Palm trees and landscaping
  for (let i = 0; i < 8; i++) {
    const angle = (i / 8) * Math.PI * 2;
    const distance = 18;
    const treeGeometry = new THREE.ConeGeometry(1.2, 4, 8);
    const treeMaterial = new THREE.MeshStandardMaterial({ color: 0x228B22 });
    const tree = new THREE.Mesh(treeGeometry, treeMaterial);
    tree.position.set(
      Math.cos(angle) * distance,
      2,
      Math.sin(angle) * distance
    );
    group.add(tree);
  }

  // Perimeter fencing with LED lighting
  for (let i = 0; i < 16; i++) {
    const angle = (i / 16) * Math.PI * 2;
    const distance = 22;
    const postGeometry = new THREE.BoxGeometry(0.3, 2, 0.3);
    const postMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
    const post = new THREE.Mesh(postGeometry, postMaterial);
    post.position.set(
      Math.cos(angle) * distance,
      1,
      Math.sin(angle) * distance
    );
    group.add(post);

    // LED lights on posts
    const lightGeometry = new THREE.SphereGeometry(0.2, 8, 8);
    const lightMaterial = new THREE.MeshStandardMaterial({ 
      color: 0xFFFF00,
      emissive: 0xFFFF00,
      emissiveIntensity: 0.5
    });
    const light = new THREE.Mesh(lightGeometry, lightMaterial);
    light.position.set(
      Math.cos(angle) * distance,
      2,
      Math.sin(angle) * distance
    );
    group.add(light);
  }

  // Automatic stainless steel gates
  const gateGeometry = new THREE.BoxGeometry(6, 2, 0.2);
  const gateMaterial = new THREE.MeshStandardMaterial({ color: 0xC0C0C0 });
  const leftGate = new THREE.Mesh(gateGeometry, gateMaterial);
  const rightGate = new THREE.Mesh(gateGeometry, gateMaterial);
  leftGate.position.set(-3, 1, 22);
  rightGate.position.set(3, 1, 22);
  group.add(leftGate);
  group.add(rightGate);

  // Perfectly paved driveway
  const drivewayGeometry = new THREE.BoxGeometry(8, 0.1, 12);
  const drivewayMaterial = new THREE.MeshStandardMaterial({ color: 0x333333 });
  const driveway = new THREE.Mesh(drivewayGeometry, drivewayMaterial);
  driveway.position.set(0, 0.05, 6);
  group.add(driveway);
};

// ULTRA LUXURY MANSION INTERIOR
const createUltraLuxuryMansionInterior = (group: THREE.Group) => {
  const wallThickness = 0.3;
  const buildingWidth = 25;
  const buildingDepth = 20;
  const buildingHeight = 12;

  // Create hollow mansion structure
  const walls = [
    // Left wall
    { pos: [-buildingWidth/2 + wallThickness/2, buildingHeight/2, 0], size: [wallThickness, buildingHeight, buildingDepth] },
    // Right wall
    { pos: [buildingWidth/2 - wallThickness/2, buildingHeight/2, 0], size: [wallThickness, buildingHeight, buildingDepth] },
    // Back wall
    { pos: [0, buildingHeight/2, -buildingDepth/2 + wallThickness/2], size: [buildingWidth, buildingHeight, wallThickness] },
  ];

  walls.forEach(wall => {
    const geometry = new THREE.BoxGeometry(wall.size[0], wall.size[1], wall.size[2]);
    const material = new THREE.MeshStandardMaterial({ color: 0xF5F5DC });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(wall.pos[0] as number, wall.pos[1] as number, wall.pos[2] as number);
    group.add(mesh);
  });

  // Marble flooring
  const floorGeometry = new THREE.BoxGeometry(buildingWidth, 0.1, buildingDepth);
  const floorMaterial = new THREE.MeshStandardMaterial({ 
    color: 0xFFFFFF,
    roughness: 0.2,
    metalness: 0.1
  });
  const floor = new THREE.Mesh(floorGeometry, floorMaterial);
  floor.position.y = 0.05;
  group.add(floor);

  // Luxury ceiling with decorative elements
  const ceilingGeometry = new THREE.BoxGeometry(buildingWidth, 0.1, buildingDepth);
  const ceilingMaterial = new THREE.MeshStandardMaterial({ color: 0xF8F8FF });
  const ceiling = new THREE.Mesh(ceilingGeometry, ceilingMaterial);
  ceiling.position.y = buildingHeight - 0.05;
  group.add(ceiling);

  // 🏰 GRAND FOYER & FLOATING STAIRCASE
  const chandelierGeometry = new THREE.SphereGeometry(1.2, 16, 16);
  const chandelierMaterial = new THREE.MeshStandardMaterial({ 
    color: 0xFFFF00,
    emissive: 0xFFFF00,
    emissiveIntensity: 0.8
  });
  const chandelier = new THREE.Mesh(chandelierGeometry, chandelierMaterial);
  chandelier.position.set(0, 10, 0);
  group.add(chandelier);

  // Floating staircase
  const stairGeometry = new THREE.BoxGeometry(2.5, 0.2, 0.8);
  const stairMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  for (let i = 0; i < 15; i++) {
    const stair = new THREE.Mesh(stairGeometry, stairMaterial);
    stair.position.set(-6, 0.1 + i * 0.25, 2 + i * 0.4);
    group.add(stair);
  }

  // Glass stair railing
  const stairRailingGeometry = new THREE.BoxGeometry(0.1, 1, 8);
  const stairRailingMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x87CEEB,
    transparent: true,
    opacity: 0.3
  });
  const stairRailing = new THREE.Mesh(stairRailingGeometry, stairRailingMaterial);
  stairRailing.position.set(-7, 2, 5);
  group.add(stairRailing);

  // 🛋️ LUXURY LIVING AREA
  const livingRoomWall = new THREE.BoxGeometry(wallThickness, buildingHeight, 8);
  const livingRoomWallMesh = new THREE.Mesh(livingRoomWall, new THREE.MeshStandardMaterial({ color: 0xE8E8E8 }));
  livingRoomWallMesh.position.set(8, buildingHeight/2, -4);
  group.add(livingRoomWallMesh);

  // Luxury sofa set
  const sofaGeometry = new THREE.BoxGeometry(4, 0.8, 1.5);
  const sofaMaterial = new THREE.MeshStandardMaterial({ color: 0x8B0000 });
  const sofa = new THREE.Mesh(sofaGeometry, sofaMaterial);
  sofa.position.set(12, 0.5, -1);
  group.add(sofa);

  const sofa2 = new THREE.Mesh(sofaGeometry, sofaMaterial);
  sofa2.position.set(12, 0.5, -7);
  sofa2.rotation.y = Math.PI;
  group.add(sofa2);

  // Designer coffee table
  const coffeeTableGeometry = new THREE.CylinderGeometry(1.5, 1.5, 0.1, 32);
  const coffeeTableMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  const coffeeTable = new THREE.Mesh(coffeeTableGeometry, coffeeTableMaterial);
  coffeeTable.position.set(12, 0.2, -4);
  group.add(coffeeTable);

  // Luxury rug
  const rugGeometry = new THREE.PlaneGeometry(6, 4);
  const rugMaterial = new THREE.MeshStandardMaterial({ color: 0x800000 });
  const rug = new THREE.Mesh(rugGeometry, rugMaterial);
  rug.rotation.x = -Math.PI / 2;
  rug.position.set(12, 0.06, -4);
  group.add(rug);

  // Wall-mounted 4K TV
  const tvGeometry = new THREE.BoxGeometry(3, 1.7, 0.1);
  const tvMaterial = new THREE.MeshStandardMaterial({ color: 0x000000 });
  const tv = new THREE.Mesh(tvGeometry, tvMaterial);
  tv.position.set(8.1, 3, -4);
  group.add(tv);

  // TV screen
  const screenGeometry = new THREE.PlaneGeometry(2.8, 1.5);
  const screenMaterial = new THREE.MeshStandardMaterial({ color: 0x0000FF });
  const screen = new THREE.Mesh(screenGeometry, screenMaterial);
  screen.position.set(8.15, 3, -4);
  group.add(screen);

  // Grand piano
  const pianoGeometry = new THREE.BoxGeometry(2.5, 0.8, 1.8);
  const pianoMaterial = new THREE.MeshStandardMaterial({ color: 0x000000 });
  const piano = new THREE.Mesh(pianoGeometry, pianoMaterial);
  piano.position.set(4, 0.5, -1);
  group.add(piano);

  // 🎬 PRIVATE CINEMA ROOM
  const cinemaWall = new THREE.BoxGeometry(8, buildingHeight, wallThickness);
  const cinemaWallMesh = new THREE.Mesh(cinemaWall, new THREE.MeshStandardMaterial({ color: 0x000000 }));
  cinemaWallMesh.position.set(0, buildingHeight/2, -8);
  group.add(cinemaWallMesh);

  // Cinema screen
  const cinemaScreenGeometry = new THREE.PlaneGeometry(6, 3);
  const cinemaScreenMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  const cinemaScreen = new THREE.Mesh(cinemaScreenGeometry, cinemaScreenMaterial);
  cinemaScreen.position.set(0, 3, -7.9);
  group.add(cinemaScreen);

  // Recliner seats
  const reclinerGeometry = new THREE.BoxGeometry(0.8, 0.6, 1);
  const reclinerMaterial = new THREE.MeshStandardMaterial({ color: 0x800000 });
  
  for (let row = 0; row < 3; row++) {
    for (let seat = 0; seat < 4; seat++) {
      const recliner = new THREE.Mesh(reclinerGeometry, reclinerMaterial);
      recliner.position.set(-3 + seat * 2, 0.4, -5 + row * 1.5);
      group.add(recliner);
    }
  }

  // Acoustic wall panels
  const panelGeometry = new THREE.BoxGeometry(1.5, 2, 0.1);
  const panelMaterial = new THREE.MeshStandardMaterial({ color: 0x2F4F4F });
  
  for (let i = 0; i < 4; i++) {
    const panel = new THREE.Mesh(panelGeometry, panelMaterial);
    panel.position.set(-6 + i * 4, 3, -7.9);
    group.add(panel);
  }

  // 🍽️ GOURMET KITCHEN
  const kitchenWall = new THREE.BoxGeometry(wallThickness, buildingHeight, 8);
  const kitchenWallMesh = new THREE.Mesh(kitchenWall, new THREE.MeshStandardMaterial({ color: 0xE8E8E8 }));
  kitchenWallMesh.position.set(-8, buildingHeight/2, -4);
  group.add(kitchenWallMesh);

  // Kitchen island with marble
  const islandGeometry = new THREE.BoxGeometry(3, 0.9, 1.5);
  const islandMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  const island = new THREE.Mesh(islandGeometry, islandMaterial);
  island.position.set(-12, 0.5, -4);
  group.add(island);

  // Premium appliances
  const fridgeGeometry = new THREE.BoxGeometry(1, 1.8, 0.8);
  const fridgeMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  const fridge = new THREE.Mesh(fridgeGeometry, fridgeMaterial);
  fridge.position.set(-14, 0.9, -6);
  group.add(fridge);

  const stoveGeometry = new THREE.BoxGeometry(0.8, 0.3, 0.8);
  const stoveMaterial = new THREE.MeshStandardMaterial({ color: 0x000000 });
  const stove = new THREE.Mesh(stoveGeometry, stoveMaterial);
  stove.position.set(-10, 0.8, -6);
  group.add(stove);

  // Wine cellar entrance
  const wineCellarGeometry = new THREE.BoxGeometry(2, 2, 0.1);
  const wineCellarMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  const wineCellar = new THREE.Mesh(wineCellarGeometry, wineCellarMaterial);
  wineCellar.position.set(-14, 1, -2);
  group.add(wineCellar);

  // Cabinets
  const cabinetGeometry = new THREE.BoxGeometry(4, 1, 0.5);
  const cabinetMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  const cabinet = new THREE.Mesh(cabinetGeometry, cabinetMaterial);
  cabinet.position.set(-12, 1.5, -6.5);
  group.add(cabinet);

  // 🏋️ PERSONAL GYM
  const gymWall = new THREE.BoxGeometry(8, buildingHeight, wallThickness);
  const gymWallMesh = new THREE.Mesh(gymWall, new THREE.MeshStandardMaterial({ color: 0xE8E8E8 }));
  gymWallMesh.position.set(-12, buildingHeight/2, -8);
  group.add(gymWallMesh);

  // Gym equipment
  const treadmillGeometry = new THREE.BoxGeometry(1.5, 0.8, 0.8);
  const treadmillMaterial = new THREE.MeshStandardMaterial({ color: 0x4169E1 });
  const treadmill = new THREE.Mesh(treadmillGeometry, treadmillMaterial);
  treadmill.position.set(-14, 0.5, -5);
  group.add(treadmill);

  const weightsGeometry = new THREE.BoxGeometry(1, 0.3, 0.5);
  const weightsMaterial = new THREE.MeshStandardMaterial({ color: 0x696969 });
  const weights = new THREE.Mesh(weightsGeometry, weightsMaterial);
  weights.position.set(-10, 0.2, -5);
  group.add(weights);

  // Mirror wall
  const mirrorGeometry = new THREE.PlaneGeometry(6, 3);
  const mirrorMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x888888,
    metalness: 0.9,
    roughness: 0.1
  });
  const mirror = new THREE.Mesh(mirrorGeometry, mirrorMaterial);
  mirror.position.set(-8, 2, -7.9);
  group.add(mirror);

  // 🛏️ MASTER SUITE
  const masterWall = new THREE.BoxGeometry(10, buildingHeight, wallThickness);
  const masterWallMesh = new THREE.Mesh(masterWall, new THREE.MeshStandardMaterial({ color: 0xE8E8E8 }));
  masterWallMesh.position.set(12, buildingHeight/2, -5);
  group.add(masterWallMesh);

  // King size bed
  const bedGeometry = new THREE.BoxGeometry(3, 0.6, 2.5);
  const bedMaterial = new THREE.MeshStandardMaterial({ color: 0x4B0082 });
  const bed = new THREE.Mesh(bedGeometry, bedMaterial);
  bed.position.set(14, 0.4, -7);
  group.add(bed);

  // Bedside tables
  const bedsideGeometry = new THREE.BoxGeometry(0.6, 0.8, 0.6);
  const bedsideMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  const bedside1 = new THREE.Mesh(bedsideGeometry, bedsideMaterial);
  const bedside2 = new THREE.Mesh(bedsideGeometry, bedsideMaterial);
  bedside1.position.set(12, 0.5, -7);
  bedside2.position.set(16, 0.5, -7);
  group.add(bedside1);
  group.add(bedside2);

  // Bedside lamps
  const lampGeometry = new THREE.CylinderGeometry(0.1, 0.1, 0.4, 16);
  const lampMaterial = new THREE.MeshStandardMaterial({ color: 0xFFD700 });
  const lamp1 = new THREE.Mesh(lampGeometry, lampMaterial);
  const lamp2 = new THREE.Mesh(lampGeometry, lampMaterial);
  lamp1.position.set(12, 1.2, -7);
  lamp2.position.set(16, 1.2, -7);
  group.add(lamp1);
  group.add(lamp2);

  // Walk-in closet
  const closetGeometry = new THREE.BoxGeometry(4, 2, 0.3);
  const closetMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  const closet = new THREE.Mesh(closetGeometry, closetMaterial);
  closet.position.set(10, 1, -5.5);
  group.add(closet);

  // LED-lit shelves in closet
  const shelfGeometry = new THREE.BoxGeometry(3.5, 0.1, 0.2);
  const shelfMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  for (let i = 0; i < 4; i++) {
    const shelf = new THREE.Mesh(shelfGeometry, shelfMaterial);
    shelf.position.set(10, 0.5 + i * 0.4, -5.4);
    group.add(shelf);
  }

  // Spa bathroom
  const bathtubGeometry = new THREE.BoxGeometry(2, 0.6, 1);
  const bathtubMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  const bathtub = new THREE.Mesh(bathtubGeometry, bathtubMaterial);
  bathtub.position.set(16, 0.4, -3);
  group.add(bathtub);

  // Bathroom vanity
  const vanityGeometry = new THREE.BoxGeometry(2, 0.9, 0.6);
  const vanityMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  const vanity = new THREE.Mesh(vanityGeometry, vanityMaterial);
  vanity.position.set(12, 0.5, -3);
  group.add(vanity);

  // Additional bedrooms
  for (let room = 0; room < 2; room++) {
    const bedroomWall = new THREE.BoxGeometry(8, buildingHeight, wallThickness);
    const bedroomWallMesh = new THREE.Mesh(bedroomWall, new THREE.MeshStandardMaterial({ color: 0xE8E8E8 }));
    bedroomWallMesh.position.set(4 + room * 8, buildingHeight/2, -8);
    group.add(bedroomWallMesh);

    // Bed in each bedroom
    const roomBedGeometry = new THREE.BoxGeometry(2, 0.5, 1.8);
    const roomBedMaterial = new THREE.MeshStandardMaterial({ color: 0x4B0082 });
    const roomBed = new THREE.Mesh(roomBedGeometry, roomBedMaterial);
    roomBed.position.set(4 + room * 8, 0.3, -10);
    group.add(roomBed);

    // Wardrobe in each bedroom
    const wardrobeGeometry = new THREE.BoxGeometry(1.5, 2, 0.3);
    const wardrobeMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
    const wardrobe = new THREE.Mesh(wardrobeGeometry, wardrobeMaterial);
    wardrobe.position.set(2 + room * 8, 1, -7.5);
    group.add(wardrobe);
  }

  // 🌿 ROOFTOP LOUNGE
  const rooftopGeometry = new THREE.BoxGeometry(20, 0.1, 16);
  const rooftopMaterial = new THREE.MeshStandardMaterial({ color: 0x228B22 });
  const rooftop = new THREE.Mesh(rooftopGeometry, rooftopMaterial);
  rooftop.position.set(0, 12, 0);
  group.add(rooftop);

  // Rooftop furniture
  const rooftopChairGeometry = new THREE.CylinderGeometry(0.3, 0.3, 0.8, 16);
  const rooftopChairMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  
  for (let i = 0; i < 6; i++) {
    const angle = (i / 6) * Math.PI * 2;
    const chair = new THREE.Mesh(rooftopChairGeometry, rooftopChairMaterial);
    chair.position.set(
      Math.cos(angle) * 4,
      12.1,
      Math.sin(angle) * 3
    );
    group.add(chair);
  }

  const rooftopTableGeometry = new THREE.CylinderGeometry(1, 1, 0.1, 32);
  const rooftopTableMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  const rooftopTable = new THREE.Mesh(rooftopTableGeometry, rooftopTableMaterial);
  rooftopTable.position.set(0, 12.1, 0);
  group.add(rooftopTable);

  // Green wall
  const greenWallGeometry = new THREE.BoxGeometry(8, 2, 0.1);
  const greenWallMaterial = new THREE.MeshStandardMaterial({ color: 0x228B22 });
  const greenWall = new THREE.Mesh(greenWallGeometry, greenWallMaterial);
  greenWall.position.set(0, 13, 7);
  group.add(greenWall);

  // Bar area
  const barGeometry = new THREE.BoxGeometry(3, 1, 1);
  const barMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  const bar = new THREE.Mesh(barGeometry, barMaterial);
  bar.position.set(5, 12.6, 5);
  group.add(bar);
};

// FUTURISTIC LUXURY HOSPITAL
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

  // Emergency wing
  const emergencyGeometry = new THREE.BoxGeometry(12, 8, 15);
  const emergencyMaterial = new THREE.MeshStandardMaterial({ color: 0xF8F8FF });
  const emergency = new THREE.Mesh(emergencyGeometry, emergencyMaterial);
  emergency.position.set(-16, 4, 0);
  group.add(emergency);

  // Helipad on roof
  const helipadGeometry = new THREE.CylinderGeometry(4, 4, 0.5, 32);
  const helipadMaterial = new THREE.MeshStandardMaterial({ color: 0x2F4F4F });
  const helipad = new THREE.Mesh(helipadGeometry, helipadMaterial);
  helipad.position.set(0, 15.5, 0);
  group.add(helipad);

  // Red cross symbol
  const crossGeometry1 = new THREE.BoxGeometry(6, 0.5, 1.5);
  const crossGeometry2 = new THREE.BoxGeometry(1.5, 0.5, 6);
  const crossMaterial = new THREE.MeshStandardMaterial({ color: 0xFF0000 });
  
  const cross1 = new THREE.Mesh(crossGeometry1, crossMaterial);
  const cross2 = new THREE.Mesh(crossGeometry2, crossMaterial);
  cross1.position.set(0, 16, 0);
  cross2.position.set(0, 16, 0);
  group.add(cross1);
  group.add(cross2);

  // Glass elevators
  const elevatorGeometry = new THREE.BoxGeometry(2, 15, 2);
  const elevatorMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x87CEEB,
    transparent: true,
    opacity: 0.3
  });
  
  const elevator1 = new THREE.Mesh(elevatorGeometry, elevatorMaterial);
  const elevator2 = new THREE.Mesh(elevatorGeometry, elevatorMaterial);
  elevator1.position.set(12, 7.5, 8);
  elevator2.position.set(12, 7.5, -8);
  group.add(elevator1);
  group.add(elevator2);

  // Solar panels on roof
  const solarPanelGeometry = new THREE.BoxGeometry(3, 0.1, 2);
  const solarPanelMaterial = new THREE.MeshStandardMaterial({ color: 0x2F4F4F });
  
  for (let i = 0; i < 4; i++) {
    for (let j = 0; j < 3; j++) {
      const panel = new THREE.Mesh(solarPanelGeometry, solarPanelMaterial);
      panel.position.set(-8 + i * 5, 15.1, -5 + j * 5);
      panel.rotation.x = Math.PI * 0.3;
      group.add(panel);
    }
  }

  // Ambulance bays
  const bayGeometry = new THREE.BoxGeometry(4, 0.2, 8);
  const bayMaterial = new THREE.MeshStandardMaterial({ color: 0x00FF00 });
  
  for (let i = 0; i < 3; i++) {
    const bay = new THREE.Mesh(bayGeometry, bayMaterial);
    bay.position.set(-20, 0.1, -8 + i * 8);
    group.add(bay);
  }

  // Backup generators
  const generatorGeometry = new THREE.BoxGeometry(3, 2, 2);
  const generatorMaterial = new THREE.MeshStandardMaterial({ color: 0x696969 });
  const generator = new THREE.Mesh(generatorGeometry, generatorMaterial);
  generator.position.set(20, 1, 0);
  group.add(generator);

  // Landscaped surroundings
  for (let i = 0; i < 20; i++) {
    const angle = (i / 20) * Math.PI * 2;
    const distance = 35;
    const treeGeometry = new THREE.ConeGeometry(1, 3, 8);
    const treeMaterial = new THREE.MeshStandardMaterial({ color: 0x228B22 });
    const tree = new THREE.Mesh(treeGeometry, treeMaterial);
    tree.position.set(
      Math.cos(angle) * distance,
      1.5,
      Math.sin(angle) * distance
    );
    group.add(tree);
  }

  // Parking lot
  const parkingGeometry = new THREE.BoxGeometry(25, 0.1, 20);
  const parkingMaterial = new THREE.MeshStandardMaterial({ color: 0x444444 });
  const parking = new THREE.Mesh(parkingGeometry, parkingMaterial);
  parking.position.set(20, 0.05, 20);
  group.add(parking);

  // Parking spaces
  const spaceGeometry = new THREE.BoxGeometry(2.5, 0.1, 5);
  const spaceMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  
  for (let row = 0; row < 3; row++) {
    for (let col = 0; col < 4; col++) {
      const space = new THREE.Mesh(spaceGeometry, spaceMaterial);
      space.position.set(15 + col * 3, 0.1, 15 + row * 6);
      group.add(space);
    }
  }
};

// FUTURISTIC HOSPITAL INTERIOR
const createFuturisticHospitalInterior = (group: THREE.Group) => {
  const wallThickness = 0.3;
  const buildingWidth = 30;
  const buildingDepth = 25;
  const buildingHeight = 15;

  // Create hollow hospital structure
  const walls = [
    // Left wall
    { pos: [-buildingWidth/2 + wallThickness/2, buildingHeight/2, 0], size: [wallThickness, buildingHeight, buildingDepth] },
    // Right wall
    { pos: [buildingWidth/2 - wallThickness/2, buildingHeight/2, 0], size: [wallThickness, buildingHeight, buildingDepth] },
    // Back wall
    { pos: [0, buildingHeight/2, -buildingDepth/2 + wallThickness/2], size: [buildingWidth, buildingHeight, wallThickness] },
  ];

  walls.forEach(wall => {
    const geometry = new THREE.BoxGeometry(wall.size[0], wall.size[1], wall.size[2]);
    const material = new THREE.MeshStandardMaterial({ color: 0xF8F8FF });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(wall.pos[0] as number, wall.pos[1] as number, wall.pos[2] as number);
    group.add(mesh);
  });

  // Hospital flooring
  const floorGeometry = new THREE.BoxGeometry(buildingWidth, 0.1, buildingDepth);
  const floorMaterial = new THREE.MeshStandardMaterial({ color: 0x696969 });
  const floor = new THREE.Mesh(floorGeometry, floorMaterial);
  floor.position.y = 0.05;
  group.add(floor);

  // 🏥 MRI CENTER
  const mriRoomWall = new THREE.BoxGeometry(wallThickness, buildingHeight, 8);
  const mriRoomWallMesh = new THREE.Mesh(mriRoomWall, new THREE.MeshStandardMaterial({ color: 0xE8E8E8 }));
  mriRoomWallMesh.position.set(8, buildingHeight/2, -4);
  group.add(mriRoomWallMesh);

  // MRI Machine
  const mriGeometry = new THREE.CylinderGeometry(1.2, 1.2, 2.5, 32);
  const mriMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  const mri = new THREE.Mesh(mriGeometry, mriMaterial);
  mri.position.set(12, 1.3, -4);
  group.add(mri);

  // Patient table
  const mriTableGeometry = new THREE.BoxGeometry(2, 0.1, 0.8);
  const mriTableMaterial = new THREE.MeshStandardMaterial({ color: 0x2F4F4F });
  const mriTable = new THREE.Mesh(mriTableGeometry, mriTableMaterial);
  mriTable.position.set(10, 0.2, -4);
  group.add(mriTable);

  // Control room window
  const controlWindowGeometry = new THREE.PlaneGeometry(4, 2);
  const controlWindowMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x87CEEB,
    transparent: true,
    opacity: 0.3
  });
  const controlWindow = new THREE.Mesh(controlWindowGeometry, controlWindowMaterial);
  controlWindow.position.set(8, 2, -0.5);
  group.add(controlWindow);

  // 🏥 SURGICAL THEATER
  const surgeryWall = new THREE.BoxGeometry(wallThickness, buildingHeight, 8);
  const surgeryWallMesh = new THREE.Mesh(surgeryWall, new THREE.MeshStandardMaterial({ color: 0xE8E8E8 }));
  surgeryWallMesh.position.set(-8, buildingHeight/2, -4);
  group.add(surgeryWallMesh);

  // Operating table
  const surgeryTableGeometry = new THREE.BoxGeometry(2.5, 0.4, 1);
  const surgeryTableMaterial = new THREE.MeshStandardMaterial({ color: 0x32CD32 });
  const surgeryTable = new THREE.Mesh(surgeryTableGeometry, surgeryTableMaterial);
  surgeryTable.position.set(-12, 0.4, -4);
  group.add(surgeryTable);

  // Surgical lights
  const surgeryLightGeometry = new THREE.SphereGeometry(0.8, 16, 16);
  const surgeryLightMaterial = new THREE.MeshStandardMaterial({ 
    color: 0xFFFF00,
    emissive: 0xFFFF00,
    emissiveIntensity: 0.6
  });
  const surgeryLight = new THREE.Mesh(surgeryLightGeometry, surgeryLightMaterial);
  surgeryLight.position.set(-12, 8, -4);
  group.add(surgeryLight);

  // Anesthesia machine
  const anesthesiaGeometry = new THREE.BoxGeometry(1, 1.5, 0.8);
  const anesthesiaMaterial = new THREE.MeshStandardMaterial({ color: 0x4169E1 });
  const anesthesia = new THREE.Mesh(anesthesiaGeometry, anesthesiaMaterial);
  anesthesia.position.set(-14, 0.8, -5);
  group.add(anesthesia);

  // 🏥 INTENSIVE CARE UNIT
  const icuWall = new THREE.BoxGeometry(12, buildingHeight, wallThickness);
  const icuWallMesh = new THREE.Mesh(icuWall, new THREE.MeshStandardMaterial({ color: 0xE8E8E8 }));
  icuWallMesh.position.set(-4, buildingHeight/2, -8);
  group.add(icuWallMesh);

  // ICU beds with monitoring
  const icuBedGeometry = new THREE.BoxGeometry(2, 0.3, 1);
  const icuBedMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  
  for (let i = 0; i < 4; i++) {
    const bed = new THREE.Mesh(icuBedGeometry, icuBedMaterial);
    bed.position.set(-8 + i * 4, 0.3, -10);
    group.add(bed);

    // Patient monitors
    const monitorGeometry = new THREE.BoxGeometry(0.4, 0.5, 0.1);
    const monitorMaterial = new THREE.MeshStandardMaterial({ color: 0x000000 });
    const monitor = new THREE.Mesh(monitorGeometry, monitorMaterial);
    monitor.position.set(-8 + i * 4, 0.9, -9.2);
    group.add(monitor);

    // IV poles
    const ivPoleGeometry = new THREE.CylinderGeometry(0.05, 0.05, 1.5, 16);
    const ivPoleMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
    const ivPole = new THREE.Mesh(ivPoleGeometry, ivPoleMaterial);
    ivPole.position.set(-8 + i * 4 + 0.5, 0.8, -9.5);
    group.add(ivPole);
  }

  // Central monitoring station
  const stationGeometry = new THREE.BoxGeometry(6, 1, 2);
  const stationMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  const station = new THREE.Mesh(stationGeometry, stationMaterial);
  station.position.set(0, 0.6, -12);
  group.add(station);

  // 🏥 RESEARCH LABORATORY
  const labWall = new THREE.BoxGeometry(12, buildingHeight, wallThickness);
  const labWallMesh = new THREE.Mesh(labWall, new THREE.MeshStandardMaterial({ color: 0xE8E8E8 }));
  labWallMesh.position.set(4, buildingHeight/2, -8);
  group.add(labWallMesh);

  // Lab benches
  const labBenchGeometry = new THREE.BoxGeometry(2, 0.9, 0.8);
  const labBenchMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  
  for (let i = 0; i < 3; i++) {
    const bench = new THREE.Mesh(labBenchGeometry, labBenchMaterial);
    bench.position.set(0 + i * 3, 0.5, -10);
    group.add(bench);
  }

  // Laboratory equipment
  const equipmentGeometry = new THREE.BoxGeometry(0.8, 1.2, 0.8);
  const equipmentMaterial = new THREE.MeshStandardMaterial({ color: 0x4169E1 });
  
  for (let i = 0; i < 2; i++) {
    const equipment = new THREE.Mesh(equipmentGeometry, equipmentMaterial);
    equipment.position.set(8 + i * 2, 0.7, -10);
    group.add(equipment);
  }

  // 🏥 LUXURY PATIENT ROOMS
  const patientWall = new THREE.BoxGeometry(wallThickness, buildingHeight, 6);
  const patientWallMesh = new THREE.Mesh(patientWall, new THREE.MeshStandardMaterial({ color: 0xE8E8E8 }));
  patientWallMesh.position.set(14, buildingHeight/2, -3);
  group.add(patientWallMesh);

  // Luxury patient beds
  const patientBedGeometry = new THREE.BoxGeometry(2, 0.3, 1);
  const patientBedMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  
  for (let i = 0; i < 2; i++) {
    const bed = new THREE.Mesh(patientBedGeometry, patientBedMaterial);
    bed.position.set(16, 0.3, -5 + i * 4);
    group.add(bed);

    // Bedside tables
    const patientBedsideGeometry = new THREE.BoxGeometry(0.5, 0.6, 0.5);
    const patientBedsideMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
    const patientBedside = new THREE.Mesh(patientBedsideGeometry, patientBedsideMaterial);
    patientBedside.position.set(14.5, 0.4, -5 + i * 4);
    group.add(patientBedside);

    // Patient monitors
    const patientMonitorGeometry = new THREE.BoxGeometry(0.3, 0.4, 0.1);
    const patientMonitorMaterial = new THREE.MeshStandardMaterial({ color: 0x000000 });
    const patientMonitor = new THREE.Mesh(patientMonitorGeometry, patientMonitorMaterial);
    patientMonitor.position.set(16, 0.8, -4.2 + i * 4);
    group.add(patientMonitor);

    // Visitor chairs
    const visitorChairGeometry = new THREE.CylinderGeometry(0.3, 0.3, 0.8, 16);
    const visitorChairMaterial = new THREE.MeshStandardMaterial({ color: 0x800000 });
    const chair = new THREE.Mesh(visitorChairGeometry, visitorChairMaterial);
    chair.position.set(14, 0.4, -5 + i * 4);
    group.add(chair);
  }

  // Private bathrooms
  const bathroomGeometry = new THREE.BoxGeometry(2, 2, 0.1);
  const bathroomMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  const bathroom = new THREE.Mesh(bathroomGeometry, bathroomMaterial);
  bathroom.position.set(18, 1, -1);
  group.add(bathroom);

  // 🏥 PHARMACY & DIAGNOSTIC AREA
  const pharmacyCounterGeometry = new THREE.BoxGeometry(4, 1, 1);
  const pharmacyCounterMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  const pharmacyCounter = new THREE.Mesh(pharmacyCounterGeometry, pharmacyCounterMaterial);
  pharmacyCounter.position.set(-14, 0.6, 5);
  group.add(pharmacyCounter);

  // Medication shelves
  const shelfGeometry = new THREE.BoxGeometry(6, 2, 0.3);
  const shelfMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  const shelf = new THREE.Mesh(shelfGeometry, shelfMaterial);
  shelf.position.set(-16, 1, 3);
  group.add(shelf);

  // Digital signage
  const signGeometry = new THREE.PlaneGeometry(3, 1);
  const signMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x0000FF,
    emissive: 0x0000FF,
    emissiveIntensity: 0.3
  });
  const sign = new THREE.Mesh(signGeometry, signMaterial);
  sign.position.set(0, 8, 12);
  group.add(sign);

  // Waiting lounge with premium furniture
  const waitingChairGeometry = new THREE.CylinderGeometry(0.3, 0.3, 0.8, 16);
  const waitingChairMaterial = new THREE.MeshStandardMaterial({ color: 0x800000 });
  
  for (let i = -3; i <= 3; i += 2) {
    const chair = new THREE.Mesh(waitingChairGeometry, waitingChairMaterial);
    chair.position.set(i, 0.4, 8);
    group.add(chair);
  }

  const waitingTableGeometry = new THREE.CylinderGeometry(1, 1, 0.1, 32);
  const waitingTableMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  const waitingTable = new THREE.Mesh(waitingTableGeometry, waitingTableMaterial);
  waitingTable.position.set(0, 0.2, 6);
  group.add(waitingTable);

  // Staff lounge
  const staffSofaGeometry = new THREE.BoxGeometry(2, 0.6, 1);
  const staffSofaMaterial = new THREE.MeshStandardMaterial({ color: 0x8B0000 });
  const staffSofa = new THREE.Mesh(staffSofaGeometry, staffSofaMaterial);
  staffSofa.position.set(-10, 0.4, 10);
  group.add(staffSofa);

  // Radiology area with CT scanner
  const ctScannerGeometry = new THREE.CylinderGeometry(1, 1, 2, 32);
  const ctScannerMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  const ctScanner = new THREE.Mesh(ctScannerGeometry, ctScannerMaterial);
  ctScanner.position.set(5, 1, 5);
  group.add(ctScanner);
};

// WORLD-CLASS CORPORATE OFFICE TOWER
const createWorldClassOfficeTower = (group: THREE.Group) => {
  // Main office tower - 20 floors
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

  // Structural frame
  const frameGeometry = new THREE.BoxGeometry(12.2, 60, 12.2);
  const frameMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x2F4F4F,
    wireframe: true
  });
  const frame = new THREE.Mesh(frameGeometry, frameMaterial);
  frame.position.y = 30;
  group.add(frame);

  // Base structure
  const baseGeometry = new THREE.BoxGeometry(16, 3, 16);
  const baseMaterial = new THREE.MeshStandardMaterial({ color: 0x696969 });
  const base = new THREE.Mesh(baseGeometry, baseMaterial);
  base.position.y = 1.5;
  group.add(base);

  // Glass elevators
  const elevatorGeometry = new THREE.BoxGeometry(1.5, 58, 1.5);
  const elevatorMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x87CEEB,
    transparent: true,
    opacity: 0.3
  });
  
  const elevator1 = new THREE.Mesh(elevatorGeometry, elevatorMaterial);
  const elevator2 = new THREE.Mesh(elevatorGeometry, elevatorMaterial);
  elevator1.position.set(5, 30, 5);
  elevator2.position.set(-5, 30, -5);
  group.add(elevator1);
  group.add(elevator2);

  // Rooftop terrace structure
  const rooftopGeometry = new THREE.BoxGeometry(14, 1, 14);
  const rooftopMaterial = new THREE.MeshStandardMaterial({ color: 0x228B22 });
  const rooftop = new THREE.Mesh(rooftopGeometry, rooftopMaterial);
  rooftop.position.y = 60.5;
  group.add(rooftop);

  // Visible floor layouts (each floor visible through glass)
  for (let floor = 0; floor < 20; floor++) {
    const floorGeometry = new THREE.BoxGeometry(11.8, 0.1, 11.8);
    const floorMaterial = new THREE.MeshStandardMaterial({ color: 0x2F4F4F });
    const floorMesh = new THREE.Mesh(floorGeometry, floorMaterial);
    floorMesh.position.y = 3 + floor * 3;
    group.add(floorMesh);

    // Core structure
    const coreGeometry = new THREE.BoxGeometry(4, 2.8, 4);
    const coreMaterial = new THREE.MeshStandardMaterial({ color: 0x666666 });
    const core = new THREE.Mesh(coreGeometry, coreMaterial);
    core.position.y = 3 + floor * 3;
    group.add(core);
  }

  // Surrounding plaza
  const plazaGeometry = new THREE.BoxGeometry(40, 0.2, 40);
  const plazaMaterial = new THREE.MeshStandardMaterial({ color: 0x888888 });
  const plaza = new THREE.Mesh(plazaGeometry, plazaMaterial);
  plaza.position.y = 0.1;
  group.add(plaza);

  // Decorative features
  const featureGeometry = new THREE.CylinderGeometry(3, 3, 0.5, 32);
  const featureMaterial = new THREE.MeshStandardMaterial({ color: 0x00BFFF });
  
  for (let i = -1; i <= 1; i += 2) {
    for (let j = -1; j <= 1; j += 2) {
      const feature = new THREE.Mesh(featureGeometry, featureMaterial);
      feature.position.set(i * 12, 0.3, j * 12);
      group.add(feature);
    }
  }

  // Landscaping
  for (let i = 0; i < 16; i++) {
    const angle = (i / 16) * Math.PI * 2;
    const distance = 25;
    const treeGeometry = new THREE.ConeGeometry(1, 4, 8);
    const treeMaterial = new THREE.MeshStandardMaterial({ color: 0x228B22 });
    const tree = new THREE.Mesh(treeGeometry, treeMaterial);
    tree.position.set(
      Math.cos(angle) * distance,
      2,
      Math.sin(angle) * distance
    );
    group.add(tree);
  }
};

// WORLD-CLASS OFFICE INTERIOR
const createWorldClassOfficeInterior = (group: THREE.Group) => {
  const wallThickness = 0.3;
  const buildingSize = 12;
  const buildingHeight = 60;

  // Glass walls (mostly transparent)
  const glassMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x87CEEB,
    transparent: true,
    opacity: 0.1,
    metalness: 0.9,
    roughness: 0.1
  });

  const walls = [
    // Left wall
    { pos: [-buildingSize/2 + wallThickness/2, buildingHeight/2, 0], size: [wallThickness, buildingHeight, buildingSize] },
    // Right wall
    { pos: [buildingSize/2 - wallThickness/2, buildingHeight/2, 0], size: [wallThickness, buildingHeight, buildingSize] },
    // Back wall
    { pos: [0, buildingHeight/2, -buildingSize/2 + wallThickness/2], size: [buildingSize, buildingHeight, wallThickness] },
  ];

  walls.forEach(wall => {
    const geometry = new THREE.BoxGeometry(wall.size[0], wall.size[1], wall.size[2]);
    const mesh = new THREE.Mesh(geometry, glassMaterial);
    mesh.position.set(wall.pos[0] as number, wall.pos[1] as number, wall.pos[2] as number);
    group.add(mesh);
  });

  // Floor - premium finish
  const floorGeometry = new THREE.BoxGeometry(buildingSize, 0.1, buildingSize);
  const floorMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x2F4F4F,
    roughness: 0.4,
    metalness: 0.2
  });
  const floor = new THREE.Mesh(floorGeometry, floorMaterial);
  floor.position.y = 0.05;
  group.add(floor);

  // 🏢 EXECUTIVE FLOOR (Top level)
  // Executive office with glass walls
  const executiveDeskGeometry = new THREE.BoxGeometry(2.5, 0.8, 1.2);
  const executiveDeskMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  const executiveDesk = new THREE.Mesh(executiveDeskGeometry, executiveDeskMaterial);
  executiveDesk.position.set(0, 0.5, 0);
  group.add(executiveDesk);

  // Executive chair
  const executiveChairGeometry = new THREE.CylinderGeometry(0.5, 0.5, 1, 16);
  const executiveChairMaterial = new THREE.MeshStandardMaterial({ color: 0x000080 });
  const executiveChair = new THREE.Mesh(executiveChairGeometry, executiveChairMaterial);
  executiveChair.position.set(0, 0.5, 1);
  group.add(executiveChair);

  // Executive laptop
  const laptopGeometry = new THREE.BoxGeometry(0.4, 0.05, 0.3);
  const laptopMaterial = new THREE.MeshStandardMaterial({ color: 0x000000 });
  const laptop = new THREE.Mesh(laptopGeometry, laptopMaterial);
  laptop.position.set(0, 0.9, 0.2);
  group.add(laptop);

  // Conference area with glass table
  const glassTableGeometry = new THREE.CylinderGeometry(1.5, 1.5, 0.1, 32);
  const glassTableMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x87CEEB,
    transparent: true,
    opacity: 0.5
  });
  const glassTable = new THREE.Mesh(glassTableGeometry, glassTableMaterial);
  glassTable.position.set(3, 0.2, 0);
  group.add(glassTable);

  // Conference chairs
  const conferenceChairGeometry = new THREE.CylinderGeometry(0.3, 0.3, 0.8, 16);
  const conferenceChairMaterial = new THREE.MeshStandardMaterial({ color: 0x800000 });
  
  for (let i = 0; i < 6; i++) {
    const angle = (i / 6) * Math.PI * 2;
    const chair = new THREE.Mesh(conferenceChairGeometry, conferenceChairMaterial);
    chair.position.set(3 + Math.cos(angle) * 2, 0.4, Math.sin(angle) * 2);
    group.add(chair);
  }

  // Conference screen
  const conferenceScreenGeometry = new THREE.PlaneGeometry(2, 1.2);
  const conferenceScreenMaterial = new THREE.MeshStandardMaterial({ color: 0x0000FF });
  const conferenceScreen = new THREE.Mesh(conferenceScreenGeometry, conferenceScreenMaterial);
  conferenceScreen.position.set(3, 1.2, -2);
  group.add(conferenceScreen);

  // 🏢 OPEN WORKSPACE FLOOR
  // Modern workstations
  const workstationGeometry = new THREE.BoxGeometry(1.5, 0.7, 0.8);
  const workstationMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  
  for (let x = -3; x <= 3; x += 1.8) {
    for (let z = -3; z <= 3; z += 1.8) {
      if (Math.abs(x) > 0.5 || Math.abs(z) > 0.5) {
        const workstation = new THREE.Mesh(workstationGeometry, workstationMaterial);
        workstation.position.set(x, 0.4, z);
        group.add(workstation);

        // Office computers
        const computerGeometry = new THREE.BoxGeometry(0.3, 0.3, 0.2);
        const computerMaterial = new THREE.MeshStandardMaterial({ color: 0x000000 });
        const computer = new THREE.Mesh(computerGeometry, computerMaterial);
        computer.position.set(x, 0.8, z - 0.3);
        group.add(computer);

        // Computer monitors
        const monitorGeometry = new THREE.BoxGeometry(0.4, 0.3, 0.05);
        const monitorMaterial = new THREE.MeshStandardMaterial({ color: 0x000000 });
        const monitor = new THREE.Mesh(monitorGeometry, monitorMaterial);
        monitor.position.set(x, 0.9, z + 0.2);
        group.add(monitor);
      }
    }
  }

  // Office chairs
  const officeChairGeometry = new THREE.CylinderGeometry(0.3, 0.3, 0.8, 16);
  const officeChairMaterial = new THREE.MeshStandardMaterial({ color: 0x000080 });
  
  for (let x = -3; x <= 3; x += 1.8) {
    for (let z = -3; z <= 3; z += 1.8) {
      if (Math.abs(x) > 0.5 || Math.abs(z) > 0.5) {
        const chair = new THREE.Mesh(officeChairGeometry, officeChairMaterial);
        chair.position.set(x, 0.4, z + 0.6);
        group.add(chair);
      }
    }
  }

  // 🏢 BOARDROOM FLOOR
  const boardroomTableGeometry = new THREE.CylinderGeometry(2, 2, 0.1, 32);
  const boardroomTableMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  const boardroomTable = new THREE.Mesh(boardroomTableGeometry, boardroomTableMaterial);
  boardroomTable.position.set(0, 0.2, 0);
  group.add(boardroomTable);

  // Boardroom chairs
  const boardroomChairGeometry = new THREE.CylinderGeometry(0.4, 0.4, 0.9, 16);
  const boardroomChairMaterial = new THREE.MeshStandardMaterial({ color: 0x800000 });
  
  for (let i = 0; i < 12; i++) {
    const angle = (i / 12) * Math.PI * 2;
    const chair = new THREE.Mesh(boardroomChairGeometry, boardroomChairMaterial);
    chair.position.set(Math.cos(angle) * 3, 0.5, Math.sin(angle) * 3);
    group.add(chair);
  }

  // Boardroom presentation screen
  const boardroomScreenGeometry = new THREE.PlaneGeometry(3, 2);
  const boardroomScreenMaterial = new THREE.MeshStandardMaterial({ color: 0x0000FF });
  const boardroomScreen = new THREE.Mesh(boardroomScreenGeometry, boardroomScreenMaterial);
  boardroomScreen.position.set(0, 2, -4);
  group.add(boardroomScreen);

  // 🏢 BREAKOUT LOUNGE FLOOR
  const loungeSofaGeometry = new THREE.BoxGeometry(2, 0.6, 1);
  const loungeSofaMaterial = new THREE.MeshStandardMaterial({ color: 0x8B0000 });
  
  for (let i = 0; i < 3; i++) {
    const sofa = new THREE.Mesh(loungeSofaGeometry, loungeSofaMaterial);
    sofa.position.set(-2 + i * 2, 0.4, 2);
    group.add(sofa);
  }

  const loungeTableGeometry = new THREE.CylinderGeometry(1, 1, 0.1, 32);
  const loungeTableMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  const loungeTable = new THREE.Mesh(loungeTableGeometry, loungeTableMaterial);
  loungeTable.position.set(0, 0.2, 0);
  group.add(loungeTable);

  // Coffee station
  const coffeeStationGeometry = new THREE.BoxGeometry(1.5, 0.9, 0.8);
  const coffeeStationMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  const coffeeStation = new THREE.Mesh(coffeeStationGeometry, coffeeStationMaterial);
  coffeeStation.position.set(3, 0.5, -2);
  group.add(coffeeStation);

  // 🏢 SERVER ROOM FLOOR
  const serverRackGeometry = new THREE.BoxGeometry(0.8, 1.8, 0.6);
  const serverRackMaterial = new THREE.MeshStandardMaterial({ color: 0x2F4F4F });
  
  for (let i = 0; i < 4; i++) {
    for (let j = 0; j < 2; j++) {
      const rack = new THREE.Mesh(serverRackGeometry, serverRackMaterial);
      rack.position.set(-3 + i * 2, 0.9, -3 + j * 2);
      group.add(rack);
    }
  }

  // Network equipment
  const networkGeometry = new THREE.BoxGeometry(1, 0.3, 0.8);
  const networkMaterial = new THREE.MeshStandardMaterial({ color: 0x000000 });
  const network = new THREE.Mesh(networkGeometry, networkMaterial);
  network.position.set(3, 0.3, -3);
  group.add(network);

  // Raised floor
  const raisedFloorGeometry = new THREE.BoxGeometry(10, 0.3, 10);
  const raisedFloorMaterial = new THREE.MeshStandardMaterial({ color: 0x666666 });
  const raisedFloor = new THREE.Mesh(raisedFloorGeometry, raisedFloorMaterial);
  raisedFloor.position.set(0, 0.15, 0);
  group.add(raisedFloor);

  // 🏢 ROOFTOP TERRACE
  const terraceFloorGeometry = new THREE.BoxGeometry(11, 0.1, 11);
  const terraceFloorMaterial = new THREE.MeshStandardMaterial({ color: 0x228B22 });
  const terraceFloor = new THREE.Mesh(terraceFloorGeometry, terraceFloorMaterial);
  terraceFloor.position.y = 0.05;
  group.add(terraceFloor);

  // Outdoor seating
  const terraceChairGeometry = new THREE.CylinderGeometry(0.3, 0.3, 0.8, 16);
  const terraceChairMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  
  for (let i = 0; i < 8; i++) {
    const angle = (i / 8) * Math.PI * 2;
    const chair = new THREE.Mesh(terraceChairGeometry, terraceChairMaterial);
    chair.position.set(
      Math.cos(angle) * 3,
      0.4,
      Math.sin(angle) * 3
    );
    group.add(chair);
  }

  const terraceTableGeometry = new THREE.CylinderGeometry(1.2, 1.2, 0.1, 32);
  const terraceTableMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  const terraceTable = new THREE.Mesh(terraceTableGeometry, terraceTableMaterial);
  terraceTable.position.set(0, 0.2, 0);
  group.add(terraceTable);

  // Meeting pods
  const podGeometry = new THREE.CylinderGeometry(1.5, 1.5, 2, 16);
  const podMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x87CEEB,
    transparent: true,
    opacity: 0.3
  });
  
  for (let i = 0; i < 2; i++) {
    const pod = new THREE.Mesh(podGeometry, podMaterial);
    pod.position.set(-4 + i * 8, 1, 0);
    group.add(pod);
  }

  // Green walls
  const greenWallGeometry = new THREE.BoxGeometry(8, 2, 0.1);
  const greenWallMaterial = new THREE.MeshStandardMaterial({ color: 0x228B22 });
  const greenWall = new THREE.Mesh(greenWallGeometry, greenWallMaterial);
  greenWall.position.set(0, 1, 5);
  group.add(greenWall);
};

// ENGINEERING BRIDGE
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

  // Steel support beams
  const beamGeometry = new THREE.BoxGeometry(36, 0.5, 0.5);
  const beamMaterial = new THREE.MeshStandardMaterial({ color: 0x2F4F4F });
  
  for (let i = 0; i < 4; i++) {
    const beam = new THREE.Mesh(beamGeometry, beamMaterial);
    beam.position.set(0, 15 + i * 2, 4);
    group.add(beam);
    
    const beam2 = new THREE.Mesh(beamGeometry, beamMaterial);
    beam2.position.set(0, 15 + i * 2, -4);
    group.add(beam2);
  }

  // Bridge railings
  const railingGeometry = new THREE.BoxGeometry(40, 0.8, 0.2);
  const railingMaterial = new THREE.MeshStandardMaterial({ color: 0xC0C0C0 });
  
  const leftRailing = new THREE.Mesh(railingGeometry, railingMaterial);
  const rightRailing = new THREE.Mesh(railingGeometry, railingMaterial);
  leftRailing.position.set(0, 10.9, 4.1);
  rightRailing.position.set(0, 10.9, -4.1);
  group.add(leftRailing);
  group.add(rightRailing);

  // Road markings
  const markingGeometry = new THREE.BoxGeometry(2, 0.1, 0.2);
  const markingMaterial = new THREE.MeshStandardMaterial({ color: 0xFFFFFF });
  
  for (let i = 0; i < 15; i++) {
    const marking = new THREE.Mesh(markingGeometry, markingMaterial);
    marking.position.set(-18 + i * 3, 10.1, 0);
    group.add(marking);
  }

  // Suspension cables (for suspension bridge style)
  const cableGeometry = new THREE.CylinderGeometry(0.1, 0.1, 25, 8);
  const cableMaterial = new THREE.MeshStandardMaterial({ color: 0x2F4F4F });
  
  for (let i = 0; i < 8; i++) {
    const cable = new THREE.Mesh(cableGeometry, cableMaterial);
    cable.position.set(-15 + i * 4, 18, 0);
    cable.rotation.z = Math.PI / 6;
    group.add(cable);
    
    const cable2 = new THREE.Mesh(cableGeometry, cableMaterial);
    cable2.position.set(-15 + i * 4, 18, 0);
    cable2.rotation.z = -Math.PI / 6;
    group.add(cable2);
  }

  // Bridge towers
  const towerGeometry = new THREE.BoxGeometry(2, 25, 2);
  const towerMaterial = new THREE.MeshStandardMaterial({ color: 0x696969 });
  
  const leftTower = new THREE.Mesh(towerGeometry, towerMaterial);
  const rightTower = new THREE.Mesh(towerGeometry, towerMaterial);
  leftTower.position.set(-18, 12.5, 0);
  rightTower.position.set(18, 12.5, 0);
  group.add(leftTower);
  group.add(rightTower);
};

const DemoPage: React.FC = () => {
  const navigate = useNavigate();
  const [activeExample, setActiveExample] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [modelUrl, setModelUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showModelViewer, setShowModelViewer] = useState<boolean>(false);
  const [progress, setProgress] = useState<number>(0);
  const [showInterior, setShowInterior] = useState<boolean>(false);
  
  // Tour State
  const [tourActive, setTourActive] = useState<boolean>(false);
  const [tourStep, setTourStep] = useState<number>(0);
  const [currentRoom, setCurrentRoom] = useState<TourStop | null>(null);
  const [showRoomNav, setShowRoomNav] = useState<boolean>(false);
  
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);
  const requestRef = useRef<number>(0);

  const examples: Example[] = [
    { 
      id: "mansion", 
      title: "Ultra-Luxury Mansion", 
      img: residentialBuilding, 
      prompt: "Massive three-floor luxury mansion inspired by Mrs. Folorunsho Alakija's Ikoyi estate. Featuring grand entrance, infinity pool, private cinema, gourmet kitchen, personal gym, and rooftop lounge with panoramic views." 
    },
    { 
      id: "hospital",   
      title: "Futuristic Luxury Hospital",   
      img: medicalFacility,   
      prompt: "Advanced medical complex with MRI centers, surgical theaters, ICU, luxury patient suites, research labs, and premium amenities. Featuring glass elevators, digital signage, and solar power." 
    },
    { 
      id: "office",       
      title: "World-Class Corporate Tower",      
      img: commercialOffice,      
      prompt: "20-story premium office tower with visible floor layouts, executive suites, boardrooms, coworking spaces, server rooms, and rooftop terrace. Showcasing BIM capabilities with structural and MEP visualization." 
    },
    { 
      id: "bridge",     
      title: "Engineering Masterpiece",    
      img: highwayBridge,    
      prompt: "Architectural and engineering marvel showcasing advanced construction techniques and sustainable design principles." 
    }
  ];

  const fileFormats: FileFormat[] = [
    { 
      name: "Industry Foundation Classes", 
      extension: "IFC", 
      type: "application/xml", 
      icon: "🏗️", 
      description: "Open BIM standard for architectural data exchange" 
    },
    { 
      name: "GL Transmission Format", 
      extension: "GLB", 
      type: "model/gltf-binary", 
      icon: "📦", 
      description: "3D model format for web and mobile applications" 
    },
    { 
      name: "Revit Project", 
      extension: "RVT", 
      type: "application/xml", 
      icon: "🏢", 
      description: "Autodesk Revit native format with full BIM data" 
    },
    { 
      name: "Project Report (HTML)", 
      extension: "HTML", 
      type: "text/html", 
      icon: "📄", 
      description: "Full project documentation and specifications" 
    },
    { 
      name: "OBJ Wavefront", 
      extension: "OBJ", 
      type: "text/plain", 
      icon: "📐", 
      description: "3D geometry format with material definitions" 
    },
    { 
      name: "FBX Format", 
      extension: "FBX", 
      type: "text/plain", 
      icon: "🎬", 
      description: "Autodesk FBX for 3D animation and games" 
    }
  ];

  // Create ultra-realistic 3D models
  const createArchitecturalModel = useCallback((type: string) => {
    if (!sceneRef.current) return;

    // Clear previous model
    while(sceneRef.current.children.length > 0) { 
      sceneRef.current.remove(sceneRef.current.children[0]); 
    }

    const buildingGroup = new THREE.Group();

    // Different building types with ultra-luxury features
    switch (type) {
      case 'mansion':
        if (showInterior) {
          createUltraLuxuryMansionInterior(buildingGroup);
        } else {
          createUltraLuxuryMansion(buildingGroup);
        }
        break;
      case 'hospital':
        if (showInterior) {
          createFuturisticHospitalInterior(buildingGroup);
        } else {
          createFuturisticHospital(buildingGroup);
        }
        break;
      case 'office':
        if (showInterior) {
          createWorldClassOfficeInterior(buildingGroup);
        } else {
          createWorldClassOfficeTower(buildingGroup);
        }
        break;
      case 'bridge':
        createEngineeringBridge(buildingGroup);
        break;
      default:
        if (showInterior) {
          createUltraLuxuryMansionInterior(buildingGroup);
        } else {
          createUltraLuxuryMansion(buildingGroup);
        }
    }
    sceneRef.current.add(buildingGroup);

    // Enhanced lighting for ultra-realistic rendering
    const ambientLight = new THREE.AmbientLight(0xffffff, showInterior ? 0.8 : 0.6);
    sceneRef.current.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, showInterior ? 1.2 : 0.8);
    directionalLight.position.set(10, 10, 5);
    directionalLight.castShadow = true;
    sceneRef.current.add(directionalLight);

    // Additional point lights for interior scenes
    if (showInterior) {
      const pointLight1 = new THREE.PointLight(0xffffff, 0.5, 20);
      pointLight1.position.set(0, 5, 0);
      sceneRef.current.add(pointLight1);

      const pointLight2 = new THREE.PointLight(0xffffff, 0.3, 15);
      pointLight2.position.set(8, 5, 8);
      sceneRef.current.add(pointLight2);
    }

    // Add grid helper
    const gridHelper = new THREE.GridHelper(40, 40);
    sceneRef.current.add(gridHelper);

    // Adjust camera based on interior/exterior view
    if (cameraRef.current && controlsRef.current) {
      if (showInterior) {
        // If tour is active, use tour position, otherwise default interior view
        if (tourActive && activeExample && TOUR_DATA[activeExample]) {
          const stop = TOUR_DATA[activeExample][tourStep];
          if (stop) {
            cameraRef.current.position.copy(stop.position);
            controlsRef.current.target.copy(stop.target);
          }
        } else {
          cameraRef.current.position.set(0, 5, 15);
          controlsRef.current.target.set(0, 3, 0);
        }
      } else {
        // Exterior views adjusted for each building type
        switch (type) {
          case 'mansion':
            cameraRef.current.position.set(25, 12, 25);
            controlsRef.current.target.set(0, 5, 0);
            break;
          case 'hospital':
            cameraRef.current.position.set(30, 15, 30);
            controlsRef.current.target.set(0, 7, 0);
            break;
          case 'office':
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
      }
      controlsRef.current.update();
    }
  }, [showInterior, tourActive, activeExample, tourStep]);

  // Initialize Three.js scene with enhanced settings
  const initThreeJS = useCallback(() => {
    if (!canvasRef.current) return;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(showInterior ? 0x111111 : 0x87CEEB);
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
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1;
    rendererRef.current = renderer;

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = showInterior ? 1 : 5;
    controls.maxDistance = 100;
    controlsRef.current = controls;

    // Enhanced lighting setup
    const ambientLight = new THREE.AmbientLight(0x404040, showInterior ? 0.8 : 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, showInterior ? 1.2 : 0.8);
    directionalLight.position.set(10, 10, 5);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    scene.add(directionalLight);

    // Add grid helper
    const gridHelper = new THREE.GridHelper(40, 40, 0x000000, 0x000000);
    scene.add(gridHelper);

    // Animation loop with Smooth Camera Transition for Tour
    const animate = () => {
      requestRef.current = requestAnimationFrame(animate);
      
      if (tourActive && currentRoom && cameraRef.current && controlsRef.current) {
        // Smoothly interpolate camera position to the target room position
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
  }, [showInterior, tourActive, currentRoom]);

  // Toggle between interior and exterior view
  const toggleInteriorView = () => {
    const newShowInterior = !showInterior;
    setShowInterior(newShowInterior);
    
    // Reset tour when switching views
    setTourActive(false);
    setTourStep(0);
    setCurrentRoom(null);
  };

  // --- TOUR NAVIGATION LOGIC ---
  const startTour = () => {
    if (!activeExample || !TOUR_DATA[activeExample]) return;
    
    setShowInterior(true);
    setTourActive(true);
    setTourStep(0);
    setCurrentRoom(TOUR_DATA[activeExample][0]);
    setShowRoomNav(true);
  };

  const goToRoom = (index: number) => {
    if (!activeExample || !TOUR_DATA[activeExample]) return;
    setTourStep(index);
    setCurrentRoom(TOUR_DATA[activeExample][index]);
    setTourActive(true);
    setShowInterior(true);
  };

  const nextTourStep = () => {
    if (!activeExample || !TOUR_DATA[activeExample]) return;
    
    const nextStep = tourStep + 1;
    if (nextStep < TOUR_DATA[activeExample].length) {
      setTourStep(nextStep);
      setCurrentRoom(TOUR_DATA[activeExample][nextStep]);
    } else {
      setTourStep(0);
      setCurrentRoom(TOUR_DATA[activeExample][0]);
    }
  };

  const prevTourStep = () => {
    if (!activeExample || !TOUR_DATA[activeExample]) return;
    
    const prevStep = tourStep - 1;
    if (prevStep >= 0) {
      setTourStep(prevStep);
      setCurrentRoom(TOUR_DATA[activeExample][prevStep]);
    }
  };

  // Generate with sample models
  const generateWithSampleModel = async (exampleId: string): Promise<void> => {
    setIsGenerating(true);
    setError(null);
    setModelUrl(null);
    setProgress(0);
    setShowInterior(false);
    setTourActive(false);
    try {
      // Simulate API processing time with progress
      for (let i = 0; i <= 100; i += 10) {
        setProgress(i);
        await new Promise(resolve => setTimeout(resolve, 20));
      }
      setModelUrl(`programmatic-${exampleId}`);
      
    } catch {
      setError("Generation failed");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleExampleClick = (exampleId: string): void => {
    setActiveExample(exampleId);
    generateWithSampleModel(exampleId);
  };

  // --- REAL CONTENT GENERATION FOR DOWNLOADS ---
  const downloadModel = async (format: FileFormat): Promise<void> => {
    if (!modelUrl || !activeExample) return;
    try {
      let blob: Blob;
      let filename: string;
      
      if (format.extension === "HTML") {
        const htmlContent = `
          <!DOCTYPE html>
          <html>
          <head>
            <title>BIM Project Report - ${activeExample}</title>
            <style>
              body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 2rem; }
              h1 { color: #F8780F; border-bottom: 2px solid #eee; padding-bottom: 1rem; }
              h2 { color: #4E443C; margin-top: 2rem; }
              .meta { color: #666; margin-bottom: 2rem; background: #f9f9f9; padding: 1rem; border-radius: 8px; }
              .room { margin-bottom: 1.5rem; border: 1px solid #eee; padding: 1rem; border-radius: 8px; }
              .tag { display: inline-block; background: #eee; padding: 2px 8px; border-radius: 4px; font-size: 0.9rem; margin-right: 5px; }
              .feature { background: #e7f3ff; padding: 0.5rem; border-radius: 4px; margin: 0.2rem 0; }
            </style>
          </head>
          <body>
            <h1>BIMFlow Ultra-Luxury Project Documentation</h1>
            <div class="meta">
              <p><strong>Project Name:</strong> ${activeExample.toUpperCase()} Complex</p>
              <p><strong>Architectural Style:</strong> Ultra-Luxury Modern</p>
              <p><strong>Date Generated:</strong> ${new Date().toLocaleDateString()}</p>
              <p><strong>Status:</strong> Approved for Construction</p>
            </div>
            <h2>Architectural Features</h2>
            ${TOUR_DATA[activeExample] ? TOUR_DATA[activeExample].map(room => `
              <div class="room">
                <h3>${room.name}</h3>
                <p>${room.description}</p>
                <p><strong>Premium Materials:</strong> ${room.details.materials.map(m => `<span class="tag">${m}</span>`).join('')}</p>
                <p><strong>Advanced MEP Systems:</strong> ${room.details.mep.join(', ')}</p>
                <p><strong>Special Features:</strong> ${room.details.specialFeatures.map(f => `<div class="feature">${f}</div>`).join('')}</p>
              </div>
            `).join('') : '<p>No room data available.</p>'}
            <h2>Technical Specifications</h2>
            <p>This ultra-luxury project represents the pinnacle of architectural design and engineering excellence. All specifications meet international luxury standards.</p>
          </body>
          </html>
        `;
        blob = new Blob([htmlContent], { type: "text/html" });
        filename = `bim-ultra-luxury-${activeExample}.html`;
      
      } else if (format.extension === "OBJ") {
        const objContent = `
# BIMFlow Generated OBJ File - Ultra Luxury Model
# Project: ${activeExample}
# Generated: ${new Date().toLocaleDateString()}
o ${activeExample}_Luxury_Model
v -2.0 -2.0 2.0
v 2.0 -2.0 2.0
v -2.0 2.0 2.0
v 2.0 2.0 2.0
v -2.0 2.0 -2.0
v 2.0 2.0 -2.0
v -2.0 -2.0 -2.0
v 2.0 -2.0 -2.0
f 1 2 4 3
f 3 4 6 5
f 5 6 8 7
f 7 8 2 1
f 2 8 6 4
f 7 1 3 5
        `;
        blob = new Blob([objContent], { type: "text/plain" });
        filename = `ultra-luxury-${activeExample}.obj`;
      } else if (format.extension === "IFC" || format.extension === "RVT") {
        const xmlContent = `
<?xml version="1.0" encoding="UTF-8"?>
<BIMProject type="${format.extension}">
  <Header>
    <ProjectName>${activeExample} - Ultra Luxury Edition</ProjectName>
    <Architect>BIMFlow Premium Design Studio</Architect>
    <Date>${new Date().toISOString()}</Date>
    <Software>BIMFlow Suite Web Ultra</Software>
  </Header>
  <Building>
    <Name>${activeExample} Luxury Complex</Name>
    <Levels>
      <Level name="Ground Floor" elevation="0.0" area="450m2" />
      <Level name="First Floor" elevation="4.5" area="420m2" />
      <Level name="Second Floor" elevation="9.0" area="400m2" />
      <Level name="Rooftop" elevation="13.5" area="380m2" />
    </Levels>
    <Spaces>
      ${TOUR_DATA[activeExample]?.map(r => `<Space name="${r.name}" area="35m2" category="Premium" />`).join('\n      ')}
    </Spaces>
    <Materials>
      <Material name="Italian Marble" cost="premium" />
      <Material name="24K Gold Leaf" cost="luxury" />
      <Material name="Crystal Glass" cost="premium" />
      <Material name="Oak Hardwood" cost="premium" />
    </Materials>
  </Building>
</BIMProject>
        `;
        blob = new Blob([xmlContent], { type: "application/xml" });
        filename = `ultra-luxury-${activeExample}.${format.extension.toLowerCase()}`;
      } else {
        const modelContent = `BIM Ultra-Luxury Model: ${activeExample}\nGenerated: ${new Date().toLocaleDateString()}\nFormat: ${format.name}\nArchitectural Style: Premium Luxury`;
        blob = new Blob([modelContent], { type: format.type });
        filename = `ultra-luxury-${activeExample}.${format.extension.toLowerCase()}`;
      }
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = filename;
      
      document.body.appendChild(a);
      a.click();
      
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch {
      setError(`Failed to download ${format.extension} file`);
    }
  };

  const viewModelIn3D = (): void => {
    if (activeExample) {
      setShowModelViewer(true);
    }
  };

  const clearAll = (): void => {
    setModelUrl(null);
    setActiveExample(null);
    setIsGenerating(false);
    setError(null);
    setShowModelViewer(false);
    setProgress(0);
    setShowInterior(false);
    setTourActive(false);
    setCurrentRoom(null);
    setShowRoomNav(false);
  };

  // Initialize Three.js when component mounts
  useEffect(() => {
    if (showModelViewer) {
      const cleanup = initThreeJS();
      
      const timer = setTimeout(() => {
        if (activeExample) {
          createArchitecturalModel(activeExample);
        }
      }, 50);
      
      return () => {
        if (cleanup) cleanup();
        clearTimeout(timer);
      };
    }
  }, [showModelViewer, activeExample, showInterior, initThreeJS, createArchitecturalModel]);

  // Embedded 3D Model Viewer Component
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
        <h3 style={{ margin: 0 }}>3D Ultra-Luxury Model Viewer - {activeExample} {showInterior ? '(Interior)' : '(Exterior)'}</h3>
        <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          
          {/* Tour Button */}
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
              display: "flex",
              alignItems: "center",
              gap: "0.5rem"
            }}
          >
            <span>🚶</span> {tourActive ? "Restart Tour" : "Start Guided Tour"}
          </button>
          {/* Interior/Exterior Toggle Button */}
          <button
            onClick={toggleInteriorView}
            style={{
              background: showInterior ? "#4CAF50" : "#2196F3",
              color: "white",
              border: "none",
              padding: "0.5rem 1rem",
              borderRadius: "4px",
              cursor: "pointer",
              fontWeight: 600,
            }}
          >
            {showInterior ? "🏠 Exterior" : "🚪 Interior"}
          </button>
          
          <button
            onClick={() => setShowModelViewer(false)}
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
      
      <div style={{ flex: 1, position: "relative", display: 'flex' }}>
        
        {/* ROOM NAVIGATOR SIDEBAR */}
        {showInterior && activeExample && TOUR_DATA[activeExample] && (
          <div className={`room-navigator ${showRoomNav || tourActive ? 'open' : ''}`}>
            <div className="room-nav-title">📍 Luxury Space Navigator</div>
            {TOUR_DATA[activeExample].map((room, index) => (
              <button
                key={index}
                className={`room-btn ${currentRoom?.name === room.name ? 'active' : ''}`}
                onClick={() => goToRoom(index)}
              >
                <span className="room-btn-icon">
                  {index === 0 ? '🏰' : index === 1 ? '🌟' : index === 2 ? '🛋️' : index === 3 ? '🍽️' : 
                   index === 4 ? '🎬' : index === 5 ? '🛏️' : index === 6 ? '🏋️' : index === 7 ? '🏊' : '🌿'}
                </span>
                {room.name}
              </button>
            ))}
          </div>
        )}
        <canvas 
          ref={canvasRef} 
          style={{
            flex: 1,
            width: "100%",
            height: "100%",
            display: "block"
          }}
        />
        
        {/* BIM Insights Overlay (Only in Tour Mode) */}
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
            animation: "fadeIn 0.5s ease"
          }}>
            <h3 style={{ color: "#F8780F", margin: "0 0 0.5rem", fontSize: "1.4rem" }}>
              {currentRoom.name}
            </h3>
            <p style={{ fontSize: "0.9rem", color: "#666", marginBottom: "1rem", fontStyle: "italic" }}>
              {currentRoom.description}
            </p>
            
            <div style={{ fontSize: "0.85rem" }}>
              <div style={{ marginBottom: "0.8rem" }}>
                <strong style={{ color: "#4E443C", display: "block", marginBottom: "0.2rem" }}>🏗️ Premium Materials:</strong>
                {currentRoom.details.materials.join(", ")}
              </div>
              <div style={{ marginBottom: "0.8rem" }}>
                <strong style={{ color: "#4E443C", display: "block", marginBottom: "0.2rem" }}>⚡ Advanced MEP Systems:</strong>
                {currentRoom.details.mep.join(", ")}
              </div>
              <div style={{ marginBottom: "0.8rem" }}>
                <strong style={{ color: "#4E443C", display: "block", marginBottom: "0.2rem" }}>💡 Luxury Lighting:</strong>
                {currentRoom.details.lighting}
              </div>
              <div style={{ marginBottom: "0.8rem" }}>
                <strong style={{ color: "#4E443C", display: "block", marginBottom: "0.2rem" }}>🎯 Special Features:</strong>
                {currentRoom.details.specialFeatures.join(", ")}
              </div>
            </div>
            {/* Tour Navigation Controls */}
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
                {tourStep + 1} / {activeExample && TOUR_DATA[activeExample] ? TOUR_DATA[activeExample].length : 0}
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
          <div>🎮 Ultra-Luxury Controls:</div>
          <div>• Left click + drag: Rotate</div>
          <div>• Right click + drag: Pan</div>
          <div>• Scroll: Zoom</div>
          <div>• Toggle Interior/Exterior with button above</div>
          <div>• Start guided tour for premium experience</div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="demo-page">
      {/* Embedded 3D Model Viewer */}
      {showModelViewer && <ModelViewer />}

      {/* HERO SECTION */}
      <section 
        className="demo-hero" 
        style={{
          backgroundImage: `linear-gradient(rgba(78,68,60,0.88), rgba(248,120,15,0.4)), url(${heroBim})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          minHeight: "90vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          textAlign: "center",
          color: "white",
        }}
      >
        <div style={{ maxWidth: "1000px", padding: "2rem" }}>
          <h1 style={{ 
            fontSize: "4.8rem", 
            fontWeight: 900, 
            marginBottom: "1rem",
            color: "#F8780F",
            textShadow: "0 2px 8px rgba(0,0,0,0.5)"
          }}>
            BIMFlow Ultra-Luxury Suite
          </h1>
          <p style={{ 
            fontSize: "1.7rem", 
            margin: "2rem 0", 
            fontWeight: 300,
            textShadow: "0 1px 4px rgba(0,0,0,0.5)"
          }}>
            Hyper-Realistic 3D Architectural Models with Premium Luxury Features
          </p>
          <button 
            onClick={() => navigate("/generate-model")} 
            style={{
              background: "#F8780F",
              color: "white",
              border: "none",
              padding: "1.4rem 3.5rem",
              fontSize: "1.4rem",
              borderRadius: "16px",
              cursor: "pointer",
              fontWeight: 700,
              boxShadow: "0 10px 30px rgba(248,120,15,0.4)",
              transition: "all 0.3s ease",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "translateY(-2px)";
              e.currentTarget.style.boxShadow = "0 15px 40px rgba(248,120,15,0.6)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.boxShadow = "0 10px 30px rgba(248,120,15,0.4)";
            }}
          >
            Start Luxury Project
          </button>
        </div>
      </section>

      {/* MAIN CONTENT */}
      <div 
        className="demo-container" 
        style={{
          maxWidth: "1400px",
          margin: "5rem auto",
          padding: "0 2rem",
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "5rem",
        }}
      >
        {/* LEFT - Project Examples */}
        <div>
          <h2 style={{ fontSize: "3rem", marginBottom: "2.5rem", color: "#4E443C" }}>
            Ultra-Luxury Projects
          </h2>
          <div style={{ display: "grid", gap: "2.5rem" }}>
            {examples.map((ex) => (
              <div
                key={ex.id}
                onClick={() => !isGenerating && handleExampleClick(ex.id)}
                style={{
                  cursor: isGenerating ? "not-allowed" : "pointer",
                  borderRadius: "20px",
                  overflow: "hidden",
                  boxShadow: "0 12px 40px rgba(0,0,0,0.15)",
                  transition: "all 0.4s ease",
                  border: activeExample === ex.id ? "5px solid #F8780F" : "5px solid transparent",
                  opacity: isGenerating && activeExample !== ex.id ? 0.6 : 1,
                }}
                onMouseEnter={(e) => !isGenerating && (e.currentTarget.style.transform = "translateY(-12px)")}
                onMouseLeave={(e) => !isGenerating && (e.currentTarget.style.transform = "translateY(0)")}
              >
                <img 
                  src={ex.img} 
                  alt={ex.title} 
                  style={{ 
                    width: "100%", 
                    height: "280px", 
                    objectFit: "cover" 
                  }} 
                />
                <div style={{ padding: "2rem", background: "transparent" }}>
                  <h3 style={{ 
                    fontSize: "1.8rem", 
                    margin: "0 0 0.8rem", 
                    color: "#4E443C" 
                  }}>
                    {ex.title}
                  </h3>
                  <p style={{ 
                    color: "#666", 
                    fontSize: "1rem", 
                    lineHeight: "1.6" 
                  }}>
                    {ex.prompt}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* RIGHT - Results Section */}
        <div>
          <h2 style={{ fontSize: "3rem", marginBottom: "2.5rem", color: "#4E443C" }}>
            Luxury Results
          </h2>

          {/* Premium Notice */}
          <div style={{ 
            background: "linear-gradient(135deg, #FFF8F0 0%, #FFF5E6 100%)", 
            border: "2px solid #F8780F",
            color: "#856404",
            padding: "1.5rem",
            borderRadius: "12px",
            marginBottom: "2rem"
          }}>
            <strong>Ultra-Luxury 3D Experience:</strong> Programmatically generated premium architectural models with hyper-realistic interiors! Explore luxury mansions, futuristic hospitals, and world-class corporate towers.
          </div>

          {/* Generation Status */}
          {isGenerating && (
            <div style={{ 
              background: "white", 
              padding: "4rem", 
              borderRadius: "20px", 
              textAlign: "center", 
              boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
              marginBottom: "2rem"
            }}>
              <div style={{ fontSize: "5rem", marginBottom: "1rem" }}>🏰🔄</div>
              <p style={{ fontSize: "1.5rem", color: "#4E443C" }}>
                Generating Ultra-Luxury 3D Model...
              </p>
              <p style={{ color: "#888", marginBottom: "1rem" }}>
                {progress > 0 ? `Progress: ${progress}%` : 'Starting luxury generation...'}
              </p>
              <div style={{ 
                background: "#E5E7EB",
                height: "8px",
                borderRadius: "4px",
                margin: "2rem 0",
                overflow: "hidden"
              }}>
                <div style={{ 
                  background: "linear-gradient(90deg, #F8780F 0%, #FFA557 100%)",
                  height: "100%",
                  width: `${progress}%`,
                  transition: "width 0.3s ease",
                  borderRadius: "4px",
                }} />
              </div>
              <p style={{ color: "#666", fontSize: "0.9rem" }}>
                Creating your hyper-realistic BIM model with premium luxury features
              </p>
            </div>
          )}

          {/* Model Result */}
          {activeExample && !isGenerating && (
            <div style={{ 
              background: "transparent", 
              padding: "3rem", 
              borderRadius: "20px", 
              marginBottom: "2rem", 
              boxShadow: "0 10px 30px rgba(0,0,0,0.1)", 
              textAlign: "center" 
            }}>
              <div style={{ fontSize: "4rem", marginBottom: "1rem" }}>🎉</div>
              <h3 style={{ 
                fontSize: "2rem", 
                color: "#F8780F", 
                marginBottom: "1rem" 
              }}>
                Ultra-Luxury 3D Model Ready!
              </h3>
              <p style={{ color: "#666", marginBottom: "2rem" }}>
                Your premium {activeExample} is ready for 3D viewing with hyper-realistic interiors.
                Switch between exterior and interior views in the 3D viewer.
              </p>
              
              {/* View in 3D Button */}
              <button 
                onClick={viewModelIn3D}
                style={{
                  background: "#F8780F",
                  color: "white",
                  padding: "1.2rem 2rem",
                  borderRadius: "12px",
                  border: "none",
                  fontSize: "1.1rem",
                  fontWeight: 700,
                  cursor: "pointer",
                  width: "100%",
                  marginBottom: "2rem",
                  transition: "all 0.3s ease",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = "translateY(-2px)";
                  e.currentTarget.style.boxShadow = "0 8px 25px rgba(248,120,15,0.4)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = "translateY(0)";
                  e.currentTarget.style.boxShadow = "none";
                }}
              >
                👁️ View in Ultra-Luxury 3D
              </button>

              {/* File Format Downloads */}
              <div style={{ marginBottom: "2rem" }}>
                <h4 style={{ 
                  color: "#4E443C", 
                  marginBottom: "1.5rem",
                  fontSize: "1.3rem"
                }}>
                  Download Premium BIM Files:
                </h4>
                <div style={{ 
                  display: "grid", 
                  gridTemplateColumns: "1fr 1fr", 
                  gap: "1rem" 
                }}>
                  {fileFormats.map((format, index) => (
                    <button
                      key={index}
                      onClick={() => downloadModel(format)}
                      style={{
                        background: "white",
                        color: "#4E443C",
                        border: "2px solid #E5E5E5",
                        padding: "1rem",
                        borderRadius: "8px",
                        cursor: "pointer",
                        transition: "all 0.3s ease",
                        textAlign: "left",
                        display: "flex",
                        alignItems: "center",
                        gap: "0.75rem",
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.borderColor = "#F8780F";
                        e.currentTarget.style.transform = "translateY(-2px)";
                        e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,0,0,0.1)";
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.borderColor = "#E5E5E5";
                        e.currentTarget.style.transform = "translateY(0)";
                        e.currentTarget.style.boxShadow = "none";
                      }}
                    >
                      <span style={{ fontSize: "1.5rem" }}>{format.icon}</span>
                      <div style={{ textAlign: "left" }}>
                        <div style={{ 
                          fontWeight: 700, 
                          fontSize: "0.9rem",
                          marginBottom: "0.25rem"
                        }}>
                          {format.extension}
                        </div>
                        <div style={{ 
                          fontSize: "0.75rem", 
                          color: "#666",
                          lineHeight: "1.2"
                        }}>
                          {format.name}
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
              
              {/* Premium Features Info */}
              <div style={{ 
                marginTop: "2rem",
                padding: "1.5rem",
                background: "#f8f9fa",
                borderRadius: "8px",
                fontSize: "0.9rem",
                color: "#666",
                textAlign: "left"
              }}>
                <strong>Ultra-Luxury 3D Viewer Features:</strong>
                <ul style={{ margin: "0.5rem 0 0 1rem", padding: 0 }}>
                  <li>Full 360° rotation and premium zoom controls</li>
                  <li>Toggle between exterior and hyper-realistic interior views</li>
                  <li>Complete luxury room layouts with premium furniture</li>
                  <li>Realistic lighting, shadows, and material rendering</li>
                  <li>Guided tours with architectural insights</li>
                  <li>Professional BIM data visualization</li>
                </ul>
              </div>
            </div>
          )}

          {/* Quick Preview */}
          {activeExample && !showModelViewer && (
            <div style={{
              background: "white",
              padding: "2rem",
              borderRadius: "20px",
              marginBottom: "2rem",
              boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
              textAlign: "center"
            }}>
              <h4 style={{ color: "#4E443C", marginBottom: "1rem" }}>Ultra-Luxury 3D Preview</h4>
              <div style={{
                width: "100%",
                height: "200px",
                background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                borderRadius: "12px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "white",
                fontSize: "1.1rem",
                position: "relative",
                overflow: "hidden"
              }}>
                <div style={{
                  position: "absolute",
                  top: 0,
                  left: 0,
                  right: 0,
                  bottom: 0,
                  background: "rgba(0,0,0,0.3)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  flexDirection: "column"
                }}>
                  <div style={{ fontSize: "3rem", marginBottom: "0.5rem" }}>
                    {activeExample === 'mansion' ? '🏰' : 
                     activeExample === 'hospital' ? '🏥' : 
                     activeExample === 'office' ? '🏢' : '🌉'}
                  </div>
                  <p style={{ margin: 0, fontWeight: 600 }}>Ultra-Luxury {activeExample} Ready</p>
                  <p style={{ margin: "0.25rem 0", fontSize: "0.9rem", opacity: 0.9 }}>
                    Hyper-Realistic Interior + Exterior Views
                  </p>
                  <button 
                    onClick={viewModelIn3D}
                    style={{
                      background: "rgba(255,255,255,0.2)",
                      color: "white",
                      border: "1px solid rgba(255,255,255,0.5)",
                      padding: "0.5rem 1rem",
                      borderRadius: "6px",
                      cursor: "pointer",
                      marginTop: "0.5rem",
                      fontWeight: 600
                    }}
                  >
                    Open Ultra-Luxury 3D
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Premium Avatar Placeholder */}
          <div style={{
            background: "linear-gradient(135deg, #FFF8F0 0%, #FFF5E6 100%)",
            border: "2px dashed #F8780F",
            borderRadius: "24px",
            padding: "4rem 2rem",
            textAlign: "center",
          }}>
            <div style={{ fontSize: "6rem", marginBottom: "1.5rem" }}>👑</div>
            <h2 style={{ fontSize: "2.6rem", color: "#4E443C", margin: "0 0 1rem" }}>
              Premium Architect Avatar (Coming Soon)
            </h2>
            <p style={{ 
              fontSize: "1.2rem", 
              color: "#666", 
              maxWidth: "480px", 
              margin: "0 auto", 
              lineHeight: "1.7" 
            }}>
              Walk through your ultra-luxury 3D BIM models in our premium embedded viewer with architectural insights.
            </p>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div style={{ 
          textAlign: "center", 
          color: "#EF4444", 
          fontSize: "1.3rem", 
          margin: "3rem auto",
          maxWidth: "800px", 
          padding: "2rem", 
          background: "#FEF2F2", 
          borderRadius: "12px", 
          border: "1px solid #FECACA" 
        }}>
          {error}
        </div>
      )}

      {/* Clear Button */}
      <button 
        onClick={clearAll} 
        style={{
          display: "block",
          margin: "6rem auto",
          padding: "1.3rem 4rem",
          background: "#4E443C",
          color: "white",
          border: "none",
          borderRadius: "16px",
          fontSize: "1.2rem",
          cursor: "pointer",
          fontWeight: 700,
          transition: "all 0.3s ease",
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = "translateY(-2px)";
          e.currentTarget.style.boxShadow = "0 8px 25px rgba(78,68,60,0.4)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = "translateY(0)";
          e.currentTarget.style.boxShadow = "none";
        }}
      >
        Clear All & Start New Luxury Project
      </button>
    </div>
  );
};

export default DemoPage;