from flask import Flask, request, jsonify
from yt_vid_list import get_top_videos
from mic_quality_analyzer import analyze_static

app = Flask(__name__)

# outputs list of video IDs based on the search query. Right now it is configured to output the top 10 videos
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

# route for analyzing static in vids, feed a list of IDs in and it will output a dictionary: {<ID>: <0 or 1>}
@app.route('/analyze', methods=['POST'])
def analyze_videos():
    data = request.get_json()
    video_ids = data.get('video_ids', [])

    if not video_ids:
        return jsonify({"error": "No video IDs provided"}), 400

    try:
        static_detection_results = analyze_static(video_ids)
        return jsonify(static_detection_results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
