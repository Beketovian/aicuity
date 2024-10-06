import text_sim
import yt_transcript
import yt_vid_list

query = "How to do Long Division"
vids = yt_vid_list.get_top_videos(query)

texts_list = []

for vid in vids:
    transcript = yt_transcript.get_yt_transcript(vid)
    texts_list.append(transcript)

scores, relevant_times = text_sim.do_text_sim(query, texts_list)

max_score = max(scores)
max_idx = scores.index(max_score)

# min_score = min(scores)
# min_idx = scores.index(min_score)

# print("Min Similarity Score:", min_idx, "https://www.youtube.com/watch?v=" + vids[min_idx])
print("Max Similarity Score Index:", max_idx, "https://www.youtube.com/watch?v=" + vids[max_idx], relevant_times[max_idx])
