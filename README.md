<div align="center">

<img alt="hivision_logo" src="assets/hivision_logo.png" width=120 height=120>
<h1>HivisionIDPhoto TPU</h1>

[![][release-shield]][release-link]
[![][dockerhub-shield]][dockerhub-link]
[![][github-stars-shield]][github-stars-link]
[![][github-issues-shield]][github-issues-link]
[![][github-contributors-shield]][github-contributors-link]
[![][github-forks-shield]][github-forks-link]
[![][license-shield]][license-link]  
[![][wechat-shield]][wechat-link]
[![][spaces-shield]][spaces-link]
[![][swanhub-demo-shield]][swanhub-demo-link]
[![][modelscope-shield]][modelscope-link]
[![][modelers-shield]][modelers-link]

[![][trendshift-shield]][trendshift-link]
[![][hellogithub-shield]][hellogithub-link]

<img src="assets/demoImage.jpg" width=900>

</div>


<br>

# 🔧 准备工作

环境安装与依赖：
- Python >= 3.7（项目主要测试在 python 3.10）
- OS: Linux, Windows, MacOS

## 1. 克隆项目

```bash
git clone https://github.com/wlc952/HivisionIDPhotos.git
cd  HivisionIDPhotos
```

## 2. 安装依赖环境

> 建议 venv 创建一个 python 虚拟环境后，执行以下命令

```bash
bash prepare.sh
```

## 3. 下载人像抠图模型权重文件

```bash
bash download.sh
```

## 4. BMCV加速（可选）

```bash
pip uninstall opencv-python
cp /opt/sophon/sophon-opencv-latest/opencv-python/cv2.so your_venv_path/lib/python3.8/site-packages
```

<br>

# ⚡️ 运行 Gradio Demo

```bash
python app.py
```

运行程序将生成一个本地 Web 页面，在页面中可完成证件照的操作与交互。

<img src="assets/harry.png" width=900>

<br>

# 🚀 Python 推理

核心参数：

- `-i`: 输入图像路径
- `-o`: 保存图像路径
- `-t`: 推理类型，有idphoto、human_matting、add_background、generate_layout_photos可选
- `--matting_model`: 人像抠图模型权重选择
- `--face_detect_model`: 人脸检测模型选择

更多参数可通过`python inference.py --help`查看

## 1. 证件照制作

输入 1 张照片，获得 1 张标准证件照和 1 张高清证件照的 4 通道透明 png

```python
python inference.py -i demo/images/test0.jpg -o ./idphoto.png --height 413 --width 295
```

## 2. 人像抠图

输入 1 张照片，获得 1张 4 通道透明 png

```python
python inference.py -t human_matting -i demo/images/test0.jpg -o ./idphoto_matting.png --matting_model hivision_modnet
```

## 3. 透明图增加底色

输入 1 张 4 通道透明 png，获得 1 张增加了底色的 3通道图像

```python
python inference.py -t add_background -i ./idphoto.png -o ./idphoto_ab.jpg  -c 4f83ce -k 30 -r 1
```

## 4. 得到六寸排版照

输入 1 张 3 通道照片，获得 1 张六寸排版照

```python
python inference.py -t generate_layout_photos -i ./idphoto_ab.jpg -o ./idphoto_layout.jpg  --height 413 --width 295 -k 200
```

## 5. 证件照裁剪

输入 1 张 4 通道照片（抠图好的图像），获得 1 张标准证件照和 1 张高清证件照的 4 通道透明 png

```python
python inference.py -t idphoto_crop -i ./idphoto_matting.png -o ./idphoto_crop.png --height 413 --width 295
```


<br>

# ⚡️ 部署 API 服务

## 启动后端

```
python deploy_api.py
```

## 请求 API 服务

详细请求方式请参考 [API 文档](docs/api_CN.md)，包含以下请求示例：
- [cURL](docs/api_CN.md#curl-请求示例)
- [Python](docs/api_CN.md#python-请求示例)

<br>


# FAQ

## 1. 如何修改预设尺寸和颜色？

- 尺寸：修改[size_list_CN.csv](demo/assets/size_list_CN.csv)后再次运行 `app.py` 即可，其中第一列为尺寸名，第二列为高度，第三列为宽度。
- 颜色：修改[color_list_CN.csv](demo/assets/color_list_CN.csv)后再次运行 `app.py` 即可，其中第一列为颜色名，第二列为Hex值。

## 2. 如何修改水印字体？

1. 将字体文件放到`hivision/plugin/font`文件夹下
2. 修改`hivision/plugin/watermark.py`的`font_file`参数值为字体文件名

## 3. 如何添加社交媒体模板照？

1. 将模板图片放到`hivision/plugin/template/assets`文件夹下。模板图片是一个4通道的透明png。
2. 在`hivision/plugin/template/assets/template_config.json`文件中添加最新的模板信息，其中`width`为模板图宽度(px)，`height`为模板图高度(px)，`anchor_points`为模板中透明区域的四个角的坐标(px)；`rotation`为透明区域相对于垂直方向的旋转角度，>0为逆时针，<0为顺时针。
3. 在`demo/processor.py`的`_generate_image_template`函数中的`TEMPLATE_NAME_LIST`变量添加最新的模板名

<img src="assets/social_template.png" width="500">

## 4. 如何修改Gradio Demo的顶部导航栏？

- 修改`demo/assets/title.md`

<br>

# 📧 联系我们

如果您有任何问题，请发邮件至 zeyi.lin@swanhub.co

<br>

# 🙏 感谢支持

[![Stargazers repo roster for @Zeyi-Lin/HivisionIDPhotos](https://reporoster.com/stars/Zeyi-Lin/HivisionIDPhotos)](https://github.com/Zeyi-Lin/HivisionIDPhotos/stargazers)

[![Forkers repo roster for @Zeyi-Lin/HivisionIDPhotos](https://reporoster.com/forks/Zeyi-Lin/HivisionIDPhotos)](https://github.com/Zeyi-Lin/HivisionIDPhotos/network/members)

[![Star History Chart](https://api.star-history.com/svg?repos=Zeyi-Lin/HivisionIDPhotos&type=Date)](https://star-history.com/#Zeyi-Lin/HivisionIDPhotos&Date)

贡献者们：

<a href="https://github.com/Zeyi-Lin/HivisionIDPhotos/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Zeyi-Lin/HivisionIDPhotos" />
</a>

[Zeyi-Lin](https://github.com/Zeyi-Lin)、[SAKURA-CAT](https://github.com/SAKURA-CAT)、[Feudalman](https://github.com/Feudalman)、[swpfY](https://github.com/swpfY)、[Kaikaikaifang](https://github.com/Kaikaikaifang)、[ShaohonChen](https://github.com/ShaohonChen)、[KashiwaByte](https://github.com/KashiwaByte)

<br>

# 📜 Lincese

This repository is licensed under the [Apache-2.0 License](LICENSE).

<br>

# 📚 引用

如果您在研究或项目中使用了HivisionIDPhotos，请考虑引用我们的工作。您可以使用以下BibTeX条目：

```bibtex
@misc{hivisionidphotos,
      title={{HivisionIDPhotos: A Lightweight and Efficient AI ID Photos Tool}},
      author={Zeyi Lin and SwanLab Team},
      year={2024},
      publisher={GitHub},
      url = {\url{https://github.com/Zeyi-Lin/HivisionIDPhotos}},
}
```




[github-stars-shield]: https://img.shields.io/github/stars/zeyi-lin/hivisionidphotos?color=ffcb47&labelColor=black&style=flat-square
[github-stars-link]: https://github.com/zeyi-lin/hivisionidphotos/stargazers

[swanhub-demo-shield]: https://swanhub.co/git/repo/SwanHub%2FAuto-README/file/preview?ref=main&path=swanhub.svg
[swanhub-demo-link]: https://swanhub.co/ZeYiLin/HivisionIDPhotos/demo

[spaces-shield]: https://img.shields.io/badge/🤗-Open%20in%20Spaces-blue
[spaces-link]: https://huggingface.co/spaces/TheEeeeLin/HivisionIDPhotos

<!-- 微信群链接 -->
[wechat-shield]: https://img.shields.io/badge/WeChat-微信-4cb55e
[wechat-link]: https://docs.qq.com/doc/DUkpBdk90eWZFS2JW

<!-- Github Release -->
[release-shield]: https://img.shields.io/github/v/release/zeyi-lin/hivisionidphotos?color=369eff&labelColor=black&logo=github&style=flat-square
[release-link]: https://github.com/zeyi-lin/hivisionidphotos/releases

[license-shield]: https://img.shields.io/badge/license-apache%202.0-white?labelColor=black&style=flat-square
[license-link]: https://github.com/Zeyi-Lin/HivisionIDPhotos/blob/master/LICENSE

[github-issues-shield]: https://img.shields.io/github/issues/zeyi-lin/hivisionidphotos?color=ff80eb&labelColor=black&style=flat-square
[github-issues-link]: https://github.com/zeyi-lin/hivisionidphotos/issues

[dockerhub-shield]: https://img.shields.io/docker/v/linzeyi/hivision_idphotos?color=369eff&label=docker&labelColor=black&logoColor=white&style=flat-square
[dockerhub-link]: https://hub.docker.com/r/linzeyi/hivision_idphotos/tags

[trendshift-shield]: https://trendshift.io/api/badge/repositories/11622
[trendshift-link]: https://trendshift.io/repositories/11622

[hellogithub-shield]: https://abroad.hellogithub.com/v1/widgets/recommend.svg?rid=8ea1457289fb4062ba661e5299e733d6&claim_uid=Oh5UaGjfrblg0yZ
[hellogithub-link]: https://hellogithub.com/repository/8ea1457289fb4062ba661e5299e733d6

[github-contributors-shield]: https://img.shields.io/github/contributors/zeyi-lin/hivisionidphotos?color=c4f042&labelColor=black&style=flat-square
[github-contributors-link]: https://github.com/zeyi-lin/hivisionidphotos/graphs/contributors

[github-forks-shield]: https://img.shields.io/github/forks/zeyi-lin/hivisionidphotos?color=8ae8ff&labelColor=black&style=flat-square
[github-forks-link]: https://github.com/zeyi-lin/hivisionidphotos/network/members

[modelscope-shield]: https://img.shields.io/badge/Demo_on_ModelScope-purple?logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjIzIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KCiA8Zz4KICA8dGl0bGU+TGF5ZXIgMTwvdGl0bGU+CiAgPHBhdGggaWQ9InN2Z18xNCIgZmlsbD0iIzYyNGFmZiIgZD0ibTAsODkuODRsMjUuNjUsMGwwLDI1LjY0OTk5bC0yNS42NSwwbDAsLTI1LjY0OTk5eiIvPgogIDxwYXRoIGlkPSJzdmdfMTUiIGZpbGw9IiM2MjRhZmYiIGQ9Im05OS4xNCwxMTUuNDlsMjUuNjUsMGwwLDI1LjY1bC0yNS42NSwwbDAsLTI1LjY1eiIvPgogIDxwYXRoIGlkPSJzdmdfMTYiIGZpbGw9IiM2MjRhZmYiIGQ9Im0xNzYuMDksMTQxLjE0bC0yNS42NDk5OSwwbDAsMjIuMTlsNDcuODQsMGwwLC00Ny44NGwtMjIuMTksMGwwLDI1LjY1eiIvPgogIDxwYXRoIGlkPSJzdmdfMTciIGZpbGw9IiMzNmNmZDEiIGQ9Im0xMjQuNzksODkuODRsMjUuNjUsMGwwLDI1LjY0OTk5bC0yNS42NSwwbDAsLTI1LjY0OTk5eiIvPgogIDxwYXRoIGlkPSJzdmdfMTgiIGZpbGw9IiMzNmNmZDEiIGQ9Im0wLDY0LjE5bDI1LjY1LDBsMCwyNS42NWwtMjUuNjUsMGwwLC0yNS42NXoiLz4KICA8cGF0aCBpZD0ic3ZnXzE5IiBmaWxsPSIjNjI0YWZmIiBkPSJtMTk4LjI4LDg5Ljg0bDI1LjY0OTk5LDBsMCwyNS42NDk5OWwtMjUuNjQ5OTksMGwwLC0yNS42NDk5OXoiLz4KICA8cGF0aCBpZD0ic3ZnXzIwIiBmaWxsPSIjMzZjZmQxIiBkPSJtMTk4LjI4LDY0LjE5bDI1LjY0OTk5LDBsMCwyNS42NWwtMjUuNjQ5OTksMGwwLC0yNS42NXoiLz4KICA8cGF0aCBpZD0ic3ZnXzIxIiBmaWxsPSIjNjI0YWZmIiBkPSJtMTUwLjQ0LDQybDAsMjIuMTlsMjUuNjQ5OTksMGwwLDI1LjY1bDIyLjE5LDBsMCwtNDcuODRsLTQ3Ljg0LDB6Ii8+CiAgPHBhdGggaWQ9InN2Z18yMiIgZmlsbD0iIzM2Y2ZkMSIgZD0ibTczLjQ5LDg5Ljg0bDI1LjY1LDBsMCwyNS42NDk5OWwtMjUuNjUsMGwwLC0yNS42NDk5OXoiLz4KICA8cGF0aCBpZD0ic3ZnXzIzIiBmaWxsPSIjNjI0YWZmIiBkPSJtNDcuODQsNjQuMTlsMjUuNjUsMGwwLC0yMi4xOWwtNDcuODQsMGwwLDQ3Ljg0bDIyLjE5LDBsMCwtMjUuNjV6Ii8+CiAgPHBhdGggaWQ9InN2Z18yNCIgZmlsbD0iIzYyNGFmZiIgZD0ibTQ3Ljg0LDExNS40OWwtMjIuMTksMGwwLDQ3Ljg0bDQ3Ljg0LDBsMCwtMjIuMTlsLTI1LjY1LDBsMCwtMjUuNjV6Ii8+CiA8L2c+Cjwvc3ZnPg==&labelColor=white
[modelscope-link]: https://modelscope.cn/studios/SwanLab/HivisionIDPhotos

[modelers-shield]: https://img.shields.io/badge/Demo_on_Modelers-c42a2a?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAxMjQgNjQiIGZpbGw9Im5vbmUiPgo8cGF0aCBkPSJNNDIuNzc4MyAwSDI2LjU5NzdWMTUuNzc4N0g0Mi43NzgzVjBaIiBmaWxsPSIjREUwNDI5Ii8+CjxwYXRoIGQ9Ik0xNi41MDg4IDQuMTc5MkgwLjMyODEyNVYxOS45NTc5SDE2LjUwODhWNC4xNzkyWiIgZmlsbD0iIzI0NDk5QyIvPgo8cGF0aCBkPSJNMTIzLjk1MiA0LjE3OTJIMTA3Ljc3MVYxOS45NTc5SDEyMy45NTJWNC4xNzkyWiIgZmlsbD0iIzI0NDk5QyIvPgo8cGF0aCBkPSJNMTYuNTA4OCA0NS40NjE5SDAuMzI4MTI1VjYxLjI0MDZIMTYuNTA4OFY0NS40NjE5WiIgZmlsbD0iIzI0NDk5QyIvPgo8cGF0aCBkPSJNMTIzLjk1MiA0NS40NjE5SDEwNy43NzFWNjEuMjQwNkgxMjMuOTUyVjQ1LjQ2MTlaIiBmaWxsPSIjMjQ0OTlDIi8+CjxwYXRoIGQ9Ik0zMi43MDggMTUuNzc4OEgxNi41MjczVjMxLjU1NzVIMzIuNzA4VjE1Ljc3ODhaIiBmaWxsPSIjREUwNDI5Ii8+CjxwYXRoIGQ9Ik01Mi44NDg2IDE1Ljc3ODhIMzYuNjY4VjMxLjU1NzVINTIuODQ4NlYxNS43Nzg4WiIgZmlsbD0iI0RFMDQyOSIvPgo8cGF0aCBkPSJNOTcuNzIzNyAwSDgxLjU0M1YxNS43Nzg3SDk3LjcyMzdWMFoiIGZpbGw9IiNERTA0MjkiLz4KPHBhdGggZD0iTTg3LjY1MzQgMTUuNzc4OEg3MS40NzI3VjMxLjU1NzVIODcuNjUzNFYxNS43Nzg4WiIgZmlsbD0iI0RFMDQyOSIvPgo8cGF0aCBkPSJNMTA3Ljc5NCAxNS43Nzg4SDkxLjYxMzNWMzEuNTU3NUgxMDcuNzk0VjE1Ljc3ODhaIiBmaWxsPSIjREUwNDI5Ii8+CjxwYXRoIGQ9Ik0yNC42NzQ4IDMxLjU1NzZIOC40OTQxNFY0Ny4zMzYzSDI0LjY3NDhWMzEuNTU3NloiIGZpbGw9IiNERTA0MjkiLz4KPHBhdGggZD0iTTYwLjg3OTkgMzEuNTU3Nkg0NC42OTkyVjQ3LjMzNjNINjAuODc5OVYzMS41NTc2WiIgZmlsbD0iI0RFMDQyOSIvPgo8cGF0aCBkPSJNNzkuNjIwMSAzMS41NTc2SDYzLjQzOTVWNDcuMzM2M0g3OS42MjAxVjMxLjU1NzZaIiBmaWxsPSIjREUwNDI5Ii8+CjxwYXRoIGQ9Ik0xMTUuODI1IDMxLjU1NzZIOTkuNjQ0NVY0Ny4zMzYzSDExNS44MjVWMzEuNTU3NloiIGZpbGw9IiNERTA0MjkiLz4KPHBhdGggZD0iTTcwLjI1NDkgNDcuMzM1OUg1NC4wNzQyVjYzLjExNDdINzAuMjU0OVY0Ny4zMzU5WiIgZmlsbD0iI0RFMDQyOSIvPgo8L3N2Zz4=&labelColor=white
[modelers-link]: https://modelers.cn/spaces/SwanLab/HivisionIDPhotos



<!-- 社区项目链接 -->
[community-hivision-comfyui]: https://github.com/AIFSH/HivisionIDPhotos-ComfyUI
[community-hivision-wechat]: https://github.com/no1xuan/HivisionIDPhotos-wechat-weapp
[community-hivision-uniapp]: https://github.com/soulerror/HivisionIDPhotos-Uniapp
[community-hivision-cpp]: https://github.com/zjkhahah/HivisionIDPhotos-cpp
[community-hivision-windows-gui]: https://github.com/zhaoyun0071/HivisionIDPhotos-windows-GUI
[community-hivision-nas]: https://github.com/ONG-Leo/HivisionIDPhotos-NAS