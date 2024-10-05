from flask import Flask, request, jsonify
from yt_vid_list import get_top_videos

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search_videos():
    data = request.get_json()
    search_query = data.get('query', '')

    if not search_query:
        return jsonify({"error": "No search query provided"}), 400

    try:
        top_videos = get_top_videos(search_query)
        return jsonify({"videos": top_videos}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
