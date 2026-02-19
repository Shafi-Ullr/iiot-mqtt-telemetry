import sqlite3
import csv
import os

DB = "telemetry.db"


def connect():
    return sqlite3.connect(DB)


def fault_summary():
    con = connect()
    cur = con.cursor()

    total = cur.execute("SELECT COUNT(*) FROM telemetry").fetchone()[0]
    faults_total = cur.execute(
        "SELECT COUNT(*) FROM telemetry WHERE fault_code != 0"
    ).fetchone()[0]

    by_code = cur.execute("""
        SELECT fault_code, COUNT(*) as n
        FROM telemetry
        WHERE fault_code != 0
        GROUP BY fault_code
        ORDER BY n DESC
    """).fetchall()

    last_fault_by_asset = cur.execute("""
        SELECT asset, MAX(received_utc) as last_fault_time
        FROM telemetry
        WHERE fault_code != 0
        GROUP BY asset
        ORDER BY last_fault_time DESC
    """).fetchall()

    con.close()

    print("=== FAULT SUMMARY ===")
    print("Total rows:", total)
    print("Fault rows (fault_code != 0):", faults_total)
    print("")

    print("Faults by code:")
    if not by_code:
        print("  (none yet)")
    else:
        for code, n in by_code:
            print("  {}: {}".format(int(code), n))

    print("")
    print("Last fault time by asset:")
    if not last_fault_by_asset:
        print("  (none yet)")
    else:
        for asset, ts in last_fault_by_asset:
            print("  {}: {}".format(asset, ts))


def export_csv(filename="telemetry_export.csv", limit=5000):
    con = connect()
    cur = con.cursor()

    rows = cur.execute("""
        SELECT id, received_utc, topic, site, asset,
               temperature_c, pressure_bar, vibration_rms, power_kw, fault_code
        FROM telemetry
        ORDER BY id DESC
        LIMIT ?
    """, (int(limit),)).fetchall()

    con.close()

    # reverse so CSV is oldest -> newest
    rows = list(reversed(rows))

    header = [
        "id", "received_utc", "topic", "site", "asset",
        "temperature_c", "pressure_bar", "vibration_rms", "power_kw", "fault_code"
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print("CSV exported: {}  (rows: {})".format(filename, len(rows)))


def export_excel_guide(filename="excel_chart_guide.txt"):
    guide = (
        "CHARTS YOU CAN MAKE IN EXCEL (from telemetry_export.csv)\n\n"
        "1) Temperature over time:\n"
        "   - Select columns: received_utc, temperature_c\n"
        "   - Insert -> Line chart\n\n"
        "2) Vibration over time:\n"
        "   - Select: received_utc, vibration_rms\n"
        "   - Insert -> Line chart\n\n"
        "3) Fault count by code:\n"
        "   - Insert PivotTable\n"
        "   - Rows: fault_code\n"
        "   - Values: Count of fault_code\n"
        "   - Insert -> Column chart\n\n"
        "4) Power over time:\n"
        "   - Select: received_utc, power_kw\n"
        "   - Insert -> Line chart\n"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(guide)

    print("Wrote: {}".format(filename))


def main():
    fault_summary()
    print("\n---\n")

    # CSV export (note: close Excel if the CSV is open, otherwise Windows may block writing)
    export_csv("telemetry_export.csv", limit=5000)
    print("\n---\n")

    export_excel_guide("excel_chart_guide.txt")

    # We do NOT generate PNG charts here (matplotlib install issues on Win8)
    # Use charts_html.py for browser-based charts instead.

    print("\nDone. Files created/updated:")
    print(" - telemetry_export.csv")
    print(" - excel_chart_guide.txt")


if __name__ == "__main__":
    main()
