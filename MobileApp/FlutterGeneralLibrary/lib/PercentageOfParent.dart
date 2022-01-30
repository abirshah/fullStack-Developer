import 'package:flutter/cupertino.dart';



class PercentageOfParent extends StatelessWidget
{
  final Widget child;
  final double widthRatio;
  final double heightRatio;
  final double xRatio;
  final double yRatio;

  PercentageOfParent({required this.child, this.widthRatio = 1, this.heightRatio = 1 , this.xRatio = 0,this.yRatio= 0,});


  build(context){
    return LayoutBuilder(builder: (context, box){
      if(box.maxHeight == double.infinity )
        throw Exception("WTF?!?!?");

      return Container(
        width: box.maxWidth,
        height: box.maxHeight ,
        child: Stack(

          children: <Widget>[
            Positioned(
              left: xRatio *box.maxWidth ,
              top: yRatio * box.maxHeight,
              width: box.maxWidth * widthRatio,
              height: box.maxHeight * heightRatio,
              child: child,
            ),
          ],
        ),
      );
    },);
  }
}


