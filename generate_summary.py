import json
import glob
import os
from datetime import datetime

def generate_html_summary():
    json_files = glob.glob('summary_counts_*.json')
    json_files.sort(reverse=True) # Process latest first for version listing if needed, but for agg it doesn't matter much

    total_runs = 0
    total_alive = 0
    total_dead = 0
    unique_players = set()
    
    difficulty_stats = {
        "Normal": {"Alive": 0, "Dead": 0, "Total": 0},
        "Hard": {"Alive": 0, "Dead": 0, "Total": 0},
        "Hell": {"Alive": 0, "Dead": 0, "Total": 0},
        "Duriano": {"Alive": 0, "Dead": 0, "Total": 0}
    }
    
    platform_stats = {}
    
    version_stats = []

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                data = content.get('data', [])
                version_label = file_path.replace('summary_counts_', '').replace('.json', '')
                
                v_runs = 0
                v_alive = 0
                v_dead = 0
                v_players = set()
                
                for entry in data:
                    # Player Aggregation
                    p_name = entry.get('playerName')
                    if p_name:
                        unique_players.add(p_name)
                        v_players.add(p_name)
                    
                    # Global Run Counts
                    count = entry.get('count', 0)
                    alive = entry.get('Alive', 0)
                    dead = entry.get('Dead', 0)
                    
                    total_runs += count
                    total_alive += alive
                    total_dead += dead
                    
                    v_runs += count
                    v_alive += alive
                    v_dead += dead
                    
                    # Difficulty Aggregation
                    by_difficulty = entry.get('byDifficulty', {})
                    for diff, stats in by_difficulty.items():
                        if diff in difficulty_stats:
                            difficulty_stats[diff]["Alive"] += stats.get("Alive", 0)
                            difficulty_stats[diff]["Dead"] += stats.get("Dead", 0)
                            difficulty_stats[diff]["Total"] += stats.get("Total", 0)
                            
                    # Platform Aggregation
                    platforms = entry.get('Platform', {})
                    for plat, p_count in platforms.items():
                        platform_stats[plat] = platform_stats.get(plat, 0) + p_count

                version_stats.append({
                    "version": version_label,
                    "runs": v_runs,
                    "alive": v_alive,
                    "dead": v_dead,
                    "players": len(v_players)
                })

        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    # Calculations
    win_rate = (total_alive / total_runs * 100) if total_runs > 0 else 0
    formatted_date = datetime.now().strftime("%A, %B %d, %Y")
    
    # HTML Generation
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>All Versions UAT Summary - {formatted_date}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 20px auto; padding: 20px; background-color: #f4f7f6; }}
        .card {{ background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #2980b9; font-size: 1.2em; margin-top: 0; }}
        .date-badge {{ background: #3498db; color: white; padding: 5px 12px; border-radius: 20px; font-size: 0.9em; float: right; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-top: 15px; }}
        .metric {{ text-align: center; padding: 15px; background: #ebf5fb; border-radius: 6px; }}
        .metric-value {{ font-size: 1.5em; font-weight: bold; color: #2c3e50; display: block; }}
        .metric-label {{ font-size: 0.85em; color: #7f8c8d; text-transform: uppercase; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ text-align: left; padding: 10px; border-bottom: 1px solid #eee; }}
        th {{ color: #7f8c8d; font-size: 0.9em; background-color: #f9f9f9; }}
        .bar-container {{ background-color: #ecf0f1; border-radius: 4px; height: 10px; width: 100px; display: inline-block; vertical-align: middle; margin-right: 5px; }}
        .bar-fill {{ background-color: #2ecc71; height: 100%; border-radius: 4px; }}
        .footer {{ text-align: center; font-size: 0.8em; color: #95a5a6; margin-top: 30px; }}
    </style>
</head>
<body>

    <div class="card">
        <span class="date-badge">{formatted_date}</span>
        <h1>Global UAT Summary Report</h1>
        <p>Aggregated data from <strong>{len(json_files)} versions</strong> ({json_files[-1].replace('summary_counts_', '').replace('.json', '')} to {json_files[0].replace('summary_counts_', '').replace('.json', '')})</p>

        <div class="grid">
            <div class="metric">
                <span class="metric-value">{len(unique_players)}</span>
                <span class="metric-label">Total Unique Players</span>
            </div>
            <div class="metric">
                <span class="metric-value">{total_runs}</span>
                <span class="metric-label">Total Runs</span>
            </div>
            <div class="metric">
                <span class="metric-value">{total_alive}</span>
                <span class="metric-label">Total Survivors</span>
            </div>
            <div class="metric" style="background: {'#d4efdf' if win_rate > 20 else '#fdf2e9'};">
                <span class="metric-value" style="color: {'#27ae60' if win_rate > 20 else '#e67e22'};">{win_rate:.1f}%</span>
                <span class="metric-label">Global Win Rate</span>
            </div>
        </div>
    </div>

    <div class="card">
        <h2>Difficulty Breakdown</h2>
        <table>
            <tr>
                <th>Difficulty</th>
                <th>Total Runs</th>
                <th>Survivors</th>
                <th>Win Rate</th>
            </tr>"""
    
    for diff, stats in difficulty_stats.items():
        wr = (stats['Alive'] / stats['Total'] * 100) if stats['Total'] > 0 else 0
        html_content += f"""
            <tr>
                <td><strong>{diff}</strong></td>
                <td>{stats['Total']}</td>
                <td>{stats['Alive']}</td>
                <td>
                    <div class="bar-container"><div class="bar-fill" style="width: {wr}%;"></div></div>
                    {wr:.1f}%
                </td>
            </tr>"""

    html_content += """
        </table>
    </div>

    <div class="card">
        <h2>Platform Distribution</h2>
        <div class="grid">"""
        
    for plat, count in platform_stats.items():
        html_content += f"""
            <div class="metric" style="background: #fff; border: 1px solid #eee;">
                <span class="metric-value" style="font-size: 1.2em;">{count}</span>
                <span class="metric-label">{plat}</span>
            </div>"""

    html_content += """
        </div>
    </div>

    <div class="card">
        <h2>History by Version</h2>
        <table>
            <tr>
                <th>Version</th>
                <th>Players</th>
                <th>Runs</th>
                <th>Win Rate</th>
            </tr>"""
            
    for v in version_stats:
        v_wr = (v['alive'] / v['runs'] * 100) if v['runs'] > 0 else 0
        html_content += f"""
            <tr>
                <td>{v['version']}</td>
                <td>{v['players']}</td>
                <td>{v['runs']}</td>
                <td>{v_wr:.1f}%</td>
            </tr>"""

    html_content += """
        </table>
    </div>

    <div class="footer">
        Generated by Durian Player Summary System
    </div>

</body>
</html>"""

    with open('all_versions_summary.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Successfully generated all_versions_summary.html")

if __name__ == "__main__":
    generate_html_summary()