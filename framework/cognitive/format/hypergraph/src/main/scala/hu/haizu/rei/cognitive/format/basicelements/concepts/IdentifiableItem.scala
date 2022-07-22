package hu.haizu.rei.cognitive.format.basicelements.concepts

abstract class IdentifiableItem(val name: String) extends IIdentifiable {
  var qualifiedName: String = constructQualifiedName()


  override def getName: String = name

  override def getQualifiedName: String = qualifiedName

  protected def constructQualifiedName(): String

  protected def refreshIdentification() = {
    qualifiedName = constructQualifiedName()
  }
}
