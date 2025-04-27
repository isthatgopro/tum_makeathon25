from src.utils.representative_selector import select_group_representatives

if __name__ == '__main__':
    select_group_representatives(
        location_groups_path='results/location_groups.json',
        barcodes_path='results/yolov8_best_predictionn_test_data.json',
        output_path='results/representatives.json',
        big_group_threshold_ratio=1.0,  # 大于平均大小的组为大组
        min_big_group_size=50           # 或者直接按最小 50 张以上为大组
    )
