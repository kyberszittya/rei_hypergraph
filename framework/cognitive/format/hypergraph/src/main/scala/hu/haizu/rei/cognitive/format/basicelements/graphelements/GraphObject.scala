package hu.haizu.rei.cognitive.format.basicelements.graphelements

import hu.haizu.rei.cognitive.format.basicelements.ITreeObject
import hu.haizu.rei.cognitive.format.basicelements.concepts.IUniqueIdentifiable

abstract class GraphObject[Parent <: IUniqueIdentifiable](parent: Parent = null) extends ITreeObject[Parent] {
  var parentId: Array[Byte]

}
