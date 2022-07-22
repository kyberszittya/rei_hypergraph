package hu.haizu.rei.cognitive.format.basicelements.concepts
import hu.haizu.rei.cognitive.format.identification.IIdentificationStrategy

abstract class UniqueIdentifiableItem[A <: IIdentificationStrategy]
  (val identificationStrategy: A) extends IUniqueIdentifiable {
  val uid: Array[Byte] = generateUid()
  override def getUid: Array[Byte] = uid

  protected def generateIdentificationFragment(): String

  private def generateUid(): Array[Byte] = {
    val idFragment: String = generateIdentificationFragment()
    identificationStrategy.encode(idFragment)
  }


}
