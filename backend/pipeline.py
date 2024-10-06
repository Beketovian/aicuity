import text_sim
import yt_transcript
import yt_vid_list

query = "Prime Number Theorem"
vids = yt_vid_list.get_top_videos(query)

texts_list = []

for vid in vids:
    transcript = yt_transcript.get_yt_transcript(vid)
    full_text = [elem["text"] for elem in transcript]
    full_text = " ".join(full_text)
    texts_list.append(full_text)

scores = text_sim.do_text_sim(query, texts_list)

max_score = max(scores)
max_idx = scores.index(max_score)
print("Similarity Score:", max_score, "https://www.youtube.com/watch?v=" + vids[max_idx])
