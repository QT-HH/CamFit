import torch
import numpy as np
import sys
import os 
import torch.nn as nn
import torch.nn.functional as F
import yaml
import pickle
from model import AE
from utils import *
from functools import reduce
import json
from collections import defaultdict
from torch.utils.data import Dataset
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader
from argparse import ArgumentParser, Namespace
from scipy.io.wavfile import write
import random
from preprocess.tacotron.utils import melspectrogram2wav
from preprocess.tacotron.utils import get_spectrograms
import librosa 
from preprocess.audio2mel import Audio2Mel


class Inferencer(object):
    def __init__(self, config, args):
        # config store the value of hyperparameters, turn to attr by AttrDict
        self.config = config
        print(config)
        # args store other information
        self.args = args
        print(self.args)

        # init the model with config
        self.build_model()

        # load model
        self.load_model()
        self.fft = Audio2Mel().to(self.get_default_device())
        self.vocoder = torch.hub.load('descriptinc/melgan-neurips', 'load_melgan')
        
        with open(self.args.attr, 'rb') as f:
            self.attr = pickle.load(f)
    def get_default_device(self):
        if torch.cuda.is_available():
            return "cuda"
        else:
            return "cpu"


    def load_model(self):
        print(f'Load model from {self.args.model}')
        self.model.load_state_dict(torch.load(f'{self.args.model}'))
        return

    def build_model(self): 
        # create model, discriminator, optimizers
        self.model = cc(AE(self.config))
        print(self.model)
        self.model.eval()
        return

    def utt_make_frames(self, x):
        frame_size = self.config['data_loader']['frame_size']
        remains = x.size(0) % frame_size 
        if remains != 0:
            x = F.pad(x, (0, remains))
        out = x.view(1, x.size(0) // frame_size, frame_size * x.size(1)).transpose(1, 2)
        return out
    
    def convert_file(self,path):
        y, _ = librosa.load(path, sr=22050)
        print("0",y.shape, np.mean(y)) 
        y, index = librosa.effects.trim(y, top_db=17)
        print("0",y.shape, np.mean(y))
        y = torch.from_numpy(y)

        y = y[None, None]

        mel = self.fft(y.to("cuda"))
        mel = mel.transpose(1,2).detach().cpu().numpy()
        mel = mel[0]
        return mel.astype(np.float32)

    def inference_one_utterance(self, x, x_cond):
        print("11",x.shape, x.mean())  
        print("22",x_cond.shape,x_cond.mean())
        x = self.utt_make_frames(x)
        x_cond = self.utt_make_frames(x_cond)
        print("111",x.shape, x.mean())  
        print("222",x_cond.shape,x_cond.mean())
        dec = self.model.inference(x, x_cond)
        dec = dec.transpose(1, 2).squeeze(0)
        dec = dec.detach().cpu().numpy()
        dec = self.denormalize(dec)
        print("5",dec.shape, dec.mean())  
        
        dec=torch.from_numpy(dec).unsqueeze(0).transpose(1,2)

        self.melgan(dec)
        #wav_data = melspectrogram2wav(dec)
        #return wav_data, dec

    def denormalize(self, x):
        m, s = self.attr['mean'], self.attr['std']
        ret = x * s + m
        return ret

    def normalize(self, x):
        m, s = self.attr['mean'], self.attr['std']
        ret = (x - m) / s
        return ret

    def write_wav_to_file(self, wav_data, output_path):
        write(output_path, rate=self.args.sample_rate, data=wav_data)
        return
    
    def melgan(self,mel):        
        recons = self.vocoder.inverse(mel).squeeze().cpu().numpy()
        librosa.output.write_wav("mel_output.wav", recons, sr=22050)
    
    def inference_from_path(self):
        #src_mel1, _ = get_spectrograms(self.args.source)
        #print(src_mel1.shape)
        #tar_mel1, _ = get_spectrograms(self.args.target)
        src_mel = self.convert_file(self.args.source)
        tar_mel = self.convert_file(self.args.target)
        print("1",src_mel.shape, np.mean(src_mel))  
        print("2",tar_mel.shape,np.mean(tar_mel))
        src_mel = torch.from_numpy(self.normalize(src_mel)).cuda()
        tar_mel = torch.from_numpy(self.normalize(tar_mel)).cuda()
        print("3",src_mel.shape, src_mel.mean())  
        print("4",tar_mel.shape,  tar_mel.mean())
        self.inference_one_utterance(src_mel, tar_mel)
        #conv_wav, conv_mel = self.inference_one_utterance(src_mel, tar_mel)
        #self.write_wav_to_file(conv_wav, self.args.output)
        return

if __name__ == '__main__':
    os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"]="1"
    
    parser = ArgumentParser()
    parser.add_argument('-attr', '-a', help='attr file path',default = '/home/sung/proejct/adaptive_voice_conversion/preprocessed/attr.pkl')
    parser.add_argument('-config', '-c', help='config file path',default='config.yaml')
    parser.add_argument('-model', '-m', help='model path',default='./checkpoints/vctk_model69.ckpt')
    parser.add_argument('-source', '-s', help='source wav path')
    parser.add_argument('-target', '-t', help='target wav path')
    parser.add_argument('-output', '-o', help='output wav path',default='output.wav')
    parser.add_argument('-sample_rate', '-sr', help='sample rate', default=22050, type=int)
    args = parser.parse_args()
    # load config file 
    with open(args.config) as f:
        config = yaml.load(f)
    inferencer = Inferencer(config=config, args=args)
    inferencer.inference_from_path()
