import marimo

__generated_with = "0.20.4"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import duckdb

    return duckdb, mo


@app.cell
def _(duckdb):
    _con = duckdb.connect()

    states_data = _con.execute("""
        WITH state_info(code, name, lon, lat) AS (
            VALUES
                ('AL','Alabama',        -86.9, 32.7), ('AK','Alaska',         -153.4, 64.2),
                ('AZ','Arizona',        -111.9, 34.4), ('AR','Arkansas',       -92.4,  34.9),
                ('CA','California',     -119.4, 37.2), ('CO','Colorado',       -105.5, 39.0),
                ('CT','Connecticut',     -72.7, 41.6), ('DE','Delaware',        -75.5, 39.0),
                ('FL','Florida',         -81.5, 27.8), ('GA','Georgia',         -83.4, 32.7),
                ('HI','Hawaii',         -157.5, 20.2), ('ID','Idaho',          -114.5, 44.4),
                ('IL','Illinois',        -89.2, 40.1), ('IN','Indiana',         -86.3, 39.8),
                ('IA','Iowa',            -93.1, 42.0), ('KS','Kansas',          -98.4, 38.5),
                ('KY','Kentucky',        -84.5, 37.5), ('LA','Louisiana',       -92.4, 31.2),
                ('ME','Maine',           -68.9, 44.7), ('MD','Maryland',        -76.8, 39.1),
                ('MA','Massachusetts',   -71.5, 42.2), ('MI','Michigan',        -85.4, 44.3),
                ('MN','Minnesota',       -94.3, 46.3), ('MS','Mississippi',     -89.7, 32.7),
                ('MO','Missouri',        -92.5, 38.5), ('MT','Montana',        -110.5, 47.0),
                ('NE','Nebraska',        -99.9, 41.5), ('NV','Nevada',         -116.4, 38.8),
                ('NH','New Hampshire',   -71.6, 43.7), ('NJ','New Jersey',      -74.4, 40.1),
                ('NM','New Mexico',     -106.1, 34.4), ('NY','New York',        -75.5, 43.0),
                ('NC','North Carolina',  -79.4, 35.6), ('ND','North Dakota',   -100.5, 47.5),
                ('OH','Ohio',            -82.8, 40.4), ('OK','Oklahoma',        -97.5, 35.5),
                ('OR','Oregon',         -120.5, 44.0), ('PA','Pennsylvania',    -77.2, 40.9),
                ('RI','Rhode Island',    -71.5, 41.7), ('SC','South Carolina',  -80.9, 33.8),
                ('SD','South Dakota',   -100.2, 44.4), ('TN','Tennessee',       -86.3, 35.9),
                ('TX','Texas',           -99.3, 31.4), ('UT','Utah',           -111.1, 39.3),
                ('VT','Vermont',         -72.7, 44.0), ('VA','Virginia',        -78.7, 37.5),
                ('WA','Washington',     -120.5, 47.4), ('WV','West Virginia',   -80.6, 38.9),
                ('WI','Wisconsin',       -89.8, 44.5), ('WY','Wyoming',        -107.6, 43.0)
        ),
        numbered AS (
            SELECT *, row_number() OVER (ORDER BY code) AS rn FROM state_info
        )
        SELECT
            code, name, lon, lat,
            40000 + (rn * 1337 % 40000)               AS median_income,
            round(2.5 + (rn * 7919 % 100) / 20.0, 1) AS unemployment_rate,
            round(30  + (rn * 2741 % 100) / 1.5,  1) AS innovation_index,
            round(1.0 + (rn * 3571 % 100) / 20.0, 2) AS gdp_growth,
            500000 + (rn * 8191 % 9500000)            AS population
        FROM numbered
    """).df()

    ts_data = _con.execute("""
        WITH months AS (
            SELECT
                generate_series                               AS m,
                2024 + (generate_series - 1) / 12            AS yr,
                ((generate_series - 1) % 12) + 1             AS mn
            FROM generate_series(1, 24)
        ),
        sectors(sector, sn, base, trend) AS (
            VALUES
                ('Technology',    1, 120.0, 3.2),
                ('Healthcare',    2,  95.0, 1.8),
                ('Manufacturing', 3,  85.0, 1.1),
                ('Finance',       4, 110.0, 2.5),
                ('Energy',        5,  75.0, 0.8)
        )
        SELECT
            printf('%04d-%02d', yr::INTEGER, mn::INTEGER)        AS month,
            sector,
            round(base + trend * m + (m * sn * 137 % 20) - 10, 1) AS revenue_index
        FROM months CROSS JOIN sectors
        ORDER BY m, sector
    """).df()

    _con.close()
    return states_data, ts_data


@app.cell
def _(states_data):
    _df        = states_data
    avg_income = int(_df["median_income"].mean())
    avg_unemp  = round(float(_df["unemployment_rate"].mean()), 1)
    avg_gdp    = round(float(_df["gdp_growth"].mean()), 2)
    total_pop  = int(_df["population"].sum())
    top_state  = _df.loc[_df["innovation_index"].idxmax(), "name"]
    return avg_gdp, avg_income, avg_unemp, top_state, total_pop


@app.cell
def _(states_data):
    import plotly.express as px

    _scale = [[0.0, "#0d4f8b"], [0.35, "#0d7a9a"], [0.7, "#1aaa82"], [1.0, "#2dd4a0"]]

    map_fig = px.choropleth(
        states_data,
        locations="code",
        locationmode="USA-states",
        color="median_income",
        scope="usa",
        color_continuous_scale=_scale,
        hover_name="name",
        hover_data={
            "code": False,
            "median_income": ":,.0f",
            "unemployment_rate": ":.1f",
            "innovation_index": ":.1f",
            "gdp_growth": ":.2f",
            "population": ":,.0f",
        },
        labels={
            "median_income": "Median Income ($)",
            "unemployment_rate": "Unemployment (%)",
            "innovation_index": "Innovation Index",
            "gdp_growth": "GDP Growth (%)",
            "population": "Population",
        },
    )
    _ = map_fig.update_layout(
        dragmode="pan",
        paper_bgcolor="#080f1e",
        font=dict(color="#94d4c8", family="sans-serif"),
        title=dict(
            text="MEDIAN HOUSEHOLD INCOME BY STATE",
            font=dict(size=13, color="#2dd4a0", family="sans-serif"),
            x=0.5,
            xanchor="center",
        ),
        geo=dict(
            bgcolor="#080f1e",
            lakecolor="#0a1525",
            landcolor="#0d1e2e",
            showlakes=True,
            showcoastlines=False,
            showframe=False,
            showsubunits=True,
            subunitcolor="#1a3040",
        ),
        coloraxis_colorbar=dict(
            title=dict(text="Income", font=dict(color="#94d4c8", size=10)),
            tickfont=dict(color="#94d4c8", family="monospace", size=10),
            bgcolor="#0a1525",
            bordercolor="#1a3040",
            borderwidth=1,
            tickformat="$,.0f",
        ),
        margin=dict(l=0, r=0, t=40, b=10),
        height=600,
    )
    _ = map_fig.update_traces(marker_line_color="#1a3040", marker_line_width=0.5)
    return (map_fig,)


@app.cell
def _(
    avg_gdp,
    avg_income,
    avg_unemp,
    states_data,
    top_state,
    total_pop,
    ts_data,
):
    # ── colour helpers ────────────────────────────────────────────────────────────
    def _lerp(t, c1, c2):
        return tuple(int(a + t * (b - a)) for a, b in zip(c1, c2))

    def _hex(rgb):
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    _BLUE = (13,  79, 139)   # deep blue   #0d4f8b
    _TEAL = (45, 212, 160)   # teal green  #2dd4a0

    # ═══════════════════════════════════════════════════════════════════════════════
    # LINE CHART  –  sector revenue index over 24 months
    # ═══════════════════════════════════════════════════════════════════════════════
    _LW, _LH           = 600, 310
    _LL, _LR, _LT, _LB = 52,  18, 34, 64

    _months  = sorted(ts_data["month"].unique().tolist())
    _sectors = sorted(ts_data["sector"].unique().tolist())
    _SCOLS   = {
        "Technology":    "#2dd4a0",
        "Healthcare":    "#38bdf8",
        "Manufacturing": "#818cf8",
        "Finance":       "#4ade80",
        "Energy":        "#fb923c",
    }
    _lpw = _LW - _LL - _LR
    _lph = _LH - _LT - _LB
    _Y0, _Y1 = 55.0, 210.0

    def _lx(i):
        return round(_LL + i / max(len(_months) - 1, 1) * _lpw, 1)

    def _ly(v):
        return round(_LT + _lph - (v - _Y0) / (_Y1 - _Y0) * _lph, 1)

    _lc_els = [
        f'<rect width="{_LW}" height="{_LH}" fill="#080f1e" rx="10"/>',
        f'<text x="{_LW//2}" y="22" text-anchor="middle" font-size="12" fill="#2dd4a0"'
        f' font-family="sans-serif" font-weight="600" letter-spacing="0.04em">'
        f'SECTOR REVENUE INDEX — 2024–2025</text>',
        f'<line x1="{_LL}" y1="{_LT}" x2="{_LL}" y2="{_LT+_lph}" stroke="#162840" stroke-width="1"/>',
        f'<line x1="{_LL}" y1="{_LT+_lph}" x2="{_LW-_LR}" y2="{_LT+_lph}" stroke="#162840" stroke-width="1"/>',
    ]
    for _gv in range(60, 220, 30):
        _gy = _ly(_gv)
        _lc_els += [
            f'<line x1="{_LL}" y1="{_gy}" x2="{_LW-_LR}" y2="{_gy}" stroke="#0e1e30" stroke-width="1"/>',
            f'<text x="{_LL-5}" y="{_gy}" text-anchor="end" dominant-baseline="middle"'
            f' font-size="9" fill="#4a7a70" font-family="monospace">{_gv}</text>',
        ]
    for _mi, _m in enumerate(_months):
        if _mi % 4 == 0:
            _lc_els.append(
                f'<text x="{_lx(_mi)}" y="{_LT+_lph+13}" text-anchor="middle"'
                f' font-size="8" fill="#4a7a70" font-family="monospace">{_m}</text>'
            )

    for _li, _sec in enumerate(_sectors):
        _sdf  = ts_data[ts_data["sector"] == _sec].sort_values("month")
        _midx = {m: i for i, m in enumerate(_months)}
        _pts  = " ".join(
            f"{_lx(_midx[r['month']])},{_ly(r['revenue_index'])}"
            for _, r in _sdf.iterrows()
        )
        _col  = _SCOLS[_sec]
        _last = _sdf.iloc[-1]
        _ex, _ey = _lx(len(_months) - 1), _ly(_last["revenue_index"])
        _lleg_x = _LL + (_li % 3) * 180
        _lleg_y = _LT + _lph + 36 + (_li // 3) * 14
        _lc_els += [
            f'<polyline points="{_pts}" fill="none" stroke="{_col}" stroke-width="2"'
            f' stroke-linejoin="round" stroke-linecap="round" opacity="0.9"/>',
            f'<circle cx="{_ex}" cy="{_ey}" r="3.5" fill="{_col}"/>',
            f'<rect x="{_lleg_x}" y="{_lleg_y-4}" width="14" height="5" fill="{_col}" rx="2"/>',
            f'<text x="{_lleg_x+18}" y="{_lleg_y}" dominant-baseline="middle"'
            f' font-size="9" fill="#94d4c8" font-family="sans-serif">{_sec}</text>',
        ]

    lc_svg = (
        f'<svg viewBox="0 0 {_LW} {_LH}" xmlns="http://www.w3.org/2000/svg"'
        f' style="width:100%;height:100%">'
        + "".join(_lc_els)
        + "</svg>"
    )

    # ═══════════════════════════════════════════════════════════════════════════════
    # SCATTER  –  innovation index vs GDP growth (colour = unemployment, size = pop)
    # ═══════════════════════════════════════════════════════════════════════════════
    _SW, _SH           = 420, 310
    _SL, _SR, _ST, _SB = 45, 20, 34, 48
    _spw = _SW - _SL - _SR
    _sph = _SH - _ST - _SB

    _ix_lo, _ix_hi   = float(states_data["innovation_index"].min()), float(states_data["innovation_index"].max())
    _gdp_lo, _gdp_hi = float(states_data["gdp_growth"].min()),       float(states_data["gdp_growth"].max())
    _un_lo,  _un_hi  = float(states_data["unemployment_rate"].min()), float(states_data["unemployment_rate"].max())
    _sp_pop_lo = float(states_data["population"].min())
    _sp_pop_hi = float(states_data["population"].max())

    def _sx(v):
        return round(_SL + (v - _ix_lo) / (_ix_hi - _ix_lo) * _spw, 1)

    def _sy(v):
        return round(_ST + _sph - (v - _gdp_lo) / (_gdp_hi - _gdp_lo) * _sph, 1)

    _sc_els = [
        f'<rect width="{_SW}" height="{_SH}" fill="#080f1e" rx="10"/>',
        f'<text x="{_SW//2}" y="22" text-anchor="middle" font-size="12" fill="#2dd4a0"'
        f' font-family="sans-serif" font-weight="600" letter-spacing="0.04em">'
        f'INNOVATION vs GDP GROWTH</text>',
        f'<line x1="{_SL}" y1="{_ST}" x2="{_SL}" y2="{_ST+_sph}" stroke="#162840" stroke-width="1"/>',
        f'<line x1="{_SL}" y1="{_ST+_sph}" x2="{_SW-_SR}" y2="{_ST+_sph}" stroke="#162840" stroke-width="1"/>',
        f'<text x="{_SW//2}" y="{_ST+_sph+30}" text-anchor="middle" font-size="8.5" fill="#4a7a70"'
        f' font-family="sans-serif">Innovation Index</text>',
        f'<text x="10" y="{_ST+_sph//2}" text-anchor="middle" dominant-baseline="middle"'
        f' font-size="8.5" fill="#4a7a70" font-family="sans-serif"'
        f' transform="rotate(-90,10,{_ST+_sph//2})">GDP Growth %</text>',
    ]
    for _gix in [40, 60, 80]:
        _gsx = _sx(float(_gix))
        _sc_els += [
            f'<line x1="{_gsx}" y1="{_ST}" x2="{_gsx}" y2="{_ST+_sph}" stroke="#0e1e30" stroke-width="1"/>',
            f'<text x="{_gsx}" y="{_ST+_sph+12}" text-anchor="middle" font-size="8" fill="#3a5a50"'
            f' font-family="monospace">{_gix}</text>',
        ]
    for _ggdp in [2.0, 3.0, 4.0, 5.0]:
        _gsy = _sy(_ggdp)
        _sc_els += [
            f'<line x1="{_SL}" y1="{_gsy}" x2="{_SW-_SR}" y2="{_gsy}" stroke="#0e1e30" stroke-width="1"/>',
            f'<text x="{_SL-4}" y="{_gsy}" text-anchor="end" dominant-baseline="middle"'
            f' font-size="8" fill="#3a5a50" font-family="monospace">{_ggdp:.1f}</text>',
        ]

    for _, _s in states_data.iterrows():
        _tu   = (_s["unemployment_rate"] - _un_lo) / (_un_hi - _un_lo)
        _tpop = (_s["population"]        - _sp_pop_lo) / (_sp_pop_hi - _sp_pop_lo)
        _scol = _hex(_lerp(_tu, _TEAL, _BLUE))
        _sr   = round(3.5 + _tpop * 9, 1)
        _scx  = _sx(float(_s["innovation_index"]))
        _scy  = _sy(float(_s["gdp_growth"]))
        _sc_els.append(
            f'<circle cx="{_scx}" cy="{_scy}" r="{_sr}" fill="{_scol}" fill-opacity="0.8"'
            f' stroke="#94d4c8" stroke-width="0.3" stroke-opacity="0.4">'
            f'<title>{_s["name"]} | Innovation: {_s["innovation_index"]}'
            f' | GDP: {_s["gdp_growth"]}% | Unemp: {_s["unemployment_rate"]}%</title>'
            f'</circle>'
        )

    # scatter legend
    _sc_els += [
        f'<text x="{_SL+5}" y="{_SH-8}" font-size="7.5" fill="#2a4a40" font-family="sans-serif">'
        f'Colour: unemployment (blue=high) · Size: population</text>',
    ]
    sc_svg = (
        f'<svg viewBox="0 0 {_SW} {_SH}" xmlns="http://www.w3.org/2000/svg"'
        f' style="width:100%;height:100%">'
        + "".join(_sc_els)
        + "</svg>"
    )

    # ═══════════════════════════════════════════════════════════════════════════════
    # KPI CARDS
    # ═══════════════════════════════════════════════════════════════════════════════
    def _card(icon, label, value, sub, accent):
        return (
            f'<div style="background:#080f1e;border:1px solid {accent}30;border-radius:10px;'
            f'padding:16px 18px;flex:1;min-width:130px;box-shadow:0 0 20px {accent}15">'
            f'<div style="font-size:18px;margin-bottom:6px">{icon}</div>'
            f'<div style="font-size:10px;color:#3a6a60;text-transform:uppercase;'
            f'letter-spacing:.07em;margin-bottom:7px">{label}</div>'
            f'<div style="font-size:24px;font-weight:700;color:{accent};'
            f'font-family:monospace;line-height:1">{value}</div>'
            f'<div style="font-size:10px;color:#2a4a40;margin-top:5px">{sub}</div>'
            f'</div>'
        )

    kpi_html = (
        '<div style="display:flex;gap:10px;font-family:sans-serif">'
        + _card("💵", "Avg Median Income",  f"${avg_income:,}",     "across all 50 states",     "#2dd4a0")
        + _card("📉", "Avg Unemployment",   f"{avg_unemp}%",        "national simulated avg",   "#38bdf8")
        + _card("👥", "Total Population",   f"{total_pop/1_000_000:.0f}M", "simulated aggregate", "#818cf8")
        + _card("🏆", "Top Innovator",      top_state,              "highest innovation score", "#4ade80")
        + _card("📈", "Avg GDP Growth",     f"{avg_gdp}%",          "annual growth rate",       "#fb923c")
        + "</div>"
    )

    # ═══════════════════════════════════════════════════════════════════════════════
    # HEADER
    # ═══════════════════════════════════════════════════════════════════════════════
    header_html = (
        '<div style="background:linear-gradient(135deg,#05080f 0%,#0c1e36 55%,#05140e 100%);'
        'border-bottom:1px solid #1a3828;padding:18px 24px 12px;font-family:sans-serif;'
        'border-radius:10px;overflow:hidden">'
        '<div style="display:flex;align-items:baseline;gap:12px">'
        '<div style="font-size:18px;font-weight:700;color:#2dd4a0;letter-spacing:.06em">'
        'US ECONOMIC INTELLIGENCE DASHBOARD</div>'
        '<div style="font-size:10px;color:#2a5a48;letter-spacing:.08em">'
        'SIMULATED DATA &nbsp;·&nbsp; 50 STATES &nbsp;·&nbsp; 2024–2025</div>'
        '</div>'
        '</div>'
    )
    return header_html, kpi_html, lc_svg, sc_svg


@app.cell
def _(
    avg_gdp,
    avg_income,
    avg_unemp,
    lc_svg,
    map_fig,
    mo,
    sc_svg,
    top_state,
    total_pop,
):
    import pathlib
    import plotly.io as _pio
    import typst as _typst

    def _export(_):
        try:
            _dir = pathlib.Path("figures")
            _dir.mkdir(exist_ok=True)
            _pio.write_image(map_fig, str(_dir / "map.png"), width=1200, height=600, scale=2)
            (_dir / "line_chart.svg").write_text(lc_svg, encoding="utf-8")
            (_dir / "scatter.svg").write_text(sc_svg, encoding="utf-8")
            (_dir / "kpis.typ").write_text(
                '#let kpi-data = (\n'
                f'  ("Avg Median Income", "${avg_income:,}",     rgb("#2dd4a0")),\n'
                f'  ("Avg Unemployment",  "{avg_unemp}%",        rgb("#38bdf8")),\n'
                f'  ("Total Population",  "{total_pop/1_000_000:.0f}M", rgb("#818cf8")),\n'
                f'  ("Top Innovator",     "{top_state}",         rgb("#4ade80")),\n'
                f'  ("Avg GDP Growth",    "{avg_gdp}%",          rgb("#fb923c")),\n'
                ')\n',
                encoding="utf-8",
            )
            _typst.compile("report.typ", output="report.pdf")
            return "Report exported to report.pdf"
        except Exception as _e:
            return f"Error: {_e}"

    export_btn = mo.ui.button(
        label="Export PDF Report",
        on_click=_export,
    )
    return (export_btn,)


@app.cell
def _(export_btn, header_html, kpi_html, lc_svg, map_fig, mo, sc_svg):
    _map_h  = 600
    _gap    = 12
    _lc_h   = (_map_h - _gap) // 2   # 294 — lc + sc + gap = 600, matches map
    _sc_h   = _map_h - _lc_h - _gap  # 294
    _bg     = "padding:4px;background:#080f1e;border-radius:10px;overflow:hidden"

    _header = mo.Html(header_html)
    _kpis   = mo.Html(kpi_html)
    _map    = mo.ui.plotly(map_fig)
    _lc     = f'<div style="{_bg};height:{_lc_h}px">{lc_svg}</div>'
    _sc     = f'<div style="{_bg};height:{_sc_h}px">{sc_svg}</div>'
    _bottom = mo.Html(
        '<div style="display:flex;gap:12px;align-items:flex-start">'
        f'<div style="flex:3;min-width:0;border-radius:10px;overflow:hidden">{_map}</div>'
        f'<div style="flex:2;min-width:0;display:flex;flex-direction:column;gap:{_gap}px">'
        f'{_lc}{_sc}'
        '</div>'
        '</div>'
    )

    _export_row = mo.Html(
        '<div style="display:flex;align-items:center;gap:12px;font-family:sans-serif">'
        f'{export_btn}'
        + (
            f'<span style="font-size:10px;color:#2dd4a0;letter-spacing:.05em">'
            f'{export_btn.value}</span>'
            if export_btn.value else ""
        )
        + '</div>'
    )

    mo.vstack([
        _header,
        _kpis,
        _bottom,
        _export_row,
    ], gap="0.6rem")
    return


if __name__ == "__main__":
    app.run()
