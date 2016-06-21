from keras.utils import np_utils
from pypokerengine.engine.card import Card

class ModelTester:


  def run_popular_test_case(self, model):
    results = ["*** POPULAR TEST CASE ***"]
    for title, cards in self.__gen_popular_test_case():
      card_ids = [card.to_id() for card in cards]
      X = self.__gen_x(*card_ids)
      score = model.predict(X)
      res = "score = %f : %s (%s) " % (score[0][0], [str(card) for card in cards], title)
      results.append(res)
    return "\n".join(results)


  def __gen_x(self, hole_id1, hole_id2):
    return np_utils.to_categorical([hole_id1], 52) + np_utils.to_categorical([hole_id2], 52)


  def __gen_popular_test_case(self):
    return [
        ("bad", [Card(Card.CLUB, 3), Card(Card.CLUB, 4)]),
        ("pocket", [Card(Card.HEART, 12), Card(Card.SPADE, 12)]),
        ("connector", [Card(Card.CLUB, 8), Card(Card.DIAMOND, 9)]),
        ("suited", [Card(Card.DIAMOND, 2), Card(Card.DIAMOND, 13)]),
        ("suited connector", [Card(Card.SPADE, 4), Card(Card.SPADE, 5)]),
        ("gapper", [Card(Card.HEART, 7), Card(Card.SPADE, 9)]),
        ("premier hand", [Card(Card.SPADE, 14), Card(Card.HEART, 14)])
    ]
