
class MODEL_NAME:
    ACHEN="achen"
    ACHEN_SUM="achen_sum"
    ACHEN_CONV="achen_conv"
    DEEP_BILSTM="deepbilstm"
    ARCNET="arc_net"
    CONVNET="conv_net"

class DEFAULT_FILENAMES:
    SAT="sat_local"


class SCOPES:
    SPEAKER_ADAPTAION="speaker_adaptation"
    OUTPUT="output_layers"

    SAT_CONCAT="output_layers"
    SAT_FUSE="output_layers"

#names
class DEFAULT_NAMES:
    NO_LANGUAGE_NAME = "no_name_language"
    NO_TARGET_NAME = "no_target_name"
    MODEL_DIR_NAME = "model"
    SAT_DIR_NAME = "sat"

class CONF_TAGS:

    #general arguments
    DEBUG="debug"
    STORE_MODEL = "store_model"
    DATA_DIR = "data_dir"
    TRAIN_DIR = "train_dir"
    MODEL_DIR = "model_dir"

    #io arguments
    CONTINUE_CKPT="continue_ckpt"
    DIFF_NUM_TARGET_CKPT="diff_num_target_ckpt"
    FORCE_LR_EPOCH_CKPT="force_lr_epoch"

    BATCH_SIZE="batch_size"
    DO_SHUF="do_shuf"
    ONLINE_AUGMENT_CONF = "online_augment_conf"

    #architecture arguments
    LSTM_TYPE = "lstm_type"
    MODEL = "model"
    NPROJ = "nproj"
    L2="l2"
    NLAYERS="nlayer"
    NHIDDEN="nhidden"
    CLIP="clip"
    BATCH_NORM = "batch_norm"
    FEAT_PROJ = "feat_proj"
    GRAD_OPT="grad_opt"
    LANGUAGE_SCHEME = "target_scheme"
    INPUT_FEATS_DIM = "input_feats_dim"

    #runtime arguments
    NEPOCH="nepoch"
    LR_RATE="lr_rate"
    HALF_PERIOD="half_period"
    HALF_RATE="half_rate"
    HALF_AFTER="half_after"

    #training conf
    RANDOM_SEED="random_seed"

    #sat arguments
    SAT_CONF="sat_conf"
    SAT_SATGE="sat_stage"
    SAT_TYPE = "sat_type"
    NUM_SAT_LAYERS="num_sat_layers"
    SAT_FEAT_DIM="sat_feat_dim"

class AUGMENTATION:
    WINDOW="window"
    SUBSAMPLING="subsampling"
    ROLL="roll"

class LSTM_TYPE:
    CUDNN= "cudnn_lstm"
    FUSE= "fuse_lstm"
    NATIVE= "native_lstm"

class SAT_SATGES:
    TRAIN_SAT = "train_sat"
    FINE_TUNE = "fine_tune"

class SAT_TYPE:
    CONCAT = "concat"
    SHIFT = "shift"
    UNADAPTED = "non_adapted"

class CONFIG_TAGS_TEST:


    TRAIN_CONFIG = "train_config"
    PRIORS_SCHEME = "priors_scheme"
    ONLINE_STORAGE = "online_store"

    #io dir
    DATA_DIR = "data_dir"
    RESULTS_DIR = "results_dir"

    #train configuration
    EVAL_CONFIG_FILE = "eval_config_file"
    TRAINED_WEIGHTS = "trained_weights"

    #computing options
    BATCH_SIZE = "batch_size"
    TEMPERATURE = "temperature"
    USE_PRIORS = "use_priors"
    COMPUTE_TER = "compute_ter"
    COUNT_AUGMENT = "count_augment"

