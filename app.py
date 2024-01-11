from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

videos = [
    {"id": 1, "url": "https://www.youtube.com/watch?v=h0ffIJ7ZO4U", "title": "Video 1"},
    {"id": 2, "url": "https://www.youtube.com/watch?v=EL_pBJN_O3M", "title": "Video 2"},
]

@app.route('/api/videos', methods=['GET'])
def get_videos():
    return jsonify(videos)

@app.route('/api/videos', methods=['POST'])
def add_video():
    if not request.json or 'url' not in request.json:
        abort(400)
    video = {
        'id': videos[-1]['id'] + 1,
        'url': request.json['url'],
        'title': request.json.get('title', "")
    }
    videos.append(video)
    return jsonify(video), 201

@app.route('/api/videos/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    video = next((video for video in videos if video['id'] == video_id), None)
    if video is None:
        abort(404)
    videos.remove(video)
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
