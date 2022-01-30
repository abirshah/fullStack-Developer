import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_general/Utils.dart';



createRoundedCornerRaisedButton(String title,
        {EdgeInsetsGeometry padding = EdgeInsets.zero,
        Color shapeColor = const Color(0xff4691d5),
        Color borderColor = Colors.transparent,
        Color textColor = Colors.white,
        String fontFamily = "PTSansCaption",
        double cornerRadius = 10,
        double fontSize = 10,
        void Function()? onPress,
        double minWidth = double.infinity,
        double height = 36}) =>

    ButtonTheme(
      materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
      padding: padding,
      minWidth: minWidth,
      height: height,
      child: RaisedButton(
        shape: RoundedRectangleBorder(
            side: BorderSide(color: borderColor),
            borderRadius: BorderRadius.all(Radius.circular(cornerRadius))),
        onPressed: onPress,
        child: Text(
          title,
          style: TextStyle(
              color: textColor, fontFamily: fontFamily, fontSize: fontSize),
        ),
        color: shapeColor,
      ),
    );

createRoundedCornerFlatButton(String title,
        {EdgeInsetsGeometry padding = EdgeInsets.zero,
        Color shapeColor = Colors.transparent,
        Color borderColor = Colors.transparent,
        FontWeight fontWeight = FontWeight.normal,
        Color textColor = const Color(0xff4691d5),
        String fontFamily = "PTSansCaption",
        double cornerRadius = 10,
        double fontSize = 10,
        void Function()? onPress ,
        double minWidth = double.infinity,
        double height = 36}) =>
    ButtonTheme(
      materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
      padding: EdgeInsets.zero,
      minWidth: minWidth,
      height: height,
      child: FlatButton(
        padding: padding,
        color: shapeColor,
        shape: RoundedRectangleBorder(
            side: BorderSide(color: borderColor),
            borderRadius: BorderRadius.all(Radius.circular(cornerRadius))),
        onPressed: onPress,
        child: Text(
          title,
          style: TextStyle(
              color: textColor,
              fontFamily: fontFamily,
              fontSize: fontSize,
              fontWeight: fontWeight),
        ),
      ),
    );

halveticaText(String text,
        {Color color = Colors.black,
        FontWeight weight = FontWeight.normal,
        double fontSize = 14,EdgeInsetsGeometry padding = EdgeInsets.zero , TextAlign textAlign = TextAlign.start , double lineHeight = 1.5}) =>
    Padding(
      padding: padding == null ? EdgeInsets.zero:padding,
      child: Text(
        text,
        textAlign: textAlign,
        style: TextStyle(height: lineHeight,
            color: color,
            fontFamily: "Halvetica",
            fontWeight: weight,
            fontSize: fontSize),
      ),
    );

halveticaBoldText(String text,
        {Color color = Colors.black, double fontSize = 14,EdgeInsetsGeometry padding = EdgeInsets.zero}) =>
    halveticaText(text,
        color: color, weight: FontWeight.w700, fontSize: fontSize,padding: padding);

halveticaLightText(String text,
        {Color color = Colors.black, double fontSize = 14,EdgeInsetsGeometry padding= EdgeInsets.zero}) =>
    halveticaText(text,
        color: color, weight: FontWeight.w100, fontSize: fontSize,padding: padding);

halveticaNormalText(String text,
        {Color color = Colors.black, double fontSize = 14,EdgeInsetsGeometry padding= EdgeInsets.zero, TextAlign textAlign = TextAlign.start , double lineHeight = 1.0}) =>
    halveticaText(text,
        color: color, weight: FontWeight.w600, fontSize: fontSize,padding: padding,textAlign: textAlign,lineHeight: lineHeight);

ptSansCaptionBoldText(String text,
    {Color color = Colors.black, double fontSize = 14,EdgeInsetsGeometry padding= EdgeInsets.zero}) =>
    Padding(
      padding: padding,
      child: Text(
        text,
        style: TextStyle(
            color: color,
            fontFamily: "PTSansCaption",
            fontWeight: FontWeight.w700,
            fontSize: fontSize),
      ),
    );


extension  MapExtension on Map {
  List<MapEntry<K,V>> filter<K,V>(bool Function(MapEntry<K,V>) filter) {
    List<MapEntry<K,V>> filteredList = [];

    this.entries.forEach((element) {
      if (filter(element as MapEntry<K,V>)) filteredList.add(element);
    });

    return filteredList;
  }
}



createFavoritesButton(bool isChecked,void Function() callback , {double size = 30})=>
    RaisedButton(
    color: Colors.white,
    padding: EdgeInsets.all(6),
    shape: CircleBorder(),
    onPressed: callback,
    child: Icon(
      isChecked ? Icons.star :Icons.star_border,size:size,
      color: isChecked? Colors.red:Colors.grey,
    ));





showDialogWithOptions(context,String message,List<String> options
    ,void Function(String option) optionClicked)
{
  showDialog(
      context: context,
      builder:(context)=> Center(
        child: Container(
          width: percentageOfDeviceWidth(context, 0.8),
          child: Card(
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: _createDialogContentBasedOnCustomerStatus(context,message,options,optionClicked),
            ),
          ),
        ),
      ));
}

Column _createDialogContentBasedOnCustomerStatus(context,String message,List<String> options,void Function(String option) optionClicked) {
  return Column(
    crossAxisAlignment: CrossAxisAlignment.center,
    mainAxisSize: MainAxisSize.min,
    children: [
      halveticaText(message),

      SizedBox(height: 20,),
      Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: options.map<Widget>((op)=>createRoundedCornerRaisedButton(op, minWidth: percentageOfDeviceWidth(context, 0.35),
            onPress:(){
              optionClicked(op);
              Navigator.of(context).pop();
            })).toList()
      )
    ],
  );
}

