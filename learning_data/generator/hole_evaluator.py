from pypokerengine.engine.card import Card
from pypokerengine.engine.hand_evaluator import HandEvaluator
from learning_data.generator.contribution_checker import ContributionChecker
import random

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
    else:
      value = self.__scale_evaluation_value(value)
    return value, self.__card_to_str(hole), self.__card_to_str(complete_community), detail


  @classmethod
  def __fill_blank_card(self, community_):
    community = [Card.from_id(card.to_id()) for card in community_]  # deep copy
    need_card = 5 - len(community)
    for _ in range(need_card):
      card_id = random.randint(1, 52)
      community.append(Card.from_id(card_id))
    return community

  @classmethod
  def __card_to_str(self, cards):
    return [str(card) for card in cards]

  @classmethod
  def __scale_evaluation_value(self, value):
    return value

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

