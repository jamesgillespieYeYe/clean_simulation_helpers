BEGIN {
    step = 0
    time = 0
    temp = 0
    EPtot = 0
}
{
    if ($1 == "NSTEP")
    {
        step = $3
        time = $6
        temp = $9
    }
    else
    {
        EPtot = $9
        printf "%f, %f, %f, %f\n", step, time, temp, EPtot
    }
}