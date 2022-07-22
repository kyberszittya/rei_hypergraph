package hu.haizu.rei.cognitive.format.basicelements.concepts

trait IClassifiable {

  def getClusterName: String

  def geClusterId(): Array[Byte]
}
