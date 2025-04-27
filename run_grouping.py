from src.utils.image_geogrouping import group_by_location_only

if __name__ == '__main__':
    group_by_location_only(
        metadata_json='results/metadata.json',
        output_json='results/location_groups.json',
        eps_meters=3.2,    # 距离阈值（3.2米）
        min_samples=6      # 每组至少6张图片
    )
