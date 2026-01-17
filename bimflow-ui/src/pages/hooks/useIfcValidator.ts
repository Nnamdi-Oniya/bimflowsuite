// src/hooks/useIfcValidator.ts
import { useState } from "react";
import * as WebIFC from "web-ifc";

export interface ValidationResult {
  isValid: boolean;
  schema?: string;
  error?: string;
  modelId?: number;
}

export const useIfcValidator = () => {
  const [isValidating, setIsValidating] = useState(false);

  const validateFile = async (file: File): Promise<ValidationResult> => {
    setIsValidating(true);
    
    // Initialize the WASM library
    const ifcApi = new WebIFC.IfcAPI();
    
    // Point to where the wasm file is located (public folder)
    ifcApi.SetWasmPath("/"); 

    try {
      await ifcApi.Init();
      
      const buffer = await file.arrayBuffer();
      const data = new Uint8Array(buffer);

      // 1. TRY TO OPEN MODEL
      const modelID = ifcApi.OpenModel(data);

      // 2. CHECK SCHEMA
      const schema = ifcApi.GetModelSchema(modelID);

      ifcApi.CloseModel(modelID);

      setIsValidating(false);
      return { isValid: true, schema, modelId: modelID };

    } catch (e) {
      setIsValidating(false);
      const errorMessage = e instanceof Error ? e.message : "Unknown parsing error";
      return { isValid: false, error: errorMessage };
    }
  };

  return { validateFile, isValidating };
};