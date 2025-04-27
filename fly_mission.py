# fly_mission.py
# 第二步：读取安全航点，进行路径规划，并控制无人机飞行

import json
import math
import time
from dji_sdk.dji_drone import DJIDrone

# ========================
# 参数配置
# ========================
WAYPOINTS_FILE = 'safe_waypoints.json'  # 第一步生成的新航点文件

# ========================
# 计算两点之间的大圆距离
# ========================
EARTH_RADIUS = 6371000  # 地球半径，米

def haversine_distance(lat1, lon1, lat2, lon2):
    """计算地球上两点之间的直线距离（米）"""
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return EARTH_RADIUS * c

# ========================
# 路径规划（最近邻算法）
# ========================
def plan_best_path(waypoints):
    if not waypoints:
        return []

    unvisited = waypoints.copy()
    path = []
    current = unvisited.pop(0)  # 从第一个点开始
    path.append(current)

    while unvisited:
        nearest = min(unvisited, key=lambda wp: haversine_distance(current['latitude'], current['longitude'], wp['latitude'], wp['longitude']))
        unvisited.remove(nearest)
        path.append(nearest)
        current = nearest

    return path

# ========================
# 上传航点任务到无人机
# ========================
def upload_waypoints_to_drone(drone, waypoints):
    print(f"Uploading {len(waypoints)} waypoints...")
    drone.init_waypoint_task(len(waypoints))
    
    for idx, wp in enumerate(waypoints):
        waypoint_task = {
            'index': idx,
            'latitude': wp['latitude'],
            'longitude': wp['longitude'],
            'altitude': wp['altitude'],
            'damping_distance': 0,
            'target_yaw': 0,
            'target_gimbal_pitch': 0,
            'turn_mode': 0,
            'has_action': 0,
            'action_time_limit': 0,
            'waypoint_action': [],
        }
        drone.upload_waypoint(waypoint_task)

    print("Waypoints uploaded successfully.")

# ========================
# 主程序入口
# ========================
def main():
    # 1. 读取安全航点
    with open(WAYPOINTS_FILE, 'r') as f:
        waypoints = json.load(f)

    print(f"Loaded {len(waypoints)} safe waypoints.")

    # 2. 路径优化
    optimized_waypoints = plan_best_path(waypoints)
    print("Waypoint path optimized.")

    # 3. 连接无人机
    drone = DJIDrone()
    print("Connected to drone.")

    # 4. 获取控制权限
    print("Requesting control authority...")
    drone.request_sdk_permission_control()
    time.sleep(2)

    # 5. 起飞
    print("Taking off...")
    drone.takeoff()
    time.sleep(10)  # 等待飞稳

    # 6. 上传航点任务
    upload_waypoints_to_drone(drone, optimized_waypoints)
    time.sleep(2)

    # 7. 开始任务
    print("Starting waypoint mission...")
    drone.start_waypoint_task()
    print("Mission started.")

    # 8. 等待任务完成
    mission_duration = len(optimized_waypoints) * 10  # 估算每个点飞行10秒
    time.sleep(mission_duration)

    # 9. 降落
    print("Landing...")
    drone.landing()

if __name__ == "__main__":
    main()
