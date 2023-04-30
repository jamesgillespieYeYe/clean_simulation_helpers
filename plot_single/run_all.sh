INPUT_LIST="input_filelist.txt"
DIR="files"
FRAMES="frames.out"
COUNT=0
rm $FRAMES
while read -r line
do
    echo $line
    full_path="$DIR/$line"
    echo $full_path
    ./parse.sh "$full_path.out"
    $(python3 plot.py -np:0)
    FRAME=$(cat step.txt)
    echo "FRAME: $FRAME"
    echo "$COUNT,$line.mdcrd,$FRAME" >> $FRAMES
    ((COUNT = COUNT + 1))

done < $INPUT_LIST