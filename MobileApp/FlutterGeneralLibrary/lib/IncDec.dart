

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';

import 'Callback.dart';
import 'LoadingPage.dart';

enum IncDecSizeSpec{
  GivenConstantSizeForButtonsAndTitle,OnThirdOfWidthForEachPiece,EveryPieceAsMuchAsHeight
}

class IncDec extends StatefulWidget
{

  final void Function(int) onValueChangedCallback;

  final double buttonSize;
  final int _count;

  final IncDecSizeSpec sizeSpec;

  final Color activeButtonBorderColor;
  final Color activeButtonFillColor;
  final Color activeButtonTitleColor;

  final Color deActiveButtonBorderColor;
  final Color deActiveButtonFillColor;
  final Color deActiveButtonTitleColor;

  final double borderWidth ;


  IncDec(this._count, this.onValueChangedCallback,
      {
        this.buttonSize = 45,

        this.sizeSpec = IncDecSizeSpec.GivenConstantSizeForButtonsAndTitle ,

        this.borderWidth = 0.4,

        this.activeButtonBorderColor =  Colors.black,
        this.activeButtonFillColor = Colors.grey,
        this.activeButtonTitleColor = Colors.black,

        this.deActiveButtonBorderColor = Colors.black,
        this.deActiveButtonFillColor = Colors.grey,
        this.deActiveButtonTitleColor = Colors.black,
      });


  createState() => IncDecState(_count);
}

class IncDecState extends State<IncDec>
{
  int count;

  IncDecState(this.count);

  build(context)
  {
    return LayoutBuilder(
     builder: (context,b)=>createRow(pieceSize(b.maxWidth,b.maxHeight))
    );
  }


  didUpdateWidget(oldWidget) {
    super.didUpdateWidget(oldWidget);
    count = widget._count;
  }

  createRow(pieceSize)=> Row(
    children: <Widget>[
      createMinusButton(pieceSize),
      Container(width:pieceSize, child: Center(child: Text(count.toString()))),
      createPlusButton(pieceSize)
    ],
  );

  pieceSize(width,height)
  {
    switch(widget.sizeSpec)
    {

      case IncDecSizeSpec.GivenConstantSizeForButtonsAndTitle:
        return widget.buttonSize;
      case IncDecSizeSpec.OnThirdOfWidthForEachPiece:
        return width/3;
      case IncDecSizeSpec.EveryPieceAsMuchAsHeight:
        return height;
    }
  }

  createMinusButton(size) => createButton(size,
      icon: Icons.remove,
      onPressed: ()
      {
        if(count > 0)
        {
          count -= 1;
          setState(() {});
          widget.onValueChangedCallback(count);
        }
      });

  createPlusButton(size) => createButton(size,
      icon: Icons.add,
      onPressed: () {
        count += 1;
        setState(() {});
        widget.onValueChangedCallback(count);
      });

  createButton(size,{IconData? icon, Callback? onPressed}) => Container(
    height: size,
    width: size,
    child: RaisedButton(
      padding: EdgeInsets.all(0),
      onPressed: onPressed,
      color: buttonFillColor(),
      shape: CircleBorder(side: BorderSide(width: widget.borderWidth , color:buttonBorderColor())),
      child: Icon(icon,size:size/2.0,color: buttonContentColor(),),
    ),
  );

  buttonBorderColor() => count >0 ? widget.activeButtonBorderColor : widget.deActiveButtonBorderColor;
  buttonFillColor() => count >0 ? widget.activeButtonFillColor : widget.deActiveButtonFillColor;
  buttonContentColor() => count >0 ? widget.activeButtonTitleColor : widget.deActiveButtonTitleColor;
}