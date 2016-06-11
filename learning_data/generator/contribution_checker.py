from pypokerengine.engine.hand_evaluator import HandEvaluator

class ContributionChecker:

  @classmethod
  def check(self, hole, value):
    hand = HandEvaluator._HandEvaluator__mask_strength(value)
    high = HandEvaluator._HandEvaluator__high_rank(value)
    low  = HandEvaluator._HandEvaluator__low_rank(value)
    if hand == HandEvaluator.HIGHCARD:
      return self.__highcard_check(hole, high, low)
    if hand == HandEvaluator.ONEPAIR:
      return self.__onepair_check(hole, high)
    if hand == HandEvaluator.TWOPAIR:
      return self.__twopair_check(hole, high, low)
    if hand == HandEvaluator.THREECARD:
      return self.__threecard_check(hole, high)
    if hand == HandEvaluator.STRAIGHT:
      return self.__straight_check(hole, high)
    if hand == HandEvaluator.FLASH:
      return self.__flash_check(hole)
    if hand == HandEvaluator.FULLHOUSE:
      return self.__fullhouse_check(hole, high, low)
    if hand == HandEvaluator.FOURCARD:
      return self.__fourcard_check(hole, high)
    if hand == HandEvaluator.STRAIGHTFLASH:
      return self.__straight_check(hole, high)

  # Check if one of hole card matches to the highcard rank
  @classmethod
  def __highcard_check(self, hole, high, low):
    ranks = [card.rank for card in hole]
    return high in ranks

  # Check if one of hole card matches to the onepair rank
  @classmethod
  def __onepair_check(self, hole, high):
    ranks = [card.rank for card in hole]
    return high in ranks

  # Check if one of hole card mathces to the one of twopair ranks
  @classmethod
  def __twopair_check(self, hole, high, low):
    ranks = [card.rank for card in hole]
    return high in ranks or low in ranks

  # Check if one of hole card matches to the three card rank
  @classmethod
  def __threecard_check(self, hole, high):
    ranks = [card.rank for card in hole]
    return high in ranks

  # Check if one of hole card is in the straight cards
  @classmethod
  def __straight_check(self, hole, high):
    ranks = [card.rank for card in hole]
    ans_range = [rank for rank in range(high, high+5)]
    return reduce(lambda acc, r: acc or r in ans_range, ranks, False)

  # Check if suit of both of hole card is the same
  @classmethod
  def __flash_check(self, hole):
    return hole[0].suit == hole[1].suit

  # Check if one of hole card is in the full house ranks
  @classmethod
  def __fullhouse_check(self, hole, high, low):
    ranks = [card.rank for card in hole]
    return high in ranks or low in ranks

  # Check if both of hole card is in the four card ranks
  @classmethod
  def __fourcard_check(self, hole, high):
    ranks = [card.rank for card in hole]
    return reduce(lambda acc, r: acc and r == high, ranks, True)

