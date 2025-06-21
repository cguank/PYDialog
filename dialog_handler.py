import os
import cv2
import pyautogui
import numpy as np
import time
import logging
from datetime import datetime

from utils import get_template_paths, prehandle_template, preprocess_for_button_detection

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dialog_handler.log'),
        logging.StreamHandler()
    ]
)

class DialogHandler:
    def __init__(self, match_threshold):
        # 设置PyAutoGUI的安全设置
        pyautogui.FAILSAFE = True
        # 设置操作间隔
        pyautogui.PAUSE = 0.5
        # 设置模板匹配阈值
        self.match_threshold = match_threshold
        
    def capture_screen(self):
        """捕获屏幕截图"""
        try:
            screenshot = pyautogui.screenshot()
            # 转换为BGR格式，确保与模板颜色通道一致
            screen_array = np.array(screenshot)
            if screen_array.shape[2] == 4:  # RGBA
                screen_bgr = cv2.cvtColor(screen_array, cv2.COLOR_RGBA2BGR)
            else:  # RGB
                screen_bgr = cv2.cvtColor(screen_array, cv2.COLOR_RGB2BGR)
            # 缩小图像尺寸为原来的一半
            screen_bgr = cv2.resize(screen_bgr, (screen_bgr.shape[1]//2, screen_bgr.shape[0]//2))
            print(f"=========screen_bgr.shape{screen_bgr.shape}")
            return screen_bgr
        except Exception as e:
            logging.error(f"截图失败: {str(e)}")
            return None

    def find_dialog(self, template_path):
        """查找弹窗"""
        try:
            # 读取模板图片
            template_img = cv2.imread(template_path)
            template_img = cv2.resize(template_img, (template_img.shape[1]//2, template_img.shape[0]//2))
            print(f"=========template_img.shape{template_img.shape}")
            if template_img is None:
                logging.error(f"无法读取模板图片: {template_path}")
                return None

            # 获取屏幕截图
            screen = self.capture_screen()
            if screen is None:
                return None

            try:
                
                [handled_screen_json, handled_template_json] = prehandle_template(screen, template_img)
                img_type = 'original_img'  # 使用模糊图像，因为诊断显示它的匹配值最高
                # 保存预处理后的图片用于调试
                result4 = cv2.matchTemplate(handled_screen_json[img_type], handled_template_json[img_type], cv2.TM_SQDIFF_NORMED)
                min_val4, max_val4, min_loc4, max_loc4 = cv2.minMaxLoc(result4)
                print(f"传统预处理方法 - 最大匹配值: {min_val4} {max_val4}")
                
                if min_val4 < self.match_threshold:
                    print(f"✅ 传统预处理方法找到匹配! 位置: {max_loc4}, 匹配值: {max_val4:.3f}")
                    return min_loc4
            except Exception as e:
                print(f"传统预处理方法失败: {e}")

            print(f"❌ 所有方法都未达到阈值 {self.match_threshold}")
            return None

        except Exception as e:
            logging.error(f"查找弹窗失败: {str(e)}")
            return None

    def click_dialog(self, location, template_path):
        """点击弹窗"""
        try:
            if location:
                # 获取模板图片尺寸
                template = cv2.imread(template_path)
                h, w = template.shape[:2]
                print("========location",location,h,w)
                
                # 计算点击位置（模板中心）
                click_x = location[0] + w // 4
                click_y = location[1] + h // 4
                
                # 移动鼠标并点击
                # pyautogui.moveTo(location[0], location[1], duration=0.5)
                pyautogui.moveTo(click_x, click_y, duration=0.5)
                pyautogui.click()
                logging.info(f"成功点击弹窗，位置: ({click_x}, {click_y})")
                # 保存当前截图
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot = pyautogui.screenshot()
                screenshot_path = f"screenshots/click_{timestamp}.png"
                os.makedirs("screenshots", exist_ok=True)
                screenshot.save(screenshot_path)
                logging.info(f"截图已保存至: {screenshot_path}")
                exit()
                return True
            return False
        except Exception as e:
            logging.error(f"点击弹窗失败: {str(e)}")
            return False

    def monitor_dialog(self, template_paths, interval=1):
        """持续监控弹窗"""
        logging.info("开始监控弹窗...")
        while True:
            try:
                for template_path in template_paths:
                    location = self.find_dialog(template_path)
                    if location:
                        if self.click_dialog(location, template_path):
                            logging.info("弹窗处理成功")
                time.sleep(interval)
            except KeyboardInterrupt:
                logging.info("监控已停止")
                break
            except Exception as e:
                logging.error(f"监控过程出错: {str(e)}")
                time.sleep(interval)

if __name__ == "__main__":
    # 获取屏幕宽高
    screen_width, screen_height = pyautogui.size()
    print(f"屏幕分辨率: {screen_width} x {screen_height}")
    
    # 创建处理器实例，可以调整匹配阈值
    # 如果匹配太严格，可以降低阈值，比如 0.5 或 0.4
    # 如果匹配太宽松，可以提高阈值，比如 0.7 或 0.8
    handler = DialogHandler(match_threshold=0.1)
    
    # 实时打印鼠标位置
    # def print_mouse_position():
    #     while True:
    #         x, y = pyautogui.position()
    #         print(f"当前鼠标位置: x={x}, y={y}")
    #         time.sleep(1)
    
    # # 启动打印鼠标位置的线程
    # import threading
    # mouse_thread = threading.Thread(target=print_mouse_position)
    # mouse_thread.daemon = True  # 设置为守护线程,主程序退出时会自动结束
    # mouse_thread.start()
    
    # 这里需要替换为实际的弹窗模板图片路径
    # 定义多个模板图片路径
    template_paths = get_template_paths("./imgs")
    
    # 遍历所有模板图片进行监控
    # for template_path in template_paths:
    #         handler.monitor_dialog(template_path)
    # template_path = "./imgs/img2.png"
    handler.monitor_dialog(template_paths) 