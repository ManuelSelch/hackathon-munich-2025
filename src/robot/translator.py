import numpy as np
from typing import Tuple

def depth_map_to_world_coordinates(
    depth_map: np.ndarray,
    camera_intrinsics: dict,
    translation: list = [-0.008014187922463454, 0.10701197858990913, 0.025430542829620165],
    rotation: list = [0.3041858241574262, -0.0006167631890864009, 0.0023871846853336254, 0.952609524062254]
) -> np.ndarray:
    """
    Convert depth map pixels to world coordinates relative to robot TCP using hand-eye calibration.
    
    Args:
        depth_map (np.ndarray): Depth map array (H x W) with depth values in meters
        camera_intrinsics (dict): Camera intrinsic parameters containing:
            - 'fx': focal length in x
            - 'fy': focal length in y  
            - 'cx': principal point x
            - 'cy': principal point y
        hand_eye_translation (list): Translation vector from TCP to camera [x, y, z] in meters
        hand_eye_rotation_quat (list): Rotation quaternion from TCP to camera [x, y, z, w]
    
    Returns:
        np.ndarray: Array of shape (H, W, 3) containing world XYZ coordinates for each pixel
                   relative to robot TCP
    """
    
    def quaternion_to_rotation_matrix(q: list) -> np.ndarray:
        """Convert quaternion [x, y, z, w] to 3x3 rotation matrix."""
        x, y, z, w = q
        
        # Normalize quaternion
        norm = np.sqrt(x*x + y*y + z*z + w*w)
        x, y, z, w = x/norm, y/norm, z/norm, w/norm
        
        # Convert to rotation matrix
        R = np.array([
            [1 - 2*(y*y + z*z),     2*(x*y - z*w),     2*(x*z + y*w)],
            [    2*(x*y + z*w), 1 - 2*(x*x + z*z),     2*(y*z - x*w)],
            [    2*(x*z - y*w),     2*(y*z + x*w), 1 - 2*(x*x + y*y)]
        ])
        
        return R
    
    # Get depth map dimensions
    height, width = depth_map.shape
    
    # Extract camera intrinsics
    fx = camera_intrinsics['fx']
    fy = camera_intrinsics['fy']
    cx = camera_intrinsics['cx']
    cy = camera_intrinsics['cy']
    
    # Create pixel coordinate grids
    u, v = np.meshgrid(np.arange(width), np.arange(height))
    
    # Convert depth map to camera coordinates
    # Remove invalid depth values (typically 0 or very large values)
    valid_depth = (depth_map > 0) & (depth_map < 10.0)  # Assume max valid depth of 10m
    
    # Initialize output array
    world_coordinates = np.zeros((height, width, 3))
    
    # Convert pixels to camera coordinates where depth is valid
    z_cam = depth_map.copy()
    x_cam = (u - cx) * z_cam / fx
    y_cam = (v - cy) * z_cam / fy
    
    # Stack into homogeneous coordinates (N x 3)
    camera_points = np.stack([x_cam, y_cam, z_cam], axis=-1)
    
    # Convert hand-eye calibration to transformation matrix
    R_tcp_to_cam = quaternion_to_rotation_matrix(rotation)
    t_tcp_to_cam = np.array(translation).reshape(3, 1)
    
    # Create transformation matrix from TCP to camera
    T_tcp_to_cam = np.eye(4)
    T_tcp_to_cam[:3, :3] = R_tcp_to_cam
    T_tcp_to_cam[:3, 3] = t_tcp_to_cam.flatten()
    
    # Invert to get camera to TCP transformation
    T_cam_to_tcp = np.linalg.inv(T_tcp_to_cam)
    R_cam_to_tcp = T_cam_to_tcp[:3, :3]
    t_cam_to_tcp = T_cam_to_tcp[:3, 3]
    
    # Transform camera coordinates to TCP coordinates
    # Reshape for matrix multiplication
    camera_points_reshaped = camera_points.reshape(-1, 3).T  # 3 x N
    
    # Apply rotation and translation
    tcp_points = R_cam_to_tcp @ camera_points_reshaped + t_cam_to_tcp.reshape(3, 1)
    
    # Reshape back to original dimensions
    world_coordinates = tcp_points.T.reshape(height, width, 3)
    
    # Set invalid depth pixels to NaN
    world_coordinates[~valid_depth] = np.nan
    
    return world_coordinates


def get_pixel_world_coordinate(
    pixel_u: int, 
    pixel_v: int, 
    depth_value: float,
    camera_intrinsics: dict,
    hand_eye_translation: list = [-0.008014187922463454, 0.10701197858990913, 0.025430542829620165],
    hand_eye_rotation_quat: list = [0.3041858241574262, -0.0006167631890864009, 0.0023871846853336254, 0.952609524062254]
) -> Tuple[float, float, float]:
    """
    Get world coordinates for a single pixel.
    
    Args:
        pixel_u (int): Pixel u coordinate (column)
        pixel_v (int): Pixel v coordinate (row)
        depth_value (float): Depth value at the pixel in meters
        camera_intrinsics (dict): Camera intrinsic parameters
        hand_eye_translation (list): Translation vector from TCP to camera
        hand_eye_rotation_quat (list): Rotation quaternion from TCP to camera
        
    Returns:
        Tuple[float, float, float]: World XYZ coordinates relative to robot TCP
    """
    
    # Create a minimal depth map for this single pixel
    depth_map = np.zeros((pixel_v + 1, pixel_u + 1))
    depth_map[pixel_v, pixel_u] = depth_value
    
    # Get world coordinates
    world_coords = depth_map_to_world_coordinates(
        depth_map, camera_intrinsics, hand_eye_translation, hand_eye_rotation_quat
    )
    
    return tuple(world_coords[pixel_v, pixel_u])


# RealSense D435 typical intrinsics
def get_realsense_d435_intrinsics() -> dict:
    """
    Get typical intrinsic parameters for Intel RealSense D435 camera.
    
    Args:
        resolution (str): Camera resolution - "640x480", "1280x720", or "1920x1080"
        
    Returns:
        dict: Camera intrinsic parameters
        
    Note: These are typical values. For best accuracy, retrieve actual calibrated
          intrinsics from your specific camera using pyrealsense2.
    """
    
    intrinsics = {
        'fx': 383.0,   # focal length x (pixels)
        'fy': 383.0,   # focal length y (pixels)  
        'cx': 320.0,   # principal point x (pixels)
        'cy': 240.0,   # principal point y (pixels)
        'width': 640,
        'height': 480
    }
    
    return intrinsics