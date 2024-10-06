from flask import Flask, request, jsonify
from yt_vid_list import get_top_videos
from mic_quality_analyzer import analyze_static
from yt_transcript import get_yt_transcript
from text_sim import do_text_sim
from matching_algo import perform_matching

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
        transcripts = get_yt_transcript(top_videos)
        scores, relevant_times = do_text_sim(search_query, transcripts)

        # list with (id, text score, static score)
        ids_and_scores = [(top_videos[i], scores[i], static_detection_results[top_videos[i]]) for i in range(len(top_videos))]

        rankings = perform_matching(ids_and_scores)

        return jsonify({
            "ranking": rankings
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
