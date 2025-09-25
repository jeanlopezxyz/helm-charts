import yaml
import os
import glob

charts = []

# Scan all Chart.yaml files
for chart_file in glob.glob('../charts/*/Chart.yaml'):
    try:
        with open(chart_file, 'r') as f:
            chart_data = yaml.safe_load(f)
            chart_name = chart_data.get('name', 'unknown')
            chart_version = chart_data.get('version', '1.0.0')
            chart_description = chart_data.get('description', 'Helm chart')
            
            # Extract keywords for tags
            keywords = chart_data.get('keywords', [])
            tags = keywords[:3] if keywords else ['helm', 'chart']
            
            charts.append({
                'name': chart_name,
                'version': chart_version,
                'description': chart_description,
                'tags': tags
            })
    except Exception as e:
        print(f"Error reading {chart_file}: {e}")

# Sort charts by name
charts.sort(key=lambda x: x['name'])

# Generate HTML
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Helm Charts Repository</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            line-height: 1.6; color: #e2e8f0;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            min-height: 100vh;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 0 12px; }
        header {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.98) 0%, rgba(30, 41, 59, 0.95) 100%);
            backdrop-filter: blur(20px); border-bottom: 1px solid rgba(59, 130, 246, 0.2);
            padding: 2rem 0; position: relative; overflow: hidden;
        }
        .header-content { position: relative; z-index: 1; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 2rem; }
        .header-left { flex: 1; min-width: 300px; }
        .header-icons { display: flex; gap: 1.5rem; align-items: center; }
        .enterprise-icon {
            width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
            font-size: 1.5rem; color: #f8fafc; background: rgba(59, 130, 246, 0.2);
            border: 1px solid rgba(59, 130, 246, 0.3); backdrop-filter: blur(10px);
        }
        h1 { font-size: 2.2rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 1rem; }
        .subtitle { color: #94a3b8; font-size: 1rem; margin-bottom: 1.5rem; font-weight: 500; }
        .repo-add {
            background: rgba(15, 23, 42, 0.9); border: 1px solid #475569; border-radius: 10px;
            padding: 1rem 1.5rem; font-family: "SF Mono", "Monaco", "Cascadia Code", monospace;
            font-size: 0.9rem; color: #10b981; display: inline-flex; align-items: center; gap: 0.75rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }
        main { padding: 2rem 0; }
        .search-section { margin-bottom: 2rem; }
        .search-box {
            width: 100%; max-width: 400px; padding: 1rem 1.5rem; border: 1px solid #475569;
            border-radius: 12px; font-size: 1rem; background: rgba(30, 41, 59, 0.8);
            color: #f8fafc; backdrop-filter: blur(20px);
        }
        .search-box:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3); }
        .search-box::placeholder { color: #94a3b8; }
        .charts-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin-top: 2rem; max-width: 1200px; margin-left: auto; margin-right: auto; }
        @media (max-width: 1024px) { .charts-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 640px) { .charts-grid { grid-template-columns: 1fr; gap: 1.5rem; } }
        .chart-card {
            background: rgba(30, 41, 59, 0.9); border: 1px solid #475569; border-radius: 16px;
            padding: 1.5rem; transition: all 0.3s ease; backdrop-filter: blur(20px);
            position: relative; overflow: hidden; height: 320px; display: flex; flex-direction: column;
        }
        .chart-card::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
            background: linear-gradient(90deg, #3b82f6, #06b6d4);
        }
        .chart-card:hover { transform: translateY(-8px); border-color: #3b82f6; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5); }
        .chart-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 0.75rem; position: relative; }
        .chart-main-info { display: flex; align-items: center; flex: 1; }
        .chart-actions-top { display: flex; gap: 0.4rem; flex-shrink: 0; }
        .icon-btn {
            width: 30px; height: 30px; border-radius: 6px; display: flex; align-items: center; justify-content: center;
            text-decoration: none; transition: all 0.2s ease; backdrop-filter: blur(10px); font-size: 0.8rem;
        }
        .icon-btn-secondary { background: rgba(51, 65, 85, 0.8); border: 1px solid #64748b; color: #e2e8f0; }
        .icon-btn-secondary:hover { background: rgba(71, 85, 105, 0.9); border-color: #3b82f6; transform: scale(1.05); }
        .icon-btn-success { background: rgba(16, 185, 129, 0.8); border: 1px solid #10b981; color: white; }
        .icon-btn-success:hover { background: rgba(5, 150, 105, 0.9); transform: scale(1.05); }
        .chart-icon {
            width: 44px; height: 54px; margin-right: 1rem; border-radius: 10px; display: flex;
            align-items: center; justify-content: center; font-size: 1.2rem; color: #3b82f6;
            background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2);
            align-self: flex-start;
        }
        .chart-info h3 { font-size: 1.1rem; font-weight: 600; margin-bottom: 0.1rem; color: #f8fafc; line-height: 1.3; }
        .chart-version { color: #94a3b8; font-size: 0.75rem; font-weight: 500; }
        .chart-description { color: #cbd5e1; font-size: 0.9rem; margin-bottom: 1rem; line-height: 1.5; flex: 1; }
        .chart-tags { margin-bottom: 1rem; }
        .tag {
            display: inline-block; background: rgba(59, 130, 246, 0.15); color: #93c5fd;
            padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.7rem; font-weight: 500;
            margin-right: 0.4rem; margin-bottom: 0.3rem; border: 1px solid rgba(59, 130, 246, 0.25);
        }
        .artifact-hub-link {
            margin-bottom: 1rem; text-align: center;
        }
        .artifact-hub-link a {
            color: #8b5cf6; text-decoration: none; font-size: 0.8rem; font-weight: 500;
            display: inline-flex; align-items: center; gap: 0.5rem;
            padding: 0.5rem 1rem; background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.2);
            border-radius: 8px; transition: all 0.2s ease;
        }
        .artifact-hub-link a:hover {
            background: rgba(139, 92, 246, 0.2); border-color: #8b5cf6; transform: translateY(-1px);
        }
        .install-command {
            background: rgba(15, 23, 42, 0.9); border: 1px solid #475569; border-radius: 10px;
            padding: 1rem 1.25rem; font-family: "SF Mono", "Monaco", "Cascadia Code", monospace;
            font-size: 0.85rem; color: #10b981; font-weight: 400; letter-spacing: 0.025em;
            margin-top: auto; text-align: center;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <div class="header-left">
                    <h1><i class="fas fa-dharmachakra" style="color: #3b82f6;"></i>Helm Charts Repository</h1>
                    <p class="subtitle">Enterprise Helm charts for Red Hat environments</p>
                    <div class="repo-add">
                        <i class="fas fa-terminal" style="color: #64748b; margin-right: 0.5rem;"></i>
                        helm repo add jeanlopezxyz https://jeanlopezxyz.github.io/helm-charts
                    </div>
                </div>
                <div class="header-icons">
                    <div class="enterprise-icon" title="Kubernetes Native"><i class="fas fa-dharmachakra"></i></div>
                    <div class="enterprise-icon" title="Red Hat Certified"><i class="fab fa-redhat"></i></div>
                    <div class="enterprise-icon" title="Enterprise Ready"><i class="fas fa-shield-alt"></i></div>
                </div>
            </div>
        </div>
    </header>
    <main>
        <div class="container">
            <div class="search-section">
                <input type="text" class="search-box" placeholder="Search charts..." id="search">
            </div>
            <div class="charts-grid" id="charts-container">'''

# Filter to show only main operator charts (enterprise focus)
featured_charts = [chart for chart in charts if chart['name'].startswith('setup-rh-operator-')][:3]

# Generate cards for featured charts only
for chart in featured_charts:
    install_name = chart['name'].replace('setup-rh-operator-', '').replace('setup-', '').replace('helper-', '')
    tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in chart['tags']])
    
    html_content += f'''
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-main-info">
                            <div class="chart-icon">
                                <i class="fas fa-dharmachakra"></i>
                            </div>
                            <div class="chart-info">
                                <h3>{chart['name']}</h3>
                                <div class="chart-version">v{chart['version']}</div>
                            </div>
                        </div>
                        <div class="chart-actions-top">
                            <a href="https://github.com/jeanlopezxyz/helm-charts/tree/main/charts/{chart['name']}" target="_blank" class="icon-btn icon-btn-secondary" title="View Source">
                                <i class="fab fa-github"></i>
                            </a>
                            <a href="https://jeanlopezxyz.github.io/helm-charts/{chart['name']}-{chart['version']}.tgz" class="icon-btn icon-btn-success" title="Download Chart">
                                <i class="fas fa-download"></i>
                            </a>
                        </div>
                    </div>
                    <div class="chart-description">{chart['description']}</div>
                    <div class="chart-tags">{tags_html}</div>
                    <div class="artifact-hub-link">
                        <a href="https://artifacthub.io/packages/helm/jeanlopezxyz/{chart['name']}" target="_blank">
                            <i class="fas fa-external-link-alt"></i> View on Artifact Hub
                        </a>
                    </div>
                    <div class="install-command">helm install {install_name} jeanlopezxyz/{chart['name']}</div>
                </div>'''

html_content += '''
            </div>
        </div>
    </main>
    <footer>
        <div class="container">
            <p>&copy; 2025 jeanlopezxyz. Licensed under Apache License.</p>
        </div>
    </footer>
    <script>
        document.getElementById('search').addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const cards = document.querySelectorAll('.chart-card');
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                card.style.display = text.includes(searchTerm) ? 'block' : 'none';
            });
        });
    </script>
</body>
</html>'''

with open('index.html', 'w') as f:
    f.write(html_content)

print(f"Generated website with {len(charts)} charts")
