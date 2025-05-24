import numpy as np
import cv2
from skimage.segmentation import felzenszwalb

class SegmentsDepthEnsemble:
    def __init__(self, scale=200, sigma=0.8, min_size=50):
        self.scale, self.sigma, self.min_size = scale, sigma, min_size
    
    def segment_image(self, image):
        return felzenszwalb(image, scale=self.scale, 
                            sigma=self.sigma, min_size=self.min_size)
    
    def compute_segment_features(self, depth_map, segmentation):
        features = {}
        for i in range(np.max(segmentation) + 1):
            mask = (segmentation == i)
            if mask.sum() > 0:
                features[i] = {
                    'mask': mask,
                    'mean_depth': depth_map[mask].mean(),
                    'std_depth': depth_map[mask].std(),
                    'confidence': 1 / (depth_map[mask].std() + 1e-5),
                    'size': mask.sum()
                }
        return features
    
    def fuse_depths(self, depth1, depth2, segments1, segments2, 
                    conf_threshold=1.2):
        fused_depth = depth1.copy()
        for i in segments1:
            if i in segments2:
                s1, s2 = segments1[i], segments2[i]
                mask = s1['mask']
                if (s1['mean_depth'] > 0.999 and s1['std_depth'] < 0.001) or \
                (s2['mean_depth'] > 0.999 and s2['std_depth'] < 0.001):
                    fused_depth[mask] = 1.0
                    continue
                conf_ratio = s2['confidence'] / (s1['confidence'] + 1e-5)
                if conf_ratio > conf_threshold:
                    fused_depth[mask] = depth2[mask]
        return fused_depth
    
    def ensemble_depth_maps(self, depth1, depth2, image):
        segmentation = self.segment_image(image)
        seg1 = self.compute_segment_features(depth1, segmentation)
        seg2 = self.compute_segment_features(depth2, segmentation)
        return self.fuse_depths(depth1, depth2, seg1, seg2)
