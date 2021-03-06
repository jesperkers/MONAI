# Copyright 2020 MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import torch
from parameterized import parameterized

from monai.networks.blocks import FCN, MCFCN
from monai.networks.nets import AHNet

TEST_CASE_FCN_1 = [{"out_channels": 3, "upsample_mode": "transpose"}, torch.randn(5, 3, 64, 64), (5, 3, 64, 64)]
TEST_CASE_FCN_2 = [{"out_channels": 2, "upsample_mode": "transpose"}, torch.randn(5, 3, 64, 64), (5, 2, 64, 64)]
TEST_CASE_FCN_3 = [{"out_channels": 1, "upsample_mode": "bilinear"}, torch.randn(5, 3, 64, 64), (5, 1, 64, 64)]

TEST_CASE_MCFCN_1 = [
    {"out_channels": 3, "in_channels": 8, "upsample_mode": "transpose"},
    torch.randn(5, 8, 64, 64),
    (5, 3, 64, 64),
]
TEST_CASE_MCFCN_2 = [
    {"out_channels": 2, "in_channels": 1, "upsample_mode": "transpose"},
    torch.randn(5, 1, 64, 64),
    (5, 2, 64, 64),
]
TEST_CASE_MCFCN_3 = [
    {"out_channels": 1, "in_channels": 2, "upsample_mode": "bilinear"},
    torch.randn(5, 2, 64, 64),
    (5, 1, 64, 64),
]

TEST_CASE_AHNET_2D_1 = [
    {"spatial_dims": 2, "upsample_mode": "bilinear"},
    torch.randn(3, 1, 128, 128),
    (3, 1, 128, 128),
]
TEST_CASE_AHNET_2D_2 = [
    {"spatial_dims": 2, "upsample_mode": "transpose", "out_channels": 2},
    torch.randn(2, 1, 128, 128),
    (2, 2, 128, 128),
]
TEST_CASE_AHNET_3D_1 = [
    {"spatial_dims": 3, "upsample_mode": "trilinear"},
    torch.randn(3, 1, 128, 128, 64),
    (3, 1, 128, 128, 64),
]
TEST_CASE_AHNET_3D_2 = [
    {"spatial_dims": 3, "upsample_mode": "transpose", "out_channels": 2},
    torch.randn(2, 1, 128, 128, 64),
    (2, 2, 128, 128, 64),
]
TEST_CASE_AHNET_3D_WITH_PRETRAIN_1 = [
    {"spatial_dims": 3, "upsample_mode": "trilinear"},
    torch.randn(3, 1, 128, 128, 64),
    (3, 1, 128, 128, 64),
    {"out_channels": 1, "upsample_mode": "transpose"},
]
TEST_CASE_AHNET_3D_WITH_PRETRAIN_2 = [
    {"spatial_dims": 3, "upsample_mode": "transpose", "out_channels": 2},
    torch.randn(2, 1, 128, 128, 64),
    (2, 2, 128, 128, 64),
    {"out_channels": 1, "upsample_mode": "bilinear"},
]


class TestFCN(unittest.TestCase):
    @parameterized.expand([TEST_CASE_FCN_1, TEST_CASE_FCN_2, TEST_CASE_FCN_3])
    def test_fcn_shape(self, input_param, input_data, expected_shape):
        net = FCN(**input_param)
        net.eval()
        with torch.no_grad():
            result = net.forward(input_data)
            self.assertEqual(result.shape, expected_shape)


class TestMCFCN(unittest.TestCase):
    @parameterized.expand([TEST_CASE_MCFCN_1, TEST_CASE_MCFCN_2, TEST_CASE_MCFCN_3])
    def test_mcfcn_shape(self, input_param, input_data, expected_shape):
        net = MCFCN(**input_param)
        net.eval()
        with torch.no_grad():
            result = net.forward(input_data)
            self.assertEqual(result.shape, expected_shape)


class TestAHNET(unittest.TestCase):
    @parameterized.expand([TEST_CASE_AHNET_2D_1, TEST_CASE_AHNET_2D_2, TEST_CASE_AHNET_3D_1, TEST_CASE_AHNET_3D_2])
    def test_ahnet_shape(self, input_param, input_data, expected_shape):
        net = AHNet(**input_param)
        net.eval()
        with torch.no_grad():
            result = net.forward(input_data)
            self.assertEqual(result.shape, expected_shape)


class TestAHNETWithPretrain(unittest.TestCase):
    @parameterized.expand([TEST_CASE_AHNET_3D_WITH_PRETRAIN_1, TEST_CASE_AHNET_3D_WITH_PRETRAIN_2])
    def test_ahnet_shape(self, input_param, input_data, expected_shape, fcn_input_param):
        net = AHNet(**input_param)
        net2d = FCN(**fcn_input_param)
        net.copy_from(net2d)
        net.eval()
        with torch.no_grad():
            result = net.forward(input_data)
            self.assertEqual(result.shape, expected_shape)


if __name__ == "__main__":
    unittest.main()
