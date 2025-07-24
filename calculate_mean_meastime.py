import os
import sys
from datetime import datetime, timedelta
import statistics

SERIES_GAP_THRESHOLD = 1200  # 20 minutes

def get_cps_dirs(path):
    cps_dirs = []
    for entry in os.scandir(path):
        if entry.is_dir() and 'CPS' in entry.name:
            ctime = entry.stat().st_mtime
            cps_dirs.append((entry.name, ctime))
    return sorted(cps_dirs, key=lambda x: x[1])

def group_into_series(cps_dirs, threshold=SERIES_GAP_THRESHOLD):
    series = []
    current_series = []

    for i, item in enumerate(cps_dirs):
        if i == 0:
            current_series.append(item)
        else:
            prev_time = cps_dirs[i - 1][1]
            curr_time = item[1]
            if curr_time - prev_time > threshold:
                series.append(current_series)
                current_series = [item]
            else:
                current_series.append(item)

    if current_series:
        series.append(current_series)

    return series

def analyze_series(series_list):
    all_laps = []

    print("\n--- 各シリーズの統計 ---")
    for idx, series in enumerate(series_list):
        print(f"\nSeries {idx+1}:")
        print(f"  ディレクトリ数: {len(series)}")

        # シリーズの開始・終了時間
        start_time = datetime.fromtimestamp(series[0][1])
        end_time   = datetime.fromtimestamp(series[-1][1])
        print(f"  開始時間: {start_time}")
        print(f"  終了時間: {end_time}")

        if len(series) < 2:
            print("  ※ ディレクトリ数が1つのみのためラップタイム統計は計算不能")
            continue

        # (lap_time, dir1, dir2)
        laps = [
            (series[i][1] - series[i-1][1], series[i-1][0], series[i][0])
            for i in range(1, len(series))
        ]

        all_laps.extend([lap[0] for lap in laps])

        # 統計値
        mean_lap = statistics.mean([lap[0] for lap in laps])
        min_lap_entry = min(laps, key=lambda x: x[0])
        max_lap_entry = max(laps, key=lambda x: x[0])

        print(f"  測定間隔（平均）: {timedelta(seconds=mean_lap)}")
        print(f"  測定間隔（最小）: {timedelta(seconds=min_lap_entry[0])}  （{min_lap_entry[1]} → {min_lap_entry[2]}）")
        print(f"  測定間隔（最大）: {timedelta(seconds=max_lap_entry[0])}  （{max_lap_entry[1]} → {max_lap_entry[2]}）")

    return all_laps

def main(target_dir):
    cps_dirs = get_cps_dirs(target_dir)
    if not cps_dirs:
        print("CPSを含むディレクトリが見つかりません。")
        return

    series_list = group_into_series(cps_dirs)
    print(f"\n検出されたシリーズ数: {len(series_list)}")

    lap_times = analyze_series(series_list)

    if not lap_times:
        print("\n全体のラップタイム統計は計算できませんでした。")
        return

    avg_lap = statistics.mean(lap_times)
    print("\n--- 全体統計 ---")
    print(f"  総ラップタイム数: {len(lap_times)}")
    print(f"  平均ラップタイム（全シリーズ含む）: {timedelta(seconds=avg_lap)}（{avg_lap:.1f}秒）")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使い方: python cps_laptime_analyzer.py /path/to/target_dir")
        sys.exit(1)
    main(sys.argv[1])

