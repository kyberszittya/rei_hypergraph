package hu.haizu.rei.cognitive.format.identification

trait IIdentificationStrategy {
  def encode(fragment: String): Array[Byte]

}
