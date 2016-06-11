from tests.base_unittest import BaseUnitTest
from pypokerengine.engine.card import Card
from pypokerengine.engine.hand_evaluator import HandEvaluator
from learning_data.generator.contribution_checker import ContributionChecker

class ContributionCheckerTest(BaseUnitTest):

  def test_highcard(self):
    hole = [Card(Card.CLUB, 3), Card(Card.CLUB, 4)]
    val = HandEvaluator.HIGHCARD | (14 << 4) | 4
    self.false(ContributionChecker.check(hole, val))
    val = HandEvaluator.HIGHCARD | (4 << 4) | 2
    self.true(ContributionChecker.check(hole, val))

  def test_onepair(self):
    hole = [Card(Card.CLUB, 3), Card(Card.CLUB, 4)]
    val = HandEvaluator.ONEPAIR| (5 << 4) | 0
    self.false(ContributionChecker.check(hole, val))
    val = HandEvaluator.ONEPAIR | (4 << 4) | 0
    self.true(ContributionChecker.check(hole, val))
    val = HandEvaluator.ONEPAIR | (3 << 4) | 0
    self.true(ContributionChecker.check(hole, val))

  def test_twopair(self):
    hole = [Card(Card.CLUB, 3), Card(Card.CLUB, 4)]
    val = HandEvaluator.TWOPAIR | (14 << 4) | 5
    self.false(ContributionChecker.check(hole, val))
    val = HandEvaluator.TWOPAIR | (14 << 4) | 3
    self.true(ContributionChecker.check(hole, val))
    val = HandEvaluator.TWOPAIR | (3 << 4) | 14
    self.true(ContributionChecker.check(hole, val))

  def test_threecard(self):
    hole = [Card(Card.CLUB, 3), Card(Card.CLUB, 4)]
    val = HandEvaluator.THREECARD | (5 << 4) | 0
    self.false(ContributionChecker.check(hole, val))
    val = HandEvaluator.THREECARD | (3 << 4) | 0
    self.true(ContributionChecker.check(hole, val))
    val = HandEvaluator.THREECARD | (4 << 4) | 0
    self.true(ContributionChecker.check(hole, val))

  def test_straight(self):
    hole = [Card(Card.CLUB, 7), Card(Card.CLUB, 8)]
    val = HandEvaluator.STRAIGHT | (6 << 4) | 0
    self.true(ContributionChecker.check(hole, val))
    val = HandEvaluator.STRAIGHT | (8 << 4) | 0
    self.false(ContributionChecker.check(hole, val))
    val = HandEvaluator.STRAIGHT | (3 << 4) | 0
    self.false(ContributionChecker.check(hole, val))

  def test_flash(self):
    hole = [Card(Card.HEART, 7), Card(Card.CLUB, 8)]
    val = HandEvaluator.FLASH | 0 | 0
    self.false(ContributionChecker.check(hole, val))
    hole = [Card(Card.CLUB, 7), Card(Card.CLUB, 8)]
    self.true(ContributionChecker.check(hole, val))

  def test_fullhouse(self):
    hole = [Card(Card.HEART, 7), Card(Card.CLUB, 8)]
    val = HandEvaluator.FULLHOUSE | (6 << 4) | 3
    self.false(ContributionChecker.check(hole, val))
    val = HandEvaluator.FULLHOUSE | (7 << 4) | 3
    self.true(ContributionChecker.check(hole, val))

  def test_fourcard(self):
    hole = [Card(Card.HEART, 6), Card(Card.CLUB, 7)]
    val = HandEvaluator.FOURCARD | (6 << 4) | 0
    self.false(ContributionChecker.check(hole, val))
    hole = [Card(Card.HEART, 6), Card(Card.CLUB, 6)]
    self.true(ContributionChecker.check(hole, val))

