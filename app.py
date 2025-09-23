from flask import Flask, render_template, jsonify, request
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from xml.etree import ElementTree as ET

app = Flask(__name__, static_folder='static', static_url_path='')
app.url_map.strict_slashes = False

@app.after_request
def add_cors_headers(response):
    # Headers needed for Godot projects
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    return response

# Homepage
@app.route('/')
def home():
    return render_template('index.html')

# RSS Feed API
@app.route('/api/feed', methods=['GET'])
def fetch_feed():
    feed_url = request.args.get('url')
    if not feed_url:
        return jsonify({"error": "No feed URL provided"}), 400

    try:
        with urlopen(feed_url) as response:
            content = response.read()
            xml_root = ET.fromstring(content)

            # Parse RSS feed items
            items = []
            for item in xml_root.findall(".//item"):
                title = item.find("title").text if item.find("title") is not None else "No title"
                link = item.find("link").text if item.find("link") is not None else "#"
                items.append({"title": title, "link": link})

            return jsonify(items)
    except HTTPError as e:
        return jsonify({"error": f"HTTP error: {e.code}"}), 500
    except URLError as e:
        return jsonify({"error": f"URL error: {e.reason}"}), 500
    except ET.ParseError:
        return jsonify({"error": "Failed to parse RSS feed"}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
