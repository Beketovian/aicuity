from flask import Flask, request, jsonify
from yt_vid_list import get_top_videos
from mic_quality_analyzer import analyze_static

app = Flask(__name__)

# Combined route for searching videos and analyzing static noise
@app.route('/search_and_analyze', methods=['POST'])
def search_and_analyze_videos():
    data = request.get_json()
    search_query = data.get('query', '')

    if not search_query:
        return jsonify({"error": "No search query provided"}), 400

    try:
        top_videos = get_top_videos(search_query)

        static_detection_results = analyze_static(top_videos)

        return jsonify({
            "static_analysis": static_detection_results
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
