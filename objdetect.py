import numpy as np
import os
import pathlib
# import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
import json
utils_ops.tf = tf.compat.v1
tf.gfile = tf.io.gfile

class NumpyEncoder(json.JSONEncoder):
  def default(self, obj):
    import numpy
    if isinstance(obj, numpy.ndarray):
      return {
        "_kind_": "ndarray",
        "_value_": obj.tolist()
      }
    if isinstance(obj, numpy.integer):
      return int(obj)
    elif isinstance(obj, numpy.floating):
      return float(obj)
    elif isinstance(obj,range):
      value = list(obj)
      return {
        "_kind_" : "range",
        "_value_" : [value[0],value[-1]+1]
      }
    return super(NumpyEncoder, self).default(obj)

class NumpyDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        import numpy
        if '_kind_' not in obj:
            return obj
        kind = obj['_kind_']
        if kind == 'ndarray':
            return numpy.array(obj['_value_'])
        elif kind == 'range':
            value = obj['_value_']
            return range(value[0],value[-1])
        return obj


class ObjDetectApi:
  def __init__(self, model_name, path_to_labels):
    self.model = self.load_model(model_name)
    self.category_index = label_map_util.create_category_index_from_labelmap(
                            path_to_labels, use_display_name=True)

  # 모델 로더 
  def load_model(self, model_name):
    base_url = 'http://download.tensorflow.org/models/object_detection/'
    model_file = model_name + '.tar.gz'
    model_dir = tf.keras.utils.get_file(
      fname=model_name, 
      origin=base_url + model_file,
      untar=True)
    model_dir = pathlib.Path(model_dir)/"saved_model"
    print(model_dir)
    model = tf.saved_model.load(str(model_dir))
    return model


  # 이미지에서 객체 검출
  def inference_image(self, image):
    # image = np.asarray(image)

    # 입력은 텐서여야하며 'tf.convert_to_tensor'를 사용하여 변환
    input_tensor = tf.convert_to_tensor(image)

    # 모델은 이미지 배치를 예상하므로 tf.newaxis로 축을 추가
    input_tensor = input_tensor[tf.newaxis,...]

    # 추론 실행
    model_fn = self.model.signatures['serving_default']
    output_dict = model_fn(input_tensor)

    # 모든 출력은 배치 텐서
    # numpy 배열로 변환하고 인덱스 [0]을 사용하여 배치 차원을 제거
    # 우리는 처음 num_detections에만 관심이 있음
    num_detections = int(output_dict.pop('num_detections'))
    output_dict = {key:value[0, :num_detections].numpy() 
                  for key,value in output_dict.items()}
    output_dict['num_detections'] = num_detections
    # detection_classes should be ints.
    output_dict['detection_classes'] = output_dict['detection_classes'
                                           ].astype(np.int64)
    
    # Handle models with masks:
    if 'detection_masks' in output_dict:
      # Reframe the the bbox mask to the image size.
      detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                output_dict['detection_masks'], output_dict['detection_boxes'],
                image.shape[0], image.shape[1])      
      detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5,
                                        tf.uint8)
      output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()
      
    return output_dict

  def inference_file(self, image_path):
    image_np = np.array(Image.open(image_path))
    output_dict = self.inference_image(image_np)

    return image_np, output_dict

  # 검출결과 시각화 
  def visualize(self, image_np, output_dict):
    labeled_image = image_np.copy()
    vis_util.visualize_boxes_and_labels_on_image_array(
        labeled_image,
        output_dict['detection_boxes'],
        output_dict['detection_classes'],
        output_dict['detection_scores'],
        self.category_index,
        instance_masks=output_dict.get('detection_masks_reframed', None),
        use_normalized_coordinates=True,
        line_thickness=8)

    return labeled_image

