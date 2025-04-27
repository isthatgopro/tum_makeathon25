# generate_safe_waypoints.py
# 第一步：读取原始json，偏移组合，输出新的航点

import json
import math

# ========================
# 参数配置
# ========================
INPUT_JSON_FILE = 'barcode_global_coords_full.json'  # 原始json文件
OUTPUT_JSON_FILE = 'safe_waypoints.json'  # 生成新航点文件
OFFSET_METERS = 5.0  # 偏移距离（米）
DEFAULT_ALTITUDE = 10.0  # 默认飞行高度（米）

METER_PER_DEGREE_LAT = 111320
METER_PER_DEGREE_LON = 40075000 * math.cos(math.radians(48.19)) / 360  # 根据经度调整

# ========================
# 从json读取原始数据，生成安全航点
# ========================
def generate_safe_waypoints(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    waypoints = []
    for entry in data:
        center_lat = entry['latitude']
        center_lon = entry['longitude']

        delta_lat = OFFSET_METERS / METER_PER_DEGREE_LAT
        delta_lon = OFFSET_METERS / METER_PER_DEGREE_LON

        safe_lat = center_lat + delta_lat
        safe_lon = center_lon + delta_lon

        waypoint = {
            'latitude': safe_lat,
            'longitude': safe_lon,
            'altitude': DEFAULT_ALTITUDE
        }
        waypoints.append(waypoint)

    # 写入新文件
    with open(output_file, 'w') as f:
        json.dump(waypoints, f, indent=4)
    print(f"Generated {len(waypoints)} safe waypoints saved to {output_file}")

if __name__ == "__main__":
    generate_safe_waypoints(INPUT_JSON_FILE, OUTPUT_JSON_FILE)
