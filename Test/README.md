# Test
Before entering the `query` folder, we should prepare the required files:

Assuming we have downloaded the VSC22 training and test reference datasets, and stored as follows:

```
cd /data
wget -i https://dl.fbaipublicfiles.com/video_similarity_challenge/46ef53734a4/vsc_url_list.txt \
  --cut-dirs 2 -x -nH
/data/dataset_train/refs
/data/dataset_val/refs
```

Also, we have $4$ models here(They can also be directly downloaded from https://huggingface.co/WenhaoWang/VSC22_trained):

1. ```train_v1_swin_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_1_cls_FIN.pth.tar```

2. ```train_v1_vit_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_1_cls_FIN.pth.tar```

3. ```train_v1_t2t_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_1_cls_FIN.pth.tar```

4. ```train_v1_50SK_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_2_cls_FIN.pth.tar```


Then: 

1. We first transform ```/data/dataset_val/refs``` into images using ```ffmpeg``` by:

```
bash video2images_ref_ff.sh
```
Note we have transformed the ```/data/dataset_train/refs``` into images in the training section.

2. Download the model needed during feature extraction and store them into checkpoints folder by:

```
mkdir pths
cd pths 
cp ../pth.txt ./
wget -i pth.txt \
  --cut-dirs 2 -x -nH
find . -type f -exec cp {} /root/.cache/torch/hub/checkpoints/ \;
```
3. Get the training reference features (normalization features) by:

```
bash swin_train_ref.sh 
bash vit_train_ref.sh 
bash t2t_train_ref.sh 
bash 50SK_train_ref.sh 
```
Finally, by running ```python hdf5_to_npz_train.py```, you can get the training (normalization) reference features (```reference_v1_sort_train.npz```) in each folder.


4. Get the test reference features:

```
bash swin_test_ref.sh 
bash vit_test_ref.sh 
bash t2t_test_ref.sh 
bash 50SK_test_ref.sh
```

Finally, by running ```python hdf5_to_npz_test.py```, you can get the test reference features (```reference_v1_sort_test.npz```) in each folder.

## Copy

After doing this, you should copy the trained models and extracted features (detailed as below) in to the ```query``` folder.
1. ```train_v1_swin_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_1_cls_FIN.pth.tar```

2. ```train_v1_vit_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_1_cls_FIN.pth.tar```

3. ```train_v1_t2t_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_1_cls_FIN.pth.tar```

4. ```train_v1_50SK_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_2_cls_FIN.pth.tar```

5.

```
cp feature/train_v1_swin_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_1_cls_FIN_test/reference_v1_sort_test.npz ./query/feature/train_v1_swin_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_1_cls_FIN/reference_v1_sort_test.npz
cp feature/train_v1_t2t_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_1_cls_FIN_test/reference_v1_sort_test.npz ./query/feature/train_v1_t2t_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_1_cls_FIN/reference_v1_sort_test.npz
cp feature/train_v1_vit_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_1_cls_FIN_test/reference_v1_sort_test.npz ./query/feature/train_v1_vit_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_1_cls_FIN/reference_v1_sort_test.npz
cp feature/train_v1_50SK_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_2_cls_FIN_test/reference_v1_sort_test.npz ./query/feature/train_v1_50SK_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_2_cls_FIN/reference_v1_sort_test.npz


cp feature/train_v1_swin_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_1_cls_FIN/reference_v1_sort_train.npz ./query/feature/train_v1_swin_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_1_cls_FIN/reference_v1_sort_train.npz
cp feature/train_v1_t2t_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_1_cls_FIN/reference_v1_sort_train.npz ./query/feature/train_v1_t2t_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_1_cls_FIN/reference_v1_sort_train.npz
cp feature/train_v1_vit_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_1_cls_FIN/reference_v1_sort_train.npz ./query/feature/train_v1_vit_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_1_cls_FIN/reference_v1_sort_train.npz
cp feature/train_v1_50SK_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_2_cls_FIN/reference_v1_sort_train.npz ./query/feature/train_v1_50SK_s3_512_twolosses_com_L2_norm_100_all_tune_bw_gt_ng_2_cls_FIN/reference_v1_sort_train.npz
```

