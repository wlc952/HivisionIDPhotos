import onnx
from onnx import helper, shape_inference

def convert_dynamic_to_static_onnx(input_model_path, output_model_path, static_shape):
    # 加载动态 ONNX 模型
    model = onnx.load(input_model_path)

    # 获取模型的图
    graph = model.graph

    # 修改输入的形状
    for input_tensor in graph.input:
        input_tensor.type.tensor_type.shape.dim[0].dim_value = static_shape[0]
        input_tensor.type.tensor_type.shape.dim[1].dim_value = static_shape[1]
        input_tensor.type.tensor_type.shape.dim[2].dim_value = static_shape[2]
        input_tensor.type.tensor_type.shape.dim[3].dim_value = static_shape[3]

    # 推断形状
    model = shape_inference.infer_shapes(model)

    # 保存静态 ONNX 模型
    onnx.save(model, output_model_path)
    onnx.checker.check_model(output_model_path)

# 示例用法
rmbg_input_model_path = "hivision/creator/weights/rmbg-1.4_d.onnx"
rmbg_output_model_path = "hivision/creator/weights/rmbg-1.4.onnx"
rmbg_static_shape = [1, 3, 1024, 1024]

retinaface_input_model_path = "hivision/creator/retinaface/weights/retinaface-resnet50_d.onnx"
retinaface_output_model_path = "hivision/creator/retinaface/weights/retinaface-resnet50.onnx"
retinaface_static_shape = [1, 3, 512, 512]

convert_dynamic_to_static_onnx(rmbg_input_model_path, rmbg_output_model_path, rmbg_static_shape)
convert_dynamic_to_static_onnx(retinaface_input_model_path, retinaface_output_model_path, retinaface_static_shape)
