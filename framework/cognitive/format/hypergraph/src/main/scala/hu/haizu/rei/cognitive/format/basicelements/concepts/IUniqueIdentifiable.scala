package hu.haizu.rei.cognitive.format.basicelements.concepts

import hu.haizu.rei.cognitive.format.identification.IIdentificationStrategy

trait IUniqueIdentifiable {
  def getUid: Array[Byte]
}
