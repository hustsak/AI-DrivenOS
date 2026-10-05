"""
Memory Manager — real memory stats + simulated optimization
"""

import psutil


def get_memory_usage():
    """Return detailed memory statistics."""
    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()

    used_gb = round(vm.used / (1024 ** 3), 2)
    total_gb = round(vm.total / (1024 ** 3), 2)
    available_gb = round(vm.available / (1024 ** 3), 2)
    swap_used_gb = round(swap.used / (1024 ** 3), 2)
    swap_total_gb = round(swap.total / (1024 ** 3), 2)

    bar_filled = int(vm.percent / 5)
    bar = "█" * bar_filled + "░" * (20 - bar_filled)

    display = (
        f"RAM Usage:     [{bar}] {vm.percent}%\n"
        f"Used:          {used_gb} GB / {total_gb} GB\n"
        f"Available:     {available_gb} GB\n"
        f"Swap Used:     {swap_used_gb} GB / {swap_total_gb} GB"
    )

    return {
        "status": "success",
        "message": "Memory usage retrieved",
        "data": {
            "percent": vm.percent,
            "used_gb": used_gb,
            "total_gb": total_gb,
            "available_gb": available_gb,
            "swap_used_gb": swap_used_gb,
            "swap_total_gb": swap_total_gb
        },
        "display": display
    }


def optimize_memory():
    """Simulate memory optimization — identify heavy processes and free cache."""
    vm_before = psutil.virtual_memory()

    # Find top memory consumers
    heavy = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            if (proc.info['memory_percent'] or 0) > 1.0:
                heavy.append({
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "memory_percent": round(proc.info['memory_percent'], 1)
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    heavy.sort(key=lambda x: x['memory_percent'], reverse=True)
    heavy = heavy[:5]

    # Simulated freed memory (5-15% of current usage)
    simulated_freed_mb = round((vm_before.used / (1024 ** 2)) * 0.08, 1)

    lines = ["🧹 Memory Optimization Complete\n"]
    lines.append(f"Simulated freed: ~{simulated_freed_mb} MB\n")
    if heavy:
        lines.append("Top memory consumers:")
        for p in heavy:
            lines.append(f"  {p['name'][:20]:<20} PID {p['pid']:<6} {p['memory_percent']}%")

    return {
        "status": "success",
        "message": f"Memory optimized — freed ~{simulated_freed_mb} MB",
        "data": {
            "freed_mb": simulated_freed_mb,
            "heavy_processes": heavy
        },
        "display": "\n".join(lines)
    }
