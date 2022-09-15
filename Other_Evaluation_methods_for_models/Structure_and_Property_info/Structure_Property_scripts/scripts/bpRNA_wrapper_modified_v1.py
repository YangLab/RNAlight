import argparse
import json
import pickle
import pdb
import subprocess
def parse_args():
    parser=argparse.ArgumentParser(description="Wrapper for bpRNA")
    parser.add_argument("--data_bracket")
    parser.add_argument("--text_out",default=None)
    parser.add_argument("--pickle_out",default=None)
    return parser.parse_args()

def get_bpRNA_annotation(input_string):
    #use an intermediate tmp file because bpRNA needs it
    out_tmp=open('tmp.dbn','w')
    out_tmp.write(input_string+'\n')
    out_tmp.close()
    subprocess.call("perl scripts/bpRNA.pl tmp.dbn", shell=True)
    in_tmp=open("tmp.st",'r')
    annotation=in_tmp.read()
    in_tmp.close()
    return annotation    


def main():
    args=parse_args()
    outf=open(args.text_out,'w')
    cn=0
    tmp_title=""
    tmp_seq=""
    f=open(args.data_bracket,'r')
    data_dict=dict()
    key=""
    for line in f:
        if cn%3==0:
            tmp_title=line
            x=tmp_title.split("  ")
            y=x[0].split(" = ")
            z=x[1].split("\n")
            data_dict[z[0]]=dict()
            data_dict[z[0]]["ENERGY"]=y[1]
            key=z[0]
        if cn%3==1:
            tmp_seq=line
        if cn%3==2:
            print(tmp_seq)
            bpRNA_annotation=get_bpRNA_annotation('\n'.join([tmp_title,tmp_seq,line]))
            data_dict[key]["computational"]=bpRNA_annotation
            outf.write(tmp_title)
            outf.write(bpRNA_annotation)
        cn=cn+1		

    with open(args.pickle_out,'wb') as handle:
        pickle.dump(data_dict,handle,protocol=pickle.HIGHEST_PROTOCOL)

'''
    data=json.load(open(args.data_json,'r'))
    data_dict=dict()
    for item in data['items']:
        #pdb.set_trace()
        cur_id=item['rna_id']
        print("processing structure data for item:"+str(cur_id))
        data_dict[cur_id]=dict()
        sequence_string=item['sequence_string']
        structure=item['_'.join([args.approach,'structure'])]
        try:
            bootstrap_structures=item['bootstrap_structures']
            data_dict[cur_id]['bootstraps']=dict()
            struct_tally=dict()
            #get a tally of how frequent each bootstrapped structure is
            for struct in bootstrap_structures:
                if struct not in struct_tally:
                    struct_tally[struct]=1
                else:
                    struct_tally[struct]+=1
            bootstrap_count=0
            for struct in struct_tally:
                header=','.join(['>bootstrap',cur_id+'.'+str(bootstrap_count),'frequency:'+str(struct_tally[struct])])
                bpRNA_annotation=get_bpRNA_annotation('\n'.join([header,sequence_string,struct]))
                bootstrap_count+=1
                data_dict[cur_id]['bootstraps'][bpRNA_annotation]=struct_tally[struct]
        except:
            print("no bootstrap structures for "+str(cur_id)+", continuing")
        header=','.join(['>'+args.approach,cur_id])
        bpRNA_annotation=get_bpRNA_annotation('\n'.join([header,sequence_string,structure]))
        data_dict[cur_id][args.approach]=bpRNA_annotation
    #save to pickle
    with open(args.pickle_out,'wb') as handle:
        pickle.dump(data_dict,handle,protocol=pickle.HIGHEST_PROTOCOL)
    #write to text file
    outf=open(args.text_out,'w')
    for cur_id in data_dict:
        outf.write(">"+cur_id+','+args.approach+'\n')
        outf.write(data_dict[cur_id][args.approach]+'\n')
        i=0
        if 'bootstraps' in data_dict[cur_id]: 
            for entry in data_dict[cur_id]['bootstraps']:
                outf.write('>'+cur_id+'.'+str(i)+',bootstrap,count='+str(data_dict[cur_id]['bootstraps'][entry])+'\n')
                outf.write(entry)
                i+=1
'''
        
if __name__=="__main__":
    main()
    
