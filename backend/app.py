from flask import Flask, request, jsonify
from yt_vid_list import get_top_videos
from mic_quality_analyzer import analyze_static
from yt_transcript import get_yt_transcript
from text_sim import do_text_sim
from matching_algo import perform_matching
import random
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
        transcripts = []
        for id in top_videos:
            transcripts.append(get_yt_transcript(id))
        scores, relevant_times = do_text_sim(search_query, transcripts)

        # list with (id, text score, static score)
        #print(static_detection_results)
        #print(relevant_times)
        ids_and_scores = [(top_videos[i], scores[i], static_detection_results[top_videos[i]], relevant_times[i]) for i in range(len(top_videos))]

        rankings = perform_matching(ids_and_scores)

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
            "ranking": rankings
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
