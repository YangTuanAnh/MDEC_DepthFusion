# Ensemble-based Monocular Depth Estimation with Diffusion and Transformer Fusion via Felzenszwalb-Guided Refinement

## Methodology

### 1. Problem Formulation

Given an RGB image $I \in \mathbb{R}^{H \times W \times 3}$, we generate:
- $D_m$: Depth map predicted by **Marigold**
- $D_d$: Depth map predicted by **Depth Anything V2**, converted from disparity to affine-invariant depth

### 2. Felzenszwalb Segmentation

We apply Felzenszwalb’s graph-based segmentation algorithm to partition the image into consistent regions:

```math
S = \text{Felzenszwalb}(I, \text{scale}=200, \sigma=0.8, \text{min\_size}=50)
````

Each unique value in $S \in \mathbb{Z}^{H \times W}$ represents a segment.

### 3. Segment-Based Feature Extraction

For each segment $P_i$, we extract:

* Mean depth $\mu_i$
* Depth variance $\sigma^2_i$
* Confidence $c_i = \frac{1}{\sigma_i + \epsilon}$, with $\epsilon = 10^{-9}$

These are computed for both depth maps $D_m$ and $D_d$, yielding:

* $F^m_i = \{\mu^m_i, (\sigma^m_i)^2, c^m_i\}$
* $F^d_i = \{\mu^d_i, (\sigma^d_i)^2, c^d_i\}$

### 3. Adaptive Depth Fusion

For each segment $P_i$, we compute the confidence ratio:

```math
R = \frac{c^d_i}{c^m_i + \epsilon}
```

We then apply the following rules:

* If the segment is flat ($\mu_i \approx 1.0$, $\sigma^2_i < 0.001$), set output depth to 1.0
* Else, if $R > T$ (with $T = 1.2$), use Depth Anything V2
* Otherwise, use Marigold

This ensures that the fusion respects regions of high confidence and selectively incorporates information from Depth Anything V2 where it clearly outperforms Marigold.

## Citation

```
@misc{obukhov2025fourthmonoculardepthestimation,
      title={The Fourth Monocular Depth Estimation Challenge}, 
      author={Anton Obukhov and Matteo Poggi and Fabio Tosi and Ripudaman Singh Arora and Jaime Spencer and Chris Russell and Simon Hadfield and Richard Bowden and Shuaihang Wang and Zhenxin Ma and Weijie Chen and Baobei Xu and Fengyu Sun and Di Xie and Jiang Zhu and Mykola Lavreniuk and Haining Guan and Qun Wu and Yupei Zeng and Chao Lu and Huanran Wang and Guangyuan Zhou and Haotian Zhang and Jianxiong Wang and Qiang Rao and Chunjie Wang and Xiao Liu and Zhiqiang Lou and Hualie Jiang and Yihao Chen and Rui Xu and Minglang Tan and Zihan Qin and Yifan Mao and Jiayang Liu and Jialei Xu and Yifan Yang and Wenbo Zhao and Junjun Jiang and Xianming Liu and Mingshuai Zhao and Anlong Ming and Wu Chen and Feng Xue and Mengying Yu and Shida Gao and Xiangfeng Wang and Gbenga Omotara and Ramy Farag and Jacket Demby and Seyed Mohamad Ali Tousi and Guilherme N DeSouza and Tuan-Anh Yang and Minh-Quang Nguyen and Thien-Phuc Tran and Albert Luginov and Muhammad Shahzad},
      year={2025},
      eprint={2504.17787},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2504.17787}, 
}
```
