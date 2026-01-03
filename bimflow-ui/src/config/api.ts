// src/config/api.ts
export const HITEM3D_CONFIG = {
  accessKey: 'ak_1ebd5410dd4c4bf78bb221e8182f28d3',
  secretKey: 'sk_6ba1413519224e26bd4b4dfe71759e71',
  baseUrl: 'https://api.hitem3d.ai',
};

export const getAuthHeaders = () => ({
  'Authorization': `Bearer ${HITEM3D_CONFIG.accessKey}`,
  'X-Secret-Key': HITEM3D_CONFIG.secretKey,
  'Content-Type': 'application/json',
});