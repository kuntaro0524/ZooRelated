import os
import sys
from datetime import datetime

def get_cps_dirs(path):
    cps_dirs = []
    for entry in os.scandir(path):
        if entry.is_dir() and 'CPS' in entry.name:
            cps_dirs.append((entry.name, entry.stat().st_mtime))
    return cps_dirs

def main(target_dir):
    cps_dirs = get_cps_dirs(target_dir)
    if not cps_dirs:
        print("CPS を含むディレクトリが見つかりませんでした。")
        return

    # 最小・最大を取得（mtimeがキー）
    oldest = min(cps_dirs, key=lambda x: x[1])
    newest = max(cps_dirs, key=lambda x: x[1])

    dt_old = datetime.fromtimestamp(oldest[1])
    dt_new = datetime.fromtimestamp(newest[1])
    delta = dt_new - dt_old

    print(f"最古: {dt_old} ({oldest[0]})")
    print(f"最新: {dt_new} ({newest[0]})")
    print(f"時間差: {delta}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使い方: python script.py /path/to/target_dir")
        sys.exit(1)
    main(sys.argv[1])

