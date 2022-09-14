# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.9.1
#   kernelspec:
#     display_name: tensorflow2
#     language: python
#     name: tensorflow2
# ---

# # Python

# ## 1. Python import and define functions

# *** 
# ###  

# Python import
import os
import argparse
import collections
import random
import copy
import numpy as np
import pandas as pd
import gensim
from gensim.models import Word2Vec
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
import  sklearn.preprocessing as preprocessing
from sklearn.model_selection import KFold
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, backend
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from tfdeterminism import patch


# CNN Model
def create_CC_model(kmer_len,filter_num,units):
    model = models.Sequential()

    #Conv1d layer1
    model.add(layers.Conv1D(filters = filter_num,kernel_size = 12,strides = 1,padding = "valid",input_shape = (4000-kmer_len,100),activation = "relu"))

    #Conv1d layer2
    model.add(layers.Conv1D(filters = int(filter_num/2),kernel_size = 6,strides = 1,padding = "valid",activation = "relu"))
    model.add(layers.Dropout(0.3))

    #Max_pooling layer
    model.add(layers.MaxPooling1D(pool_size =4, strides =4))
    model.add(layers.Dropout(0.3))

    #Flatten
    model.add(layers.Flatten())

    #Dense Layer
    model.add(layers.Dense(units = units, activation = "relu"))
    model.add(layers.Dropout(0.3))

    #Output
    model.add(layers.Dense(units = 2, activation = "softmax"))
    
    return model


# Whether in jupyter notebook
def isnotebook() -> bool:
    """
    Returns True if the current execution environment is a jupyter notebook
    https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
    """
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


#get filepath of input and output
def get_filepath():
    parser = argparse.ArgumentParser()
    parser.add_argument("--training",dest = "training", help = "TrainingSet file")
    parser.add_argument("--test",dest = "test",default = 20,help = "TestSet file")
    parser.add_argument("-O","-o","--outputdir",dest = "outputdir",help = "Output dir of models")
    args = parser.parse_args()
    return args


# padding sequence to 4000nt
def padding_truncate_seq(seq):
    length = len(seq)  
    if length > 4000: 
        seq = seq[:4000]   # trancate seq to 4000nt
    else:
        seq =  seq + (4000 -length)*'N'  #padding N after seq to 4000nt
    return seq


# Convert to tensor by pretrained word2vec model
def convert2tensor(data,kmer_len,word2vec_model):
    
    label_dict = {'0': 0, '1':1}
    data["kmer"] = data.apply(lambda x: [ x["seq"][i:i+kmer_len] for i in range(0,len(x["seq"])-kmer_len)],axis = 1)
    seq = tf.convert_to_tensor(data["kmer"].apply(lambda x:np.array(word2vec_model[x],dtype=np.float32)))
    label = tf.convert_to_tensor(data["label"].apply(lambda x:np.array(label_dict[str(x)],dtype=np.float32)))
    
    Set = {"seq":seq,"label":label}
    
    return Set


#Evaluate performance of model
def evaluate_performance(y_test, y_pred, y_prob):
    # AUROC
    auroc = metrics.roc_auc_score(y_test,y_prob)
    auroc_curve = metrics.roc_curve(y_test, y_prob)
    # AUPRC
    auprc=metrics.average_precision_score(y_test, y_prob) 
    auprc_curve=metrics.precision_recall_curve(y_test, y_prob)
    #Accuracy
    accuracy=metrics.accuracy_score(y_test,y_pred) 
    #MCC
    mcc=metrics.matthews_corrcoef(y_test,y_pred)
    
    recall=metrics.recall_score(y_test, y_pred)
    precision=metrics.precision_score(y_test, y_pred)
    f1=metrics.f1_score(y_test, y_pred)
    class_report=metrics.classification_report(y_test, y_pred,target_names = ["control","case"])

    model_perf = {"auroc":auroc,"auroc_curve":auroc_curve,
                  "auprc":auprc,"auprc_curve":auprc_curve,
                  "accuracy":accuracy, "mcc": mcc,
                  "recall":recall,"precision":precision,"f1":f1,
                  "class_report":class_report}
        
    return model_perf


# Output result of evaluation
def eval_output(model_perf,path):
    with open(os.path.join(path,"Evaluate_Result_TestSet.txt"),'w') as f:
        f.write("AUROC=%s\tAUPRC=%s\tAccuracy=%s\tMCC=%s\tRecall=%s\tPrecision=%s\tf1_score=%s\n" %
               (model_perf["auroc"],model_perf["auprc"],model_perf["accuracy"],model_perf["mcc"],model_perf["recall"],model_perf["precision"],model_perf["f1"]))
        f.write("\n######NOTE#######\n")
        f.write("#According to help_documentation of sklearn.metrics.classification_report:in binary classification, recall of the positive class is also known as sensitivity; recall of the negative class is specificity#\n\n")
        f.write(model_perf["class_report"])


# Plot AUROC of model
def plot_AUROC(model_perf,path):
    #get AUROC,FPR,TPR and threshold
    roc_auc = model_perf["auroc"]
    fpr,tpr,threshold = model_perf["auroc_curve"]
    #return AUROC info
    temp_df = pd.DataFrame({"FPR":fpr,"TPR":tpr})
    temp_df.to_csv(os.path.join(path,"AUROC_info.txt"),header = True,index = False, sep = '\t')
    #plot
    plt.figure()
    lw = 2
    plt.figure(figsize=(10,10))
    plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label='AUROC (area = %0.2f)' % roc_auc) 
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("AUROC of Models")
    plt.legend(loc="lower right")
    plt.savefig(os.path.join(path,"AUROC_TestSet.pdf"),format = "pdf")


# *** 
# ###  

# ## 2. Configution

# +
# GPU Device
CONFIG = ConfigProto()
CONFIG.gpu_options.allow_growth = True
SESSION = InteractiveSession(config=CONFIG)
TF_DETERMINISTIC_OPS=1
# hdf5 
os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"
# Random seed
patch()
SEED = 100
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)
# Hyper-parameters
OPTIMIZER = "adam"
BATCH = 32
SHUFFLE = True
EPOCH = 100
LOSS = "sparse_categorical_crossentropy"
METRICS = ["accuracy","sparse_categorical_crossentropy"]
PATIENCE = 10
filters_num_list = [32,64,128]
units_list = [256,512,1024]

# Index of model performance
ModelPerf = collections.namedtuple('ModelPerf',
                                   ['auroc', 'auroc_curve', 'auprc', 'auprc_curve', 'accuracy', 
                                    'mcc','recall', 'precision', 'f1', 'class_report','ce_loss'])

# kmer length
kmer_len = 5

# *** 
# ###  

# ## 3. Data Processing

# Get input_file path
if isnotebook():
    training_f = "/data/rnomics8/yuanguohua/RNA-Light_Original/lncRNA/03_Model_Construction/lncRNA_sublocation_TrainingSet.tsv"
    test_f = "/data/rnomics8/yuanguohua/RNA-Light_Original/lncRNA/03_Model_Construction/lncRNA_sublocation_TestSet.tsv"
else:
    args = get_filepath()
    training_f = args.training
    test_f = args.test
    output_dir = args.outputdir
    if not (os.path.exists(output_dir)):
        os.makedirs(output_dir)
# Load data
dataset_training = pd.read_csv(training_f,sep='\t',index_col = False)    #3412  
dataset_test = pd.read_csv(test_f,sep='\t',index_col = False)    #380
# Fix seq to 4000nt
dataset_training["cdna"] = dataset_training["cdna"].apply(lambda x:padding_truncate_seq(x))
dataset_test["cdna"] = dataset_test["cdna"].apply(lambda x:padding_truncate_seq(x))
# Format :[seq] [label]
dataset_training = dataset_training.iloc[:,2:4]
dataset_training.columns = ["seq","label"]
dataset_test = dataset_test.iloc[:,2:4]
dataset_test.columns = ["seq","label"]

# Load word2vec model
word2vec_model = Word2Vec.load("/data/rnomics8/yuanguohua/RNAlight_review/lncRNA/word2vec/Pretrained_CNN_word2vec_model/00_pretrained_CNN_word2vec_" + str(kmer_len) + "_mer_len.model")

# *** 
# ###  

# ## 4. Optimize hyperparameters by five-fold cross validation

# +
# This dataframe can store the highest mean of auroc among five-fold cross validations with each combination of hyperparameters
comb_auroc = pd.DataFrame(columns = ["filter_num","units","auroc_on_CV"])

# Optimize hyperparameters about model architechture
for filter_num in filters_num_list:
    for units in units_list:
        # Five-fold cross validation
        cvscore_auroc_iter = []
        kfold = KFold(n_splits=5, random_state=SEED, shuffle=True)
        for train_index, validate_index in kfold.split(dataset_training):
            # Get cross validation set
            train,validate = dataset_training.loc[train_index,],dataset_training.loc[validate_index,]
            TrainingSet = convert2tensor(train,kmer_len,word2vec_model)
            ValidationSet = convert2tensor(validate,kmer_len,word2vec_model)

            # Train model
            Net = create_CC_model(kmer_len = kmer_len, filter_num = filter_num, units = units)
            callbacks = [keras.callbacks.EarlyStopping(monitor = "val_accuracy",patience=PATIENCE, 
                                                       min_delta=1e-3,mode = "auto",restore_best_weights = True)]
            Net.compile(optimizer = OPTIMIZER, loss = LOSS, metrics = METRICS)
            Net_history = Net.fit(TrainingSet["seq"],
                                  TrainingSet["label"],
                                  batch_size = BATCH,
                                  epochs = EPOCH,
                                  shuffle = SHUFFLE,
                                  callbacks = callbacks,
                                  validation_data = (ValidationSet["seq"],ValidationSet["label"]),
                                  verbose = 0)

            # Get the auroc of the model with maximum accuracy on validation set per fold
            cvscore_auroc_iter.append(Net_history.history["val_accuracy"][-(PATIENCE+1)])
            
        # Add to the dataframe    
        comb_auroc.loc[len(comb_auroc)] = [filter_num,units,cvscore_auroc_iter]

        
# Choose the optimal combnation of hyperparameters
comb_auroc["mean_auroc_on_CV"] = comb_auroc["auroc_on_CV"].apply(np.mean)
optimal_comb_index = comb_auroc["mean_auroc_on_CV"].argmax()
optimal_filter_num = comb_auroc["filter_num"].loc[optimal_comb_index]
optimal_units = comb_auroc["units"].loc[optimal_comb_index]

# Output result of cross validation
comb_auroc.to_csv(os.path.join(output_dir,"CNN_CV_result.tsv"),sep = '\t',header = True,index = False)
# -

# *** 
# ###  

# ## 5. Refit model with the optimal hyperparameters and whole training set

# +
# Whole training set
Whole_training = convert2tensor(dataset_training,kmer_len,word2vec_model)

# Refit model
logdir = os.path.join(output_dir,"log")
Net_final = create_CC_model(kmer_len = kmer_len, filter_num = optimal_filter_num , units = optimal_units)
callbacks_final = [keras.callbacks.TensorBoard(log_dir=logdir),
                   keras.callbacks.EarlyStopping(monitor = "val_accuracy",patience=PATIENCE,restore_best_weights = True),
                   keras.callbacks.ModelCheckpoint(filepath = os.path.join(output_dir, "best_model.h5"), monitor="val_accuracy",
                                                   save_best_only=True,mode = "auto")]
Net_final.compile(optimizer = OPTIMIZER, loss = LOSS, metrics = METRICS)
Net_final_history = Net_final.fit(Whole_training["seq"],
                                  Whole_training["label"],
                                  batch_size = BATCH,
                                  epochs = EPOCH,
                                  shuffle = SHUFFLE,
                                  callbacks = callbacks_final,
                                  validation_split = 0.1,
                                  verbose = 2)
Net_final.summary()
# -

# *** 
# ###  

# ## 6. Evaluate model performance on Test set

# +
################################# Model Construction #############################
print("\n********************** Start Model Construction ***********************")
# Whole test set
TestSet = convert2tensor(dataset_test,kmer_len,word2vec_model)

# Load best model
best_model =  tf.keras.models.load_model(os.path.join(output_dir,"best_model.h5"))
# Predict
prediction = best_model.predict(TestSet["seq"])
# Evaluate
pre_label = np.argmax(prediction,axis=1)
true_label = TestSet["label"].numpy()
posi_prob = prediction[:,1]
model_perf = evaluate_performance(true_label,pre_label,posi_prob)

# Output performance
eval_output(model_perf,output_dir)
# Plot AUROC
plot_AUROC(model_perf,output_dir)
# -


