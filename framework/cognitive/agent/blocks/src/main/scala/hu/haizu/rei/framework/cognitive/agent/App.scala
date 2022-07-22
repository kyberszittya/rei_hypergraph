package hu.haizu.rei.framework.cognitive.agent

import akka.actor.ActorSystem
import akka.actor.{Actor, ActorRef, Props}

class Agent {

}

class OutputActor extends Actor {
  override def receive: Receive = {
    case message =>
      println(message)
  }

}

class AppendActor(outputActor: ActorRef) extends Actor {
  override def receive: Receive = {
    case message: String =>
      val changed = s"Hello, $message"
      outputActor ! changed
    case unknown =>
      println(s"INCONNU $unknown")
  }
}

object HelloWorld extends App {
  val system = ActorSystem("HelloWorld")
  val outputActor = system.actorOf(Props[OutputActor], name = "output")
  val appendActor = system.actorOf(Props(classOf[AppendActor], outputActor), name = "appender")
  appendActor ! "Akka"
  Thread.sleep(500)
  system.terminate()
}