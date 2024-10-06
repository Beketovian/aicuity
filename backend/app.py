from flask import Flask, request, jsonify
from yt_vid_list import get_top_videos
from mic_quality_analyzer import analyze_static
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

        """
        his is a placeholder return for now. Output example:
        "static_analysis": {
            "5WpUfmhGAt4.wav": 0,
            "6XQB7y_FaVw.wav": 1,
            "8mZOKUNEYHc.wav": 0,
            "EX52BuZxpQM.wav": 0,
            "FdutLmvwPWk.wav": 0,
            "LORrwdqxtmg.wav": 0,
            "Rg8hC-Xx7RM.wav": 1,
            "ZZvbhY4I0Dw.wav": 1,
            "kYkiDan8Cnk.wav": 1,
            "p4FQyOwjhLA.wav": 0
        }
        
        We want to feed this into The Algorithm for ranking
        """
        return jsonify({
            "static_analysis": static_detection_results
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
