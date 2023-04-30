input="dict_filenames.log"
RAW_STORAGE=out
while read -r line
do
    echo $line
    cat $line | grep "TIME\|EPtot\|NSTEP" > $RAW_STORAGE
    newfile="${line}.csv"
    echo $newfile
    echo "step,time,temp,EPtot" > $newfile
    cat $RAW_STORAGE | awk -f parse.awk >> $newfile
    #python3 plot.py -i:$newfile -t:$newfile
done < "$input"