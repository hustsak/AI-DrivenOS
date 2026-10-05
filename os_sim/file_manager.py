"""
File Manager — disk usage stats + simulated temp file cleaning
"""

import os
import tempfile
import psutil
import glob


def get_disk_usage():
    """Return disk usage for all mounted partitions."""
    lines = [f"{'MOUNT':<20} {'TOTAL':<10} {'USED':<10} {'FREE':<10} {'USE%'}"]
    lines.append("-" * 60)

    partitions_data = []
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
            total_gb = round(usage.total / (1024 ** 3), 1)
            used_gb = round(usage.used / (1024 ** 3), 1)
            free_gb = round(usage.free / (1024 ** 3), 1)
            percent = usage.percent

            lines.append(f"{part.mountpoint:<20} {total_gb:<10} {used_gb:<10} {free_gb:<10} {percent}%")
            partitions_data.append({
                "mount": part.mountpoint,
                "total_gb": total_gb,
                "used_gb": used_gb,
                "free_gb": free_gb,
                "percent": percent
            })
        except PermissionError:
            continue

    return {
        "status": "success",
        "message": "Disk usage retrieved",
        "data": partitions_data,
        "display": "\n".join(lines)
    }


def clean_temp_files():
    """Scan and simulate cleaning of temp files."""
    temp_dir = tempfile.gettempdir()
    cleaned_files = []
    total_size = 0
    errors = 0

    try:
        entries = os.scandir(temp_dir)
        for entry in entries:
            try:
                size = entry.stat().st_size
                cleaned_files.append({
                    "name": entry.name[:40],
                    "size_kb": round(size / 1024, 1)
                })
                total_size += size
            except (PermissionError, FileNotFoundError):
                errors += 1
    except Exception as e:
        return {
            "status": "error",
            "message": f"Could not scan temp directory: {e}",
            "data": None
        }

    total_mb = round(total_size / (1024 ** 2), 2)
    count = len(cleaned_files)
    cleaned_files.sort(key=lambda x: x['size_kb'], reverse=True)

    lines = [f"🧹 Temp Directory Scan: {temp_dir}\n"]
    lines.append(f"Files found:    {count}")
    lines.append(f"Total size:     {total_mb} MB")
    lines.append(f"Skipped:        {errors} (permission denied)\n")
    if cleaned_files[:5]:
        lines.append("Largest files (simulated clean):")
        for f in cleaned_files[:5]:
            lines.append(f"  {f['name'][:35]:<35} {f['size_kb']} KB")
    lines.append(f"\n✅ Simulated: {count} files cleaned, {total_mb} MB freed.")

    return {
        "status": "success",
        "message": f"Cleaned {count} temp files ({total_mb} MB freed)",
        "data": {
            "files_cleaned": count,
            "freed_mb": total_mb,
            "top_files": cleaned_files[:5]
        },
        "display": "\n".join(lines)
    }


def list_files(directory="."):
    """List files in a given directory."""
    try:
        entries = list(os.scandir(directory))
        files = []
        for e in entries[:20]:
            try:
                size = e.stat().st_size
                files.append({
                    "name": e.name,
                    "type": "dir" if e.is_dir() else "file",
                    "size_kb": round(size / 1024, 1)
                })
            except:
                pass

        lines = [f"📁 Contents of: {os.path.abspath(directory)}\n"]
        lines.append(f"{'NAME':<35} {'TYPE':<8} {'SIZE (KB)'}")
        lines.append("-" * 55)
        for f in files:
            icon = "📂" if f['type'] == "dir" else "📄"
            lines.append(f"{icon} {f['name'][:33]:<35} {f['type']:<8} {f['size_kb']}")

        return {
            "status": "success",
            "message": f"Listed {len(files)} items in {directory}",
            "data": files,
            "display": "\n".join(lines)
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "data": None}
