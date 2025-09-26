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
        .repo-command-container {
            position: relative; margin-top: 1rem;
        }
        .repo-header {
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;
        }
        .repo-label {
            color: #94a3b8; font-size: 0.8rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;
        }
        .repo-copy-btn {
            background: rgba(59, 130, 246, 0.2); border: 1px solid #3b82f6;
            color: #3b82f6; padding: 0.4rem; border-radius: 6px; cursor: pointer; font-size: 0.75rem;
            transition: all 0.2s ease; display: flex; align-items: center; justify-content: center;
            width: 32px; height: 32px;
        }
        .repo-copy-btn:hover {
            background: rgba(59, 130, 246, 0.3); transform: scale(1.05);
        }
        .repo-add {
            background: rgba(15, 23, 42, 0.9); border: 1px solid #475569; border-radius: 10px;
            padding: 1rem 1.5rem; font-family: "SF Mono", "Monaco", "Cascadia Code", monospace;
            font-size: 0.9rem; color: #10b981; font-weight: 400; letter-spacing: 0.025em;
            display: block; text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }
        main { padding: 2rem 0; }
        .search-section { margin-bottom: 2rem; display: flex; justify-content: flex-start; }
        .search-box {
            width: 350px; padding: 0.75rem 1.25rem; border: 1px solid #475569;
            border-radius: 10px; font-size: 0.95rem; background: rgba(30, 41, 59, 0.8);
            color: #f8fafc; backdrop-filter: blur(20px);
        }
        .search-box:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3); }
        .search-box::placeholder { color: #94a3b8; }
        .charts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1.5rem; margin-top: 2rem; max-width: 1400px; margin-left: auto; margin-right: auto; }
        @media (max-width: 768px) { 
            .charts-grid { grid-template-columns: 1fr; gap: 1rem; } 
            .search-box { width: 100%; }
            .search-section { justify-content: center; }
        }
        .chart-card {
            background: rgba(30, 41, 59, 0.9); border: 1px solid #475569; border-radius: 16px;
            padding: 1.25rem; transition: all 0.3s ease; backdrop-filter: blur(20px);
            position: relative; overflow: hidden; height: 260px; display: flex; flex-direction: column;
        }
        .chart-card::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
            background: linear-gradient(90deg, #3b82f6, #06b6d4);
        }
        .chart-card:hover { transform: translateY(-8px); border-color: #3b82f6; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5); }
        .chart-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 0.75rem; position: relative; }
        .chart-main-info { display: flex; align-items: center; flex: 1; }
        .chart-actions-top { display: flex; gap: 0.3rem; flex-shrink: 0; }
        .icon-btn {
            width: 30px; height: 30px; border-radius: 6px; display: flex; align-items: center; justify-content: center;
            text-decoration: none; transition: all 0.2s ease; backdrop-filter: blur(10px); font-size: 0.8rem;
        }
        .icon-btn-secondary { background: rgba(51, 65, 85, 0.8); border: 1px solid #64748b; color: #e2e8f0; }
        .icon-btn-secondary:hover { background: rgba(71, 85, 105, 0.9); border-color: #3b82f6; transform: scale(1.05); }
        .icon-btn-success { background: rgba(16, 185, 129, 0.8); border: 1px solid #10b981; color: white; }
        .icon-btn-success:hover { background: rgba(5, 150, 105, 0.9); transform: scale(1.05); }
        .icon-btn-purple { background: rgba(139, 92, 246, 0.8); border: 1px solid #8b5cf6; color: white; }
        .icon-btn-purple:hover { background: rgba(124, 58, 237, 0.9); transform: scale(1.05); }
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
        .command-container {
            margin-top: auto; position: relative;
        }
        .command-header {
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;
        }
        .command-label {
            color: #94a3b8; font-size: 0.75rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;
        }
        .copy-btn {
            background: rgba(59, 130, 246, 0.2); border: 1px solid #3b82f6;
            color: #3b82f6; padding: 0.4rem; border-radius: 6px; cursor: pointer; font-size: 0.7rem;
            transition: all 0.2s ease; display: flex; align-items: center; justify-content: center;
            width: 28px; height: 28px;
        }
        .copy-btn:hover {
            background: rgba(59, 130, 246, 0.3); transform: scale(1.05);
        }
        .install-command {
            background: rgba(15, 23, 42, 0.9); border: 1px solid #475569; border-radius: 10px;
            padding: 1rem 1.25rem; font-family: "SF Mono", "Monaco", "Cascadia Code", monospace;
            font-size: 0.85rem; color: #10b981; font-weight: 400; letter-spacing: 0.025em;
            text-align: center; word-break: break-all;
        }
        .footer-content {
            display: flex; justify-content: space-between; align-items: center; padding: 2.5rem 0;
            border-top: 1px solid rgba(59, 130, 246, 0.2); flex-wrap: wrap; gap: 2rem;
        }
        .footer-left, .footer-right {
            display: flex; align-items: center;
        }
        .footer-right {
            flex-direction: column; align-items: flex-end;
        }
        .footer-right p {
            color: #94a3b8; font-size: 0.9rem; margin: 0; line-height: 1.4;
        }
        .footer-links {
            display: flex; gap: 1rem; margin-top: 1rem;
        }
        .footer-links a {
            color: #3b82f6; text-decoration: none; font-size: 0.9rem; font-weight: 500;
            display: inline-flex; align-items: center; gap: 0.5rem;
            padding: 0.5rem 1rem; background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 8px; transition: all 0.2s ease;
        }
        .footer-links a:hover {
            background: rgba(59, 130, 246, 0.2); transform: translateY(-1px);
        }
        .footer-command {
            margin-top: 1rem;
        }
        .footer-command code {
            background: rgba(15, 23, 42, 0.9); color: #10b981; padding: 0.75rem 1rem;
            border-radius: 8px; font-size: 0.8rem; border: 1px solid #475569;
            display: block; font-family: "SF Mono", "Monaco", "Cascadia Code", monospace;
        }
        @media (max-width: 768px) {
            .footer-content { flex-direction: column; text-align: center; }
            .footer-left, .footer-right { align-items: center; }
            .footer-right { align-items: center; }
            .footer-links { justify-content: center; margin-top: 0; }
            .repo-header { justify-content: center; }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <div class="header-left">
                    <h1><i class="fas fa-dharmachakra" style="color: #3b82f6;"></i>Helm Charts Repository</h1>
                    <p class="subtitle">Production-ready Helm charts for Red Hat OpenShift operators and enterprise applications. Automated installation with helper charts and comprehensive monitoring.</p>
                    <div class="repo-command-container">
                        <div class="repo-header">
                            <span class="repo-label">Add Repository</span>
                            <button class="repo-copy-btn" onclick="copyRepoCommand()" title="Copy command">
                                <i class="fas fa-copy"></i>
                            </button>
                        </div>
                        <div class="repo-add">helm repo add jeanlopezxyz https://jeanlopezxyz.github.io/helm-charts</div>
                    </div>
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

# Generate cards for all charts
for chart in charts:
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
                            <a href="https://artifacthub.io/packages/helm/jeanlopezxyz/{chart['name']}" target="_blank" class="icon-btn icon-btn-purple" title="Artifact Hub">
                                <i class="fas fa-cube"></i>
                            </a>
                        </div>
                    </div>
                    <div class="chart-description">{chart['description']}</div>
                    <div class="chart-tags">{tags_html}</div>
                    <div class="command-container">
                        <div class="command-header">
                            <span class="command-label">Install Command</span>
                            <button class="copy-btn" onclick="copyToClipboard('helm install {install_name} jeanlopezxyz/{chart['name']}')" title="Copy command">
                                <i class="fas fa-copy"></i>
                            </button>
                        </div>
                        <div class="install-command">helm install {install_name} jeanlopezxyz/{chart['name']}</div>
                    </div>
                </div>'''

html_content += '''
            </div>
        </div>
    </main>
    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-left">
                    <div class="footer-links">
                        <a href="https://github.com/jeanlopezxyz/helm-charts" target="_blank">
                            <i class="fab fa-github"></i> GitHub
                        </a>
                        <a href="https://artifacthub.io/packages/search?repo=jeanlopezxyz" target="_blank">
                            <i class="fas fa-cube"></i> Artifact Hub
                        </a>
                    </div>
                </div>
                <div class="footer-right">
                    <p>&copy; 2025 jeanlopezxyz</p>
                    <p>Apache License 2.0</p>
                </div>
            </div>
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
        
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                const btn = event.target.closest('.copy-btn');
                const original = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-check"></i>';
                btn.style.background = 'rgba(16, 185, 129, 0.3)';
                btn.style.borderColor = '#10b981';
                btn.style.color = '#10b981';
                setTimeout(() => {
                    btn.innerHTML = original;
                    btn.style.background = '';
                    btn.style.borderColor = '';
                    btn.style.color = '';
                }, 2000);
            });
        }
        
        function copyRepoCommand() {
            const text = 'helm repo add jeanlopezxyz https://jeanlopezxyz.github.io/helm-charts';
            navigator.clipboard.writeText(text).then(() => {
                const btn = event.target.closest('.repo-copy-btn');
                const original = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-check"></i>';
                btn.style.background = 'rgba(16, 185, 129, 0.3)';
                btn.style.borderColor = '#10b981';
                btn.style.color = '#10b981';
                setTimeout(() => {
                    btn.innerHTML = original;
                    btn.style.background = '';
                    btn.style.borderColor = '';
                    btn.style.color = '';
                }, 2000);
            });
        }
    </script>
</body>
</html>'''

with open('index.html', 'w') as f:
    f.write(html_content)

print(f"Generated website with {len(charts)} charts")
