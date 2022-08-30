#get command line parameters
ARGS=`getopt -o q:m:p:O:h:v --long query:,prefix:,outputdir:,mRNA:,RNA:,version:,help  -- "$@"`
eval set -- "$ARGS"
while true ; do
    case "$1" in
        -q|--query) QUERY=$2 ; shift;;
        -m|--mRNA) mRNA="True"
            case "$2" in ""); shift 2 ;;
        -p|--prefix) PREFIX=$2 ; shift;;
        -O|--outputdir) OUTPUTDIR=$2 ; shift;;
        --RNA) RNA="True"; shift;;
		-v|--version) VERSION ; shift;;
		-h|--help) HELP ; exit 1;;
		--)
			shift
			break
			;;
		*) echo "unknown parameter:" $1; echo "Please input RNA-Light -h/--help to see usage"; exit 1;;
	esac
done

echo $QUERY 
echo $OUTPUTDIR