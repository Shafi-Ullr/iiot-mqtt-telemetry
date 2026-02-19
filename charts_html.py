import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DB = "telemetry.db"


def load_df(limit=3000, downsample_step=None):
    con = sqlite3.connect(DB)
    df = pd.read_sql_query("""
        SELECT received_utc, site, asset,
               temperature_c, pressure_bar, vibration_rms, power_kw, fault_code
        FROM telemetry
        ORDER BY id DESC
        LIMIT ?
    """, con, params=(int(limit),))
    con.close()

    df["received_utc"] = pd.to_datetime(df["received_utc"], errors="coerce")
    df = df.sort_values("received_utc")

    if downsample_step is not None and downsample_step > 1:
        df = df.iloc[::downsample_step, :]

    return df


def add_rolling_average(fig, df, y_col, window=60):
    assets = sorted(df["asset"].dropna().unique())
    for asset in assets:
        dfa = df[df["asset"] == asset].copy()
        dfa["roll"] = dfa[y_col].rolling(window=window, min_periods=1).mean()

        fig.add_trace(go.Scatter(
            x=dfa["received_utc"],
            y=dfa["roll"],
            mode="lines",
            name="{} (avg)".format(asset),
            line=dict(width=3)
        ))
    return fig


def hide_raw_traces(fig):
    fig.update_traces(visible=False, showlegend=False)
    return fig


def chart_temperature(df):
    fig = px.line(
        df,
        x="received_utc",
        y="temperature_c",
        color="asset",
        title="Temperature (°C) over time",
        labels={"received_utc": "Time (UTC)", "temperature_c": "Temperature (°C)"}
    )
    fig = hide_raw_traces(fig)
    fig = add_rolling_average(fig, df, "temperature_c", window=60)
    fig.write_html("chart_temperature.html")
    print("Created: chart_temperature.html")


def chart_vibration(df):
    fig = px.line(
        df,
        x="received_utc",
        y="vibration_rms",
        color="asset",
        title="Vibration RMS over time",
        labels={"received_utc": "Time (UTC)", "vibration_rms": "Vibration RMS"}
    )
    fig = hide_raw_traces(fig)
    fig = add_rolling_average(fig, df, "vibration_rms", window=60)
    fig.write_html("chart_vibration.html")
    print("Created: chart_vibration.html")


def chart_power(df):
    fig = px.line(
        df,
        x="received_utc",
        y="power_kw",
        color="asset",
        title="Power (kW) over time",
        labels={"received_utc": "Time (UTC)", "power_kw": "Power (kW)"}
    )
    fig = hide_raw_traces(fig)
    fig = add_rolling_average(fig, df, "power_kw", window=60)
    fig.write_html("chart_power.html")
    print("Created: chart_power.html")


def chart_fault_counts(df_full):
    # IMPORTANT: use FULL (not downsampled) data for accurate counting
    faults = df_full[df_full["fault_code"] != 0].copy()

    if len(faults) == 0:
        px.bar(title="Fault counts by code (no faults yet)").write_html("chart_fault_counts.html")
        print("Created: chart_fault_counts.html")
        return

    counts = faults.groupby(["asset", "fault_code"]).size().reset_index(name="count")
    counts["fault_code"] = counts["fault_code"].astype(int).astype(str)

    fig = px.bar(
        counts,
        x="fault_code",
        y="count",
        color="asset",
        barmode="group",
        title="Fault counts by code (per asset) — accurate",
        labels={"fault_code": "Fault code", "count": "Count"}
    )
    fig.write_html("chart_fault_counts.html")
    print("Created: chart_fault_counts.html")


def main():
    # Clean charts: downsample for readability
    df_clean = load_df(limit=3000, downsample_step=10)

    if df_clean.empty:
        print("No data found in telemetry.db yet.")
        print("Make sure collector_sqlite.py and publisher.py are running first.")
        return

    # Accurate faults: load more rows and DO NOT downsample
    df_full = load_df(limit=20000, downsample_step=None)

    chart_temperature(df_clean)
    chart_vibration(df_clean)
    chart_power(df_clean)
    chart_fault_counts(df_full)

    print("\nOpen the .html files by double-clicking them:")
    print(" - chart_temperature.html")
    print(" - chart_vibration.html")
    print(" - chart_power.html")
    print(" - chart_fault_counts.html")


if __name__ == "__main__":
    main()
