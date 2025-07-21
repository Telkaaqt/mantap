
rm -rf extracted_db font-module downloads/* output/* tmp/* *.jpg *.png *.raw *.mp3 *.mp4 *.zip
rm -rf *session* *log* *tmp* *unknown* *errors*

find . -type d -name "__pycache__" -exec rm -rf {} +

ls