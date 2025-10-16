from flask import Flask, render_template_string, request, jsonify, Response
import os
import base64
import hashlib

app = Flask(__name__)

app.config['SECRET_KEY'] = 'gt_titans_2024_champions'
app.config['FLASK_ENV'] = 'production'

HIDDEN_ENDPOINT = base64.b64decode('L3N5c3RlbS9oZWFsdGgvZGlhZ25vc3RpY3M=').decode()

FLAG_PART_1 = 'Fl4g-X{'
FLAG_PART_2 = base64.b64encode('hardik_'.encode()).decode()
FLAG_PART_3 = 'pandya_'
FLAG_PART_4 = hashlib.md5('shubman'.encode()).hexdigest()[:8]
FLAG_PART_5 = '_captain}'

PLAYERS = {
    'shubman_gill': {'role': 'Batsman', 'runs': 890, 'average': 59.33},
    'hardik_pandya': {'role': 'All-rounder', 'runs': 487, 'wickets': 8},
    'rashid_khan': {'role': 'Bowler', 'wickets': 19, 'economy': 8.23},
    'david_miller': {'role': 'Batsman', 'runs': 449, 'strike_rate': 142.35},
    'mohammed_shami': {'role': 'Bowler', 'wickets': 28, 'economy': 8.03}
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gujarat Titans Analytics System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        header {
            text-align: center;
            padding: 40px 0;
            border-bottom: 3px solid #ffd700;
        }
        h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }
        .player-card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 2px solid rgba(255,215,0,0.3);
            transition: transform 0.3s ease;
        }
        .player-card:hover {
            transform: translateY(-5px);
            border-color: #ffd700;
        }
        .player-name {
            font-size: 1.5em;
            margin-bottom: 10px;
            color: #ffd700;
        }
        .player-role {
            font-size: 0.9em;
            opacity: 0.8;
            margin-bottom: 15px;
        }
        .stat-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .system-info {
            margin-top: 50px;
            text-align: center;
            padding: 20px;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            font-size: 0.85em;
            opacity: 0.7;
        }
        .loading {
            text-align: center;
            padding: 50px;
            font-size: 1.2em;
        }
        .footer-note {
            margin-top: 30px;
            text-align: center;
            font-size: 0.75em;
            opacity: 0.5;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏏 GUJARAT TITANS</h1>
            <p class="subtitle">Match Analytics System v2.4.1</p>
        </header>
        <div id="players-container" class="stats-grid">
            <div class="loading">Loading player statistics...</div>
        </div>
        <div class="system-info">
            <p>System Status: <span id="system-status">Active</span> | Container ID: gt-analytics-7f8a9b2c</p>
            <p>Environment: Production | Uptime: 45 days</p>
        </div>
        <div class="footer-note">
            💡 Tip: Search engines respect certain conventions. Maybe we do too?
        </div>
    </div>
    <script>
        async function loadPlayers() {
            try {
                const response = await fetch('/api/players');
                const data = await response.json();
                const container = document.getElementById('players-container');
                container.innerHTML = '';
                for (const [name, stats] of Object.entries(data.players)) {
                    const card = document.createElement('div');
                    card.className = 'player-card';
                    let statsHtml = '';
                    for (const [key, value] of Object.entries(stats)) {
                        statsHtml += `
                            <div class="stat-item">
                                <span>${key.replace('_', ' ').toUpperCase()}</span>
                                <strong>${value}</strong>
                            </div>
                        `;
                    }
                    card.innerHTML = `
                        <div class="player-name">${name.replace('_', ' ').toUpperCase()}</div>
                        <div class="player-role">${stats.role}</div>
                        ${statsHtml}
                    `;
                    container.appendChild(card);
                }
            } catch (error) {
                console.error('Error loading players:', error);
            }
        }
        loadPlayers();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/players')
def get_players():
    return jsonify({'players': PLAYERS, 'status': 'active'})

@app.route('/api/stats/<player>')
def get_stats(player):
    if player in PLAYERS:
        return jsonify(PLAYERS[player])
    return jsonify({'error': 'Player not found'}), 404

@app.route('/api/system/info')
def system_info():
    info = {
        'version': '2.4.1',
        'environment': 'production',
        'container_id': 'gt-analytics-7f8a9b2c',
        'uptime': '45 days',
        'debug_mode': 'disabled',
        'note': 'System wellness checks require proper clearance. Path structure mirrors medical terminology.'
    }
    return jsonify(info)

@app.route(HIDDEN_ENDPOINT)
def diagnostics():
    auth_header = request.headers.get('X-GT-Internal-Auth')
    if auth_header.lower() == 'aavade':
        diagnostic_data = {
            'cpu_usage': '23%',
            'memory': '1.2GB/4GB',
            'disk': '45%',
            'network': 'healthy',
            'config_file': '/app/.env.backup',
            'observation': 'Configuration archives exist. Container orchestration tools identify themselves uniquely when accessing internal resources.'
        }
        return jsonify(diagnostic_data)
    return jsonify({'error': 'Unauthorized', 'message': 'GT spirit required for internal access(X-GT-Internal-Auth). Think about what makes us roar.'}), 401

@app.route('/api/config')
def config():
    return jsonify({'error': 'Access denied'}), 403

@app.route('/.env.backup')
def env_backup():
    user_agent = request.headers.get('User-Agent', '')
    if 'DockerClient' in user_agent:
        env_content = f"""GT_DATABASE_URL=postgresql://gt_admin:titans2024@db:5432/analytics
GT_REDIS_URL=redis://cache:6379/0
GT_API_KEY=gt_api_7f8a9b2c_internal
FLAG_PART_2_DECODED={base64.b64decode(FLAG_PART_2).decode()}
FLAG_PART_3={FLAG_PART_3}
INTERNAL_AUTH_TOKEN=aavade
SESSION_SECRET=shubman_hardik_rashid
ADMIN_ENDPOINT=/api/admin/flag
NOTE=The trophy room requires entry credentials. GT leadership trio holds the key - hash their combined identity with SHA256 and present it as 'gt_session'.
"""
        return Response(env_content, mimetype='text/plain')
    return jsonify({'error': 'Not found', 'status': 'Resource restricted to containerized service clients only'}), 404

@app.route('/robots.txt')
def robots():
    robots_content = """User-agent: *
Disallow: /api/admin/
Disallow: /internal/
Allow: /api/players
Allow: /api/stats/

User-agent: GoogleBot
Allow: /

Disallow: /api/system/

# For infrastructure details, explore system information endpoints
"""
    return Response(robots_content, mimetype='text/plain')

@app.route('/api/admin/flag')
def admin_flag():
    cookie_value = request.cookies.get('gt_session')
    if cookie_value == hashlib.sha256('shubman_hardik_rashid'.encode()).hexdigest():
        final_flag = FLAG_PART_1 + base64.b64decode(FLAG_PART_2).decode() + FLAG_PART_3 + FLAG_PART_4 + FLAG_PART_5
        return jsonify({'flag': final_flag, 'message': 'Congratulations! You cracked the Titans system!'})
    return jsonify({'error': 'Invalid session', 'status': 'GT leadership verification failed. The three pillars must unite.'}), 401

@app.route('/.git/HEAD')
def git_head():
    return Response('ref: refs/heads/production\n', mimetype='text/plain')

@app.route('/.git/config')
def git_config():
    config = """[core]
	repositoryformatversion = 0
	filemode = true
[remote "origin"]
	url = https://github.com/gujarat-titans/analytics-system.git
	fetch = +refs/heads/*:refs/remotes/origin/*
[branch "production"]
	remote = origin
	merge = refs/heads/production
[user]
	name = GT DevOps
	email = devops@gujarattitans.internal
"""
    return Response(config, mimetype='text/plain')

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'GT Analytics System'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)