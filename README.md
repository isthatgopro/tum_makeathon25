# DeepSick GR9 项目

## 项目概述
这是一个基于无人机和计算机视觉的项目，主要用于条形码识别和路径规划。项目结合了YOLO目标检测、路径规划和无人机控制等功能。

## 主要功能
- 条形码检测与识别
- 无人机路径规划
- 安全航点生成
- 可视化工具
- AWS S3和Bedrock集成

## 技术栈
- Python 3.x
- YOLOv8
- AWS S3
- AWS Bedrock
- OpenCV
- NumPy
- scikit-learn

## 安装步骤

### 1. 环境准备
```bash
# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. AWS配置
1. 创建AWS访问密钥 [链接](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-key-self-managed.html)
2. 创建`.env`文件并添加以下内容：
```
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
```

## 详细使用说明

### 1. 条形码检测 (yolo_barcode_predict.py)
```bash
python yolo_barcode_predict.py
```
- 功能：使用YOLOv8模型检测图像中的条形码
- 输入：`drive/MyDrive/test_data/`目录下的图像
- 输出：
  - 标注后的图像保存在`pred_test_data0427`目录
  - 检测结果保存在`yolov8_best_predictions_test_data0427.json`
- 参数说明：
  - `imgsz`: 图像大小（默认1280）
  - `conf`: 置信度阈值（默认0.25）
  - `device`: 运行设备（0表示GPU）

### 2. 路径规划 (path.py)
```bash
python path.py
```
- 功能：优化无人机飞行路径，使用最近邻算法计算最短路径
- 输入：`munich_drone_path.kmz`文件
- 输出：`path_to_output.kmz`文件
- 参数说明：
  - `input_kmz`: 输入KMZ文件路径
  - `output_kmz`: 输出KMZ文件路径

### 3. 安全航点生成 (generate_safe_points.py)
```bash
python generate_safe_points.py
```
- 功能：根据障碍物信息生成安全的飞行航点
- 输入：障碍物信息JSON文件
- 输出：`safe_waypoints.json`文件
- 参数说明：
  - 输入文件路径可在代码中配置

### 4. 无人机任务执行 (fly_mission.py)
```bash
python fly_mission.py
```
- 功能：控制无人机执行飞行任务
- 输入：`safe_waypoints.json`文件
- 参数说明：
  - `WAYPOINTS_FILE`: 航点文件路径
  - 飞行高度、速度等参数可在代码中配置
- 注意事项：
  - 确保无人机已连接
  - 确保有足够的GPS信号
  - 确保飞行区域安全

### 5. AWS S3示例 (s3_local.py)
```bash
python s3_local.py
```
- 功能：演示AWS S3的基本操作
- 配置：
  - 需要设置正确的AWS凭证
  - 需要修改代码中的bucket名称和文件路径

### 6. AWS Bedrock示例 (bedrock_local.py)
```bash
python bedrock_local.py
```
- 功能：演示AWS Bedrock的基本操作
- 配置：
  - 需要设置正确的AWS凭证
  - 需要选择适当的模型和参数

## 项目结构
```
.
├── src/                    # 源代码目录
├── weights/               # 模型权重文件
├── test_data/            # 测试数据
├── results/              # 输出结果
├── .venv/                # 虚拟环境
├── requirements.txt      # 项目依赖
└── README.md            # 项目文档
```

## 注意事项
1. 确保在使用前正确配置AWS凭证
2. 运行程序时，先启动后端（端口3000），再启动前端（端口3001）
3. 如果端口被占用，请关闭所有相关程序后重试
4. 请勿在公共仓库中存储访问密钥
5. 使用无人机功能时，请确保：
   - 遵守当地无人机飞行法规
   - 确保飞行区域安全
   - 保持足够的GPS信号
   - 注意电池电量

## 贡献指南
欢迎提交Issue和Pull Request来改进项目。

## 许可证
[待定]
