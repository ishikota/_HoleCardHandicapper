from tests.base_unittest import BaseUnitTest
from pypokerengine.engine.hand_evaluator import HandEvaluator
from learning_data.generator.hole_evaluator import HoleEvaluator

class ScalingTest(BaseUnitTest):

  def test_highcard(self):
    val = HandEvaluator.HIGHCARD | (14 << 4) | 4
    self.eq(18, HoleEvaluator._HoleEvaluator__scale_evaluation_value(val))
    val = HandEvaluator.HIGHCARD | (4 << 4) | 2
    self.eq(6, HoleEvaluator._HoleEvaluator__scale_evaluation_value(val))

  def test_onepair(self):
    val = HandEvaluator.ONEPAIR| (5 << 4) | 0
    self.eq(5 + 28, HoleEvaluator._HoleEvaluator__scale_evaluation_value(val))
    val = HandEvaluator.ONEPAIR | (4 << 4) | 0
    self.eq(4 + 28, HoleEvaluator._HoleEvaluator__scale_evaluation_value(val))
    val = HandEvaluator.ONEPAIR | (3 << 4) | 0
    self.eq(3 + 28, HoleEvaluator._HoleEvaluator__scale_evaluation_value(val))

  def test_twopair(self):
    val = HandEvaluator.TWOPAIR | (14 << 4) | 5
    self.eq(14+5 + 28*2, HoleEvaluator._HoleEvaluator__scale_evaluation_value(val))
    val = HandEvaluator.TWOPAIR | (14 << 4) | 3
    self.eq(14+3 + 28*2, HoleEvaluator._HoleEvaluator__scale_evaluation_value(val))
    val = HandEvaluator.TWOPAIR | (3 << 4) | 14
    self.eq(3+14 + 28*2, HoleEvaluator._HoleEvaluator__scale_evaluation_value(val))

  def test_threecard(self):
    val = HandEvaluator.THREECARD | (5 << 4) | 0
    self.eq(5 + 28*3, HoleEvaluator._HoleEvaluator__scale_evaluation_value(val))
    val = HandEvaluator.THREECARD | (3 << 4) | 0
    self.eq(3 + 28*3, HoleEvaluator._HoleEvaluator__scale_evaluation_value(val))
    val = HandEvaluator.THREECARD | (4 << 4) | 0
    self.eq(4 + 28*3, HoleEvaluator._HoleEvaluator__scale_evaluation_value(val))

  def test_straight(self):
    val = HandEvaluator.STRAIGHT | (6 << 4) | 0
    self.eq(6 + 28*4, HoleEvaluator._HoleEvaluator__scale_evaluation_value(val))
    val = HandEvaluator.STRAIGHT | (8 << 4) | 0
    self.eq(8 + 28*4, HoleEvaluator._HoleEvaluator__scale_evaluation_value(val))
    val = HandEvaluator.STRAIGHT | (3 << 4) | 0
    self.eq(3 + 28*4, HoleEvaluator._HoleEvaluator__scale_evaluation_value(val))

  def test_flash(self):
    val = HandEvaluator.FLASH | 0 | 0
    self.eq(0 + 28*5, HoleEvaluator._HoleEvaluator__scale_evaluation_value(val))

  def test_fullhouse(self):
    val = HandEvaluator.FULLHOUSE | (6 << 4) | 3
    self.eq(6+3 + 28*6, HoleEvaluator._HoleEvaluator__scale_evaluation_value(val))
    val = HandEvaluator.FULLHOUSE | (7 << 4) | 3
    self.eq(7+3 + 28*6, HoleEvaluator._HoleEvaluator__scale_evaluation_value(val))

  def test_fourcard(self):
    val = HandEvaluator.FOURCARD | (6 << 4) | 0
    self.eq(6 + 28*7, HoleEvaluator._HoleEvaluator__scale_evaluation_value(val))

