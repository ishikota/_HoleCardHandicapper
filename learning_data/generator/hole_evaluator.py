from pypokerengine.engine.card import Card
from pypokerengine.engine.hand_evaluator import HandEvaluator
from learning_data.generator.contribution_checker import ContributionChecker
from learning_data.generator.round_simulator import RoundSimulator
import random
import math

class HoleEvaluator:

  HAND_MAP = {
      HandEvaluator.HIGHCARD : "HIGH CARD",
      HandEvaluator.ONEPAIR : "ONE PAIR",
      HandEvaluator.TWOPAIR : "TWO PAIR",
      HandEvaluator.THREECARD : "THREE CARD",
      HandEvaluator.STRAIGHT : "STRAIGHT",
      HandEvaluator.FLASH : "FLASH",
      HandEvaluator.FULLHOUSE : "FULLHOUSE",
      HandEvaluator.FOURCARD : "FOUR CARD",
      HandEvaluator.STRAIGHTFLASH : "STRAIGHT FLASH"
  }

  @classmethod
  def eval_hole(self, hole, community=None):
    community = [] if community is None else community
    complete_community = self.__fill_blank_card(community)
    value = HandEvaluator.eval_hand(hole, complete_community)
    detail = self.__analyze_detail(value)
    if not ContributionChecker.check(hole, value):
      value = max([card.rank for card in hole])
      detail = "hand was [%s]. but holecard do not contribute." % detail[0]
    scaled_value = self.__scale_evaluation_value(value)
    return scaled_value, hole[0].to_id(), hole[1].to_id(), self.__analyze_hand(value),\
        self.__card_to_str(hole), self.__card_to_str(complete_community), detail

  @classmethod
  def estimate_win_rate(self, hole, player_num, simulation_num):
    simulation_result = [\
        RoundSimulator.simulation(player_num, hole, self.__fill_blank_card([]))\
        for _ in range(simulation_num)]
    win_count = len([1 for is_win in simulation_result if is_win])
    return 1.0 * win_count / simulation_num

  @classmethod
  def __fill_blank_card(self, community_):
    community = [Card.from_id(card.to_id()) for card in community_]  # deep copy
    need_card = 5 - len(community)
    card_id_range = range(1, 53)
    for card_id in random.sample(card_id_range, need_card):
      community.append(Card.from_id(card_id))
    return community

  @classmethod
  def __card_to_str(self, cards):
    return [str(card) for card in cards]

  @classmethod
  def __scale_evaluation_value(self, value):
    hand = self.__analyze_hand(value)
    high = HandEvaluator._HandEvaluator__high_rank(value)
    low  = HandEvaluator._HandEvaluator__low_rank(value)
    strength = HandEvaluator._HandEvaluator__mask_strength(value) >> 8
    scale = 0 if strength == 0 else math.log(strength, 2) + 1
    return int(scale * 28 + high + low)

  @classmethod
  def __analyze_detail(self, value):
    hand = self.__analyze_hand(value)
    high = HandEvaluator._HandEvaluator__high_rank(value)
    low  = HandEvaluator._HandEvaluator__low_rank(value)
    return hand, high, low

  @classmethod
  def __analyze_hand(self, value):
    flg = HandEvaluator._HandEvaluator__mask_strength(value)
    return self.HAND_MAP[flg]

