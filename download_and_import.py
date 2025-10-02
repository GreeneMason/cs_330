"""Download a Kaggle dataset (by dataset slug) and import CSV files into a SQLite database.

Usage:
    python download_and_import.py <kaggle-dataset-slug> [--db path/to/db.sqlite]

Example dataset slug formats:
    zynicide/wine-reviews
    uciml/iris

This script expects a local `kaggle.json` file with your API credentials in the same
directory or in ~/.kaggle/kaggle.json. The script will download files into ./data/
and create a SQLite database (default: data/dataset.db).
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd


def ensure_kaggle_config():
    # kaggle CLI looks for ~/.kaggle/kaggle.json on Windows too.
    home = Path.home()
    kaggle_dir = home / '.kaggle'
    target = kaggle_dir / 'kaggle.json'
    local = Path('kaggle.json')
    if target.exists():
        return
    if local.exists():
        kaggle_dir.mkdir(exist_ok=True)
        shutil.copy(local, target)
        os.chmod(target, 0o600)
        print(f'Copied local kaggle.json to {target}')
        return
    print('kaggle.json not found. Please place your kaggle.json in this directory or in ~/.kaggle/')
    sys.exit(1)


def download_dataset(slug, force=False, dest='data'):
    dest_path = Path(dest)
    dest_path.mkdir(parents=True, exist_ok=True)
    cmd = ['kaggle', 'datasets', 'download', '-d', slug, '-p', str(dest_path)]
    if force:
        cmd.append('--force')
    print('Running:', ' '.join(cmd))
    subprocess.check_call(cmd)


def unzip_all(dest='data'):
    import zipfile
    dest_path = Path(dest)
    for z in dest_path.glob('*.zip'):
        print('Extracting', z)
        with zipfile.ZipFile(z, 'r') as zf:
            zf.extractall(dest_path)


def import_csvs_to_sqlite(db_path='data/dataset.db', data_dir='data'):
    db_path = Path(db_path)
    data_dir = Path(data_dir)
    csv_files = list(data_dir.glob('**/*.csv'))
    if not csv_files:
        print('No CSV files found in', data_dir)
        return
    import sqlite3
    conn = sqlite3.connect(str(db_path))
    for csv in csv_files:
        table_name = csv.stem
        print(f'Importing {csv} -> table {table_name}')
        df = pd.read_csv(csv)
        # sanitize column names
        df.columns = [c.strip().replace(' ', '_').replace('-', '_') for c in df.columns]
        df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()
    print('Imported', len(csv_files), 'files into', db_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('slug', help='Kaggle dataset slug, e.g. owner/dataset')
    parser.add_argument('--db', default='data/dataset.db', help='Path for output SQLite DB')
    parser.add_argument('--force', action='store_true', help='Force redownload')
    args = parser.parse_args()

    ensure_kaggle_config()
    download_dataset(args.slug, force=args.force)
    unzip_all()
    import_csvs_to_sqlite(db_path=args.db)


if __name__ == '__main__':
    main()
