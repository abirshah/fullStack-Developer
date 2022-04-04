raspivid -o - -t 0 -vf -w 640 -h 480 -n -fps 30 -rot 180 |cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:3000}' :demux=h264
