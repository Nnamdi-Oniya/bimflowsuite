// src/services/hitem3dService.ts
import { HITEM3D_CONFIG, getAuthHeaders } from '../config/api';

export interface GenerateModelParams {
  imageUrl?: string;
  prompt: string;
  resolution?: '512' | '1024' | '1536' | '1536-pro';
  format?: 'glb' | 'obj' | 'stl' | 'fbx';
  version?: 'v1.0' | 'v1.5';
  generationType?: 'all-in-one' | 'geometry-only' | 'staged';
}

interface TaskStatus {
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress?: number;
  model_url?: string;
  error?: string;
}

class Hitem3DService {
  private baseUrl = HITEM3D_CONFIG.baseUrl;
  public currentProgress: number = 0;

  private async createTask(params: GenerateModelParams): Promise<string> {
    const response = await fetch(`${this.baseUrl}/v1/generate`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({
        prompt: params.prompt,
        image_url: params.imageUrl,
        resolution: params.resolution || '1024',
        format: params.format || 'glb',
        version: params.version || 'v1.5',
        generation_type: params.generationType || 'all-in-one',
      }),
    });

    if (!response.ok) {
      throw new Error(`API Error ${response.status}`);
    }

    const data = await response.json();
    return data.task_id;
  }

  private async pollTask(taskId: string): Promise<string> {
    const maxAttempts = 60;
    const interval = 5000;

    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      const response = await fetch(`${this.baseUrl}/v1/tasks/${taskId}`, {
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data: TaskStatus = await response.json();

      if (data.status === 'completed' && data.model_url) {
        this.currentProgress = 100;
        return data.model_url;
      }

      if (data.status === 'failed') {
        throw new Error(data.error || 'Generation failed');
      }

      if (data.progress !== undefined) {
        this.currentProgress = data.progress;
      }

      await new Promise(resolve => setTimeout(resolve, interval));
    }

    throw new Error('Generation timed out');
  }

  async generateModel(params: GenerateModelParams): Promise<string> {
    this.currentProgress = 0;
    const taskId = await this.createTask(params);
    return await this.pollTask(taskId);
  }
}

export const hitem3dService = new Hitem3DService();