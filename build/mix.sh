V=$1; mkdir -p w_$V; rm -f list_$V.txt
for i in 1 2 3 4 5 6 7 8 9 10; do
  ffmpeg -y -loglevel error -i $V/s$i.mp3 -ar 24000 -ac 1 -c:a pcm_s16le w_$V/s$i.wav
  echo "file 'w_$V/s$i.wav'" >> list_$V.txt; echo "file 'pad.wav'" >> list_$V.txt
done
ffmpeg -y -loglevel error -i pad.wav -ar 24000 -ac 1 -c:a pcm_s16le pad24.wav
sed -i "s/pad.wav/pad24.wav/" list_$V.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i list_$V.txt -c:a pcm_s16le narr_$V.wav
ffmpeg -y -loglevel error -i narr_$V.wav -i pad_music.wav -filter_complex "[1]volume=0.35[m];[0][m]amix=inputs=2:duration=first:normalize=0" mix_$V.wav
