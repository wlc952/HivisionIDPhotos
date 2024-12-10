import numpy as np
import cv2
from tpu_perf.infer import SGInfer
from hivision.creator.retinaface.box_utils import decode, decode_landm
from hivision.creator.retinaface.prior_box import PriorBox


def py_cpu_nms(dets, thresh):
    """Pure Python NMS baseline."""
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]
    scores = dets[:, 4]

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter)

        inds = np.where(ovr <= thresh)[0]
        order = order[inds + 1]

    return keep


# 替换掉 argparse 的部分，直接使用普通变量
network = "resnet50"
use_cpu = False
confidence_threshold = 0.8
top_k = 5000
nms_threshold = 0.2
keep_top_k = 750
save_image = True
vis_thres = 0.6


class LoadBmodel:
    def __init__(self, model_path="", batch=1,device_id=0) :
        self.model = SGInfer(model_path , batch=batch, devices=[device_id])
        
    def __call__(self, args):
        if isinstance(args, list):
            values = args
        elif isinstance(args, dict):
            values = list(args.values())
        else:
            raise TypeError("args is not list or dict")
        task_id = self.model.put(*values)
        task_id, results, valid = self.model.get()
        return results


def retinaface_detect_faces_bmodel(image, model_path: str, sess=None):
    cfg = {
        "name": "Resnet50",
        "min_sizes": [[16, 32], [64, 128], [256, 512]],
        "steps": [8, 16, 32],
        "variance": [0.1, 0.2],
        "clip": False,
        "loc_weight": 2.0,
        "gpu_train": True,
        "batch_size": 24,
        "ngpu": 4,
        "epoch": 100,
        "decay1": 70,
        "decay2": 90,
        "image_size": 840,
        "pretrain": True,
        "return_layers": {"layer2": 1, "layer3": 2, "layer4": 3},
        "in_channel": 256,
        "out_channel": 256,
    }

    # Load Bmodel
    if sess is None:
        retinaface = LoadBmodel(model_path)
    else:
        retinaface = sess

    resize = 1

    # Read and preprocess the image
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 保存原始尺寸用于后续还原
    orig_height, orig_width = img_rgb.shape[:2]
    
    # 将图像缩放到512x512
    img_rgb = cv2.resize(img_rgb, (512, 512))
    img = np.float32(img_rgb)

    im_height, im_width, _ = img.shape
    scale = np.array([img.shape[1], img.shape[0], img.shape[1], img.shape[0]])
    img -= (104, 117, 123)
    img = img.transpose(2, 0, 1)
    img = np.expand_dims(img, axis=0)

    # Run the model
    inputs = {"input": img}
    loc, conf, landms = retinaface(inputs)

    priorbox = PriorBox(cfg, image_size=(im_height, im_width))
    priors = priorbox.forward()

    prior_data = priors

    boxes = decode(np.squeeze(loc, axis=0), prior_data, cfg["variance"])
    boxes = boxes * scale / resize
    scores = np.squeeze(conf, axis=0)[:, 1]

    landms = decode_landm(np.squeeze(landms.data, axis=0), prior_data, cfg["variance"])

    scale1 = np.array(
        [
            img.shape[3],
            img.shape[2],
            img.shape[3],
            img.shape[2],
            img.shape[3],
            img.shape[2],
            img.shape[3],
            img.shape[2],
            img.shape[3],
            img.shape[2],
        ]
    )
    landms = landms * scale1 / resize

    # ignore low scores
    inds = np.where(scores > confidence_threshold)[0]
    boxes = boxes[inds]
    landms = landms[inds]
    scores = scores[inds]

    # keep top-K before NMS
    order = scores.argsort()[::-1][:top_k]
    boxes = boxes[order]
    landms = landms[order]
    scores = scores[order]

    # do NMS
    dets = np.hstack((boxes, scores[:, np.newaxis])).astype(np.float32, copy=False)
    keep = py_cpu_nms(dets, nms_threshold)
    dets = dets[keep, :]
    landms = landms[keep]

    # keep top-K faster NMS
    dets = dets[:keep_top_k, :]
    landms = landms[:keep_top_k, :]

    # 将坐标还原到原始图像尺寸
    scale_x = orig_width / 512
    scale_y = orig_height / 512
    
    dets[:, [0,2]] *= scale_x  # x坐标
    dets[:, [1,3]] *= scale_y  # y坐标
    
    landms[:, [0,2,4,6,8]] *= scale_x  # landmarks x坐标
    landms[:, [1,3,5,7,9]] *= scale_y  # landmarks y坐标

    dets = np.concatenate((dets, landms), axis=1)

    # return dets, retinaface
    return dets


if __name__ == "__main__":
    import gradio as gr

    # Create Gradio interface
    iface = gr.Interface(
        fn=retinaface_detect_faces_bmodel,
        inputs=[
            gr.Image(
                type="numpy", label="上传图片", height=400
            ),  # Set the height to 400
            gr.Textbox(value="hivision/creator/retinaface/weights/retinaface-resnet50.bmodel", label="Bmodel模型路径"),
        ],
        outputs=gr.Textbox(label="检测结果"),
        title="人脸检测",
        description="上传图片并提供Bmodel模型路径以检测人脸数量。",
    )

    # Launch the Gradio app
    iface.launch()
