import zipfile
import xml.etree.ElementTree as ET
import math
import os
# 最优飞行顺序达到最短路径

def haversine(coord1, coord2):
    R = 6371000
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def nearest_neighbor(points):
    unvisited = points.copy()
    path = [unvisited.pop(0)]
    while unvisited:
        last = path[-1]
        next_point = min(unvisited, key=lambda point: haversine(last, point))
        path.append(next_point)
        unvisited.remove(next_point)
    return path

def read_kmz_points(kmz_path):
    with zipfile.ZipFile(kmz_path, 'r') as kmz:
        kml_filename = [name for name in kmz.namelist() if name.endswith('.kml')][0]
        with kmz.open(kml_filename) as kml_file:
            tree = ET.parse(kml_file)
            root = tree.getroot()
            namespace = {'kml': 'http://www.opengis.net/kml/2.2'}
            
            coordinates = []
            for placemark in root.findall('.//kml:Placemark', namespace):
                coord = placemark.find('.//kml:coordinates', namespace)
                if coord is not None:
                    lon, lat, *_ = map(float, coord.text.strip().split(','))
                    coordinates.append((lat, lon))
            return coordinates

def write_kmz(points, output_kmz_path):
    kml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    {''.join([f'<Placemark><name>Point {i+1}</name><Point><coordinates>{lon},{lat},0</coordinates></Point></Placemark>' for i, (lat, lon) in enumerate(points)])}
    <Placemark>
      <name>Flight Path</name>
      <LineString>
        <coordinates>
          {''.join([f'{lon},{lat},0 ' for lat, lon in points])}
        </coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>
'''
    kml_filename = 'doc.kml'
    temp_kml_path = kml_filename  # 使用当前目录

    with open(temp_kml_path, 'w', encoding='utf-8') as f:
        f.write(kml_content)

    with zipfile.ZipFile(output_kmz_path, 'w', zipfile.ZIP_DEFLATED) as kmz:
        kmz.write(temp_kml_path, arcname=kml_filename)

    os.remove(temp_kml_path)

def plan_flight(input_kmz_path, output_kmz_path):
    points = read_kmz_points(input_kmz_path)
    if not points:
        raise ValueError("No points found in KMZ file.")
    optimized_points = nearest_neighbor(points)
    write_kmz(optimized_points, output_kmz_path)

if __name__ == "__main__":
    input_kmz = "munich_drone_path.kmz"   # 输入KMZ文件路径
    output_kmz = "path_to_output.kmz"       # 输出新的KMZ路径
    plan_flight(input_kmz, output_kmz)
    print(f"Optimized flight path saved to {output_kmz}")