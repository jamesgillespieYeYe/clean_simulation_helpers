input="frames.out"
output_list="input_files.txt"
OLD_IFS=$IFS
PRM_FILE=minip.altE.prmtop
#PRM_FILE=minip.prmtop
while read -r line
do
    echo $line
    IFS=','
    read -ra arr <<< "$line"
    # for val in ${arr[@]}
    # do
    #     echo "$val"
    # done
    IFS=$OLD_IFS

    NUM=${arr[0]}
    FILENAME=${arr[1]}
    FRAME=${arr[2]}
    echo "NUM: $NUM"
    echo "NAME: $FILENAME"
    echo "FRAME: $FRAME"
    RST_FILE="traj$NUM.rst"
    PDB_FILE="traj$NUM.pdb"
    echo "Restart output going to: $RST_FILE"
    echo "PDB output going to: $PDB_FILE"
    echo "traj$NUM" >> $output_list
    CMD="parm $PRM_FILE\n trajin $FILENAME \n"
    CMD="$CMD reference $FILENAME\n"
    CMD="$CMD trajout $RST_FILE restart onlyframes $FRAME\n"
    CMD="$CMD trajout $PDB_FILE pdb onlyframes $FRAME\n"
    echo -e "$CMD" | cpptraj
done < "$input"
