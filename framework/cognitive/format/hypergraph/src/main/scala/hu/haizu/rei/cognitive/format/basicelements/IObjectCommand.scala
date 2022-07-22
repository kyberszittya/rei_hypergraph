package hu.haizu.rei.cognitive.format.basicelements

import hu.haizu.rei.cognitive.format.basicelements.concepts.IUniqueIdentifiable

trait IObjectCommand[Target <: ITreeObject[?]] {
  def execute(): IUniqueIdentifiable
  def setTarget(tree: Target): Unit
}
