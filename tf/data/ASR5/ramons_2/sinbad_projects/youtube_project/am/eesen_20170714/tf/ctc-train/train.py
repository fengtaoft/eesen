#!/usr/bin/env python

from utils.fileutils import debug
"""
this project has been wrtien following this naming convention:

https://google.github.io/styleguide/pyguide.html#naming
plus mutable vars in function (that are actually changes m_*)

"""

# -----------------------------------------------------------------
#   Main script
# -----------------------------------------------------------------

import argparse
import os
import constants
import os.path
import pickle
import sys
from eesen import Eesen
from utils.checkers import set_checkers

from reader.feats_reader import feats_reader_factory
from reader.labels_reader import labels_reader_factory


# -----------------------------------------------------------------
#   Parser and Configuration
# -----------------------------------------------------------------

def main_parser():
    parser = argparse.ArgumentParser(description='Train TF-Eesen Model')

    #general arguments
    parser.add_argument('--debug', default=False, dest='debug', action='store_true', help='enable debug mode')
    parser.add_argument('--store_model', default=False, dest='store_model', action='store_true', help='store model')
    parser.add_argument('--data_dir', default = "./tmp", help = "data dir")
    parser.add_argument('--train_dir', default = "log", help='log and model (output) dir')

    #TODO check name of config.pkl
    parser.add_argument('--import_config', default = "", help='load an old configuration file (config.pkl) extra labels will be added to old configuration')

    #io arguments
    parser.add_argument('--continue_ckpt', default = "", help='continue this experiment')
    parser.add_argument('--batch_size', default = 32, type=int, help='batch size')
    parser.add_argument('--noshuffle', default=True, dest='do_shuf', action='store_false', help='do not shuffle training samples')
    parser.add_argument('--augment', default=False, dest='augment', action='store_true', help='do internal data augmentation')

    #architecture arguments
    parser.add_argument('--lstm_type', default="cudnn", help = "lstm type: cudnn, fuse, native")
    parser.add_argument('--nproj', default = 0, type=int, help='dimension of projection units, set to 0 if no projection needed')
    parser.add_argument('--l2', default = 0.0, type=float, help='l2 normalization')
    parser.add_argument('--nlayer', default = 5, type=int, help='#layer')
    parser.add_argument('--nhidden', default = 320, type=int, help='dimension of hidden units in single direction')
    parser.add_argument('--clip', default = 0.1, type=float, help='gradient clipping')
    parser.add_argument('--batch_norm', default = False, dest='batch_norm', action='store_true', help='add batch normalization to FC layers')
    parser.add_argument('--feat_proj', default = 0, type=int, help='dimension of feature projection units, set to 0 if no projection needed')
    parser.add_argument('--grad_opt', default = "grad", help='optimizer: grad, adam, momentum, cuddnn only work with grad')

    #runtime arguments
    parser.add_argument('--nepoch', default = 30, type=int, help='#epoch')
    parser.add_argument('--lr_rate', default = 0.03, type=float, help='learning rate')
    parser.add_argument('--half_period', default = 10, type=int, help='half period in epoch of learning rate')
    parser.add_argument('--half_rate', default = 0.5, type=float, help='halving factor')
    parser.add_argument('--half_after', default = 0, type=int, help='halving becomes enabled after this many epochs')

    #sat arguments
    parser.add_argument('--apply_sat', default = False, action='store_true', help='apply and train a sat layer')
    parser.add_argument('--num_sat_layers', default = 2, type=int, help='continue this experiment')

    return parser

def create_sat_config(args):

    sat={}

    sat[constants.CONF_TAGS.APPLY_SAT]=args.apply_sat
    sat[constants.CONF_TAGS.NUM_SAT_LAYERS]=args.num_sat_layers

    return sat

def create_online_argu_config(args):

    #TODO enter the values using a conf file or something
    online_augment_config={}
    online_augment_config[constants.AUGMENTATION.WINDOW]=3
    online_augment_config[constants.AUGMENTATION.FACTOR]=3
    online_augment_config[constants.AUGMENTATION.ROLL]=False

    return online_augment_config

def create_global_config(args):

    config = {

        #general arguments
        constants.CONF_TAGS.DEBUG: False,
        constants.CONF_TAGS.STORE_MODEL: args.store_model,
        constants.CONF_TAGS.DATA_DIR: args.data_dir,
        constants.CONF_TAGS.TRAIN_DIR: args.train_dir,
        constants.CONF_TAGS.RANDOM_SEED: 15213,

        #io arguments
        constants.CONF_TAGS.BATCH_SIZE: args.batch_size,
        constants.CONF_TAGS.DO_SHUF: args.do_shuf,

        #runtime arguments
        constants.CONF_TAGS.NEPOCH: args.nepoch,
        constants.CONF_TAGS.LR_RATE: args.lr_rate,
        constants.CONF_TAGS.HALF_PERIOD: args.half_period,
        constants.CONF_TAGS.HALF_RATE: args.half_rate,
        constants.CONF_TAGS.HALF_AFTER: args.half_after,

        #architecture arguments
        #TODO this can be joined with one argument
        constants.CONF_TAGS.LSTM_TYPE: args.lstm_type,
        constants.CONF_TAGS.NPROJ: args.nproj,
        constants.CONF_TAGS.L2: args.l2,
        constants.CONF_TAGS.NLAYERS: args.nlayer,
        constants.CONF_TAGS.NHIDDEN: args.nhidden,
        constants.CONF_TAGS.CLIP: args.clip,
        constants.CONF_TAGS.BATCH_NORM: args.batch_norm,
        constants.CONF_TAGS.FEAT_PROJ: args.feat_proj,
        constants.CONF_TAGS.GRAD_OPT: args.grad_opt,

        #adptation
        constants.CONF_TAGS.APPLY_SAT: args.apply_sat,
        constants.CONF_TAGS.NUM_SAT_LAYERS: args.num_sat_layers
    }

    #org_path has been removed we will use continue_cpkt
    config[constants.CONF_TAGS.SAT] = create_sat_config(args)
    config[constants.CONF_TAGS.ONLINE_AUGMENT_CONF] = create_online_argu_config(args)

    if len(args.continue_ckpt):
        config[constants.CONF_TAGS.CONTINUE_CKPT] = args.continue_ckpt

    return config


def import_config(args):

    if not os.path.exists(args.import_config):
        print("Error: path_config does not correspond to a valid path: "+args.import_config)
        print(debug.get_debug_info())
        print("exiting...")
        sys.exit()

    config = pickle.load(open(args.import_config, "rb"))
    #TODO get non default args and add/substitute them

    #for now we will only consider sat arguments
    sat_config = create_sat_config(args)
    config.update(sat_config)

    config[constants.CONF_TAGS.DATA_DIR]= args.data_dir
    config[constants.CONF_TAGS.ONLINE_AUGMENT_CONF] = create_online_argu_config(args)

    return config



# -----------------------------------------------------------------
#   Main part
# -----------------------------------------------------------------

def main():

    #TODO construct a factory/helper to load everything by just looking at data_dir

    parser = main_parser()
    args = parser.parse_args()

    if(args.import_config):
        config = import_config(args)
    else:
        config = create_global_config(args)

    #load training feats
    tr_x = feats_reader_factory.create_reader('train', 'kaldi', config)

    #load training targets
    tr_y = labels_reader_factory.create_reader('train', 'txt', config, tr_x.get_batches_id())


    #create reader for labels
    cv_x = feats_reader_factory.create_reader('cv', 'kaldi', config)

    #create reader for labels
    cv_y = labels_reader_factory.create_reader('cv', 'txt', config, cv_x.get_batches_id())

    #set config (targets could change)
    config[constants.CONF_TAGS.INPUT_FEATS_DIM] = cv_x.get_num_dim()
    config[constants.CONF_TAGS.LANGUAGE_SCHEME] = cv_y.get_language_scheme()


    #TODO how to fine tune an addapted model?
    if config[constants.CONF_TAGS.APPLY_SAT]:
        cv_sat = feats_reader_factory.create_reader('sat', 'kaldi', config, cv_x.get_batches_id())
        tr_sat = feats_reader_factory.create_reader('sat', 'kaldi', config, tr_x.get_batches_id())
        data = (cv_x, tr_x, cv_y, tr_y, cv_sat, tr_sat)
        config[constants.CONF_TAGS.SAT_FEAT_DIM] = tr_sat.get_num_dim()
        config[constants.CONF_TAGS.MODEL_DIR] = os.path.join(config[constants.CONF_TAGS.TRAIN_DIR],
                                                             constants.DEFAULT_NAMES.MODEL_DIR_NAME,
                                                             constants.DEFAULT_NAMES.SAT_DIR_NAME)
        #checking that all sets are consitent
        set_checkers.check_sets_training(cv_x, cv_y, tr_x, tr_y, tr_sat)

    else:
        data = (cv_x, tr_x, cv_y, tr_y)
        config[constants.CONF_TAGS.MODEL_DIR] = os.path.join(config[constants.CONF_TAGS.TRAIN_DIR],
                                                             constants.DEFAULT_NAMES.MODEL_DIR_NAME)
        #checking that all sets are consitent
        set_checkers.check_sets_training(cv_x, cv_y, tr_x, tr_y)

    #create folder for storing experiment
    if not os.path.exists(config[constants.CONF_TAGS.MODEL_DIR]):
        os.makedirs(config[constants.CONF_TAGS.MODEL_DIR])

    pickle.dump(config, open(os.path.join(config[constants.CONF_TAGS.MODEL_DIR], "config.pkl"), "wb"))

    #start the acutal training
    eesen=Eesen()

    print("done!!!")
    sys.exit()
    eesen.train(data, config)

if __name__ == "__main_":
    main()
