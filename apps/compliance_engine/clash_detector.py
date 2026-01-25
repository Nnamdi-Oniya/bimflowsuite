# compliance_engine/clash_detector.py
import ifcopenshell
import ifcopenshell.geom
import json
from typing import List, Dict, Tuple
from io import BytesIO
import numpy as np

class AdvancedClashDetector:
    def __init__(self, tolerance_hard: float = 0.01, tolerance_soft: float = 0.05):
        self.tolerance_hard = tolerance_hard
        self.tolerance_soft = tolerance_soft
        self.settings = ifcopenshell.geom.settings()
        self.settings.set(self.settings.INCLUDE_CURVES, True)
        self.settings.set(self.settings.USE_PYTHON_OPENCASCADE, True)
        self.results = {}  # For engine integration
    
    def detect_clashes(self, ifc_string: str, clash_sets: List[Dict[str, str]] = None, soft_clearance: bool = True) -> Dict:
        ifc_file = ifcopenshell.open(BytesIO(ifc_string.encode('utf-8')))
        
        if not clash_sets:
            clash_sets = [
                {'group_a': 'IfcWall', 'group_b': 'IfcDuctSegment'},
                {'group_a': 'IfcBeam', 'group_b': 'IfcPipeSegment'}
            ]
        
        clashes = []
        element_bboxes = self._get_all_bboxes(ifc_file)
        
        for cs in clash_sets:
            group_a = ifc_file.by_type(cs['group_a'])
            group_b = ifc_file.by_type(cs['group_b'])
            
            for elem_a in group_a:
                bbox_a = element_bboxes.get(elem_a.GlobalId)
                for elem_b in group_b:
                    bbox_b = element_bboxes.get(elem_b.GlobalId)
                    if not bbox_a or not bbox_b:
                        continue
                    
                    if self._aabb_overlap(bbox_a, bbox_b, self.tolerance_hard):
                        clashes.append({
                            'id_a': elem_a.GlobalId, 'name_a': elem_a.Name or 'Unnamed',
                            'id_b': elem_b.GlobalId, 'name_b': elem_b.Name or 'Unnamed',
                            'type': 'hard', 'severity': 'high',
                            'description': f'Overlap between {cs["group_a"]} and {cs["group_b"]}'
                        })
                    
                    if soft_clearance:
                        dist = self._min_distance_between_meshes(elem_a, elem_b)
                        if dist < self.tolerance_soft:
                            clashes.append({
                                'id_a': elem_a.GlobalId, 'name_a': elem_a.Name or 'Unnamed',
                                'id_b': elem_b.GlobalId, 'name_b': elem_b.Name or 'Unnamed',
                                'type': 'soft', 'distance': dist,
                                'severity': 'medium' if dist > self.tolerance_soft / 2 else 'high',
                                'description': f'Clearance violation: {dist:.3f}m'
                            })
        
        summary = {
            'total_clashes': len(clashes),
            'hard_clashes': len([c for c in clashes if c['type'] == 'hard']),
            'soft_clashes': len([c for c in clashes if c['type'] == 'soft'])
        }
        self.results = {'clashes': clashes, 'summary': summary}
        
        return self.results
    
    def _get_all_bboxes(self, ifc_file):
        bboxes = {}
        for elem in ifc_file:
            if hasattr(elem, 'Representation') and elem.Representation:
                try:
                    shape = ifcopenshell.geom.create_shape(self.settings, elem)
                    bbox = shape.geometry.bbox
                    bboxes[elem.GlobalId] = bbox
                except:
                    pass
        return bboxes
    
    @staticmethod
    def _aabb_overlap(bbox1: Tuple, bbox2: Tuple, tol: float) -> bool:
        return not (
            bbox1[0] > bbox2[3] + tol or bbox2[0] > bbox1[3] + tol or
            bbox1[1] > bbox2[4] + tol or bbox2[1] > bbox1[4] + tol or
            bbox1[2] > bbox2[5] + tol or bbox2[2] > bbox1[5] + tol
        )
    
    def _min_distance_between_meshes(self, elem_a, elem_b) -> float:
        shape_a = ifcopenshell.geom.create_shape(self.settings, elem_a)
        shape_b = ifcopenshell.geom.create_shape(self.settings, elem_b)
        centroid_a = np.mean(np.array(shape_a.geometry.verts).reshape(-1, 3), axis=0)
        centroid_b = np.mean(np.array(shape_b.geometry.verts).reshape(-1, 3), axis=0)
        return np.linalg.norm(centroid_a - centroid_b)