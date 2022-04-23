import scala.io.Source
import scala.util.{Failure, Success, Using}

object Deformations {
  def main(args: Array[String]): Unit = {
    Using(Source.fromFile("your dict file")) { file =>
      //词典区区几百兆, 何足挂齿
      val lines = file.getLines().mkString("\n")
//      println(s"lines: ${lines}")
      val wordPattern = "</>\n(.+)\n(.*)\n".r

      val all = wordPattern.findAllMatchIn(lines)

     for (pairs <- all) {
       val deformationsP = "i_text\">(\\w+)<".r
       val deformations = deformationsP.findAllMatchIn(pairs.group(2)).map(_.group(1)).toSeq
       if(deformations.nonEmpty){
//         println(pairs.group(1))
//         println(s"deformations: ${deformations}")
         //reversed output
         deformations.foreach {
           w =>
             println(s"$w ${pairs.group(1)}")
         }
       }
     }
    } match {
      case Success(value) =>
      case Failure(exception) => throw exception
    }
  }
}
