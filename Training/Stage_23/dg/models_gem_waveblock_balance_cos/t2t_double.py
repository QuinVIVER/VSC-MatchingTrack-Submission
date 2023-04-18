from __future__ import absolute_import

from torch import nn
from torch.nn import functional as F
from torch.nn import init
import torchvision
import torch
import random
from collections import OrderedDict

from .gem import GeneralizedMeanPoolingP
from .metric import build_metric
from dg.models_gem_waveblock_balance_cos.t2t_models import t2t_vit_14

__all__ = ['T2T', 'T2T_vit_14']

class T2T(nn.Module):
    def __init__(self, depth, pretrained=True, cut_at_pooling=False,
                 num_features=0, norm=False, dropout=0, num_classes=0, num_classes_small=0,
                 dev = None):
        super(T2T, self).__init__()
        self.pretrained = True
        self.depth = depth
        self.cut_at_pooling = cut_at_pooling
        self.num_classes = num_classes
        self.num_classes_small = num_classes_small
        
        t2t = t2t_vit_14(pretrained=False)
        print("Loading the supervised T2T pre-trained model")
        ckpt = torch.load('logs/pretrained/81.5_T2T_ViT_14.pth.tar', map_location='cpu')
        t2t.load_state_dict(ckpt['state_dict_ema'])
        t2t.head = nn.Sequential()
        
        self.base = nn.Sequential(
            t2t
        )#.cuda()
        
        self.linear = nn.Linear(384, 512)
        
        self.classifier = build_metric('cos', 384, self.num_classes, s=64, m=0.35).cuda()
        self.classifier_1 = build_metric('cos', 512, self.num_classes, s=64, m=0.6).cuda()
        self.classifier_small = build_metric('cos', 384, self.num_classes_small, s=64, m=0.35).cuda()
        self.classifier_small_1 = build_metric('cos', 512, self.num_classes_small, s=64, m=0.6).cuda()
        
        self.projector_feat_bn = nn.Sequential(
                nn.Identity()
            ).cuda()

        self.projector_feat_bn_1 = nn.Sequential(
                self.linear,
                nn.Identity()
            ).cuda()
        

    def forward(self, x, y=None, y_small=None):
        x = self.base(x)
        x = x.view(x.size(0), -1)
        
        bn_x = self.projector_feat_bn(x)
        prob = self.classifier(bn_x, y)
        prob_small = self.classifier_small(bn_x, y_small)
        
        bn_x_512 = self.projector_feat_bn_1(bn_x)
        prob_1 = self.classifier_1(bn_x_512, y)
        prob_small_1 = self.classifier_small_1(bn_x_512, y_small)
        
        
        return bn_x_512, prob, prob_1, prob_small, prob_small_1


def T2T_vit_14_double(**kwargs):
    return T2T(50, **kwargs)
