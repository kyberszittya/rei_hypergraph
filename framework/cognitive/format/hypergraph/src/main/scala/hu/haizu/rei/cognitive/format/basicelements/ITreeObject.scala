package hu.haizu.rei.cognitive.format.basicelements

import hu.haizu.rei.cognitive.format.basicelements.concepts.IUniqueIdentifiable

trait ITreeObject[Parent <: IUniqueIdentifiable] extends IUniqueIdentifiable{
  def getParentId: Array[Byte]
  def getParentObj: Parent
  def setParentObj(parent: Parent): Unit
  def setParentId(parent: Parent): Unit
  def expand(): Iterable[ITreeObject[?]]
  def propose(command: IObjectCommand[?]): Unit
}
