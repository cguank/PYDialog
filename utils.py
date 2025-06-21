import os
import cv2
import numpy as np

def get_template_paths(dir_path):
    """
    遍历imgs目录获取所有图片路径
    
    Returns:
        list: 图片路径列表
    """
    template_paths = []
    imgs_dir = dir_path
    
    # 确保目录存在
    if not os.path.exists(imgs_dir):
        return template_paths
        
    # 遍历目录下所有文件
    for file in os.listdir(imgs_dir):
        # 检查是否为图片文件
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            template_paths.append(os.path.join(imgs_dir, file))
            
    return template_paths

def prehandle_template(screen,template):
    # 预处理：灰度化 + 高斯模糊 + 直方图均衡化
    list = [screen,template]
    result = []
    for img in list:
        original_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
        equalized_img = cv2.equalizeHist(gray_img)
        normalize_img = cv2.normalize(gray_img, None, 0, 255, cv2.NORM_MINMAX)
        result.append({"gray_img":gray_img,"blurred_img":blurred_img,"equalized_img":equalized_img,"original_img":img,"normalize":normalize_img})
    return result
    # return equalized_img

def preprocess_for_button_detection(image):
    """专门用于按钮检测的预处理"""
    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 定义蓝色的HSV范围
    blue_lower = np.array([100, 150, 50])
    blue_upper = np.array([130, 255, 255])
    
    # 创建蓝色掩码
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    
    # 形态学操作，去除噪声
    kernel = np.ones((3,3), np.uint8)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernel)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
    
    # 找到轮廓
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 创建结果图像
    result = np.zeros_like(image)
    
    # 只保留最大的蓝色区域（通常是按钮）
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(result, [largest_contour], -1, (255, 255, 255), -1)
    
    # 转换为灰度图
    gray_result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    
    return gray_result
