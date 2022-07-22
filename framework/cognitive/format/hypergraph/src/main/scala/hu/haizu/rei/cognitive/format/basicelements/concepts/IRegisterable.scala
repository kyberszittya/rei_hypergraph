package hu.haizu.rei.cognitive.format.basicelements.concepts

case class ItemTimestamp(sec: Long, nsec: Long)

trait IRegisterable {
  def getUuid: Array[Byte]
  def getTimestampNSec: BigInt
  def getTime: ItemTimestamp
}

