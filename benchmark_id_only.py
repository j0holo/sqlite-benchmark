import sqlite3
import time
import statistics
from prettytable import PrettyTable


def benchmark_query(db_path, query, params, iterations=100):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Warmup
    for _ in range(10):
        cursor.execute(query, params)
        cursor.fetchall()

    timings = []
    for _ in range(iterations):
        # Clear cache between runs (optional, depends on what you're measuring)
        # conn.execute("PRAGMA cache_size=0")
        # conn.execute("PRAGMA cache_size=-2000")

        start = time.perf_counter()
        cursor.execute(query, params)
        cursor.fetchall()
        end = time.perf_counter()

        timings.append((end - start) * 1000)

    conn.close()

    return {
        "mean": statistics.mean(timings),
        "median": statistics.median(timings),
        "stdev": statistics.stdev(timings),
        "min": min(timings),
        "max": max(timings),
    }


queries = {
    "enum_as_string_color": (
        "select id from enum_as_string where color = ? limit 1000",
        ("RED",),
    ),
    "enum_as_fk_color": (
        "select e.id from enum_as_fk e inner join color c on c.id = e.color where c.color = ? limit 1000",
        ("RED",),
    ),
    "enum_as_int_color": (
        "select id from enum_as_int where color = ? limit 1000",
        (1,),
    ),
    "enum_as_string_color_in": (
        "select id from enum_as_string where color in (?, ?) limit 1000",
        ("RED", "GREEN"),
    ),
    "enum_as_fk_color_in": (
        "select e.id from enum_as_fk e inner join color c on c.id = e.color where c.color IN (?, ?) limit 1000",
        ("RED", "GREEN"),
    ),
    "enum_as_int_color_in": (
        "select id from enum_as_int where color IN (?,?) limit 1000",
        (1, 4),
    ),
    "enum_as_string_color_and_status": (
        "select id from enum_as_string where color = ? and status = ? limit 1000",
        ("RED", "IN_PROGRESS"),
    ),
    "enum_as_fk_color_and_status": (
        """select e.id
        from enum_as_fk e
        inner join color c on c.id = e.color
        inner join status s on s.id = e.status
        where c.color = ? 
        and s.status = ?
        limit 1000""",
        ("RED", "IN_PROGRESS"),
    ),
    "enum_as_int_color_and_status": (
        "select id from enum_as_int where color = ? and status = ? limit 1000",
        (1, 2),
    ),
    "enum_as_string_color_and_status_and_order_type": (
        "select id from enum_as_string where color = ? and status = ? and order_type = ? limit 1000",
        ("RED", "IN_PROGRESS", "ONLINE"),
    ),
    "enum_as_fk_color_and_status_and_order_type": (
        """select e.id
        from enum_as_fk e
        inner join color c on c.id = e.color
        inner join status s on s.id = e.status
        inner join order_type ot on ot.id = e.order_type
        where c.color = ? 
        and s.status = ?
        and ot.order_type = ?
        limit 1000""",
        ("RED", "IN_PROGRESS", "ONLINE"),
    ),
    "enum_as_int_color_and_status_and_order_type": (
        "select id from enum_as_int where color = ? and status = ? and order_type = ? limit 1000",
        (1, 2, 2),
    ),
    "enum_as_string_two_negative_status_and_order_type": (
        "select id from enum_as_string where (status != ? and status != ?) and order_type = ? limit 1000",
        ("COMPLETED", "FAILED", "ONLINE"),
    ),
    "enum_as_fk_two_negative_status_and_order_type": (
        """select e.id
        from enum_as_fk e
        inner join status s on s.id = e.status
        inner join order_type ot on ot.id = e.order_type
        where (s.status != ? and s.status != ?)
        and ot.order_type = ?
        limit 1000""",
        ("COMPLETED", "FAILED", "ONLINE"),
    ),
    "enum_as_int_two_negative_status_and_order_type": (
        "select id from enum_as_int where (status != ? and status != ?) and order_type = ? limit 1000",
        (3, 4, 2),
    ),
    "enum_as_string_todo_in_progress_status_and_order_type": (
        "select id from enum_as_string where status in (?,?) and order_type = ? limit 1000",
        ("TODO", "IN_PROGRESS", "ONLINE"),
    ),
    "enum_as_fk_todo_in_progress_status_and_order_type": (
        """select e.id
        from enum_as_fk e
        inner join status s on s.id = e.status
        inner join order_type ot on ot.id = e.order_type
        where s.status in (?,?)
        and ot.order_type = ?
        limit 1000""",
        ("TODO", "IN_PROGRESS", "ONLINE"),
    ),
    "enum_as_int_todo_in_progress_status_and_order_type": (
        "select id from enum_as_int where status in (?,?) and order_type = ? limit 1000",
        (1, 2, 2),
    ),
}

results = {}
for name, (query, params) in queries.items():
    print(f"Benchmarking: {name}")
    results[name] = benchmark_query("benchmark.db", query, params)

table = PrettyTable()
table.field_names = ["Name", "Mean (ms)", "Median (ms)", "StdDev (ms)"]

for name, stats in results.items():
    table.add_row(
        [
            name,
            f"{stats['mean']:.3f}",
            f"{stats['median']:.3f}",
            f"{stats['stdev']:.3f}",
        ]
    )

print(table)
