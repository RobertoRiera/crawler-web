# coding=UTF-8
# import os
import sys
import caffe.proto.caffe_pb2

__author__ = 'Javier Lorenzo-Navarro'


def create_net():
    # caffe_dir = '/Descargas/caffe-master/'
    caffe_dir = '/usr/lib/python3/dist-packages/'

    # caffe_root = os.environ['HOME'] + caffe_dir
    caffe_root = caffe_dir

    sys.path.insert(0, caffe_root + 'python')

    model_file = 'GenderHSNet.prototxt'
    weights_file = 'GenderHSNet.caffemodel'
    mean_file = 'GenderHSNet_mean.binaryproto'

    # set gpu mode
    caffe.set_mode_gpu()

    # init the net
    proto_data = open(mean_file, "rb").read()

    a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
    mean_image = caffe.io.blobproto_to_array(a)[0]

    net = caffe.Classifier(model_file, weights_file,
                           mean=mean_image.mean(1).mean(1),
                           channel_swap=(2, 1, 0),
                           raw_scale=255,
                           image_dims=(227, 227)
                           )

    assert isinstance(net, caffe.Classifier)
    return net


def image_gender_classifier(input_image):
    net = create_net()
    image = caffe.io.load_image(input_image)
    prediction = net.predict([image])
    return prediction[0][0], prediction[0][1]

    # input_image = caffe.io.load_image('image002.png')
    # prediction = net.predict([input_image])
    # print '{} -> Female probability: {:.2f} Male probability: {:.2f}\n'.format(os.path.basename("maleProb.txt"),
    #                                                                            prediction[0][0], prediction[0][1])
