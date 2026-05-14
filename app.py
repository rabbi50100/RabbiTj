from flask import Flask, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL লাগবে'}), 400
    
    try:
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        return jsonify({
            'title': info.get('title'),
            'thumbnail': info.get('thumbnail'),
            'download_url': f'/file/{os.path.basename(filename)}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/file/<filename>')
def get_file(filename):
    return send_file(os.path.join(DOWNLOAD_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
